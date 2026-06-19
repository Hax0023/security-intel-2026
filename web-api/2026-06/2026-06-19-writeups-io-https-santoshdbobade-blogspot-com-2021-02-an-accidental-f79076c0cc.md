# An Accidental XSS on uu.nl

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Reflected XSS, Improper Input Validation
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered on a uu.nl subdomain where user-supplied input via the 'uuid' parameter was reflected without proper sanitization within HTML title tags. The attacker was able to break out of the title tag context and inject arbitrary JavaScript code.

## Attack scenario (step by step)
1. Researcher enumerated subdomains of uu.nl to identify potential targets
2. Used waybackurls tool to collect historical URLs from target subdomain
3. Identified a URL pattern with a 'uuid' parameter that reflected user input
4. Crafted payload to break out of the title tag context: test</title><script>alert(document.domain)</script>
5. Injected payload via the vulnerable parameter
6. JavaScript executed in browser context, demonstrating arbitrary code execution capability

## Root cause
The application failed to properly sanitize or encode user-supplied input (uuid parameter) before reflecting it in HTML context within title tags. No Content Security Policy (CSP) or output encoding was implemented to prevent tag breakout.

## Attacker mindset
Systematic reconnaissance approach using subdomain enumeration and historical URL analysis to identify attack surface. Opportunistic exploitation of common parameter names (uuid) combined with basic tag-breaking payloads to achieve code execution.

## Defensive takeaways
- Implement proper output encoding based on context (HTML entity encoding for HTML context)
- Use parameterized templates or auto-escaping template engines
- Deploy Content Security Policy (CSP) headers to mitigate XSS impact
- Validate and sanitize all user input at both client and server side
- Implement input validation whitelists for UUID parameters
- Conduct security code review focusing on reflection points
- Regular penetration testing of subdomains and legacy URLs

## Variant hunting
['Check for similar reflection points in other URL parameters on uu.nl subdomains', 'Test other HTML context breakout scenarios (attribute-based, event handler-based)', 'Investigate historical endpoints via Wayback Machine for similar patterns', 'Search for other UUID-based parameters across the application', 'Test for stored XSS if any data is persisted with uuid parameter', 'Check for DOM-based XSS in JavaScript handling of uuid parameter']

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The writeup lacks specific details about subdomain and timeline. No information provided about bounty amount or disclosure process. The vulnerability appears relatively straightforward but highlights importance of testing historical/legacy URLs. The researcher's methodology of combining enumeration tools with wayback history proved effective for discovery.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
