# CSRF Token Bypass in Account Deletion

## Metadata
- **Source:** HackerOne
- **Report:** 182487 | https://hackerone.com/reports/182487
- **Submitted:** 2016-11-16
- **Reporter:** 7h0r4pp4n
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
The authentication token `authenticity_token` used in the POST request for deleting an account can be bypassed, by replacing the same with a token generated for deleting another account. This way, a self submitting form can be used to delete another user's account as long as he/she's logged in.

**Steps to Reproduce:**
1. Create an account and copy the POST request for deleting it.

```
POST /user

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

The authentication token `authenticity_token` used in the POST request for deleting an account can be bypassed, by replacing the same with a token generated for deleting another account. This way, a self submitting form can be used to delete another user's account as long as he/she's logged in.

**Steps to Reproduce:**
1. Create an account and copy the POST request for deleting it.

```
POST /users HTTP/1.1
Host: gitlab.com
Referer: https://gitlab.com/profile/account
Cookie: _gitlab_session=1staccount_cookie;
Content-Type: application/x-www-form-urlencoded

_method=delete&authenticity_token=auth_1staccount
```
2. Create another account and send the above request after replacing the `_gitlab_session` cookie with that of the new one.  The `authenticity_token` remains the same as that of the first account.
3. Send the request and the new account gets deleted.

I have not explored all possible scenarios like different IP addresses or something. But the above situation, where I used accounts created using emails from a temporary email address generator, was reproduced multiple times.

</details>

---
*Analysed by Claude on 2026-05-24*
