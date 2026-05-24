# Self-XSS in Partners Profile

## Metadata
- **Source:** HackerOne
- **Report:** 145289 | https://hackerone.com/reports/145289
- **Submitted:** 2016-06-17
- **Reporter:** s0nk3y
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi , I have found an XSS stored vulnerability in the page paterns uber profile edit. the vulnerability in the vat number. Steps to reproduce:
1. Login to partners.uber.com
2. Go to a page https://partners.uber.com/profile/
3. In the vat number enter a payload xss :  "><img src=x onerror=alert(0)> "><img src=x onerror=alert(0)> <script>alert(0)</script>
4. save

thank you, please tell me if the bug

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

Hi , I have found an XSS stored vulnerability in the page paterns uber profile edit. the vulnerability in the vat number. Steps to reproduce:
1. Login to partners.uber.com
2. Go to a page https://partners.uber.com/profile/
3. In the vat number enter a payload xss :  "><img src=x onerror=alert(0)> "><img src=x onerror=alert(0)> <script>alert(0)</script>
4. save

thank you, please tell me if the bug has been fixed.

</details>

---
*Analysed by Claude on 2026-05-24*
