#!/usr/bin/env python3
"""H1 Harvester: reads reddelexc/hackerone-reports, analyses each with Claude, pushes to our repo."""
import os,re,sys,time,glob,json,hashlib,subprocess,tempfile,shutil,datetime
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
sys.path.insert(0,os.path.dirname(__file__))
import analyse

load_dotenv()
GITHUB_TOKEN=os.getenv("GITHUB_TOKEN")
GITHUB_REPO=os.getenv("GITHUB_REPO","Hax0023/security-intel-2026")
H1_REPO=os.path.expanduser("~/h1-reports")
HEADERS={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0"}

CAT_MAP={
 "web-api":["xss","csrf","ssrf","idor","xxe","ssti","graphql","open redirect","sql","injection","upload","web cache","file read"],
 "auth-crypto":["auth","account takeover","oauth","mfa","openid","privilege"],
 "memory-binary":["rce","buffer overflow","memory corruption","command injection","code injection"],
 "infra-cloud":["subdomain takeover","dos","request smuggling","misconfiguration"],
 "business-logic":["business logic","race condition"],
}
def cat(vuln,fname):
 t=(vuln+fname).lower()
 for c,ks in CAT_MAP.items():
  if any(k in t for k in ks): return c
 return "uncategorised"

def parse_md_files():
 reports=[]; seen=set()
 pat=re.compile(r"\d+\.\s+\[(.+?)\]\(https://hackerone\.com/reports/(\d+)\)\s+to\s+(.+?)\s+-\s+(\d+).*?\$(\S+)")
 for mdfile in glob.glob(os.path.join(H1_REPO,"tops_by_bug_type","*.md")):
  vt=os.path.basename(mdfile).replace("TOP","").replace(".md","").lower()
  for line in open(mdfile):
   m=pat.match(line.strip())
   if not m: continue
   rid=m.group(2)
   if rid in seen: continue
   seen.add(rid)
   try: b=float(m.group(5).replace(",",""))
   except: b=0.0
   reports.append({"id":rid,"title":m.group(1),
    "url":f"https://hackerone.com/reports/{rid}",
    "program":m.group(3).strip(),
    "upvotes":int(m.group(4)),"bounty":b,"vuln_type":vt})
 reports.sort(key=lambda r:r["upvotes"],reverse=True)
 print(f"Parsed {len(reports)} unique reports")
 return reports

def fetch_h1_report(url):
 """Fetch a HackerOne report page - they render server-side for public reports."""
 try:
  r=requests.get(url,headers=HEADERS,timeout=20,allow_redirects=True)
  if r.status_code!=200: return ""
  soup=BeautifulSoup(r.text,"lxml")
  # Remove nav/header/footer
  for t in soup(["nav","header","footer","script","style"]): t.decompose()
  # HackerOne report content is in specific divs
  body=(soup.find(class_=re.compile(r"report|activity|description|vulnerability",re.I))
        or soup.find("main") or soup.body)
  if not body: return ""
  text="\n".join(l for l in body.get_text().splitlines() if l.strip())
  return text[:6000]
 except Exception as e:
  return ""

def already_exists(tmp_dir,report_id):
 """Check if this H1 report is already in our repo."""
 for f in glob.glob(os.path.join(tmp_dir,"**",f"*h1-{report_id}*"),recursive=True):
  return True
 return False

def make_fname(r):
 ts=re.sub("[^a-z0-9]+","-",r["title"].lower()).strip("-")[:55]
 prog=re.sub("[^a-z0-9]+","-",r["program"].lower()).strip("-")[:20]
 return f"h1-{r['id']}-{prog}-{ts}.md"

def main():
 import argparse
 ap=argparse.ArgumentParser()
 ap.add_argument("--limit",type=int,default=50)
 ap.add_argument("--min-upvotes",type=int,default=50)
 ap.add_argument("--vuln",default="")
 args=ap.parse_args()
 reports=parse_md_files()
 if args.min_upvotes: reports=[r for r in reports if r["upvotes"]>=args.min_upvotes]
 if args.vuln: reports=[r for r in reports if args.vuln.lower() in r["vuln_type"]]
 print(f"After filters: {len(reports)} (limit {args.limit})")
 repo_url=f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
 tmp=tempfile.mkdtemp()
 try:
  subprocess.run(["git","clone","--depth","1",repo_url,tmp],check=True,capture_output=True)
  for cfg in [["user.email","agent@localhost"],["user.name","H1 Harvester"]]:
   subprocess.run(["git","config"]+cfg,cwd=tmp,check=True,capture_output=True)
  created=skipped=0
  for r in reports[:args.limit]:
   category=cat(r["vuln_type"],r.get("source_file",""))
   fname=make_fname(r)
   dirp=os.path.join(tmp,category,"h1-reports")
   os.makedirs(dirp,exist_ok=True)
   fpath=os.path.join(dirp,fname)
   if os.path.exists(fpath): skipped+=1; continue
   print(f"\n[{created+skipped+1}] {r['program']} | {r['upvotes']}up ${r['bounty']:.0f}")
   print(f"  {r['title'][:70]}")
   text=fetch_h1_report(r["url"])
   if len(text)<100:
    text=(f"Program: {r['program']}\nVuln: {r['vuln_type']}\n"
          f"Upvotes: {r['upvotes']}\nBounty: ${r['bounty']}\n\n"
          f"Top HackerOne report: {r['title']}")
    print("  (fallback context only)")
   else:
    print(f"  Fetched {len(text)} chars")
   a=analyse.run(r["title"],r["url"],text)
   sev="critical" if r["upvotes"]>200 else "high"
   rpt={"source":"HackerOne","id":f"H1-{r['id']}",
        "title":r["title"],"url":r["url"],"author":"Various",
        "published":datetime.date.today().isoformat(),
        "program":r["program"],"bounty":r["bounty"],
        "severity":sev,"tags":[r["vuln_type"]],
        "summary":"","category":category}
   content=analyse.render(rpt,a)
   open(fpath,"w").write(content)
   subprocess.run(["git","add",fpath],cwd=tmp,check=True,capture_output=True)
   created+=1
   print(f"  saved {a.get('severity','?') if a else 'no-analysis'}")
   time.sleep(1.5)
   if created%20==0 and created>0:
    subprocess.run(["git","commit","-m",f"h1: {created} reports"],cwd=tmp,check=True,capture_output=True)
    subprocess.run(["git","push"],cwd=tmp,check=True,capture_output=True)
    print(f"-- pushed {created} --")
  if created>0:
   subprocess.run(["git","commit","--allow-empty","-m",f"h1: done {created}"],cwd=tmp,check=True,capture_output=True)
   subprocess.run(["git","push"],cwd=tmp,check=True,capture_output=True)
  print(f"\nDone: {created} created, {skipped} skipped")
 except Exception as e: print("Error:",e)
 finally: shutil.rmtree(tmp,ignore_errors=True)

if __name__=="__main__":
 main()
