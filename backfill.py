#!/usr/bin/env python3
"""One-time backfill: re-analyse all reports that lack Claude analysis."""
import os,re,glob,subprocess,tempfile,shutil,datetime
from dotenv import load_dotenv
load_dotenv()
sys_path_insert=__import__("sys").path.insert
sys_path_insert(0,os.path.dirname(__file__))
import analyse

GITHUB_TOKEN=os.getenv("GITHUB_TOKEN")
GITHUB_REPO=os.getenv("GITHUB_REPO","Hax0023/security-intel-2026")

def extract_meta(content):
    """Pull URL and title from existing markdown file."""
    url=re.search(r"\*\*(?:Original writeup|Writeup):\*\*\s*(\S+)",content)
    title=re.search(r"^#\s+(.+)$",content,re.MULTILINE)
    return (title.group(1).strip() if title else ""),\
           (url.group(1).strip() if url else "")

def get_category(path):
    return path.split(os.sep)[0]

def main():
    base=os.path.dirname(__file__)
    files=[f for f in glob.glob(os.path.join(base,"**","*.md"),recursive=True)
           if "weekly-digests" not in f
           and "Analysed by Claude" not in open(f).read()
           and f.endswith(".md")
           and "README" not in f and "_template" not in f]
    print(f"Found {len(files)} reports to backfill")
    if not files: print("Nothing to do."); return

    repo_url=f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
    tmp=tempfile.mkdtemp()
    try:
        subprocess.run(["git","clone","--depth","1",repo_url,tmp],check=True,capture_output=True)
        subprocess.run(["git","config","user.email","agent@localhost"],cwd=tmp,check=True,capture_output=True)
        subprocess.run(["git","config","user.name","BB Intel Agent"],cwd=tmp,check=True,capture_output=True)
        updated=0
        for i,fpath in enumerate(files):
            rel=os.path.relpath(fpath,base)
            content=open(fpath).read()
            title,url=extract_meta(content)
            print(f"[{i+1}/{len(files)}] {rel[:60]}")
            print(f"  URL: {url[:80]}")
            if not url: print("  skip"); continue
            raw=analyse.fetch_article(url)
            if len(raw)<100: print("  short"); continue
            a=analyse.run(title,url,raw)
            if not a: print("  no-analysis"); continue
            def g(pat): m=re.search(pat,content); return m.group(1).strip() if m else ""
            rpt={"source":g(r"\*\*Source:\*\*\s*(.+)"),
                 "author":g(r"\*\*Author:\*\*\s*(.+)"),
                 "published":g(r"\*\*Date:\*\*\s*(.+)"),
                 "url":url,"category":get_category(rel),
                 "tags":a.get("vuln_types",[]),
                 "program":a.get("program",""),
                 "bounty":0,"severity":a.get("severity","")}
            new_content=analyse.render(rpt,a)
            open(fpath,"w").write(new_content)
            gp=os.path.join(tmp,rel)
            os.makedirs(os.path.dirname(gp),exist_ok=True)
            open(gp,"w").write(new_content)
            subprocess.run(["git","add",gp],cwd=tmp,check=True,capture_output=True)
            updated+=1
            print(f"  OK [{a.get("severity","?")}] {a.get("title","")[:55]}")
            import time; time.sleep(1.5)
        if updated>0:
            subprocess.run(["git","commit","--allow-empty","-m","backfill"],cwd=tmp,check=True,capture_output=True)
            subprocess.run(["git","push"],cwd=tmp,check=True,capture_output=True)
        print(f"Done: {updated}/{len(files)}")
    except Exception as e: print("Error:",e)
    finally: shutil.rmtree(tmp,ignore_errors=True)
main()
