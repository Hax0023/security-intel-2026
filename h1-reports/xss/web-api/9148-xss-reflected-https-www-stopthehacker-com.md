# XSS Reflected - https://www.stopthehacker.com/

## Metadata
- **Source:** HackerOne
- **Report:** 9148 | https://hackerone.com/reports/9148
- **Submitted:** 2014-04-22
- **Reporter:** dekeeu
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi.

I want to report a Reflected xss vulnerability that I found in www.stopthehacker website and which can affect the safety of your users. This vulnerability allows an attacker to inject in web pages javascript content for sending malicious scripts to an unsuspecting user. This flaw can access any cookies, session tokens, or other sensitive information retained by victim's browser and used wit

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

Hi.

I want to report a Reflected xss vulnerability that I found in www.stopthehacker website and which can affect the safety of your users. This vulnerability allows an attacker to inject in web pages javascript content for sending malicious scripts to an unsuspecting user. This flaw can access any cookies, session tokens, or other sensitive information retained by victim's browser and used with that site. This flaw works only in IE browser.

Link: http://www.stopthehacker.com/?"><script>alert(document.cookie)</script>
Steps for reproduce this vulnerability: Open the link above in IE and you can see that my javascript function alert() was executed.

Regards,
Coltuneac Alexandru

</details>

---
*Analysed by Claude on 2026-05-24*
