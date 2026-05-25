# XSS Attacks and Defense: A Multi-Level Security Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Educational/General Security
- **Bounty:** N/A - Educational Article
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), HTML Injection, Attribute-based XSS, JavaScript Protocol Injection, Improper Input Validation, Insufficient Output Encoding
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
This article provides a comprehensive framework for understanding XSS vulnerabilities across three defensive levels: preventing code injection, blocking execution via CSP, and minimizing damage from successful attacks. The writeup demonstrates that simple escaping of angle brackets is insufficient and context-specific encoding is critical, using practical examples of attribute-based XSS and JavaScript protocol injection.

## Attack scenario (step by step)
1. Attacker identifies user-controllable input field (e.g., nickname, avatar URL, link)
2. Attacker analyzes output context to determine appropriate encoding bypass (e.g., HTML attributes vs text nodes)
3. Attacker crafts payload exploiting context-specific weaknesses (e.g., quote-breaking in attributes or javascript: protocol in href)
4. Attacker submits malicious payload through input validation (which only checks for basic characters like <>)
5. When other users view the page, the improperly encoded output allows payload execution
6. Attacker achieves code execution in victim's browser with access to session tokens, cookies, and user data

## Root cause
Developers implement overly simplistic input validation and output encoding strategies that fail to account for context-dependent escaping requirements. Escaping only angle brackets (<>) is insufficient when user input appears in HTML attributes, JavaScript strings, or URLs. Lack of framework-enforced encoding and context-aware sanitization allows attackers to bypass basic defenses.

## Attacker mindset
Methodical reconnaissance of application architecture to identify all output contexts where user input appears. Recognition that different contexts (text content, HTML attributes, JavaScript, URLs) require different encoding schemes. Exploitation of developer assumptions that single escape function (like htmlspecialchars) provides complete protection.

## Defensive takeaways
- Implement context-aware output encoding - use different encoding for HTML text, HTML attributes, JavaScript, URLs, and CSS contexts
- Never rely on single escaping function; understand that htmlspecialchars or similar functions may be insufficient for attribute contexts
- Apply defense-in-depth: Layer 1 (input validation/encoding), Layer 2 (Content Security Policy), Layer 3 (privilege separation and account protection mechanisms)
- Use modern templating engines and frameworks with automatic context-aware escaping built-in
- Be cautious with dangerous protocols (javascript:, data:, vbscript:) in URL contexts - whitelist safe protocols
- Escape special characters appropriate to context: for HTML attributes escape quotes, for URLs validate protocol, for JavaScript strings escape quotes and backslashes
- Conduct security code review specifically examining all user input output points and their encoding
- Implement CSP headers to provide defense layer against code execution even if injection succeeds
- For high-value actions, implement additional protections beyond XSS (CSRF tokens, re-authentication, API-level protections)

## Variant hunting
['Search for incomplete HTML entity encoding in template systems - particularly in attribute contexts', "Identify custom escaping functions that don't handle all dangerous characters for their context", 'Test URL parameters passed to href, src, or other resource attributes for protocol validation bypass', 'Hunt for JavaScript string interpolation without proper escaping (template literals, concatenation)', 'Look for CSS property injection in style attributes or style tags with inadequate encoding', 'Test for polyglot payloads that work across multiple contexts simultaneously', 'Examine data URIs and base64 encoded payloads that might bypass protocol filters', 'Check for DOM-based XSS where client-side JavaScript fails to properly sanitize before DOM insertion']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information (delivery mechanism)
- T1566 - Phishing (if used for credential theft)
- T1539 - Steal Web Session Cookie
- T1563 - Steal Web Session Cookie (browser-based)

## Notes
This is a security education article rather than a specific vulnerability disclosure. It effectively illustrates why XSS remains prevalent despite awareness - developers often implement incomplete defenses. The article emphasizes defense-in-depth strategy with multiple layers, recognizing that Layer 1 defenses alone are insufficient. Key insight: context matters enormously in web security; the same character may be dangerous or safe depending on parsing context. The framework of three defensive levels (prevention, execution blocking, damage control) provides valuable mental model for comprehensive security design.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
