# SSL-protected Reflected XSS in https://m.uber.com/0-dfffb25d2cf6ceeb0a27.js Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 300080 | https://hackerone.com/reports/300080
- **Submitted:** 2017-12-22
- **Reporter:** gregoryvperry
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary
The _cc request parameter at the https://m.uber.com/0-dfffb25d2cf6ceeb0a27.js mobile endpoint is copied into a javascript string encapsulated in double quotation marks, resulting in SSL-protected payloads being reflected unmodified in the application's response. The script-src whitelist at the endpoint includes a wildcard *.cloudfront.net host, which could be used by any attacker with a

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

## Summary
The _cc request parameter at the https://m.uber.com/0-dfffb25d2cf6ceeb0a27.js mobile endpoint is copied into a javascript string encapsulated in double quotation marks, resulting in SSL-protected payloads being reflected unmodified in the application's response. The script-src whitelist at the endpoint includes a wildcard *.cloudfront.net host, which could be used by any attacker with an Amazon Web Services account to provision an arbitrary cloudfront.net host to serve trusted files from. The endpoint also has a missing base-uri, which allows the injection of base tags. They can be used to set the base URL for all relative (script) URLs to an attacker controlled domain. In addition to the reflected XSS issue, both the script-src and basi-uri issues are considered high severity findings under Content Security Policy 3.

## Security Impact
Arbitrary SSL-protected XSS can be reflected unescaped from the https://m.uber.com/0-dfffb25d2cf6ceeb0a27.js mobile endpoint, resulting in the ability for an attacker to generate arbitrary javascript and/or html content.

## Reproduction Steps
https://m.uber.com/0-dfffb25d2cf6ceeb0a27.js?_cc=asdf"}}</script><script>alert(1)</script>

## Specifics
The resulting unescaped content rendered:
```
{"enabled":true,"sid":"bbc661585c424072","url":"www.cdn-net.com","cf":1022963},"queryParams":{"_cc":"asdf\"}}</script><script>alert(1)</script>"},"useragent":{"ua":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36","browser":
```

## Impact

With a properly crafted javascript and/or html page, an attacker could harvest Uber login and password credentials, credit card payment information etc.

</details>

---
*Analysed by Claude on 2026-05-24*
