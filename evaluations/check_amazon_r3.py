"""Read-only native-schema/binding/projection gates. Never generates Chinese or grades semantics."""
import argparse,collections,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'local/test-deps'))
import jsonschema
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate JSON key '+k)
  d[k]=v
 return d
def read(p):return [json.loads(v,object_pairs_hook=unique) for v in Path(p).read_text(encoding='utf-8-sig').splitlines() if v.strip()]
def get(doc,path):
 if path.startswith('/'):
  for k in path[1:].split('/'):
   k=k.replace('~1','/').replace('~0','~');doc=doc[int(k)] if isinstance(doc,list) else doc[k]
 else:
  for k in re.findall(r'[^.\[\]]+',path):doc=doc[int(k)] if isinstance(doc,list) else doc[k]
 return doc
def span(src,item):
 value=get(src,item['source_field']);value=str(value) if not isinstance(value,str) else value
 s=item['source_span'];q=s['quote'];assert q and q in value,'source quote absent'
 assert isinstance(s.get('occurrence'),int) and s['occurrence']>=1 and value.count(q)>=s['occurrence'],'source occurrence'
 if s.get('start') is not None or s.get('end') is not None:assert value[s['start']:s['end']]==q,'source offset'
def strings(value,path):
 if isinstance(value,str):yield path,value
 elif isinstance(value,list):
  for i,v in enumerate(value):yield from strings(v,path+'/'+str(i))
 elif isinstance(value,dict):
  for k,v in value.items():yield from strings(v,path+'/'+k.replace('~','~0').replace('/','~1'))
