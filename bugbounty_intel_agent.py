#!/usr/bin/env python3
import os,re,time,logging,hashlib,datetime,calendar
import requests,feedparser
from bs4 import BeautifulSoup
from github import Github,GithubException
from dotenv import load_dotenv
import analyse

load_dotenv()
GITHUB_TOKEN=os.getenv("GITHUB_TOKEN")
GITHUB_REPO=os.getenv("GITHUB_REPO","Hax0023/security-intel-2026")
LOOKBACK_HOURS=int(os.getenv("LOOKBACK_HOURS","24"))
MIN_BOUNTY=float(os.getenv("MIN_BOUNTY","0"))
DRY_RUN=os.getenv("DRY_RUN","false").lower()=="true"
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)-8s %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
log=logging.getLogger("bb-intel")
HEADERS={"User-Agent":"SecurityResearchBot/1.0 github.com/Hax0023/security-intel-2026"}
CUTOFF=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)-datetime.timedelta(hours=LOOKBACK_HOURS)
SEC_KWS=["xss","sql","ssrf","idor","rce","auth","bypass","vulnerability","bug bounty","exploit","injection","overflow","disclosure","cve","security","hacking","pentest","bounty","hack","0day","zero-day"]

VULN_CATEGORY={
    "web-api":["xss","sqli","sql injection","ssrf","idor","csrf","xxe","open redirect","graphql","ssti","path traversal","lfi","cors","clickjacking","injection","api","rfi"],
    "auth-crypto":["auth bypass","authentication bypass","jwt","oauth","ato","account takeover","session","password reset","2fa bypass","mfa bypass","saml","sso","token","hardcoded"],
    "memory-binary":["buffer overflow","bof","use-after-free","uaf","heap overflow","stack overflow","memory corruption","rce","remote code execution","null pointer","integer overflow","format string","out-of-bounds"],
    "infra-cloud":["kubernetes","k8s","aws","azure","gcp","docker","container","cloud","iam","s3 bucket","privilege escalation","metadata service","imds","vpc"],
    "supply-chain":["npm","pypi","maven","dependency","ci/cd","pipeline","typosquatting","supply chain","github actions","build system"],
    "ai-ml":["prompt injection","llm","ai security","jailbreak","adversarial","model theft","training data"],
    "business-logic":["business logic","race condition","price manipulation","rate limit bypass","captcha bypass","mass assignment","workflow bypass"],
    "hardware-firmware":["firmware","uefi","bios","cpu","bootloader","hardware","side channel","embedded","microcontroller"],
}

def categorise(title,tags):
    text=(title+" "+" ".join(tags)).lower()
    scores={c:sum(1 for kw in kws if kw in text) for c,kws in VULN_CATEGORY.items()}
    best=max(scores,key=scores.get)
    return best if scores[best]>0 else "uncategorised"

def infer_severity(title,tags):
    t=(title+" "+" ".join(tags)).lower()
    if any(w in t for w in ["critical","rce","remote code execution","account takeover"]): return "critical"
    if any(w in t for w in ["high","ssrf","sql injection","authentication bypass","auth bypass"]): return "high"
    if any(w in t for w in ["medium","idor","xss","csrf","open redirect"]): return "medium"
    if any(w in t for w in ["low","information disclosure","clickjacking"]): return "low"
    return "unknown"

