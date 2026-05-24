# Clickjacking via Missing X-FRAME-OPTIONS Header

## Metadata
- **Source:** HackerOne
- **Report:** 7862 | https://hackerone.com/reports/7862
- **Submitted:** 2014-04-17
- **Reporter:** mickyd
- **Program:** Unknown (HackerOne Report #7862)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
The target application is vulnerable to clickjacking attacks due to missing X-FRAME-OPTIONS HTTP headers on multiple pages. An attacker can embed the website in an iframe and overlay transparent UI elements to trick users into unintended actions such as adding arbitrary tasks. This allows attackers to perform unauthorized actions on behalf of authenticated users.

## Attack scenario
1. Attacker creates a malicious website and embeds the target application in a hidden iframe
2. Attacker overlays transparent or disguised UI elements (buttons, links) over the target website's interactive controls
3. Attacker tricks a legitimate user into visiting the malicious site while logged into the target application
4. User interacts with what appears to be content on the attacker's page but actually clicks buttons on the hidden framed application
5. Unintended actions execute on the target application (e.g., task creation, profile modification, permission changes)
6. Attacker gains the ability to perform actions on behalf of the authenticated user without consent

## Root cause
The application fails to implement X-FRAME-OPTIONS HTTP response header across its pages, allowing the site to be embedded in iframes on attacker-controlled domains. The lack of this security header provides no directive to browsers to restrict framing, making clickjacking exploitation trivial.

## Attacker mindset
An opportunistic attacker identifies this common misconfiguration to amplify the impact of social engineering campaigns. By automating task creation or other actions through clickjacking, they can scale attacks and bypass CSRF tokens that may only protect form submissions, not state-changing GET requests.

## Defensive takeaways
- Implement X-FRAME-OPTIONS header set to 'DENY' or 'SAMEORIGIN' on all HTTP responses
- Use Content-Security-Policy (CSP) with frame-ancestors directive as a modern alternative to X-FRAME-OPTIONS
- Apply frame-busting JavaScript as a defense-in-depth measure for legacy browser support
- Implement additional CSRF protections beyond token validation (SameSite cookies, origin checks)
- Regularly audit all application endpoints to ensure security headers are consistently applied
- Use security scanning tools to identify pages missing protective headers across the entire application

## Variant hunting
Search for other missing security headers (Strict-Transport-Security, Content-Security-Policy, X-Content-Type-Options) on the same or similar applications. Check for pages that allow form submissions via GET requests which may be more vulnerable. Identify any authenticated endpoints that perform state changes without additional validation.

## MITRE ATT&CK
- T1190
- T1204.1

## Notes
This report lacks technical depth (no actual PoC provided, despite mentioning one). The vulnerability is straightforward but impactful when combined with social engineering. Applies to large portions of the application rather than isolated endpoints, suggesting systemic configuration issues. Consider the business logic impact: what specific actions could be automated through clickjacking (fund transfers, data deletion, permission escalation).

## Full report
<details><summary>Expand</summary>



It allows remote attackers to do some clickjacking which can be used for adding arbitrary tasks . Why? Almost all of your page has missing X-FRAME-OPTIONS header.

Websites are at risk of a clickjacking attack when they allow content to be embedded within a frame.

An attacker may use this risk to invisibly load the target website into their own site and trick users into clicking on links which they never intended to. An "X-Frame-Options" header should be sent by the server to either deny framing of content, only allow it from the same origin or allow it from a trusted URIs.

Attacked PoC .

Daksh


</details>

---
*Analysed by Claude on 2026-05-24*
