# XSS on partners.uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 42393 | https://hackerone.com/reports/42393
- **Submitted:** 2015-01-03
- **Reporter:** kirtixs
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

I have discovered a reflected XSS on partners.uber.com 

When accessing https://partners.uber.com/signup/global/ with the appropriate parameters, for example: https://partners.uber.com/signup/global/?referrer_uuid=21f5fbbd-b79f-4a16-9976-01096fb556c7&place_id=ChIJPaCKh-tmA4wR7JEkNDrNDSU&utm_source=twitter&location=Carolina%2C+Carolina%2C+Puerto+Rico&lat=18.3807819&lng=-65.9573871999999

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

Hello,

I have discovered a reflected XSS on partners.uber.com 

When accessing https://partners.uber.com/signup/global/ with the appropriate parameters, for example: https://partners.uber.com/signup/global/?referrer_uuid=21f5fbbd-b79f-4a16-9976-01096fb556c7&place_id=ChIJPaCKh-tmA4wR7JEkNDrNDSU&utm_source=twitter&location=Carolina%2C+Carolina%2C+Puerto+Rico&lat=18.3807819&lng=-65.95738719999997 in a browser where the page has not been accessed previously in the current session (no session cookie on partners.uber.com), the GET-parameter ```location``` is reflected in the page without validation/sanitation.

POC (tested with Firefox 34.0):
https://partners.uber.com/signup/global/?place_id=ChIJPaCKh-tmA4wR7JEkNDrNDSU&location=Carolina<script>alert(1)</script>a%2C+Carolina"%2C+Puerto+Rico&lat=18.3807819&lng=-65.95738719999997

The best,
Simon


</details>

---
*Analysed by Claude on 2026-05-24*