def validate(src,first,out):
 schema=json.loads((R/'datasets/schemas/translation-output.schema.json').read_text(encoding='utf-8'));jsonschema.validate(out,schema)
 assert out['contract_extension']=='amazon-r3-v1'
 allowed={'contract_version','contract_extension','item_id','product_id','platform','source_snapshot','source','source_sha256','stage','status','translation_zh','identifiers','research_metadata','category_context','field_alignment','protected_identifiers','retained_facts','uncertainties','conflicts','preservation_ledger','compatibility_lists','numeric_role_checks','projection_map','review','run_metadata','source_audit'}
 assert set(out)<=allowed,'uncontracted extra product representation'
 assert out['product_id']==src['asin']==first['asin'] and out['item_id']==src['item_id'],'identity'
 assert out['source']==src['source'] and out['source_sha256']==src['source_sha256']==first['source_sha256'],'source mutated'
 assert out['source_snapshot']['sha256']==src['file_sha256'] and out['source_snapshot']['label']==src['source_snapshot'],'snapshot'
 assert out['status']=='REVIEW_REQUIRED' and out['stage']=='TRANSLATION_CANDIDATE'
 assert first['language_gate']['status']=='ES_ELIGIBLE','not Spanish admitted'
 assert set(first['language_gate']['checked_fields'])==set(src['source']),'language fields not fully checked'
 for e in first['language_gate']['evidence']:span(src,e)
 assert first['language_gate']['evidence'],'no actual language evidence'
 assert out['identifiers']['asin']==src['asin'] and out['identifiers']['parent_asin']==src.get('parent_asin'),'parent/child role'
 assert out['research_metadata']['input']==src['metadata'],'input metadata values missing/mutated'
 facts=out['retained_facts'];fs={f['fact_id']:f for f in facts};assert facts and len(fs)==len(facts),'facts empty/duplicate'
 pre={f['fact_id']:f for f in first['facts']};assert set(pre)==set(fs),'pre facts differ'
 for fid,f in fs.items():
  span(src,f);assert all(f[k]==pre[fid][k] for k in ['source_field','source_span','role','scope','action']),'source-first changed'
  assert f['role'] and f['scope'] and f['reason'],'fact role/scope/reason'
  if f['action'] in ['REVIEW_REQUIRED','EXCLUDE_FROM_DESCRIPTION','DEDUPLICATE']:assert f['zh'] is None,'uncertain text leaked'
  else:assert f['action'] in ['TRANSLATE','PRESERVE','METADATA'] and isinstance(f['zh'],str) and f['zh'].strip(),'no actual Chinese'
  if f['zh'] is not None:
   assert f['zh'] not in ['元数据字段','参数已保留','兼容多种型号','字段已保留'],'generic placeholder is not actual value'
   assert f['zh']!='逐项翻译：'+f['source_span']['quote'],'source echo wrapper is not translation'
   if f['action']=='TRANSLATE' and len(f['source_span']['quote'])>60:
    assert f['zh']!=f['source_span']['quote'],'long source echo is not translation'
  if f['role']=='generation' and f['zh']:
   assert re.search(r'第.{1,12}代',f['zh']) and not re.search(r'个|件|单位|包装',f['zh']),'generation treated as count'
  if re.search(r'Clasificaci[oó]n en los m[aá]s vendidos|Valoraci[oó]n media de los clientes|Opiniones de los clientes|Producto en Amazon.es desde',f['source_span']['quote'],re.I) and f['zh'] is not None:
   assert f['action']=='METADATA','platform metadata mixed with product facts'
 pm=out['projection_map'];paths=[p['target_path'] for p in pm];assert len(paths)==len(set(paths)),'duplicate projection path'
 targets=dict(strings(out['translation_zh'],'/translation_zh'))
 assert set(targets)<=set(paths),'unbound target string'
 uses=collections.defaultdict(set)
 for p in pm:
  ids=p['fact_ids'];assert ids and all(i in fs and fs[i]['zh'] is not None for i in ids),'bad/masked projection fact'
  part=p.get('part','zh');assert part in ['zh','label_zh']
  expected=p['joiner'].join(fs[i][part] for i in ids)
  assert get(out,p['target_path'])==expected,'projection mismatch '+p['target_path']
  for fid in ids:uses[fid].add(p['target_path'])
 for fid,f in fs.items():
  assert set(f['target_fields'])==uses[fid],'fact reverse targets'
  if f['action']=='METADATA':assert not any(p.startswith('/translation_zh/') for p in uses[fid]),'metadata leaked into product target'
  if f['action'] in ['TRANSLATE','PRESERVE','METADATA']:assert uses[fid],'unrendered retained fact '+fid
  if f['action']=='DEDUPLICATE':assert f['canonical_fact_id'] in fs,'dedup canonical absent'
 for x in out['compatibility_lists']:
  span(src,x);assert x['items'],'empty compatibility list'
  for it in x['items']:
   assert it['source_literal'] and it['source_literal'] in x['source_span']['quote'],'compat literal absent'
   f=fs[it['fact_id']];assert f['role']=='compatibility','compat role'
   if it['disposition']=='RETAINED':
    assert f['zh'] is not None and uses[f['fact_id']],'compat target missing'
    qualifier_needed=bool(re.search(r'generaci[oó]n|conector|con\s+(?:cancelaci[oó]n|estuche)|pulgadas',it['source_literal'],re.I))
    if qualifier_needed:assert it.get('qualifier'),'visible qualifier not registered'
    if it.get('qualifier'):
     qzh=it.get('qualifier_zh');assert isinstance(qzh,str) and re.search(r'[\u4e00-\u9fff]',qzh) and qzh in f['zh'],'qualifier Chinese missing from actual fact'
   else:assert it['disposition']=='REVIEW_REQUIRED' and f['zh'] is None,'compat uncertainty'
 for u in out['uncertainties']:
  for fid in u.get('fact_ids',[]):assert fid in fs and fs[fid]['action']=='REVIEW_REQUIRED' and fs[fid]['zh'] is None,'uncertainty not locally isolated'
 for n in out['numeric_role_checks']:
  span(src,n);f=fs[n['fact_id']];assert n['candidate_zh']==f['zh'],'numeric actual text differs'
  if n['dimension']=='generation':assert f['role']=='generation','numeric generation role'
  if re.search(r'Generaci[oó]n\s*:|[12]\.?[ªº]?\s*generaci[oó]n|segunda generaci[oó]n',n['source_span']['quote'],re.I):assert n['dimension']=='generation','generation mislabeled quantity'
 for f in facts:
  if re.search(r'Generaci[oó]n\s*:|segunda generaci[oó]n',f['source_span']['quote'],re.I):assert f['role']=='generation' and any(n['fact_id']==f['fact_id'] and n['dimension']=='generation' for n in out['numeric_role_checks']),'generation evidence unregistered'
 for p in out['protected_identifiers']:
  span(src,p);assert p['value'] in get(src,p['source_field']),'protected value absent'
 for a in out['field_alignment']:
  span(src,a);assert a['translated_text'] in get(out,a['target_field']) and all(fid in fs for fid in a['fact_ids']),'alignment actual text'
 aligned={(fid,a['target_field']) for a in out['field_alignment'] for fid in a['fact_ids']}
 assert all((fid,path) in aligned for fid,paths in uses.items() for path in paths),'projection lacks source alignment'
 assert out['review']['independence_method'] is None and not out['review']['checked_fields'],'generator self approved'
 audit_schema=json.loads((R/'datasets/schemas/source-audit.schema.json').read_text(encoding='utf-8'));jsonschema.validate(out['source_audit'],audit_schema)
 decisions=out['source_audit']['decisions'];assert len(decisions)==len(fs) and {d['decision_id'] for d in decisions}==set(fs),'source audit facts not closed'
 for d in decisions:
  f=fs[d['decision_id']];assert d['action']==f['action'] and d['source_field']==f['source_field'] and d['source_span']==f['source_span'],'audit/canonical mismatch'
 assert {v['decision_id'] for v in out['source_audit']['preservation_ledger']}=={fid for fid,f in fs.items() if f['action']!='TRANSLATE'},'nontranslation ledger missing'
 return {'facts':len(facts),'compatibility_items':sum(len(v['items']) for v in out['compatibility_lists']),'projections':len(pm)}
