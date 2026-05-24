# X-XSS-Protection -> Misconfiguration

## Metadata
- **Source:** HackerOne
- **Report:** 289846 | https://hackerone.com/reports/289846
- **Submitted:** 2017-11-13
- **Reporter:** bb343cc5cbd74210c09dafe
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there,

**URL:** https://www.sfl-tap.army.mil/
I have seen that the website is using the X-XSS-Protection Header.

But it has a strange configuration.
When I take a look at securityheaders, I've seen that you guys use this as configuration.

**X-XSS-Protection:** DENY

DENY is used for the X-Frame Option instead of the X-XSS-Protection. The good configuration should be:

**XSS-XSS-Protection:**

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

Hi there,

**URL:** https://www.sfl-tap.army.mil/
I have seen that the website is using the X-XSS-Protection Header.

But it has a strange configuration.
When I take a look at securityheaders, I've seen that you guys use this as configuration.

**X-XSS-Protection:** DENY

DENY is used for the X-Frame Option instead of the X-XSS-Protection. The good configuration should be:

**XSS-XSS-Protection:** 1; mode=block

And not DENY. This is used for the X-Frame Option.

</details>

---
*Analysed by Claude on 2026-05-24*
