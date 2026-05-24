# CSRF Account Deletion on ███ Website

## Metadata
- **Source:** HackerOne
- **Report:** 840285 | https://hackerone.com/reports/840285
- **Submitted:** 2020-04-05
- **Reporter:** notdeghost
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**

A CSRF vulnerability against the [███████](████) allows attackers to delete user accounts. 

## Impact

Users who visit a malicious website could find their ████████ account deleted. 

## Step-by-step Reproduction Instructions

1. Create and login to a new account on the [██████](███████)
2. Open the provided HTML file and press the "POC" button. Note that the POC button is used only

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

A CSRF vulnerability against the [███████](████) allows attackers to delete user accounts. 

## Impact

Users who visit a malicious website could find their ████████ account deleted. 

## Step-by-step Reproduction Instructions

1. Create and login to a new account on the [██████](███████)
2. Open the provided HTML file and press the "POC" button. Note that the POC button is used only to make testing easier, and is not necessary in an actual attack scenario. 
3. Refresh the page on the ███ website. You should find that you have been logged out, and are unable to sign back into your account. 

██████

## Product, Version, and Configuration (If applicable)

**Website**: [███████](██████████)

## Suggested Mitigation/Remediation Actions

Enforce proper CSRF control on the ██████, for example with Google captcha (which is already implemented through much of the site).

## Impact

Users who visit a malicious website could find their account deleted.

</details>

---
*Analysed by Claude on 2026-05-24*
