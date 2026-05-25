# Accidental XSS on uu.nl via UUID Parameter

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Reflected Cross-Site Scripting (XSS), Improper Output Encoding, HTML Injection
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered on a uu.nl subdomain where user-supplied UUID parameter was reflected unsanitized within HTML title tags. The attacker crafted a payload to break out of the title tag context and inject arbitrary JavaScript code that executes in the victim's browser.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of uu.nl and identifies www.*.uu.nl subdomain
2. Attacker collects historical URLs using waybackurls tool and identifies parameter-based endpoints
3. Attacker discovers URL endpoint with uuid parameter: https://www.*.uu.nl/XXXXXX/?uuid=vulnerablepoint
4. Attacker tests uuid parameter and observes reflection within HTML title tag markup
5. Attacker crafts payload: test</title><script>alert(document.domain)</script> to break out of title context
6. Attacker sends malicious URL to victim; victim's browser executes injected JavaScript, confirming XSS

## Root cause
The application accepts user-controlled input (uuid parameter) and reflects it directly into the HTML title tag without proper sanitization or encoding, failing to escape special characters like angle brackets and quotes.

## Attacker mindset
Opportunistic bug bounty hunter using passive reconnaissance techniques (subdomain enumeration, historical URL analysis) to identify attack surface, then systematically testing parameters for common injection points with minimal payloads to confirm vulnerability.

## Defensive takeaways
- Implement output encoding/escaping for all user-controlled data reflected in HTML context using context-appropriate encoding functions
- Apply Content Security Policy (CSP) headers to restrict inline script execution and reduce XSS impact
- Use security-focused templating engines that auto-escape output by default
- Conduct input validation to reject or sanitize unexpected characters in parameters
- Implement Web Application Firewall (WAF) rules to detect and block common XSS payload patterns
- Perform regular security testing including automated XSS scanning and manual penetration testing
- Train developers on secure coding practices regarding output encoding and context-aware escaping

## Variant hunting
['Test other parameters on same endpoint for similar XSS reflection', 'Check other uu.nl subdomains for identical vulnerable code patterns', 'Attempt DOM-based XSS by analyzing JavaScript handling of URL parameters', 'Test for stored XSS if uuid values are persisted and displayed to other users', 'Probe for polyglot payloads that work across multiple contexts (HTML, JavaScript, attribute)', 'Examine if other special characters bypass encoding and enable event handler injection']

## MITRE ATT&CK
- T1190
- T1598

## Notes
This is a classic reflected XSS vulnerability demonstrating the importance of context-aware output encoding. The attack required minimal reconnaissance; automated tool usage (waybackurls) accelerated discovery. The vulnerability likely went unnoticed due to limited use of the obscured endpoint. The writeup lacks specific details on bounty amount, disclosure timeline, and exact subdomain name (intentionally redacted). The payload is simple but effective, exploiting title tag context breaking.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
