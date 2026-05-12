#!/usr/bin/env python3
import os,re,csv,sys,time,json,argparse
import subprocess,tempfile,shutil,datetime,requests
from dotenv import load_dotenv
load_dotenv()
GITHUB_TOKEN=os.getenv("GITHUB_TOKEN")
GITHUB_REPO=os.getenv("GITHUB_REPO","Hax0023/security-intel-2026")
HEADERS={"User-Agent":"Mozilla/5.0 Chrome/124.0"}
CSV_URL="https://raw.githubusercontent.com/reddelexc/hackerone-reports/master/data.csv"
MD_BASE="https://raw.githubusercontent.com/reddelexc/hackerone-reports/master/tops_by_bug_type"
VULN_MAP={"xss":"web-api","sqli":"web-api","ssrf":"web-api","idor":"web-api",
 "csrf":"web-api","xxe":"web-api","graphql":"web-api","ssti":"web-api",
 "information disclosure":"web-api","insecure direct object":"web-api",
 "code injection":"memory-binary","buffer overflow":"memory-binary",
 "rce":"memory-binary","remote code execution":"memory-binary",
 "command injection":"memory-binary","authentication":"auth-crypto",
 "account takeover":"auth-crypto","oauth":"auth-crypto",
 "privilege escalation":"auth-crypto","mfa":"auth-crypto",
 "business logic":"business-logic","race condition":"business-logic",
 "subdomain takeover":"infra-cloud","kubernetes":"infra-cloud"}
def get_category(vt,title=""):
 t=(vt+" "+title).lower()
 for kw,cat in VULN_MAP.items():
  if kw in t: return cat
 return "uncategorised"

def fetch_h1(rid):
 try:
  r=requests.get(f"https://hackerone.com/reports/{rid}.json",headers=HEADERS,timeout=20)
  if r.status_code!=200: return None
  d=r.json()
  c=d.get("vulnerability_information") or ""
  if len(c)<50: return None
  return {"id":str(d.get("id",rid)),
   "title":d.get("title",""),
   "url":f"https://hackerone.com/reports/{rid}",
   "reporter":(d.get("reporter") or {}).get("username","?"),
   "program":(d.get("team") or {}).get("name","Unknown"),
   "severity":d.get("severity_rating","unknown"),
   "bounty":d.get("bounty_amount") or 0,
   "vuln_type":(d.get("weakness") or {}).get("name",""),
   "disclosed_at":(d.get("disclosed_at") or "")[:10],
   "submitted_at":(d.get("submitted_at") or "")[:10],
   "upvotes":d.get("vote_count",0),
   "cves":d.get("cve_ids",[]),
   "content":c}
 except Exception as e: print("fetch_h1 error:",e); return None

def analyse(report):
 sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
 import analyse as _a
 return _a.run(report["title"],report["url"],report["content"][:5000])

def render(report,a):
 b=report.get("bounty",0)
 try: bs=f"${float(b):,.0f}" if b and float(b)>0 else "Not disclosed"
 except: bs=str(b) or "Not disclosed"
 td=datetime.date.today().isoformat()
 cves=", ".join(report.get("cves",[]) or []) or "None"
 vt=report.get("vuln_type","")
 cat=report.get("category",get_category(vt,report.get("title","")))
 if a:
  title=a.get("title") or report["title"]
  sev=a.get("severity") or report["severity"]
  prog=a.get("program") or report["program"]
  vt_d=", ".join(a.get("vuln_types",[]) or [vt])
  if a.get("bounty","").strip(): bs=a["bounty"]
  sm=a.get("summary","")
  atk=chr(10).join(f"{i+1}. {s}" for i,s in enumerate(a.get("attack_scenario",[])))
  root=a.get("root_cause","")
  mind=a.get("attacker_mindset","")
  dfn=chr(10).join("- "+d for d in a.get("defensive_takeaways",[]))
  var_raw=a.get("variant_hunting","")
  var=chr(10).join(var_raw) if isinstance(var_raw,list) else str(var_raw or "")
  mit=chr(10).join("- "+m for m in a.get("mitre_techniques",[]))
  nts=a.get("notes","")
 else:
  title=report["title"];sev=report["severity"]
  prog=report["program"];vt_d=vt
  sm=report["content"][:400]
  atk=root=mind=dfn=var=mit=nts="*(see original)*"
 N=chr(10)
 out="# "+title+N+N+"## Metadata"+N
 out+="- **Source:** HackerOne"+N
 out+="- **Report:** "+report["id"]+" | "+report["url"]+N
 out+="- **Submitted:** "+report.get("submitted_at","")+N
 out+="- **Reporter:** "+report.get("reporter","")+N
 out+="- **Program:** "+prog+N
 out+="- **Bounty:** "+bs+N
 out+="- **Severity:** "+sev+N
 out+="- **Vuln:** "+vt_d+N
 out+="- **CVEs:** "+cves+N
 out+="- **Category:** "+cat+N+N
 out+="## Summary"+N+sm+N+N
 out+="## Attack scenario"+N+atk+N+N
 out+="## Root cause"+N+root+N+N
 out+="## Attacker mindset"+N+mind+N+N
 out+="## Defensive takeaways"+N+dfn+N+N
 out+="## Variant hunting"+N+var+N+N
 out+="## MITRE ATT&CK"+N+mit+N+N
 out+="## Notes"+N+nts+N+N
 out+="## Full report"+N+"<details><summary>Expand</summary>"+N+N
 out+=report["content"][:8000]+N+N+"</details>"+N+N
 out+="---"+N+"*Analysed by Claude on "+td+"*"+N
 return out

