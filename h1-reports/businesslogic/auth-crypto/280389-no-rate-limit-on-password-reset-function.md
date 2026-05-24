# No Rate limit on Password Reset Function

## Metadata
- **Source:** HackerOne
- **Report:** 280389 | https://hackerone.com/reports/280389
- **Submitted:** 2017-10-19
- **Reporter:** akaash_pantherdefence
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hello Infogram Security Team
***************************

###Description:-
I have identified that when resetting the password, the request has no rate limit which then can be used to brute force through one request. Which can be annoying to the infogram users.

###Steps to reproduce:-
* Request for password reset link.
* Catch the above request in burp suit send it to the repeater
* Now send conti

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

Hello Infogram Security Team
***************************

###Description:-
I have identified that when resetting the password, the request has no rate limit which then can be used to brute force through one request. Which can be annoying to the infogram users.

###Steps to reproduce:-
* Request for password reset link.
* Catch the above request in burp suit send it to the repeater
* Now send continuous request to the server.

**NOTE:**  *Every time you will receive the same response which is {"status":"ok"}*

>HTTP/1.1 200 OK
Date: Thu, 19 Oct 2017 10:39:31 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 15
Connection: close
Server: nginx
X-DNS-Prefetch-Control: off
Strict-Transport-Security: max-age=10886400
X-Download-Options: noopen
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: no-referrer
X-Frame-Options: SAMEORIGIN
ETag: W/"f-VaSQ4oDUiZblZNAEkkN+sX+q3Sg"
X-Infogram-Server: b302

{"status":"ok"}

* I tried sending 25 request which was success. (It can be more..) 
{F230753}

###Solution:- 
You should limit the rate for password reset links to avoid such kind of issues.

*************************
Best Regards
*Akaash Sharma :)*

</details>

---
*Analysed by Claude on 2026-05-24*