def render(r):
    b=r.get("bounty",0)
    bs=f"${b:,.0f}" if isinstance(b,(int,float)) and b>0 else (str(b) if b else "Not disclosed")
    today=datetime.date.today().isoformat()
    tags=", ".join(r.get("tags",[])[:6]) or "See writeup"
    src=r.get("source",""); pub=str(r.get("published",""))[:10]
    auth=r.get("author","Unknown"); prog=r.get("program","Unknown")
    sev=r.get("severity","unknown"); cat=r.get("category","")
    url=r.get("url",""); title=r.get("title","Untitled")
    summary=r.get("summary","") or "*(See original writeup — link above)*"
    return f"""# {title}

## Metadata
- **Source:** {src}
- **Date published:** {pub}
- **Author:** {auth}
- **Program / Target:** {prog}
- **Bounty:** {bs}
- **Severity:** {sev}
- **Vulnerability type(s):** {tags}
- **Category:** {cat}
- **Original writeup:** {url}

## Summary
{summary}

## Attack scenario (step by step)
1. 
2. 
3. 

## Root cause


## Attacker mindset
<!-- How did the researcher find this? What assumption did they break? -->

## Defensive takeaways
- 

## Variant hunting
<!-- Where else could this same bug class exist? -->
- 

## MITRE ATT&CK mapping
- 

## Notes
- 

---
*Auto-harvested {today}*
"""

def fetch_hackerone():
 log.info("writeups.io...")
 res=[]
 try:
  r=requests.get("https://writeups.io/new/",headers=HEADERS,timeout=20)
  r.raise_for_status()
 except Exception as e: log.warning("WU: %s",e); return []
 soup=BeautifulSoup(r.text,"lxml")
 for item in soup.select(".post-item"):
  links=item.select("a[href]")
  ext=[a for a in links if "/posts/details/" not in a.get("href","") and a.get("href","").startswith("http")]
  if not ext: continue
  url=ext[0].get("href","")
  title=ext[0].get_text(strip=True)
  cols=item.find_all("div",recursive=False)
  vuln=cols[2].get_text(strip=True) if len(cols)>2 else ""
  desc=cols[4].get_text(strip=True) if len(cols)>4 else ""
  tags=[t.strip() for t in vuln.split(",") if t.strip()]
  combo=(title+" "+desc+" "+" ".join(tags)).lower()
  if not any(kw in combo for kw in SEC_KWS): continue
  uid=hashlib.md5(url.encode()).hexdigest()[:10]
  res.append({"source":"writeups.io","id":"WU-"+uid,
   "title":title or desc[:80],"url":url,
   "author":"Various","published":datetime.date.today().isoformat(),
   "program":"Various","bounty":0,
   "severity":infer_severity(title,tags),
   "tags":tags,"summary":desc})
 log.info("writeups.io: %d",len(res))
 return res

RSS_FEEDS=[
    ("Infosec Writeups",    "https://medium.com/feed/infosecwriteups"),
    ("Medium Bug Bounty",   "https://medium.com/feed/tag/bug-bounty-writeup"),
    ("Google Project Zero", "https://googleprojectzero.blogspot.com/feeds/posts/default"),
    ("PortSwigger Research","https://portswigger.net/research/rss"),
    ("Intigriti Blog",      "https://www.intigriti.com/blog/feed"),
    ("Assetnote Research",  "https://blog.assetnote.io/feed.xml"),
    ("Detectify Labs",      "https://labs.detectify.com/feed/"),
    ("HackerOne Blog",      "https://www.hackerone.com/blog.rss"),
]

def fetch_rss():
    results=[]
    for name,url in RSS_FEEDS:
        log.info("RSS: %s",name)
        try: parsed=feedparser.parse(url,request_headers=HEADERS)
        except Exception as e: log.warning("RSS %s: %s",name,e); continue
        for e in parsed.entries:
            t=None
            for attr in ("published_parsed","updated_parsed","created_parsed"):
                raw=getattr(e,attr,None)
                if raw:
                    try: t=datetime.datetime.utcfromtimestamp(calendar.timegm(raw))
                    except: pass
                    break
            if t and t<CUTOFF: continue
            title=e.get("title",""); link=e.get("link","")
            author=e.get("author",name)
            summary=BeautifulSoup(e.get("summary",""),"lxml").get_text()[:500].strip()
            tags=[tg.get("term","") for tg in e.get("tags",[])]
            combo=(title+" "+summary+" "+" ".join(tags)).lower()
            if not any(kw in combo for kw in SEC_KWS): continue
            results.append({"source":name,
                "id":"RSS-"+hashlib.md5(link.encode()).hexdigest()[:10],
                "title":title,"url":link,"author":author,
                "published":t.isoformat() if t else "",
                "program":"Various","bounty":0,
                "severity":infer_severity(title,tags),
                "tags":tags,"summary":summary})
        time.sleep(0.5)
    log.info("RSS: %d entries",len(results))
    return results

