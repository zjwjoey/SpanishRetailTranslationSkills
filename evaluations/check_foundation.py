"""Offline engineering tests only. Never imports or runs a translation engine."""
import copy
import json
import re
import unittest
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {'es-retail-category','es-retail-terminology','es-retail-reviewer','es-retail-translator','es-retail-learning'}

def load_json(path):
    def unique(pairs):
        obj={}
        for k,v in pairs:
            if k in obj: raise ValueError('Duplicate JSON key: '+k)
            obj[k]=v
        return obj
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique)

def validate_schema(value, name):
    schema=load_json(ROOT/f'datasets/schemas/{name}.schema.json')
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(value,schema)

def field_value(record, path):
    value=record
    for token in re.findall(r'[^.\[\]]+',path):
        value=value[int(token)] if isinstance(value,list) else value[token]
    return str(value)

def check_source_audit(record,audit):
    validate_schema(audit,'source-audit')
    assert audit['item_id']==record['item_id'] and audit['product_id']==record['product_id'], 'identity mismatch'
    assert audit['source_snapshot']==record['source_snapshot'], 'source snapshot changed'
    decisions=audit['decisions']; ids=[d['decision_id'] for d in decisions]
    assert len(ids)==len(set(ids)), 'duplicate decision ids'
    ledgers={d['decision_id']:d for d in audit['preservation_ledger']}
    for d in decisions:
        assert d['item_id']==record['item_id'], 'decision identity mismatch'
        text=field_value(record,d['source_field']); span=d['source_span']; quote=span['quote']
        assert text.count(quote)>=span['occurrence'], 'quote/occurrence not in original field'
        if span['start'] is not None and span['end'] is not None:
            assert text[span['start']:span['end']]==quote, 'offset mismatch'
        if d['action']!='TRANSLATE':
            assert d['decision_id'] in ledgers, 'missing preservation proof'
            entry=ledgers[d['decision_id']]
            assert entry['source_field']==d['source_field'] and entry['source_span']==span, 'ledger source mismatch'
            assert entry['target_field']==d['target_field'], 'ledger target mismatch'
            for ref in entry['retained_fact_refs']:
                if isinstance(ref,dict) and 'canonical_decision_id' in ref:
                    assert ref['canonical_decision_id'] in ids, 'ledger canonical target missing'
                if isinstance(ref,dict) and 'source_field' in ref:
                    original=field_value(record,ref['source_field'])
                    assert original.count(ref['source_span']['quote'])>=ref['source_span']['occurrence'], 'ledger quote missing'
        if d['action']=='DEDUPLICATE':
            assert d['canonical_decision_id'] in ids and d['canonical_decision_id']!=d['decision_id'], 'invalid canonical duplicate'
    if any(d['action']=='REVIEW_REQUIRED' for d in decisions):
        assert audit['status']!='PASSED','unresolved decision passed'

