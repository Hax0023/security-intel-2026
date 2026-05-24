# HTML Form without CSRF protection

## Metadata
- **Source:** HackerOne
- **Report:** 6888 | https://hackerone.com/reports/6888
- **Submitted:** 2014-04-10
- **Reporter:** robin
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Cross-site request forgery, also known as a one-click attack or session riding and abbreviated as CSRF or XSRF, is a type of malicious exploit of a website whereby unauthorized commands are transmitted from a user that the website trusts.


Attack details
Form name: <empty>
Form action: https://www.irccloud.com/
Form method: POST

Form inputs:

email [Text]
password [Password]
org_invi

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

Cross-site request forgery, also known as a one-click attack or session riding and abbreviated as CSRF or XSRF, is a type of malicious exploit of a website whereby unauthorized commands are transmitted from a user that the website trusts.


Attack details
Form name: <empty>
Form action: https://www.irccloud.com/
Form method: POST

Form inputs:

email [Text]
password [Password]
org_invite [Hidden]

Request
GET / HTTP/1.1
Pragma: no-cache
Cache-Control: no-cache
Referer: http://www.irccloud.com/
Host: www.irccloud.com
Connection: Keep-alive
Accept-Encoding: gzip,deflate
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.63 Safari/537.36
Accept: */*

The impact of this vulnerability:-

An attacker may force the users of a web application to execute actions of the attacker's choosing. A successful CSRF exploit can compromise end user data and operation in case of normal user. If the targeted end user is the administrator account, this can compromise the entire web application.

How to fix this vulnerability:-

Check if this form requires CSRF protection and implement CSRF countermeasures if necessary.


</details>

---
*Analysed by Claude on 2026-05-24*
