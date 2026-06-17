# Accidental XSS on uu.nl via UUID Parameter

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Reflected XSS, Improper Output Encoding
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered in a uu.nl subdomain where user-supplied UUID parameter values were reflected unsanitized within HTML title tags. The attacker was able to break out of the title tag and inject malicious JavaScript to execute arbitrary code in the victim's browser context.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of uu.nl and identifies www.*.uu.nl as in-scope
2. Attacker uses waybackurls tool to discover historical URLs and identifies endpoint with vulnerable UUID parameter
3. Attacker crafts payload: test</title><script>alert(document.domain)</script> to escape the title tag context
4. Attacker injects payload via UUID parameter in URL: https://www.*.uu.nl/XXXXXX/?uuid=test</title><script>alert(document.domain)</script>
5. When victim visits the crafted URL, malicious JavaScript executes in their browser with victim's privileges
6. Attacker demonstrates proof-of-concept by executing alert() showing document.domain

## Root cause
User input from the UUID parameter was directly reflected into the HTML title tag without proper sanitization or encoding, allowing attackers to break out of the tag context and inject arbitrary HTML/JavaScript

## Attacker mindset
Methodical reconnaissance using subdomain enumeration and historical URL discovery; testing for reflection points across different HTML contexts (title tags); bypassing tag boundaries through context-aware payload construction

## Defensive takeaways
- Implement proper output encoding based on context (HTML entities for HTML content, JavaScript encoding for JS context, etc.)
- Use Content Security Policy (CSP) headers to mitigate XSS impact
- Validate and sanitize all user inputs on both client and server side
- Apply input validation whitelist for UUID parameters (format validation only)
- Use security-focused templating engines that auto-escape by default
- Implement automated security testing to identify reflection points
- Conduct regular security assessments of historical endpoints

## Variant hunting
['Test other parameters for reflection in different HTML contexts (attributes, event handlers, script context)', 'Check for similar UUID parameters across other uu.nl subdomains', 'Test for stored XSS if UUID values are persisted in application state', 'Investigate if similar parameter names exist (id, token, ref, etc.)', 'Check for DOM-based XSS in client-side processing of UUID parameter', 'Test for XSS in other location metadata (head, body attributes)']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1566 - Phishing (if used in phishing campaign)

## Notes
This vulnerability demonstrates the importance of systematic reconnaissance (subdomain enumeration + historical URL discovery). The 'accidental' nature suggests the endpoint may have been legacy or undocumented. The write-up lacks details on disclosure timeline, patch status, and actual bounty awarded. The payload uses HTML entity breaking technique which is a common XSS methodology for escaping tag boundaries.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
