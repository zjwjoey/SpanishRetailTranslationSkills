"""Offline benchmark bookkeeping only: no model calls, translations, or semantic grading."""
from __future__ import annotations
import argparse,collections,difflib,hashlib,json,re,unicodedata
from pathlib import Path
PLATFORMS=('action','amazon','ikea')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def source_hash(source):return hashlib.sha256(json.dumps(source,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def rows(p):return [json.loads(s) for s in Path(p).read_text(encoding='utf-8-sig').splitlines() if s.strip()]
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):
 with Path(p).open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2)
def norm(s):return ' '.join(re.sub(r'[^\w\s]',' ',''.join(c for c in unicodedata.normalize('NFKD',s or '').casefold() if not unicodedata.combining(c))).split())
def title(r):
 s=r.get('source',{});t=r.get('title') or s.get('title') or s.get('name') or s.get('标题（西语）') or ''
 # IKEA's generic product-type title alone (e.g. chair) does not identify a family.
 series=r.get('series') or s.get('series')
 return f'{series} {t}' if r.get('platform')=='ikea' and series else t
def close_title(a,b):
 a,b=norm(a),norm(b)
 return bool(a and b and (a==b or min(len(a),len(b))>=18 and difflib.SequenceMatcher(None,a,b).ratio()>=.9))
def prepare(pool,exposures,out,per_platform=10,allow_novelty_unverified=False):
 out=Path(out);assert not out.exists(),'Frozen output already exists; never overwrite'
 exp=load(exposures);assert exp.get('complete') is True or allow_novelty_unverified,'Exposure coverage not evidenced complete'
 assert exp.get('inventory_sources'),'Missing actual exposure inventory evidence'
 for p in exp['inventory_sources']:
  assert isinstance(p,dict) and Path(p['path']).is_file() and digest(p['path'])==p['sha256'],'Inventory evidence missing or changed'
 seen=exp.get('seen',[]);ids={(s['platform'],str(s['product_id'])) for s in seen};groups={(s['platform'],s.get('group_id')) for s in seen if s.get('group_id')}
 global_groups={s['global_group_id'] for s in seen if s.get('global_group_id')};eligible=[];rejected=[];unique=set()
 for r in rows(pool):
  key=(r['platform'],str(r['product_id']));assert key not in unique,'Duplicate source product identity';unique.add(key)
  assert r['platform'] in PLATFORMS and r.get('item_id') and r.get('group_id') and r.get('source_locations'),'Incomplete source identity/provenance'
  assert re.fullmatch('[a-f0-9]{64}',r.get('source_snapshot',{}).get('sha256','')),'Missing source snapshot hash'
  reason=None
  if r.get('source_language_status')!='SPANISH_CONFIRMED':reason='LANGUAGE_NOT_CONFIRMED'
  elif key in ids:reason='SEEN_PRODUCT'
  elif (r['platform'],r['group_id']) in groups:reason='SEEN_FAMILY'
  elif r.get('global_group_id') in global_groups:reason='SEEN_CROSS_PLATFORM_FAMILY'
  elif any(close_title(title(r),title(s)) for s in seen):reason='SEEN_NEAR_TITLE'
  if reason:rejected.append({'item_id':r['item_id'],'reason':reason});continue
  r['source_sha256']=source_hash(r['source']);eligible.append(r)
 selected=[];selected_groups=set()
 for platform in PLATFORMS:
  candidates=sorted((r for r in eligible if r['platform']==platform),key=lambda r:hashlib.sha256(('plain-vs-skills-v1:'+r['item_id']).encode()).hexdigest());chosen=[]
  for r in candidates:
   g=(platform,r['group_id'])
   if g in selected_groups or any(close_title(title(r),title(s)) for s in selected):continue
   chosen.append(r);selected.append(r);selected_groups.add(g)
   if len(chosen)==per_platform:break
  assert len(chosen)==per_platform,f'Insufficient new {platform} groups: {len(chosen)}/{per_platform}'
 out.mkdir(parents=True,exist_ok=False)
 with (out/'selected.jsonl').open('x',encoding='utf-8') as f:
  for r in selected:f.write(json.dumps(r,ensure_ascii=False)+'\n')
 freeze={'novelty_status':'LOCAL_HISTORY_SCREENED' if exp.get('complete') is True else 'NOVELTY_UNVERIFIED','exposure_coverage_complete':exp.get('complete') is True,'platform_counts':{p:per_platform for p in PLATFORMS},'count':len(selected),'pool_sha256':digest(pool),'exposures_sha256':digest(exposures),'selected_sha256':digest(out/'selected.jsonl'),'rejected_before_selection':rejected,'selection':'deterministic SHA256 order, distinct platform groups and near-title check','selected_ids':[r['item_id'] for r in selected],'novelty_boundary':exp.get('coverage_boundary','Recoverable project history only; not proof of universal non-exposure'),'human_gold':False}
 write(out/'freeze.json',freeze);return freeze
