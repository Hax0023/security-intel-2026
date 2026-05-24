# IDOR in treat subscriptions

## Metadata
- **Source:** HackerOne
- **Report:** 313050 | https://hackerone.com/reports/313050
- **Submitted:** 2018-02-07
- **Reporter:** harsh13
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
The treat subscriptions tab in my profile has an IDOR.

The corresponding api:

POST /php/filter_user_tab_content.php HTTP/1.1
user_id=██████&tab=treat_subscription&order_history_offset=0&order_history_limit=20


You can give any user id and you will be able to see the treat subscriptions of that user.

## Impact

A user can view treat subscriptions of any other user.

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

The treat subscriptions tab in my profile has an IDOR.

The corresponding api:

POST /php/filter_user_tab_content.php HTTP/1.1
user_id=██████&tab=treat_subscription&order_history_offset=0&order_history_limit=20


You can give any user id and you will be able to see the treat subscriptions of that user.

## Impact

A user can view treat subscriptions of any other user.

</details>

---
*Analysed by Claude on 2026-05-24*
