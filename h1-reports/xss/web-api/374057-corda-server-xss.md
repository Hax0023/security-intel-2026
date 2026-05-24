# Corda Server XSS ████████

## Metadata
- **Source:** HackerOne
- **Report:** 374057 | https://hackerone.com/reports/374057
- **Submitted:** 2018-06-29
- **Reporter:** alyssa_herrera
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
Cord server will display the error message if something isn't allowed to be used thus allowing xss
**Description:**
/scripts/ctredirector.dll allows users to call images or files. We can use the parameter @_FILE to dictate a file or url, if it fails it'll display the url into the page. We then leverage an additional parameter named @_TEXTDESCRIPTIONEN to make the page display as a tex

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

**Summary:**
Cord server will display the error message if something isn't allowed to be used thus allowing xss
**Description:**
/scripts/ctredirector.dll allows users to call images or files. We can use the parameter @_FILE to dictate a file or url, if it fails it'll display the url into the page. We then leverage an additional parameter named @_TEXTDESCRIPTIONEN to make the page display as a text which then allows the opportunity to trigger XSS.
## Impact
Medium
## Step-by-step Reproduction Instructions
Check the following URL in firefox
http://█████████/scripts/ctredirector.dll//?@_FILEhttp://google.com/%3Csvg/onload=confirm(document.cookie)%3E%3E@_TEXTDESCRIPTIONEN

## Product, Version, and Configuration (If applicable)
Corda Server
## Suggested Mitigation/Remediation Actions
Update corda

## Impact

An attacker can steal session cookies and conduct sophisticated phishing campaigns using this exploit

</details>

---
*Analysed by Claude on 2026-05-24*
