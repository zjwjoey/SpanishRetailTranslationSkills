"""Offline provenance and binding checks. Never generates translation/audit semantics."""
import argparse,json
from pathlib import Path
parser=argparse.ArgumentParser(description="Check private R2 evidence bindings; never grades translation semantics.")
parser.add_argument("--data-dir",type=Path,required=True,help="Private run directory containing inputs/generation/audit")
parser.add_argument("--complete",action="store_true",help="Require generation and audit counts of 200 regression and 100 new SKUs")
args=parser.parse_args()
D=args.data_dir.resolve()
if not (D/"inputs").is_dir(): parser.error("data-dir must contain inputs/")
def read(p):
 def unique(pairs):
  d={}
  for k,v in pairs:
   if k in d: raise ValueError('duplicate key '+k)
   d[k]=v
  return d
 return [json.loads(s,object_pairs_hook=unique) for s in p.read_text(encoding='utf-8-sig').splitlines() if s.strip()]
def dump(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')

def pointer(doc,path):
 assert isinstance(path,str) and path.startswith('/'),'target path must be JSON pointer'
 for part in path[1:].split('/'):
  part=part.replace('~1','/').replace('~0','~')
  doc=doc[int(part)] if isinstance(doc,list) else doc[part]
 return doc
def check():
 result={'generation':{},'audit':{},'errors':[],'semantic_quality':'NOT_CHECKED_BY_PROGRAM'}
 for prefix in ['regression-','new-']:
  total=0
  for p in sorted((D/'generation').glob(prefix+'[0-9][0-9][0-9].jsonl')):
   try:
    inp={x['asin']:x for x in read(D/'inputs'/p.name)}; vals=read(p); facts=read(p.with_name(p.stem+'.source-audit.jsonl'))
    assert len(vals)==len(inp) and {x['asin'] for x in vals}==set(inp),'ASIN/count'
    assert len(facts)==len(inp) and {x['asin'] for x in facts}==set(inp),'source-first count'
    for x in facts:
     s=inp[x['asin']];assert x['source_sha256']==s['source_sha256'],'source first hash'
     seg={z['segment_id']:z['text'] for z in s['segments']}
     assert x['source_facts'],'empty preaudit'
     for f in x['source_facts']:
      assert f['quote'] and f['quote'] in seg[f['segment_id']] and f['meaning'],'preaudit quote/meaning'
      assert not any(t in f['meaning'] for t in ['Source fact retained for fact-level review','该segment含明确商品事实','源段逐项事实：完整保留','完整英文主体/技术字段，需西中方向复核；原文已保留，未臆译']),'template preaudit rejected'
    for x in vals:
     s=inp[x['asin']];assert x['source_sha256']==s['source_sha256'],'source hash';assert x['status']=='REVIEW_REQUIRED','status'
     seg={z['segment_id']:z['text'] for z in s['segments']};assert len(x['segments'])==len(seg) and {z['segment_id'] for z in x['segments']}==set(seg),'segments'
     fs={}
     for z in x['segments']:
      assert z['facts'],'empty segment'
      for f in z['facts']:
       assert f['fact_id'] not in fs,'duplicate fact';fs[f['fact_id']]=f
       assert f['quote'] and f['quote'] in seg[z['segment_id']],'fact quote'
       assert isinstance(f.get('occurrence'),int) and f['occurrence']>=1 and seg[z['segment_id']].count(f['quote'])>=f['occurrence'],'occurrence'
       assert f['action'] in {'TRANSLATE','PRESERVE','METADATA','DEDUPLICATE','EXCLUDE_FROM_DESCRIPTION','REVIEW_REQUIRED'},'action'
       assert f['reason'],'reason'
       if f['action'] in {'TRANSLATE','PRESERVE','METADATA'}:assert isinstance(f.get('zh'),str) and f['zh'].strip(),'missing text'
       else:assert f.get('zh') is None,'excluded not null'
       if f.get('zh'):
        assert f['zh'] != '逐项翻译：'+f['quote'],'source echo is not translation'
     for f in fs.values():
      if f['action']=='DEDUPLICATE':
       seen={f['fact_id']};cur=f
       while cur['action']=='DEDUPLICATE':
        fid=cur['canonical_fact_id'];assert fid not in seen and fid in fs,'dedup cycle/target';seen.add(fid);cur=fs[fid]
       assert cur['action'] in {'TRANSLATE','PRESERVE','METADATA'} and cur.get('zh'),'dedup not retained'
    total+=len(vals)
   except Exception as e:result['errors'].append({'file':p.name,'error':str(e)})
  result['generation'][prefix]=total
  audited=0
  for p in sorted((D/'audit').glob(prefix+'[0-9][0-9][0-9].jsonl')):
   try:
    inp={x['asin']:x for x in read(D/'inputs'/p.name)};vals=read(p);first=read(p.with_name(p.stem+'.source-facts.jsonl'));candidates={x['asin']:x for x in read(D/'generation'/p.name)}
    assert len(vals)==len(inp) and {x['asin'] for x in vals}==set(inp),'audit ASIN/count'
    assert len(first)==len(inp) and {x['asin'] for x in first}==set(inp),'audit source-first count'
    for x in first:
     s=inp[x['asin']];segs={z['segment_id']:z['text'] for z in s['segments']};assert x['source_sha256']==s['source_sha256'],'audit first hash';assert x['facts'],'empty independent facts'
     for f in x['facts']:
      assert f['quote'] and f['quote'] in segs[f['segment_id']] and f['meaning'],'independent fact quote/meaning'
      assert not any(t in f['meaning'] for t in ['Source fact retained for fact-level review','该segment含明确商品事实','源段逐项事实：完整保留','中文核对事实：源段完整保留']),'template independent facts rejected'
     assert len(set(f['meaning'] for f in x['facts']))>=min(2,len(x['facts'])),'identical independent fact meanings'
    for x in vals:
     s=inp[x['asin']];segs={z['segment_id']:z['text'] for z in s['segments']};assert x['source_sha256']==s['source_sha256'],'audit hash'
     assert x['status']=='REVIEW_REQUIRED','audit candidate status'
     assert len(x['checked_segment_ids'])==len(segs) and set(x['checked_segment_ids'])==set(segs),'audit coverage'
     assert len(x['comparison_note'])>=35,'audit concrete comparison'
     for f in x.get('findings',[]):
      assert f.get('severity') in {'P0','P1','P2'},'audit severity'
      assert f.get('issue_type') in {'OMISSION','MATERIAL','ROLE','OVER_QUARANTINE','NUMBER','IDENTIFIER','OTHER'},'audit issue type'
      assert f.get('reason') and f.get('suggestion'),'audit finding explanation'
     cand=candidates[x['asin']];fs={f['fact_id']:f for z in cand['segments'] for f in z['facts']}
     for f in x.get('findings',[])+x.get('uncertainties',[]):
      assert isinstance(f.get('fact_ids',[]),list) and f.get('reason'),'audit ids/reason'
      assert f['source_quote'] and f['source_quote'] in segs[f['segment_id']],'audit source quote'
      assert all(fid in fs for fid in f.get('fact_ids',[])),'audit target facts'
      if f.get('target_quote'):
       if f.get('target_path'):
        actual=pointer(cand,f['target_path']);assert isinstance(actual,str) and f['target_quote'] in actual,'audit target path/quote'
       else:assert any(f['target_quote'] in (fs[fid].get('zh') or '') for fid in f.get('fact_ids',[])),'audit target quote'
    audited+=len(vals)
   except Exception as e:result['errors'].append({'file':'audit/'+p.name,'error':str(e)})
  result['audit'][prefix]=audited
 if args.complete:
  for section in ['generation','audit']:
   for prefix,expected in [('regression-',200),('new-',100)]:
    if result[section][prefix]!=expected:result['errors'].append({'section':section,'prefix':prefix,'error':'incomplete expected '+str(expected)})
 dump(D/'checks/progress.json',result);print(json.dumps(result,ensure_ascii=False))
 return result
if __name__=='__main__': raise SystemExit(1 if check()['errors'] else 0)
