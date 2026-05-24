# Cross-Site Scripting (XSS) in ASP.NET via ResolveUrl on ███████

## Metadata
- **Source:** HackerOne
- **Report:** 3166582 | https://hackerone.com/reports/3166582
- **Submitted:** 2025-05-29
- **Reporter:** jonasdiasrebelo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
**Description:**
Hi, team! A Cross-Site Scripting (XSS) vulnerability was identified in an ASP.NET web application on the ██████ . The issue arises from improper handling of URLs passed to the ResolveUrl method, which fails to sanitize user-controlled input. This allows injection of arbitrary JavaScript payloads that execute in the context of the user’s browser.
Some ASP.NET web applications that 

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
Hi, team! A Cross-Site Scripting (XSS) vulnerability was identified in an ASP.NET web application on the ██████ . The issue arises from improper handling of URLs passed to the ResolveUrl method, which fails to sanitize user-controlled input. This allows injection of arbitrary JavaScript payloads that execute in the context of the user’s browser.
Some ASP.NET web applications that use the Control.ResolveUrl method to resolve app-root-relative paths are vulnerable to XSS.

```
Payload used: (Z('ontestingb3t2h onload=print`` fnwve='zzzzz`8504695818`'))
- This payload successfully triggered JavaScript execution using the onload attribute.
- The use of print`` instead of alert()` was necessary to bypass Web Application Firewall (WAF) protections and filter-based sanitization.
```

PoC: ███(Z('ontestingb3t2h%20onload=print%60%60%20fnwve='zzzzz%608504695818%60'))/pageNotFound.aspx

## References

█████████

## Impact

Exploitation of this vulnerability can lead to severe consequences, including but not limited:
Session Hijacking: Attackers can steal cookies and impersonate legitimate users.

## System Host(s)
██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Open the link.

## Suggested Mitigation/Remediation Actions
Apply context-dependent encoding and/or validation to user input rendered on a page.



</details>

---
*Analysed by Claude on 2026-05-24*