def validate_audit(src,first,audit,candidate):
 assert src['asin']==first['asin']==audit['asin'] and src['source_sha256']==first['source_sha256']==audit['source_sha256'],'audit identity/hash'
 def normalized(fields):return {re.split(r'[.\[]',v.removeprefix('source.'))[0] for v in fields}
 assert set(src['source'])<=normalized(audit['checked_source_fields']),'audit source field coverage'
 assert first['facts'] and first['language_gate']['status']==audit['language_gate']['status'],'audit independent source facts/language'
 for e in first['language_gate'].get('evidence',[]):span(src,e)
 for f in first['facts']:
  span(src,f);assert len(f['meaning'])>=3 and f['meaning'] not in ['源段完整保留','参数已保留','已核对'],'audit generic source fact'
 assert audit['status']=='REVIEW_REQUIRED' and audit['human_confirmed']==0 and len(audit['comparison_note'])>=50,'audit status/note'
 assert set(audit['focus_checks'])=={'compatibility_inventory','generation_quantity','target_consistency'},'audit focus checks'
 fs={f['fact_id']:f for f in candidate['retained_facts']}
 pm={v['target_path']:v for v in candidate['projection_map']}
 for f in audit['findings']:
  assert f['severity'] in ['P0','P1','P2'] and f['issue_type'] in ['OMISSION','ROLE','NUMBER','PROJECTION','OVER_QUARANTINE','UNSUPPORTED','SOURCE_SCOPE','STRUCTURE'],'audit finding type'
  span(src,f);assert f['reason'] and f['suggestion']
  ids=f['fact_ids'];assert isinstance(ids,list) and all(fid in fs for fid in ids),'audit fact IDs'
  if f.get('target_quote'):
   assert f.get('target_path') and isinstance(get(candidate,f['target_path']),str) and f['target_quote'] in get(candidate,f['target_path']),'audit target path/quote'
   assert ids,'existing incorrect target must bind canonical fact IDs'
   if f['target_path'] in pm:assert set(ids)<=set(pm[f['target_path']]['fact_ids']),'audit fact not bound to target'
 for u in audit['uncertainties']:
  span(src,u);assert u['reason'] and all(fid in fs for fid in u.get('fact_ids',[])),'audit uncertainty binding'
 return {'findings':len(audit['findings']),'uncertainties':len(audit['uncertainties'])}
def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--source-first',required=True);p.add_argument('--candidate',required=True);args=p.parse_args()
 src={v['asin']:v for v in read(args.input)};pre={v['asin']:v for v in read(args.source_first)};rows=read(args.candidate);errors=[];stats=[]
 assert len(rows)==len({v['product_id'] for v in rows})
 for x in rows:
  try:stats.append(validate(src[x['product_id']],pre[x['product_id']],x))
  except Exception as e:errors.append({'asin':x.get('product_id'),'error':str(e)})
 rejected={a for a,v in pre.items() if v['language_gate']['status']!='ES_ELIGIBLE'}
 if {v['product_id'] for v in rows}|rejected != set(src):errors.append({'error':'input membership not closed by candidates or language rejection'})
 print(json.dumps({'candidates':len(rows),'language_rejected':len(rejected),'binding_passed':len(stats),'facts':sum(v['facts'] for v in stats),'errors':errors,'semantics':'NOT_CHECKED_BY_PROGRAM'},ensure_ascii=False));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
