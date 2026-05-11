
import re, json, requests, anthropic
from bs4 import BeautifulSoup
from anthropic.lib.credentials._providers import CredentialsFile

HEADERS = {"User-Agent": "SecurityResearchBot/1.0"}
MODEL   = "claude-haiku-4-5-20251001"

def get_client():
    return anthropic.Anthropic(credentials=CredentialsFile("default"))

def fetch_article(url,n=5000):
    bua="Mozilla/5.0 Chrome/124.0"
    for ua in [bua,HEADERS["User-Agent"]]:
        try:
            r=requests.get(url,headers={"User-Agent":ua},timeout=15,allow_redirects=True)
            if r.status_code in (403,429,503): continue
            r.raise_for_status()
            soup=BeautifulSoup(r.text,"lxml")
            for t in soup(["nav","footer","script","style","aside","header"]): t.decompose()
            body=soup.find("article") or soup.find("main") or soup.body
            if not body: continue
            text="\n".join(l for l in body.get_text().splitlines() if l.strip())
            if len(text)>200: return text[:n]
        except Exception: continue
    return ""


PROMPT = (
    "You are a senior security researcher. Analyse this bug bounty writeup. "
    "Respond ONLY with valid JSON (no markdown). Keys: "
    "title, severity(critical/high/medium/low/unknown), vuln_types(list), "
    "program, bounty(str), summary(2-3 sentences), "
    "attack_scenario(list of 4-6 steps), root_cause, attacker_mindset, "
    "defensive_takeaways(list), variant_hunting, "
    "mitre_techniques(list eg T1190 - Exploit Public-Facing App), notes"
)

def run(title, url, text):
    if not text or len(text) < 100: return None
    try:
        client = get_client()
        msg = "\n".join(["Title: "+title, "URL: "+url, "", "CONTENT:", text])
        resp = client.messages.create(
            model=MODEL, max_tokens=1500, system=PROMPT,
            messages=[{"role": "user", "content": msg}])
        raw = resp.content[0].text.strip()
        while raw.startswith("`"): raw = raw[raw.index("{"):]
        while raw.endswith("`"):  raw = raw[:raw.rindex("}")+1]
        return json.loads(raw)
    except:
        return None

def render(r, a=None):
    import datetime
    b   = r.get("bounty", 0)
    bs  = ("$"+f"{b:,.0f}") if isinstance(b,(int,float)) and b>0 else "Not disclosed"
    td  = datetime.date.today().isoformat()
    tags = ", ".join(r.get("tags",[])[:5]) or "See writeup"
    if a:
        title = a.get("title") or r.get("title","Untitled")
        sev   = a.get("severity") or r.get("severity","?")
        prog  = a.get("program")  or r.get("program","?")
        vt    = ", ".join(a.get("vuln_types",[]) or [tags])
        if a.get("bounty","") and str(a["bounty"]).strip(): bs = str(a["bounty"])
        sm    = a.get("summary") or r.get("summary","")
        atk   = "\n".join(f"{i+1}. {s}" for i,s in enumerate(a.get("attack_scenario",[])))
        root  = a.get("root_cause","")
        mind  = a.get("attacker_mindset","")
        dfn   = "\n".join("- "+d for d in a.get("defensive_takeaways",[]))
        var   = a.get("variant_hunting","")
        mit   = "\n".join("- "+m for m in a.get("mitre_techniques",[]))
        nts   = a.get("notes","")
    else:
        title = r.get("title","Untitled"); sev = r.get("severity","?")
        prog  = r.get("program","?");      vt  = tags
        sm    = r.get("summary","") or "*(see original writeup)*"
        atk   = "1. \n2. \n3. "
        root  = mind = var = nts = "*(see original writeup)*"
        dfn   = mit = "- "
    lines = [
        f"# {title}", "", "## Metadata",
        f"- **Source:** {r.get('source','')}",
        f"- **Date:** {str(r.get('published',''))[:10]}",
        f"- **Author:** {r.get('author','?')}",
        f"- **Program:** {prog}",
        f"- **Bounty:** {bs}",
        f"- **Severity:** {sev}",
        f"- **Vuln types:** {vt}",
        f"- **Category:** {r.get('category','')}",
        f"- **Writeup:** {r.get('url','')}",
        "", f"## Summary", sm,
        "", f"## Attack scenario (step by step)", atk,
        "", f"## Root cause", root,
        "", f"## Attacker mindset", mind,
        "", f"## Defensive takeaways", dfn,
        "", f"## Variant hunting", var,
        "", f"## MITRE ATT&CK", mit,
        "", f"## Notes", nts,
        "", f"---", f"*Analysed by Claude ({MODEL}) on {td}*",
    ]
    safe=[str(x) for x in lines]
    return chr(10).join(safe)+chr(10)
    return chr(10).join(ls2)+chr(10)
