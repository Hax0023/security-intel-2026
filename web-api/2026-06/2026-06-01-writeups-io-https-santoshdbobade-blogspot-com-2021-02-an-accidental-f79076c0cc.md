# An Accidental XSS on uu.nl

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Reflected XSS
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered on a Utrecht University subdomain where user-supplied input via the 'uuid' parameter was reflected unsanitized within the HTML title tag. The attacker bypassed the title tag context by closing it with a malicious script tag, achieving arbitrary JavaScript execution.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of uu.nl to identify attack surface
2. Attacker collects historical URLs using waybackmachine archive data via waybackurls tool
3. Attacker identifies a parameter-based endpoint with UUID query string parameter
4. Attacker tests the uuid parameter and identifies that input is reflected in the HTML title tag without sanitization
5. Attacker crafts payload: test</title><script>alert(document.domain)</script> to break out of title context
6. Attacker confirms XSS execution by observing script execution in browser, proving arbitrary JavaScript can run in victim context

## Root cause
User-supplied input from the 'uuid' parameter was directly reflected in the HTML title tag without proper encoding or sanitization, allowing an attacker to inject arbitrary HTML and JavaScript code by closing the title tag and injecting script elements.

## Attacker mindset
Opportunistic reconnaissance approach: systematic subdomain enumeration combined with historical URL analysis to identify low-hanging fruit. Recognition that context-matters in XSS (title tag context) and simple tag-breaking technique to achieve exploitation.

## Defensive takeaways
- Implement output encoding appropriate to the context (HTML entity encoding for title tags at minimum)
- Use security libraries that automatically handle context-aware encoding (e.g., templating engines with auto-escaping)
- Apply Content Security Policy (CSP) headers to restrict script execution even if XSS is introduced
- Validate and sanitize all user inputs on both client and server side
- Use security scanner/SAST tools to identify reflected parameters in sensitive contexts
- Implement input validation whitelist for UUID parameters to reject unexpected characters
- Regular security testing and code reviews focusing on data flow from user input to output

## Variant hunting
['Check other URL parameters on same endpoint for similar reflection vulnerabilities', 'Test other subdomains (*.uu.nl) for same parameter vulnerability', 'Look for stored XSS variants where uuid might be persisted in database', 'Check if other HTML context locations (meta tags, form attributes) have similar issues', 'Test for DOM-based XSS if JavaScript processes the uuid parameter client-side', 'Check for bypasses of any existing WAF/filtering by using encoding variations']

## MITRE ATT&CK
- T1190
- T1566

## Notes
The writeup lacks details about the specific subdomain and complete URL structure for responsible disclosure purposes. No mention of response time, bounty amount, or official acknowledgment from uu.nl. The vulnerability demonstrates a common scenario where output encoding is overlooked in non-standard contexts like title tags. The use of enumeration tools and historical archive data shows a methodical reconnaissance approach valuable for bug bounty hunting.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
