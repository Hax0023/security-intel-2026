# files.acrobat.com stored XSS via send file

## Metadata
- **Source:** HackerOne
- **Report:** 50358 | https://hackerone.com/reports/50358
- **Submitted:** 2015-03-06
- **Reporter:** reactors08
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Description of the sending file vulnerable to xss
Proof:
https://files.acrobat.com/a/preview/c9efeb22-75a5-4268-ad57-f8f694aa7a1d

steps to reproduce:
- go to https://cloud.acrobat.com/send and select file to send
-  check an option "Create Anonymous Link"
- input any subject 
- input payload `<img src=x onerror=alert(1)>` to description
- click "Create Link" button
- follow to created l

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

Description of the sending file vulnerable to xss
Proof:
https://files.acrobat.com/a/preview/c9efeb22-75a5-4268-ad57-f8f694aa7a1d

steps to reproduce:
- go to https://cloud.acrobat.com/send and select file to send
-  check an option "Create Anonymous Link"
- input any subject 
- input payload `<img src=x onerror=alert(1)>` to description
- click "Create Link" button
- follow to created link

</details>

---
*Analysed by Claude on 2026-05-24*