def fetch_pentesterland():
    log.info("Fetching Pentester.land...")
    results=[]
    try:
        r=requests.get("https://pentester.land/writeups/",headers=HEADERS,timeout=30)
        r.raise_for_status()
    except Exception as e: log.warning("Pentester.land: %s",e); return []
    soup=BeautifulSoup(r.text,"lxml")
    for row in soup.select("table tbody tr"):
        cols=row.find_all("td")
        if len(cols)<4: continue
        a=cols[0].find("a")
        if not a: continue
        title=a.get_text(strip=True); url=a.get("href","")
        tags=[t.strip() for t in cols[1].get_text(separator=",",strip=True).split(",") if t.strip()]
        prog=cols[2].get_text(strip=True) if len(cols)>2 else "Unknown"
        auth=cols[3].get_text(strip=True) if len(cols)>3 else "Unknown"
        braw=cols[4].get_text(strip=True) if len(cols)>4 else ""
        b=0.0
        if braw and braw!="-":
            try: b=float(re.sub(r"[^\d.]","",braw))
            except: pass
        pub=cols[5].get_text(strip=True) if len(cols)>5 else ""
        try:
            dt=datetime.datetime.strptime(pub[:10],"%Y-%m-%d")
            if dt<CUTOFF: continue
        except: pass
        if MIN_BOUNTY>0 and b<MIN_BOUNTY: continue
        combo=(title+" "+" ".join(tags)).lower()
        if not any(kw in combo for kw in SEC_KWS): continue
        results.append({"source":"Pentester.land",
            "id":"PL-"+hashlib.md5(url.encode()).hexdigest()[:10],
            "title":title,"url":url,"author":auth,"published":pub,
            "program":prog,"bounty":b,"severity":infer_severity(title,tags),
            "tags":tags,"summary":""})
    log.info("Pentester.land: %d",len(results))
    return results

def dedup(items):
    seen_u,seen_i,out=set(),set(),[]
    for x in items:
        u,i=x.get("url",""),x.get("id","")
        if (u and u in seen_u) or (i and i in seen_i): continue
        if u: seen_u.add(u)
        if i: seen_i.add(i)
        out.append(x)
    return out

def push(reports):
 import subprocess,tempfile,shutil
 if not GITHUB_TOKEN: log.error("No token"); return 0,0
 repo_url=f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
 tmp=tempfile.mkdtemp()
 try:
  subprocess.run(["git","clone","--depth","1",repo_url,tmp],
   check=True,capture_output=True)
  subprocess.run(["git","config","user.email","agent@localhost"],
   cwd=tmp,check=True,capture_output=True)
  subprocess.run(["git","config","user.name","BB Intel Agent"],
   cwd=tmp,check=True,capture_output=True)
  ym=datetime.date.today().strftime("%Y-%m")
  created=skipped=0
  for r in reports:
   r["category"]=categorise(r.get("title",""),r.get("tags",[]))
   ds=str(r.get("published",""))[:10] or datetime.date.today().isoformat()
   ss=re.sub("[^a-z0-9]+","-",r.get("source","").lower()).strip("-")[:20]
   ts=re.sub("[^a-z0-9]+","-",r.get("title","").lower()).strip("-")[:55]
   uid=(r.get("id","") or "")[-10:].replace("/","-")
   fname=f"{ds}-{ss}-{ts}-{uid}.md"
   cat=r["category"]
   dirp=os.path.join(tmp,cat,ym)
   os.makedirs(dirp,exist_ok=True)
   fpath=os.path.join(dirp,fname)
   if os.path.exists(fpath): skipped+=1; continue
   if DRY_RUN: log.info("[DRY] %s/%s/%s",cat,ym,fname); created+=1; continue
   raw_text=analyse.fetch_article(r.get("url",""))
   a_data=analyse.run(r.get("title",""),r.get("url",""),raw_text)
   content=analyse.render(r,a_data)
   open(fpath,"w").write(content)
   subprocess.run(["git","add",fpath],cwd=tmp,check=True,capture_output=True)
   created+=1
  if created>0 and not DRY_RUN:
   msg=f"feat: add {created} reports [{datetime.date.today().isoformat()}]"
   subprocess.run(["git","commit","-m",msg],cwd=tmp,check=True,capture_output=True)
   subprocess.run(["git","push"],cwd=tmp,check=True,capture_output=True)
   log.info("Pushed %d files in one commit",created)
 except Exception as e: log.error("push error: %s",e)
 finally: shutil.rmtree(tmp,ignore_errors=True)
 return created,skipped

