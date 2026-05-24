# Existing sessions valid after removing third party auth

## Metadata
- **Source:** HackerOne
- **Report:** 223475 | https://hackerone.com/reports/223475
- **Submitted:** 2017-04-24
- **Reporter:** brdoors3
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi team,

I noticed an authentication break when logging in with 3rd party credentials in https://hosted.weblate.org/

POC

1 access https://hosted.weblate.org/accounts/profile/#auth> link to a Google account (for example)
2 on other device access the same account using Google credentials
3 return to the device of step 1> remove the Google account at https://hosted.weblate.org/accounts/profile/#au

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

Hi team,

I noticed an authentication break when logging in with 3rd party credentials in https://hosted.weblate.org/

POC

1 access https://hosted.weblate.org/accounts/profile/#auth> link to a Google account (for example)
2 on other device access the same account using Google credentials
3 return to the device of step 1> remove the Google account at https://hosted.weblate.org/accounts/profile/#auth> disconnect

The session remains active on the device in step 2. So I continue with a valid session from credentials not linked to any account at https://hosted.weblate.org

Please check it.

</details>

---
*Analysed by Claude on 2026-05-24*
