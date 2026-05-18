# XSS Attacks and Defense: A Multi-Level Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Educational/Security Research
- **Bounty:** N/A - Educational Content
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS) - Reflected, Cross-Site Scripting (XSS) - Stored, Cross-Site Scripting (XSS) - DOM-based, HTML Injection, Attribute-based XSS, JavaScript Protocol Injection
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
This comprehensive security analysis explores XSS vulnerabilities across three defense levels: preventing code injection through input validation and escaping, preventing code execution via CSP policies, and minimizing damage when XSS is successfully exploited. The writeup demonstrates that context-aware escaping is essential, as different output contexts (HTML body, attributes, JavaScript, URLs) require different sanitization approaches.

## Attack scenario (step by step)
1. Attacker injects malicious payload into user-controllable input field (e.g., nickname, profile data)
2. Application renders user input without proper escaping or validation in HTML context
3. Attacker uses context-specific payloads: simple tags in body content, attribute manipulation with quotes in tag attributes, or javascript: protocol in href attributes
4. When victim views the compromised page, JavaScript executes in victim's browser with full access to session cookies and user context
5. Attacker escalates attack by bypassing CSP through inline event handlers or policy weaknesses if defenses are present
6. If full XSS execution achieved, attacker performs privilege escalation, session hijacking, credential theft, or platform-specific attacks (e.g., account takeover on Medium)

## Root cause
Insufficient output encoding context-awareness: developers apply generic escaping (only <> characters) without considering that different HTML contexts require different encoding schemes. Input validation alone is insufficient without proper output escaping at render time. Lack of defense-in-depth allows single encoding bypass to lead to full compromise.

## Attacker mindset
Attackers recognize that generic defenses are bypassable through context manipulation. Rather than attacking the surface level (HTML body injection), they probe for alternative injection points (attributes, URL protocols, event handlers) where standard escaping may be incomplete or misapplied. They view XSS as a privilege escalation vector to higher-impact attacks (account takeover, financial fraud) on platforms with sensitive functionality.

## Defensive takeaways
- Implement context-aware output encoding: HTML entity encoding for body content, attribute encoding for HTML attributes, URL encoding for href/src, JavaScript string escaping for JS contexts
- Never rely on input validation alone; always encode output based on context where data will be rendered
- Deploy Content Security Policy with strict directives: disable inline scripts, restrict script sources, use nonce-based or hash-based inline script allowlisting
- Apply defense-in-depth: combine input validation, output encoding, CSP, and application-level access controls to minimize blast radius if XSS succeeds
- Sanitize URLs and prevent javascript: protocol execution by validating against allowlist (http, https, mailto) rather than blacklisting
- Use security-focused templating engines that apply context-aware escaping by default (e.g., Angular, Vue with auto-escaping)
- For sensitive operations (account changes, financial transfers), implement additional protections: CSRF tokens, transaction signing, re-authentication, rate limiting
- Regular security testing: automated SAST scanning, manual penetration testing, and XSS-specific fuzzing across different output contexts

## Variant hunting
['Search for template rendering calls without explicit escaping flags in codebase (e.g., dangerouslySetInnerHTML in React, triple-curly in Handlebars)', 'Hunt for URL attribute bindings (href, src, action) that lack protocol validation', 'Identify event handler attributes (onclick, onerror, onload) rendered from user input', 'Test edge cases: newline injection in attributes, null byte injection, Unicode/UTF-8 encoding bypasses', 'Analyze CSP policies for overly permissive directives (script-src allowing unsafe-inline, unsafe-eval)', 'Review JavaScript code execution contexts (eval, setTimeout, Function constructor) with user input', 'Test for DOM-based XSS where client-side JavaScript manipulates innerHTML without sanitization', 'Probe for secondary encoding: escaped data passed through unescape() or atob() creating re-execution opportunities']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1592 - Gather Victim Host Information
- T1598 - Phishing
- T1566 - Phishing
- T1539 - Steal Web Session Cookie
- T1040 - Network Sniffing
- T1021 - Remote Services
- T1550 - Use Alternate Authentication Material

## Notes
This writeup emphasizes the layered security model: Level 1 (input/output controls), Level 2 (CSP and execution prevention), Level 3 (blast radius minimization). The critical insight is that XSS is not monolithic - different injection points require context-specific defenses. The Medium platform example illustrates business-critical impact assessment: XSS enabling account takeover or financial fraud represents severe risk justifying investment in all three defense levels. Modern frameworks with auto-escaping provide Level 1 defense by default, but developers must understand context-aware encoding to avoid bypasses. CSP provides Level 2 but can be bypassed; Level 3 requires segregation of privileges and additional controls on sensitive operations.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
