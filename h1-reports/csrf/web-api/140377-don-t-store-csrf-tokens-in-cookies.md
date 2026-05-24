# don't store CSRF tokens in cookies

## Metadata
- **Source:** HackerOne
- **Report:** 140377 | https://hackerone.com/reports/140377
- **Submitted:** 2016-05-22
- **Reporter:** 0x0ameer
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** web-api

## Summary
Your web application generates CSRF token values inside cookies
which is not a best practice for web applications as revelation of cookies can reveal CSRF Tokens as well.
Authenticity tokens should be kept separate from cookies and should be isolated to change operations in the account only.

More description:
This report tells that the CSRF tokens are present inside of the cookies value which is 

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

Your web application generates CSRF token values inside cookies
which is not a best practice for web applications as revelation of cookies can reveal CSRF Tokens as well.
Authenticity tokens should be kept separate from cookies and should be isolated to change operations in the account only.

More description:
This report tells that the CSRF tokens are present inside of the cookies value which is not a best practice and if the cookie is intercepted and compromised than the CSRF token will also be vulnerable.

This is the Captured request of edit Statement HTTP ,In this request you can see CSRF token is generating in cookies named as csrf_token

POST /~[MY USER ID]/statement.json HTTP/1.1
Host: gratipay.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:46.0) Gecko/20100101 Firefox/46.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-CSRF-Token: y44PyqG67bRQljEA5mLK1bez4hgZ8XSD
X-Requested-With: XMLHttpRequest
Referer: https://gratipay.com/~ameerassadi4/
Content-Length: 24
Cookie: csrf_token=y44PyqG67bRQljEA5mLK1bez4hgZ8XSD; suppress-welcome=; session=aa5c93be733b4aae8370af6a3fae2be3
Connection: close

lang=en&content=sssssssd

i have also added a PoC picture in attachments,

Cheers,
Ameer Assadi
www.Ameeras.me / www.Geekurity.com

</details>

---
*Analysed by Claude on 2026-05-24*
