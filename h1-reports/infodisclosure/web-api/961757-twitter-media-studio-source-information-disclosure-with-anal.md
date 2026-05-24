# Twitter Media Studio Source Information Disclosure With Analyst Role

## Metadata
- **Source:** HackerOne
- **Report:** 961757 | https://hackerone.com/reports/961757
- **Submitted:** 2020-08-18
- **Reporter:** bcc20c71c2f1f135afb8c3b
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
== Steps ==
1. With "A" account go to "https://studio.twitter.com/account_management/your_account_number_here/account_users" and Add account "B" as analyst.
2. Now, With "B" account go to "https://studio.twitter.com/" and switch to "A" account. Then go to "https://studio.twitter.com/producer" and you can't see "Sources" section same page. Because you are Analyst role.
3. With "B" account go to GET

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

== Steps ==
1. With "A" account go to "https://studio.twitter.com/account_management/your_account_number_here/account_users" and Add account "B" as analyst.
2. Now, With "B" account go to "https://studio.twitter.com/" and switch to "A" account. Then go to "https://studio.twitter.com/producer" and you can't see "Sources" section same page. Because you are Analyst role.
3. With "B" account go to GET request "https://studio.twitter.com/1/live/ingest/list.json?account_id=account_id&owner_id=owner_id&user_id=user_id" and you can Information Disclosure.

PoC Video: https://youtu.be/nalRNUeJq3Y

## Impact

With Analyst role you can access all producer sources in Victim's account.
You can see "source name", "source url" and "source key". You can will create new broadcast with this information. (With Analyst Role)

</details>

---
*Analysed by Claude on 2026-05-24*
