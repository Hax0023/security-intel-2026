# owncloud.com: Persistent XSS In Account Profile

## Metadata
- **Source:** HackerOne
- **Report:** 116254 | https://hackerone.com/reports/116254
- **Submitted:** 2016-02-13
- **Reporter:** securitary
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Quotation marks are not sanitized in one of the HTML tags inside of the profile when dealing with first & last names. It is an <iframe> tag. In the attached PoC screenshot, I included a functional first name that triggers an alert() call. Inside, I pasted the HTML tag where it breaks.

I don't know owncloud inside-out, so I don't know if anybody else is able to see my user profile. If they are, th

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

Quotation marks are not sanitized in one of the HTML tags inside of the profile when dealing with first & last names. It is an <iframe> tag. In the attached PoC screenshot, I included a functional first name that triggers an alert() call. Inside, I pasted the HTML tag where it breaks.

I don't know owncloud inside-out, so I don't know if anybody else is able to see my user profile. If they are, then this would be able to pull anybody else's session cookies. However, even if not, it could still be used to BeEF-hook others if they access your account or you get one-time access to their account, so it should still be fixed.

</details>

---
*Analysed by Claude on 2026-05-24*
