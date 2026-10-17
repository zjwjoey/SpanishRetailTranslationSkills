"""Synthetic bookkeeping tests; none are real translation or quality evidence."""
import json,tempfile,unittest
from pathlib import Path
import bench
class Controls(unittest.TestCase):
 def fixture(self):
  t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);d=Path(t.name);e=d/'inventory';e.write_text('synthetic evidence');pool=[]
  for p in bench.PLATFORMS:
   for i in range(3):pool.append({'item_id':f'{p}-{i}','platform':p,'product_id':str(i),'group_id':f'{p}-family-{i}','source_language_status':'SPANISH_CONFIRMED','source_snapshot':{'sha256':'a'*64},'source':{'title':{'action':'Synthetic kitchen vessel','amazon':'Invented computer graphics accessory','ikea':'Artificial upholstered furnishing'}[p]+str(i)},'source_locations':[{'synthetic':True}]})
  exp={'complete':True,'inventory_sources':[{'path':str(e),'sha256':bench.digest(e)}],'seen':[]};(d/'pool').write_text('\n'.join(json.dumps(r) for r in pool));(d/'exposure').write_text(json.dumps(exp));return d,pool,exp
 def test_incomplete_history_blocks(self):
  d,_,e=self.fixture();e['complete']=False;(d/'exposure').write_text(json.dumps(e))
  with self.assertRaisesRegex(AssertionError,'Exposure'):bench.prepare(d/'pool',d/'exposure',d/'frozen',1)
 def test_exploratory_keeps_incomplete_status(self):
  d,_,e=self.fixture();e['complete']=False;(d/'exposure').write_text(json.dumps(e));f=bench.prepare(d/'pool',d/'exposure',d/'frozen',1,allow_novelty_unverified=True);self.assertEqual(f['novelty_status'],'NOVELTY_UNVERIFIED');self.assertFalse(f['exposure_coverage_complete']);r=bench.score(d/'frozen');self.assertEqual(r['status'],'NOT_RUN');self.assertEqual(r['novelty_status'],'NOVELTY_UNVERIFIED')
 def test_seen_family_and_nonspanish_excluded(self):
  d,rr,e=self.fixture();e['seen']=[{'platform':'action','product_id':'0','group_id':'action-family-1','title':''}];rr[2]['source_language_status']='UNKNOWN';(d/'pool').write_text('\n'.join(json.dumps(r) for r in rr));(d/'exposure').write_text(json.dumps(e))
  with self.assertRaisesRegex(AssertionError,'Insufficient new action'):bench.prepare(d/'pool',d/'exposure',d/'frozen',1)
 def test_freeze_cannot_overwrite(self):
  d,_,_=self.fixture();r=bench.prepare(d/'pool',d/'exposure',d/'frozen',1);self.assertEqual(r['count'],3)
  with self.assertRaisesRegex(AssertionError,'already exists'):bench.prepare(d/'pool',d/'exposure',d/'frozen',1)
 def test_missing_outputs_not_complete(self):
  d,_,_=self.fixture();bench.prepare(d/'pool',d/'exposure',d/'frozen',1);r=bench.score(d/'frozen');self.assertEqual(r['status'],'NOT_RUN');self.assertEqual(r['fixed_denominators']['action'],1)
 def test_complete_ai_review_and_root_cause_dedup(self):
  d,_,_=self.fixture();bench.prepare(d/'pool',d/'exposure',d/'frozen',1);f=d/'frozen';rr=bench.rows(f/'selected.jsonl')
  for arm in ['plain','skills']:(f/f'{arm}.jsonl').write_text('\n'.join(json.dumps(x) for x in rr))
  (f/'reviews.jsonl').write_text('\n'.join(json.dumps({'item_id':x['item_id'],'coverage':'COMPLETE','source_first':True,'reviewer_independent':True}) for x in rr));x={'item_id':rr[0]['item_id'],'arm':'plain','severity':'P1','dimension':'coverage','fact_key':'synthetic-root','certainty':'CONFIRMED_AI_FINDING'};(f/'findings.jsonl').write_text(json.dumps(x)+'\n'+json.dumps(dict(x,severity='P0')));r=bench.score(f);self.assertEqual(r['status'],'PAIRED_AI_REVIEW_COMPLETE_NOT_HUMAN_GOLD');self.assertIsNone(r['accuracy_improvement']);self.assertEqual(r['results']['plain']['action']['confirmed_ai_or_human_root_issues'],1)
if __name__=='__main__':unittest.main()
