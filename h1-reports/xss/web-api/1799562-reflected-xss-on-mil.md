# Reflected XSS on ██████.mil

## Metadata
- **Source:** HackerOne
- **Report:** 1799562 | https://hackerone.com/reports/1799562
- **Submitted:** 2022-12-11
- **Reporter:** alishah
- **Program:** ██████.mil
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered on a .mil domain where user input in the search parameter is not properly sanitized before being rendered in the HTML response. An attacker can inject malicious JavaScript to steal sensitive data such as cookies and authentication tokens, potentially combined with CORS misconfigurations.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the search parameter: https://███████████████████<script>alert(document.cookie)</script>
2. Attacker sends the crafted URL to a victim (via email, social engineering, etc.)
3. Victim clicks the link and visits the vulnerable page
4. The payload executes in the victim's browser within the context of the vulnerable domain
5. Malicious script steals cookies/session tokens or exfiltrates sensitive data
6. If the site has CORS misconfiguration, attacker can access data from other domains the victim is authenticated to

## Root cause
User-supplied input from the search parameter is reflected directly into the HTML response without proper output encoding or input validation/sanitization

## Attacker mindset
Opportunistic reconnaissance on .mil domains looking for low-hanging fruit; potential interest in stealing government/military authentication tokens and session data; interest in bypassing authentication through victim compromise

## Defensive takeaways
- Implement strict input validation on all user-supplied parameters
- Apply proper output encoding based on context (HTML entity encoding for HTML context)
- Use templating engines with auto-escaping enabled by default
- Implement Content Security Policy (CSP) headers to restrict script execution
- Apply same-site cookie flags (SameSite=Strict/Lax) to prevent token theft
- Regular security testing including SAST and DAST for XSS vulnerabilities
- Sanitize search/query parameters before reflection in responses
- Implement proper CORS headers to prevent unauthorized cross-origin access

## Variant hunting
Test other search/query parameters on the same domain for similar reflection issues
Check for DOM-based XSS variants where JavaScript processes these parameters client-side
Look for stored XSS if search functionality stores/displays historical queries
Test error messages and redirects for XSS vulnerabilities
Examine other .mil domains for similar search parameter handling patterns
Check for second-order XSS where reflected data gets stored and later displayed

## MITRE ATT&CK
- T1190
- T1566
- T1195
- T1583

## Notes
This is a classic reflected XSS on a government domain. The simplicity of the payload and ease of exploitation suggest inadequate security testing in the development process. The mention of CORS as a secondary impact indicates the attacker was thinking about chaining vulnerabilities. Severity is amplified by the .mil designation and potential access to authenticated government systems.

## Full report
<details><summary>Expand</summary>

**Description:**
While looking for *.mil, I found a website that is vulnerable to reflected XSS.

## Impact

An attacker can use it to fetch cookies/tokens from any website which requires login by using a CORS bug if the site is vulnerable to CORS.

## System Host(s)
████.mil

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Go to this URL: https://███████████████████html
2. On the search bar, write this payload. <script>alert(document.cookie)</script>
3. & you'll see the pop-up.

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-12*
