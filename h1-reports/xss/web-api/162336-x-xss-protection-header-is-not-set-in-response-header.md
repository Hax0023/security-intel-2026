# x-xss protection header is not set in response header

## Metadata
- **Source:** HackerOne
- **Report:** 162336 | https://hackerone.com/reports/162336
- **Submitted:** 2016-08-23
- **Reporter:** karthic
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** web-api

## Summary
URL : http://inside.gratipay.com/

Description : 
This header enables the Cross-site scripting (XSS) filter built into most recent web browsers. It's usually enabled by default anyway, so the role of this header is to re-enable the filter for this particular website if it was disabled by the user. This header is supported in IE 8+, and in Chrome (not sure which versions). The anti-XSS filter was a

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

URL : http://inside.gratipay.com/

Description : 
This header enables the Cross-site scripting (XSS) filter built into most recent web browsers. It's usually enabled by default anyway, so the role of this header is to re-enable the filter for this particular website if it was disabled by the user. This header is supported in IE 8+, and in Chrome (not sure which versions). The anti-XSS filter was added in Chrome 4. Its unknown if that version honored this header.

Solution : Need to set X-XSS-Protection: 1; mode=block in response header

</details>

---
*Analysed by Claude on 2026-05-24*
