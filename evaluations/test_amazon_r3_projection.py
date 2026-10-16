"""Synthetic contract failure tests, not translation accuracy/gold or Skill discovery."""
import copy,hashlib,unittest
from check_amazon_r3 import validate

def fixture():
 source={'title':'Adaptador de segunda generación','variant':None,'specifications':'Generación: 2.ª Generación; Número de artículos: 3; Ancho de corte: 2 cm','description':None,'bullets':'Compatible con Modelo A y Modelo B (conector Lightning); admite ramas de hasta 20 mm.','categories':[]}
 sha=hashlib.sha256(b'synthetic-r3').hexdigest()
 src={'asin':'synthetic-r3','item_id':'synthetic-r3','source_snapshot':'synthetic','file_sha256':sha,'source_sha256':sha,'source':source,'metadata':{},'parent_asin':None}
 rows=[('f1','source.specifications','Generación: 2.ª Generación','generation','第2代'),('f2','source.specifications','Número de artículos: 3','item_count','商品数量3件'),('f3','source.bullets','Compatible con Modelo A y Modelo B (conector Lightning)','compatibility','源标称兼容Modelo A及Modelo B（Lightning连接器）'),('f4','source.specifications','Ancho de corte: 2 cm','width','剪切宽度2厘米'),('f5','source.bullets','admite ramas de hasta 20 mm','branch_diameter','可剪直径最高20毫米的枝条')]
 fs=[];pm=[];fa=[];texts=[]
 for i,(fid,sf,q,role,zh) in enumerate(rows):
  path=f'/translation_zh/bullets/{i}';sp={'quote':q,'occurrence':1,'start':None,'end':None};fs.append({'fact_id':fid,'source_field':sf,'source_span':sp,'role':role,'scope':'synthetic product','action':'TRANSLATE','reason':'synthetic exact source','zh':zh,'target_fields':[path]});pm.append({'target_path':path,'fact_ids':[fid],'part':'zh','joiner':'；'});fa.append({'source_field':sf,'source_span':sp,'target_field':path,'translated_text':zh,'fact_ids':[fid]});texts.append(zh)
 first={'asin':src['asin'],'source_sha256':sha,'language_gate':{'status':'ES_ELIGIBLE','checked_fields':list(source),'evidence':[{'source_field':'source.title','source_span':{'quote':source['title'],'occurrence':1}}]},'facts':copy.deepcopy(fs)}
 out={'contract_version':'1.0.0-foundation','contract_extension':'amazon-r3-v1','item_id':src['item_id'],'product_id':src['asin'],'platform':'amazon','source_snapshot':{'label':'synthetic','sha256':sha,'captured_at':None},'source':source,'source_sha256':sha,'stage':'TRANSLATION_CANDIDATE','status':'REVIEW_REQUIRED','translation_zh':{'bullets':texts},'identifiers':{'asin':src['asin'],'parent_asin':None},'research_metadata':{'input':{}},'field_alignment':fa,'protected_identifiers':[],'retained_facts':fs,'uncertainties':[],'conflicts':[],'review':{'independence_method':None,'checked_fields':[]},'run_metadata':{},'projection_map':pm,'compatibility_lists':[{'source_field':'source.bullets','source_span':{'quote':rows[2][2],'occurrence':1},'items':[{'source_literal':'Modelo A','fact_id':'f3','disposition':'RETAINED'},{'source_literal':'Modelo B (conector Lightning)','fact_id':'f3','disposition':'RETAINED'}]}],'numeric_role_checks':[{'source_field':rows[0][1],'source_span':{'quote':rows[0][2],'occurrence':1},'fact_id':'f1','dimension':'generation','candidate_zh':'第2代'}]}
 out['compatibility_lists'][0]['items'][1].update(qualifier='conector Lightning',qualifier_zh='Lightning连接器')
 out['source_audit']={'item_id':src['item_id'],'product_id':src['asin'],'source_snapshot':out['source_snapshot'],'mode':'SOURCE_AUDIT','contract_version':'1.0.0-foundation','knowledge_version':'1.0.0-foundation','decisions':[{'decision_id':f['fact_id'],'item_id':src['item_id'],'source_field':f['source_field'],'source_span':f['source_span'],'action':f['action'],'reason':f['reason'],'target_field':f['target_fields'][0],'review_status':'REVIEW_REQUIRED'} for f in fs],'preservation_ledger':[],'conflicts':[],'truncations':[],'status':'REVIEW_REQUIRED'}
 return src,first,out

