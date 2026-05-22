# XSS Attacks and Defense: A Multi-Level Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Educational/General Web Security
- **Bounty:** N/A - Educational writeup
- **Severity:** High
- **Vuln types:** Stored XSS, Reflected XSS, DOM-based XSS, HTML Injection, Attribute Injection, JavaScript Protocol Injection
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
Comprehensive analysis of XSS vulnerabilities across three defense levels: preventing code injection, bypassing CSP, and minimizing damage post-exploitation. Demonstrates context-specific escaping requirements and the importance of layered security defenses against XSS attacks.

## Attack scenario (step by step)
1. Attacker identifies user input field (e.g., nickname) that is rendered without proper escaping
2. Attacker injects malicious payload such as <script>alert(1)</script> or HTML attribute manipulation
3. If basic escaping exists, attacker bypasses it by leveraging context-specific weaknesses (e.g., attribute escaping vs tag escaping)
4. Injected code executes in victim's browser when page is rendered or accessed
5. If CSP is implemented, attacker may use alternative payloads or vectors to bypass policies
6. If execution succeeds, attacker performs account takeover, session hijacking, or sensitive actions (e.g., fund transfers)

## Root cause
Insufficient input validation and output escaping, failure to apply context-aware encoding, and lack of multi-layered security controls. Developers often implement generic escaping without considering different rendering contexts (HTML, attributes, JavaScript, URLs).

## Attacker mindset
Systematic exploitation through context identification; if basic XSS vectors fail, attacker probes for alternative injection points (attributes, protocols, event handlers). Assumes defenders may implement incomplete mitigations and looks for gaps in escaping logic or CSP configuration.

## Defensive takeaways
- Implement context-aware output encoding (HTML escaping, attribute escaping, JavaScript escaping, URL escaping)
- Apply layered defenses: input validation, output escaping, CSP policies
- Never trust user input; validate and sanitize at all trust boundaries
- Use frameworks and libraries that provide automatic escaping mechanisms
- Implement Content Security Policy to prevent inline script execution
- Consider additional protections like HTTPOnly cookies, SameSite attributes
- Regularly audit rendering contexts where user data appears
- Implement privilege separation to minimize damage if XSS is achieved
- Use security headers (X-XSS-Protection, X-Content-Type-Options)

## Variant hunting
['Test escaping in different HTML contexts: tag content, attributes, JavaScript strings, CSS, URL parameters', 'Identify unescaped data in href, src, data attributes using JavaScript protocols', 'Search for data flowing through template engines without proper context awareness', 'Check for bypasses using HTML entity encoding, Unicode escapes, case variations', 'Look for CDATA sections, SVG contexts, and other XML-based injection points', 'Test mutation-based XSS (mXSS) where browser DOM normalization enables code execution', "Probe for weaknesses in CSP implementation (script-src 'unsafe-inline', unsafe-eval)"]

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204
- T1105

## Notes
This is a foundational security educational article rather than a specific vulnerability report. It establishes the three-level XSS defense framework: (1) prevent injection, (2) prevent execution via CSP, (3) minimize damage post-compromise. The writeup emphasizes that generic escaping is insufficient and context-specific encoding is mandatory. Particularly valuable for understanding why SQL injection and XSS vulnerabilities remain prevalent despite being well-known.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
