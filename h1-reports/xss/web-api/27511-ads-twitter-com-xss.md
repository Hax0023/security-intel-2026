# ads.twitter.com xss

## Metadata
- **Source:** HackerOne
- **Report:** 27511 | https://hackerone.com/reports/27511
- **Submitted:** 2014-09-09
- **Reporter:** arbitrarycode
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Cross-Site Scripting vulnerability exists in card[name] parameter when creating/cloning a card via script https://ads.twitter.com/accounts/18ce53wrkma/cards/new?card_type=7. 
Here is the simple test vector: </title><script>alert(document.cookie)</script><title>
After the card is created XSS becomes persistent and can be triggered via https://ads.twitter.com/accounts/18ce53wrkma/cards/show?url_id

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

Cross-Site Scripting vulnerability exists in card[name] parameter when creating/cloning a card via script https://ads.twitter.com/accounts/18ce53wrkma/cards/new?card_type=7. 
Here is the simple test vector: </title><script>alert(document.cookie)</script><title>
After the card is created XSS becomes persistent and can be triggered via https://ads.twitter.com/accounts/18ce53wrkma/cards/show?url_id=42qj.

</details>

---
*Analysed by Claude on 2026-05-24*
