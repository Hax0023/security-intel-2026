# CSRF csrftoken in cookies

## Metadata
- **Source:** HackerOne
- **Report:** 174228 | https://hackerone.com/reports/174228
- **Submitted:** 2016-10-05
- **Reporter:** promx
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

Your web application generates CSRF token values inside cookies
which is not a best practice for web applications as revelation of cookies can reveal CSRF Tokens as well.
Authenticity tokens should be kept separate from cookies and should be isolated to change operations in the account only.

More description:
This report tells that the CSRF tokens are present inside of the cookies value whic

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

Your web application generates CSRF token values inside cookies
which is not a best practice for web applications as revelation of cookies can reveal CSRF Tokens as well.
Authenticity tokens should be kept separate from cookies and should be isolated to change operations in the account only.

More description:
This report tells that the CSRF tokens are present inside of the cookies value which is not a best practice and if the cookie is intercepted and compromised than the CSRF token will also be vulnerable.

This is the Captured request of edit Statement HTTP ,In this request you can see CSRF token is generating in cookies named as csrftoken

HTTP/1.1 200 OK
Connection: close
Server: gunicorn
Date: Wed, 05 Oct 2016 23:09:42 GMT
Cache-Control: no-cache
X-Gratipay-Version: 1986
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Content-Type: text/html; charset=UTF-8
Set-Cookie: csrf_token=zxRkWnGq3I5bMcXDRUWuWWXjxdsO1JtZ; expires=Wed, 12 Oct 2016 23:09:42 GMT; Path=/; secure
X-Xss-Protection: 1; mode=block
Via: 1.1 vegur
Content-Length: 400168

Regards,
Promx

</details>

---
*Analysed by Claude on 2026-05-24*
