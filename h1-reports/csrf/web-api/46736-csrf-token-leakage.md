# CSRF token leakage

## Metadata
- **Source:** HackerOne
- **Report:** 46736 | https://hackerone.com/reports/46736
- **Submitted:** 2015-02-05
- **Reporter:** yassineaboukir
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,
I have noticed that when the account verification fails here : https://wallet.robocoin.com/verify/ due to an error, the CSRF token is being leaked via GET method like : https://wallet.robocoin.com/verify/id?_csrf=b8ede20d-0c0b-4e16-9d05-6ad2ed8b72c4
So the authenticity token is being stored in the web browser history and can be retrieved by a malicious attacker in order to mount a successful

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

Hi,
I have noticed that when the account verification fails here : https://wallet.robocoin.com/verify/ due to an error, the CSRF token is being leaked via GET method like : https://wallet.robocoin.com/verify/id?_csrf=b8ede20d-0c0b-4e16-9d05-6ad2ed8b72c4
So the authenticity token is being stored in the web browser history and can be retrieved by a malicious attacker in order to mount a successful CSRF attack against the victim. Besides, that the token can be reused multiple times and do not get expired on first use.
Best regards.

</details>

---
*Analysed by Claude on 2026-05-24*
