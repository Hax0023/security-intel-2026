# Information disclosure - emails disclosed in response > staging.seatme.us

## Metadata
- **Source:** HackerOne
- **Report:** 49170 | https://hackerone.com/reports/49170
- **Submitted:** 2015-02-25
- **Reporter:** quistertow
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,
I found a  info disclosure vulnerability. We can enumerate emails via user_id parameter from Manage users.

And I found that :

>ID 1 is ██████
ID 514755 is ████████
ID 514775 is █████
ID 514764 is ███████

I attached photos from burp repeater to be more explicit.

We can easily bruteforce user_id parameter with ids to harvest user's emails.


Regards,
  Florin

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
I found a  info disclosure vulnerability. We can enumerate emails via user_id parameter from Manage users.

And I found that :

>ID 1 is ██████
ID 514755 is ████████
ID 514775 is █████
ID 514764 is ███████

I attached photos from burp repeater to be more explicit.

We can easily bruteforce user_id parameter with ids to harvest user's emails.


Regards,
  Florin

</details>

---
*Analysed by Claude on 2026-05-24*
