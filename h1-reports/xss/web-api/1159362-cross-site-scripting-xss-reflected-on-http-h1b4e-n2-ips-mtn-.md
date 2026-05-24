# Cross-site Scripting (XSS) - Reflected on http://h1b4e.n2.ips.mtn.co.ug:8080 via Nginx-module

## Metadata
- **Source:** HackerOne
- **Report:** 1159362 | https://hackerone.com/reports/1159362
- **Submitted:** 2021-04-09
- **Reporter:** renzi
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hello,
I found a Reflected Cross site Scripting (XSS) on  http://h1b4e.n2.ips.mtn.co.ug:8080 . With this security flaw is possible rewrite the content of page, executing JS codes...

## Steps To Reproduce:
How we can reproduce the issue:

  1. Go to http://h1b4e.n2.ips.mtn.co.ug:8080/status%3E%3Cscript%3Ealert(31337)%3C%2Fscript%3E
  2. We can see alert message 31337
  
{F1259889}

## 

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

## Summary:
Hello,
I found a Reflected Cross site Scripting (XSS) on  http://h1b4e.n2.ips.mtn.co.ug:8080 . With this security flaw is possible rewrite the content of page, executing JS codes...

## Steps To Reproduce:
How we can reproduce the issue:

  1. Go to http://h1b4e.n2.ips.mtn.co.ug:8080/status%3E%3Cscript%3Ealert(31337)%3C%2Fscript%3E
  2. We can see alert message 31337
  
{F1259889}

## Supporting Material/References:

* https://owasp.org/www-community/attacks/xss/

## Impact

* The attacker can execute JS code.
* Rewrite the content of Page

</details>

---
*Analysed by Claude on 2026-05-24*
