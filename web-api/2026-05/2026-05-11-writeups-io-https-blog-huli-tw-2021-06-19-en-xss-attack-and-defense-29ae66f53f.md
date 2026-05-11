# XSS Attack and Defense: A Multi-Level Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Educational/General
- **Bounty:** N/A
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), HTML Injection, Attribute Injection, JavaScript Code Injection, JavaScript Pseudo-Protocol Injection
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
This article provides a comprehensive framework for understanding XSS vulnerabilities across three defensive levels: preventing code injection, blocking code execution via CSP, and minimizing damage post-compromise. It discusses context-specific escaping requirements, highlighting that different output contexts (HTML body, attributes, JavaScript, URLs) require different encoding strategies to effectively prevent XSS attacks.

## Attack scenario (step by step)
1. Attacker identifies input fields (nicknames, user profiles) that are rendered without proper sanitization
2. Attacker injects payload like <script>alert(1)</script> or JavaScript pseudo-protocol javascript:alert(1)
3. Payload is stored and rendered on victim's browser during page load or interaction
4. Browser parses injected code as executable JavaScript rather than text content
5. Attacker escalates to session hijacking, account takeover, or financial fraud (e.g., Medium paywall bypass)
6. If CSP is implemented, attacker crafts payload that bypasses specific CSP rules or finds execution vectors CSP doesn't cover

## Root cause
Insufficient input validation and context-inappropriate output encoding. Developers assume generic escaping (converting <> to entities) is sufficient across all contexts, failing to recognize that HTML attributes, JavaScript strings, and URL protocols require distinct encoding strategies.

## Attacker mindset
Exploit the gap between developer understanding and execution. Target the assumption that basic escaping is universally sufficient. Test multiple injection points and contexts. Progress from simple tag injection to attribute manipulation and protocol-based attacks. If first-level defenses exist, attempt to bypass CSP or pivot to account/financial exploitation.

## Defensive takeaways
- Implement context-aware output encoding: HTML body escaping differs from attribute escaping, JavaScript string escaping, and URL parameter encoding
- Apply defense in depth: Layer 1 (input validation/output encoding) + Layer 2 (CSP with strict policies) + Layer 3 (session protection, rate limiting, account security measures)
- Never trust user input regardless of source; validate and sanitize at both input and output stages
- Use established libraries (htmlspecialchars, OWASP encoders) rather than custom escaping logic
- Be aware of JavaScript pseudo-protocols (javascript:, data:, vbscript:) in URLs and block them
- Regularly audit code for multiple injection contexts; test escaping effectiveness across HTML, attributes, and JavaScript contexts
- Implement CSP headers as a mitigation layer but recognize it is not a substitute for proper encoding

## Variant hunting
['Stored vs Reflected XSS: Test whether injection persists in database (stored) or only in immediate response (reflected)', 'DOM-based XSS: Examine client-side JavaScript that dynamically updates DOM without sanitization', 'SVG/XML contexts: Test injection in SVG elements and XML namespaces which may have different parsing rules', 'Event handler variations: Try onload, onerror, onmouseover, onfocus, onchange, and other event handlers beyond onerror', 'Encoding bypass techniques: Test double-encoding, Unicode encoding, HTML entity variations, and mixed case handlers', 'Framework-specific vulnerabilities: Audit template engines for auto-escaping bypasses', 'API endpoints: Check JSON responses rendered as HTML or JavaScript contexts for XSS']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing: Spearphishing Link (via XSS-based link generation)
- T1566 - Phishing: Email or Web Content
- T1539 - Steal Web Session Cookie
- T1056 - Adversary-in-the-Middle / Input Capture
- T1656 - Impersonation
- T1111 - Multi-Factor Authentication Interception

## Notes
This is an educational article rather than a specific vulnerability disclosure. It provides valuable meta-analysis of XSS defense strategies across three conceptual levels. The article emphasizes that generic escaping functions are insufficient and that developers must understand context-specific encoding requirements. The Medium example highlights real-world impact: XSS on platforms with authentication or financial features enables account takeover and fraud. The article implicitly criticizes developers who implement only first-level defenses and miss higher-level protections.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