def load_csv(limit=100,sort="bounty"):
 r=requests.get(CSV_URL,headers=HEADERS,timeout=30)
 rows=list(csv.DictReader(r.text.splitlines()))
 if sort=="bounty":
  rows=[x for x in rows if float(x.get("bounty","0") or 0)>0]
  rows.sort(key=lambda x:float(x.get("bounty","0") or 0),reverse=True)
 else:
  rows.sort(key=lambda x:int(x.get("upvotes","0") or 0),reverse=True)
 return rows[:limit]

def load_type(t):
 r=requests.get(MD_BASE+"/"+t+".md",headers=HEADERS,timeout=15)
 if r.status_code!=200: return []
 out=[]
 for line in r.text.splitlines():
  m=re.search(r"\[([^\]]+)\]\(https://hackerone\.com/reports/(\d+)\)",line)
  if m: out.append({"title":m.group(1),"id":m.group(2)})
 return out

def git_push(files,label):
 if not GITHUB_TOKEN: print("No token"); return
 url=f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
 tmp=tempfile.mkdtemp()
 try:
  def R(*a,**k): subprocess.run(list(a),cwd=k.get("cwd"),check=True,capture_output=True)
  R("git","clone","--depth","1",url,tmp)
  R("git","config","user.email","a@b",cwd=tmp)
  R("git","config","user.name","Agent",cwd=tmp)
  n=0
  for p,c in files:
   fp=os.path.join(tmp,p)
   if os.path.exists(fp): continue
   os.makedirs(os.path.dirname(fp),exist_ok=True)
   open(fp,"w").write(c)
   R("git","add",fp,cwd=tmp)
   n+=1
  if n>0:
   R("git","commit","-m",f"import {n} H1 [{label}]",cwd=tmp)
   R("git","push",cwd=tmp)
   print(f"  Pushed {n} [{label}]")
  else: print("  Nothing new")
 except Exception as e: print("Push error:",e)
 finally: shutil.rmtree(tmp,ignore_errors=True)

def process(ids_meta,label,sub="h1-reports"):
 batch=[]
 total=len(ids_meta)
 for i,(rid,meta) in enumerate(ids_meta):
  title=meta.get("title","?")
  print(f"[{i+1}/{total}] H1#{rid}: {title[:55]}")
  r=fetch_h1(rid)
  if not r: print("  skip"); continue
  if meta.get("bounty") and not r["bounty"]: r["bounty"]=meta["bounty"]
  if meta.get("vuln_type") and not r["vuln_type"]: r["vuln_type"]=meta["vuln_type"]
  r["category"]=get_category(r["vuln_type"],r["title"])
  a=analyse(r)
  if a: print(f"  Claude OK [{a.get("severity","?")}]: {a.get("title","")[:50]}")
  else: print("  No analysis")
  c=render(r,a)
  slug=re.sub("[^a-z0-9]+","-",r["title"].lower()).strip("-")[:60]
  p=f"{sub}/{r["category"]}/{rid}-{slug}.md"
  batch.append((p,c))
  time.sleep(1.5)
  if len(batch)>=10: git_push(batch,label); batch=[]
 if batch: git_push(batch,label)
 print(f"Done: {total} [{label}]")

ALL_TYPES=["TOPRCE","TOPXSS","TOPSSRF","TOPSQLI","TOPIDOR","TOPAUTH",
 "TOPACCOUNTTAKEOVER","TOPOAUTH","TOPCSRF","TOPBUSINESSLOGIC",
 "TOPRACECONDITION","TOPSSTI","TOPXXE","TOPGRAPHQL","TOPAPI",
 "TOPINFODISCLOSURE","TOPAUTHORIZATION","TOPSUBDOMAINTAKEOVER",
 "TOPDOS","TOPFILEREADING","TOPMFA","TOPCLICKJACKING",
 "TOPWEBCACHE","TOPREQUESTSMUGGLING","TOPUPLOAD","TOPMOBILE",
 "TOPOPENREDIRECT","TOPOPENID"]

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--limit",type=int,default=100)
 p.add_argument("--sort",default="bounty")
 p.add_argument("--type",default=None)
 p.add_argument("--all-types",dest="at",action="store_true")
 args=p.parse_args()
 if args.at or args.type:
  tlist=ALL_TYPES if args.at else [args.type.upper()]
  for t in tlist:
   rpts=load_type(t)
   cat=t.lower().replace("top","")
   print(t,len(rpts),"reports")
   ids=[(r["id"],{"title":r["title"],"vuln_type":cat}) for r in rpts]
   process(ids,t,"h1-reports/"+cat)
 else:
  rows=load_csv(args.limit,args.sort)
  print("Loaded",len(rows))
  ids=[(row["link"].split("/")[-1],row) for row in rows]
  process(ids,"top-"+str(args.limit)+"-"+args.sort)
if __name__=="__main__": main()
