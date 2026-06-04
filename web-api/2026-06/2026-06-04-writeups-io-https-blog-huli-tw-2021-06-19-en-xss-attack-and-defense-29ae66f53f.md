# XSS Attacks and Defense: A Multi-Level Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** General Security Education
- **Bounty:** N/A - Educational Article
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), HTML Injection, Attribute-based XSS, JavaScript Protocol Injection, DOM-based XSS
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
Comprehensive analysis of XSS vulnerabilities across three defensive levels: preventing code injection, mitigating execution through CSP, and minimizing damage post-compromise. The article demonstrates that context-aware escaping is critical, as different output contexts require different sanitization approaches.

## Attack scenario (step by step)
1. Attacker identifies user input field (e.g., nickname) that is rendered without proper escaping
2. Attacker injects malicious payload such as <script>alert(1)</script> or event handler attributes
3. When victim views the page containing attacker's input, JavaScript executes in victim's browser context
4. Attacker gains ability to steal session tokens, perform account takeover, or exfiltrate sensitive data
5. If CSP is bypassed, attacker escalates to unauthorized account access or financial fraud
6. If code execution achieved, attacker minimizes damage detection through subtle data theft or privilege escalation

## Root cause
Insufficient input validation and context-unaware output encoding. The root cause is developers applying generic escaping rules without understanding that different HTML contexts (tag content, attributes, JavaScript, URLs) require different encoding schemes. Additionally, dangerous protocol handlers (javascript:) and event attributes bypass simple tag-based escaping.

## Attacker mindset
Attackers recognize that developers often implement superficial defenses (escaping < and >) without understanding context-specific requirements. They exploit the gap between naive implementations and real-world rendering contexts, using attribute breakout techniques, protocol injection, and polyglot payloads to achieve code execution despite partial mitigations.

## Defensive takeaways
- Implement context-aware output encoding: use different escaping functions for HTML body, attributes, JavaScript strings, and URLs
- Use established libraries (htmlspecialchars, DOMPurify, etc.) rather than custom escaping logic
- Apply Content Security Policy (CSP) as a defense-in-depth layer to restrict dangerous directives and inline scripts
- Validate and whitelist URL protocols in href attributes to block javascript: pseudo-protocols
- Implement input validation, but recognize it is not sufficient alone without proper output encoding
- Assume code execution may occur despite first-level defenses; implement third-level protections such as privilege separation and sensitive operation authentication
- Regularly audit rendering contexts where user input appears and verify appropriate escaping is applied
- Use security headers and frame options to limit account takeover and financial transaction risks

## Variant hunting
Search for: stored XSS in user profile fields, attribute-based XSS in dynamically generated HTML, event handler injection bypassing tag filters, protocol-based XSS in link href attributes, DOM-based XSS in framework routing, CSP bypass techniques via nonce extraction or unsafe-eval, authentication token extraction via XSS, CSRF token theft via XSS, credential harvesting through fake login overlays injected via XSS

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539
- T1550
- T1005
- T1185

## Notes
This is an educational security article rather than a traditional bug bounty writeup. It provides a framework for understanding XSS at multiple defensive layers. The article emphasizes that security is not binary but layered, and defenders must think beyond simply preventing injection to include execution prevention (CSP) and damage mitigation (privilege separation, sensitive operation verification). The key insight is that context matters: the same data encoded identically for HTML body content will fail when placed in an attribute or JavaScript context.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