def push_digest(reports):
 import subprocess,tempfile,shutil
 if not GITHUB_TOKEN or not reports: return
 repo_url=f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
 today=datetime.date.today(); wk=today.isocalendar()[1]
 dpath=f"weekly-digests/{today.year}-W{wk:02d}.md"
 by_cat={}
 for r in reports: by_cat.setdefault(r.get("category","?"),[]).append(r)
 sec="\n\n## "+today.isoformat()+" - "+str(len(reports))+" reports\n"
 for cat,items in sorted(by_cat.items()):
  sec+="\n### "+cat+" ("+str(len(items))+")\n"
  for r in items:
   b=r.get("bounty",0)
   bs=f" ${b:,.0f}" if isinstance(b,(int,float)) and b>0 else ""
   sev=(r.get("severity","") or "").upper()
   t=r.get("title",""); u=r.get("url",""); src=r.get("source","")
   tags=", ".join(r.get("tags",[])[:4])
   sec+="- ["+t+"]("+u+") | "+sev+bs+" | "+src+" | "+tags+"\n"
 if DRY_RUN: return
 tmp=tempfile.mkdtemp()
 try:
  def R(*a,**k):
   subprocess.run(list(a),cwd=k.get("cwd"),check=True,capture_output=True)
  R("git","clone","--depth","1",repo_url,tmp)
  R("git","config","user.email","a@b",cwd=tmp)
  R("git","config","user.name","Agent",cwd=tmp)
  fp=os.path.join(tmp,dpath)
  os.makedirs(os.path.dirname(fp),exist_ok=True)
  hdr="# BB Intel W"+str(wk)+" "+str(today.year)+"\n"
  base=open(fp).read() if os.path.exists(fp) else hdr
  if today.isoformat() in base: log.info("Digest already has today, skipping"); return
  open(fp,"w").write(base+sec)
  R("git","add",fp,cwd=tmp)
  R("git","commit","-m","digest",cwd=tmp)
  R("git","push",cwd=tmp)
  log.info("Digest pushed: %s",dpath)
 except Exception as e: log.error("digest:%s",e)
 finally: shutil.rmtree(tmp,ignore_errors=True)

def main():
    log.info("="*55)
    log.info("Bug Bounty Intel Agent  %s",datetime.datetime.now().isoformat())
    log.info("Lookback: %dh | DRY_RUN: %s",LOOKBACK_HOURS,DRY_RUN)
    log.info("="*55)
    all_r=dedup(fetch_hackerone()+fetch_rss()+fetch_pentesterland())
    log.info("Total unique: %d",len(all_r))
    if not all_r: log.info("Nothing new."); return
    c,s=push(all_r)
    log.info("Created: %d  Skipped: %d",c,s)
    push_digest(all_r)
    log.info("Done.")

if __name__=="__main__":
    main()