class ProjectionTests(unittest.TestCase):
 def test_native_binding_positive(self):
  s,f,o=fixture();self.assertEqual(validate(s,f,o)['compatibility_items'],2)
 def test_old_2cm_to_20cm_drift_rejected(self):
  s,f,o=fixture();o['translation_zh']['bullets'][3]='剪切宽度20厘米'
  with self.assertRaisesRegex(AssertionError,'projection mismatch'):validate(s,f,o)
 def test_consistent_wrong_generation_count_still_rejected(self):
  s,f,o=fixture();o['retained_facts'][0]['zh']='2个单位';o['translation_zh']['bullets'][0]='2个单位';o['numeric_role_checks'][0]['candidate_zh']='2个单位'
  with self.assertRaisesRegex(AssertionError,'generation treated as count'):validate(s,f,o)
 def test_unmapped_summary_rejected(self):
  s,f,o=fixture();o['translation_zh']['description']='剪切宽度20厘米'
  with self.assertRaisesRegex(AssertionError,'unbound target string'):validate(s,f,o)
 def test_second_uncontracted_copy_rejected(self):
  s,f,o=fixture();o['summary']='剪切宽度20厘米'
  with self.assertRaisesRegex(AssertionError,'uncontracted extra'):validate(s,f,o)
 def test_mask_not_propagated_rejected(self):
  s,f,o=fixture();f['facts'][3]['action']='REVIEW_REQUIRED';o['retained_facts'][3]['action']='REVIEW_REQUIRED';o['retained_facts'][3]['zh']=None
  with self.assertRaisesRegex(AssertionError,'bad/masked projection'):validate(s,f,o)
 def test_compatibility_false_binding_rejected(self):
  s,f,o=fixture();o['compatibility_lists'][0]['items'][1]['fact_id']='missing'
  with self.assertRaises(KeyError):validate(s,f,o)
 def test_native_objects_missing_rejected(self):
  s,f,o=fixture();del o['research_metadata']
  with self.assertRaises(Exception):validate(s,f,o)
 def test_actual_source_echo_wrapper_rejected(self):
  s,f,o=fixture();o['retained_facts'][2]['zh']='逐项翻译：'+o['retained_facts'][2]['source_span']['quote']
  with self.assertRaisesRegex(AssertionError,'source echo wrapper'):validate(s,f,o)
 def test_metadata_placeholder_rejected(self):
  s,f,o=fixture();o['retained_facts'][4]['zh']='元数据字段'
  with self.assertRaisesRegex(AssertionError,'generic placeholder'):validate(s,f,o)
 def test_visible_qualifier_silently_null_rejected(self):
  s,f,o=fixture();o['compatibility_lists'][0]['items'][1]['qualifier']=None
  with self.assertRaisesRegex(AssertionError,'visible qualifier not registered'):validate(s,f,o)
 def test_source_qualifier_only_not_translation_rejected(self):
  s,f,o=fixture();o['compatibility_lists'][0]['items'][1]['qualifier_zh']='conector Lightning'
  with self.assertRaisesRegex(AssertionError,'qualifier Chinese missing'):validate(s,f,o)
 def test_uncertainty_note_without_actual_isolation_rejected(self):
  s,f,o=fixture();o['uncertainties']=[{'fact_ids':['f4'],'reason':'uncertain dimension'}]
  with self.assertRaisesRegex(AssertionError,'uncertainty not locally isolated'):validate(s,f,o)
 def test_metadata_leak_into_product_rejected(self):
  s,f,o=fixture();f['facts'][4]['action']='METADATA';o['retained_facts'][4]['action']='METADATA'
  with self.assertRaisesRegex(AssertionError,'metadata leaked into product'):validate(s,f,o)

if __name__=='__main__':unittest.main()
