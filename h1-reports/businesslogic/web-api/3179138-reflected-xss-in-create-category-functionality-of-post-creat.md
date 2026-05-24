# Reflected XSS in "Create Category" Functionality of Post Creation Module

## Metadata
- **Source:** HackerOne
- **Report:** 3179138 | https://hackerone.com/reports/3179138
- **Submitted:** 2025-06-05
- **Reporter:** rishail01
- **Program:** Unknown
- **Bounty:** $50
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected Cross-Site Scripting (XSS) vulnerability was identified in the “Create Category” feature of the post creation functionality.

When a user enters a malicious JavaScript payload in the Category Name field, the input is reflected and executed immediately after submission. However, this XSS only executes in the attacker’s own session, and does not persist or affect other users.

## Impact


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

A reflected Cross-Site Scripting (XSS) vulnerability was identified in the “Create Category” feature of the post creation functionality.

When a user enters a malicious JavaScript payload in the Category Name field, the input is reflected and executed immediately after submission. However, this XSS only executes in the attacker’s own session, and does not persist or affect other users.

## Impact

The presence of such a vulnerability indicates that user input is not properly sanitized or encoded before being reflected back into the HTML response.

While not directly exploitable by other users, this flaw can have the following implications:

- It highlights a potential entry point for more severe XSS vulnerabilities if similar input handling exists elsewhere in the application.

- It poses a client-side security risk, especially in environments with browser extensions, debugging tools, or when integrating third-party scripts.

- It reduces trust in the platform’s secure coding practices, especially in an admin interface that manages multiple WordPress sites.

- It can be used by attackers with access to the dashboard (e.g., insider threat or compromised low-privilege user) to test or explore further payload injection points.

Addressing such vulnerabilities improves the overall resilience of the application and helps prevent future, more impactful exploits.

</details>

---
*Analysed by Claude on 2026-05-24*