class FoundationChecks(unittest.TestCase):
    def setUp(self):
        self.item=load_json(ROOT/'evaluations/fixtures/oneblade.synthetic.json')
    def test_exact_five_skills(self):
        self.assertEqual({p.parent.name for p in (ROOT/'.agents/skills').glob('*/SKILL.md')},EXPECTED)
    def test_frontmatter_and_links(self):
        for p in (ROOT/'.agents/skills').rglob('*.md'):
            text=p.read_text(encoding='utf-8')
            if p.name=='SKILL.md':
                meta=yaml.safe_load(text.split('---',2)[1]); self.assertEqual(meta['name'],p.parent.name); self.assertTrue(meta['description'])
            for link in re.findall(r'\]\(([^)]+)\)',text):
                if '://' not in link and not link.startswith('#'):
                    self.assertTrue((p.parent/link.split('#')[0]).resolve().exists(),(str(p),link))
    def test_all_schema_documents(self):
        for p in (ROOT/'datasets/schemas').glob('*.json'): jsonschema.Draft202012Validator.check_schema(load_json(p))
    def test_synthetic_input(self):
        validate_schema(self.item,'item-input'); self.assertTrue(self.item['is_synthetic'])
    def test_missing_identity_rejected(self):
        del self.item['product_id']
        with self.assertRaises(jsonschema.ValidationError): validate_schema(self.item,'item-input')
    def test_ai_verified_rejected(self):
        self.item.update(verification_status='VERIFIED',verification={'reviewer_type':'AI'})
        with self.assertRaises(jsonschema.ValidationError): validate_schema(self.item,'item-input')
    def test_unverified_holdout_rejected(self):
        self.item.update(dataset_split='holdout',group_id='group-1')
        with self.assertRaises(jsonschema.ValidationError): validate_schema(self.item,'item-input')
    def test_duplicate_key_rejected(self):
        with self.assertRaises(ValueError):
            def reject(pairs):
                result={}
                for k,v in pairs:
                    if k in result: raise ValueError(k)
                    result[k]=v
                return result
            json.loads('{"quantity":2,"quantity":1}',object_pairs_hook=reject)
    def minimal_audit(self):
        span={'quote':'PHILIPS','occurrence':1,'start':0,'end':7}
        d={'decision_id':'d1','item_id':self.item['item_id'],'source_field':'source.title','source_span':span,'action':'PRESERVE','reason':'brand','target_field':'identifiers.brand','review_status':'PROPOSED'}
        ledger={'decision_id':'d1','source_field':d['source_field'],'source_span':span,'disposition':'retained','target_field':'identifiers.brand','retained_fact_refs':['brand']}
        return {'item_id':self.item['item_id'],'product_id':self.item['product_id'],'source_snapshot':self.item['source_snapshot'],'mode':'SOURCE_AUDIT','contract_version':'1.0.0-foundation','knowledge_version':'1.0.0-foundation','decisions':[d],'preservation_ledger':[ledger],'conflicts':[],'truncations':[],'status':'PASSED'}
    def test_source_span_and_ledger_control(self): check_source_audit(self.item,self.minimal_audit())
    def test_missing_preservation_proof_rejected(self):
        a=self.minimal_audit(); a['preservation_ledger']=[]
        with self.assertRaises(AssertionError): check_source_audit(self.item,a)
    def test_wrong_quote_rejected(self):
        a=self.minimal_audit(); a['decisions'][0]['source_span']['quote']='NOT_IN_SOURCE'
        with self.assertRaises(AssertionError): check_source_audit(self.item,a)
    def test_structured_ledger_source_reference(self):
        a=self.minimal_audit(); d=a['decisions'][0]
        a['preservation_ledger'][0]['retained_fact_refs']=[{'source_field':d['source_field'],'source_span':d['source_span'],'value':'PHILIPS'}]
        check_source_audit(self.item,a)
    def test_missing_ledger_canonical_rejected(self):
        a=self.minimal_audit(); a['preservation_ledger'][0]['retained_fact_refs']=[{'canonical_decision_id':'does-not-exist'}]
        with self.assertRaises(AssertionError): check_source_audit(self.item,a)
    def test_conflict_cannot_pass(self):
        a=self.minimal_audit(); a['conflicts']=[{'slot':'blade_count','values':[1,2]}]
        with self.assertRaises(jsonschema.ValidationError): check_source_audit(self.item,a)
    def test_dedup_requires_canonical_reference(self):
        a=self.minimal_audit(); a['decisions'][0]['action']='DEDUPLICATE'
        with self.assertRaises(jsonschema.ValidationError): check_source_audit(self.item,a)
    def test_translator_cannot_approve(self):
        value={'item_id':'test','product_id':'test','platform':'amazon','source_snapshot':self.item['source_snapshot'],'stage':'TRANSLATION_CANDIDATE','status':'PASSED','translation_zh':{},'identifiers':{},'research_metadata':{},'field_alignment':[],'protected_identifiers':[],'retained_facts':[],'uncertainties':[],'conflicts':[],'review':None,'run_metadata':{}}
        with self.assertRaises(jsonschema.ValidationError): validate_schema(value,'translation-output')

if __name__=='__main__': unittest.main(verbosity=2)