def indexed(p):
 if not Path(p).exists():return {}
 rr=rows(p);assert len({r['item_id'] for r in rr})==len(rr),f'Duplicate output identity: {p}'
 return {r['item_id']:r for r in rr}
def score(directory):
 d=Path(directory);f=load(d/'freeze.json');assert digest(d/'selected.jsonl')==f['selected_sha256'],'Frozen inputs changed'
 ss=indexed(d/'selected.jsonl');arms={a:indexed(d/f'{a}.jsonl') for a in ['plain','skills']};reviews=indexed(d/'reviews.jsonl');issues=[];coverage={}
 for a,aa in arms.items():
  assert not set(aa)-set(ss),'Output contains unselected items'
  for k,r in aa.items():
   assert all(r.get(x)==ss[k].get(x) for x in ['platform','product_id','source_sha256']),f'Output input-binding mismatch {a}/{k}'
  coverage[a]={p:sum(k in aa for k,s in ss.items() if s['platform']==p) for p in PLATFORMS}
 qa={p:sum(r.get('coverage')=='COMPLETE' and r.get('source_first') is True and r.get('reviewer_independent') is True for k,r in reviews.items() if k in ss and ss[k]['platform']==p) for p in PLATFORMS}
 findings=rows(d/'findings.jsonl') if (d/'findings.jsonl').exists() else []
 rank={'P0':0,'P1':1,'P2':2};dedup={}
 for x in findings:
  assert x['item_id'] in ss and x['arm'] in arms and x['severity'] in rank and x.get('fact_key'),'Invalid finding identity'
  assert x['certainty'] in ['CONFIRMED_AI_FINDING','UNCERTAIN','HUMAN_VERIFIED']
  key=(x['item_id'],x['arm'],x['fact_key'],x['certainty'])
  if key not in dedup or rank[x['severity']]<rank[dedup[key]['severity']]:dedup[key]=x
 totals={}
 for a in arms:
  totals[a]={}
  for p in PLATFORMS:
   xx=[x for x in dedup.values() if x['arm']==a and ss[x['item_id']]['platform']==p and x['certainty'] in ['CONFIRMED_AI_FINDING','HUMAN_VERIFIED']]
   totals[a][p]={'fixed_denominator':f['platform_counts'][p],'produced':coverage[a][p],'complete_independent_qa':qa[p],'P0_affected_items':len({x['item_id'] for x in xx if x['severity']=='P0'}),'P0_or_P1_affected_items':len({x['item_id'] for x in xx if x['severity'] in ['P0','P1']}),'confirmed_ai_or_human_root_issues':len(xx)}
 complete=all(len(a)==len(ss) for a in arms.values()) and all(qa[p]==f['platform_counts'][p] for p in PLATFORMS)
 status='PAIRED_AI_REVIEW_COMPLETE_NOT_HUMAN_GOLD' if complete else ('NOT_RUN' if all(not a for a in arms.values()) else 'PARTIAL_NOT_COMPARABLE')
 result={'status':status,'novelty_status':f.get('novelty_status','NOT_RECORDED'),'exposure_coverage_complete':f.get('exposure_coverage_complete',False),'fixed_denominators':f['platform_counts'],'total_selected':len(ss),'coverage':coverage,'complete_independent_qa':qa,'results':totals,'unique_findings_by_certainty':dict(collections.Counter(x['certainty'] for x in dedup.values())),'accuracy_improvement':None,'warning':'AI findings are not human gold or production accuracy. Source-first/independence flags require actual external process evidence.','usage':{a:load(d/f'{a}_usage.json') if (d/f'{a}_usage.json').exists() else None for a in arms}}
 p=d/'report.json'
 if p.exists():raise AssertionError('Report already exists; preserve earlier actual report before rescoring')
 write(p,result);return result
def main():
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest='command',required=True);s=sub.add_parser('prepare');s.add_argument('--pool',required=True);s.add_argument('--exposures',required=True);s.add_argument('--out',required=True);s.add_argument('--per-platform',type=int,default=10);s.add_argument('--allow-novelty-unverified',action='store_true',help='Exploratory only: preserve incomplete history status; never formal Holdout');s=sub.add_parser('score');s.add_argument('--dir',required=True);a=p.parse_args();r=prepare(a.pool,a.exposures,a.out,a.per_platform,a.allow_novelty_unverified) if a.command=='prepare' else score(a.dir);print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
