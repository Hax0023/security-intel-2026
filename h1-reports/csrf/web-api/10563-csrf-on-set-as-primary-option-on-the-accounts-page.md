# CSRF on "Set as primary" option on the accounts page

## Metadata
- **Source:** HackerOne
- **Report:** 10563 | https://hackerone.com/reports/10563
- **Submitted:** 2014-05-02
- **Reporter:** anshuman_bh
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
On navigating to the Accounts page, a Coinbase user can create multiple accounts.
The user can then make any of these accounts as their primary account.
There are also other options of renaming and deleting these accounts.

Although there is a CSRF token being sent as a POST parameter for the delete operation, there is no such CSRF token for the "set as primary" operation. Infact, this request

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

On navigating to the Accounts page, a Coinbase user can create multiple accounts.
The user can then make any of these accounts as their primary account.
There are also other options of renaming and deleting these accounts.

Although there is a CSRF token being sent as a POST parameter for the delete operation, there is no such CSRF token for the "set as primary" operation. Infact, this request is a GET request. Similar CSRF controls should be implemented for the "Set as primary" operation as well.

Also, the account number/id is not something that is trivial for an attacker to predict. But, since it is sent as a GET request, it gets cached in the browser history, proxies, logs, etc. So, once the attacker gets hold of such an account number of a legitimate coinbase user, he can exploit a CSRF attack by framing a URL which looks as simple as this:

https://coinbase.com/accounts/<account_number>/set_as_primary

The attacker can then trick the legitimate user to switch his primary account without the user's intention.

Please see the screenshot attached which shows that a GET request was sent requesting to switch the primary account. All that is required for it to be successfully processed is the session cookie.

</details>

---
*Analysed by Claude on 2026-05-24*
