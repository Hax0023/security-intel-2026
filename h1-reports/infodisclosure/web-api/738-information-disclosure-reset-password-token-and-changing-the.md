# Information disclosure (reset password token) and changing the user's password

## Metadata
- **Source:** HackerOne
- **Report:** 738 | https://hackerone.com/reports/738
- **Submitted:** 2014-01-17
- **Reporter:** dawidczagan
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
The user gets an e-mail with password recovery link, which includes reset password token. The user clicks this link and is expected to enter a new password twice. Before entering the password the user clicks a link to a picture (https://xkcd.com/936/). When this happens, cross-domain referer leakage takes place. 


GET /936/ HTTP/1.1
Host: xkcd.com
User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW

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

The user gets an e-mail with password recovery link, which includes reset password token. The user clicks this link and is expected to enter a new password twice. Before entering the password the user clicks a link to a picture (https://xkcd.com/936/). When this happens, cross-domain referer leakage takes place. 


GET /936/ HTTP/1.1
Host: xkcd.com
User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: pl,en-us;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://hackerone.com/users/password/edit?reset_password_token=HERE_IS_THE_VALUE_OF_RESET_PASSWORD_TOKEN
Connection: keep-alive


It allows the person who has control of xkcd.com to change the user's password (CSRF attack), because this person knows reset password token of the user, uses a new user's password of his choice and authenticity_token is not needed to make it happen. 

</details>

---
*Analysed by Claude on 2026-05-24*
