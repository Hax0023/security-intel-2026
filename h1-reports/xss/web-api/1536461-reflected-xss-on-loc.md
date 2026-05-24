# Reflected  XSS on  ███?loc=

## Metadata
- **Source:** HackerOne
- **Report:** 1536461 | https://hackerone.com/reports/1536461
- **Submitted:** 2022-04-10
- **Reporter:** 3amoura
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Summary:
=========
Detalis XSS
-----------
Cross-Site Scripting (XSS) attacks are a type of injection, in which malicious scripts are injected into otherwise benign and trusted websites. XSS attacks occur when an attacker uses a web application to send malicious code, generally in the form of a browser side script, to a different end user. Flaws that allow these attacks to succeed are quite widesp

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

Summary:
=========
Detalis XSS
-----------
Cross-Site Scripting (XSS) attacks are a type of injection, in which malicious scripts are injected into otherwise benign and trusted websites. XSS attacks occur when an attacker uses a web application to send malicious code, generally in the form of a browser side script, to a different end user. Flaws that allow these attacks to succeed are quite widespread and occur anywhere a web application uses input from a user within the output it generates without validating or encoding it.

## Steps To Reproduce:


  1. Go to Those Links.
███████
Filter input on arrival
Encode data on output
Use appropriate response headers
Content Security Policy.
These all are standards concepts for fix the XSS vulnerabilities.

## Impact

screenshot:
████████
POC:
██████████

</details>

---
*Analysed by Claude on 2026-05-24*
