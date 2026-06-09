# XSS Attacks and Defense: A Multi-Level Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Educational/General Security
- **Bounty:** N/A - Educational Article
- **Severity:** HIGH
- **Vuln types:** Stored XSS, Reflected XSS, DOM-based XSS, HTML Injection, Attribute-based XSS, JavaScript Protocol XSS
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
This comprehensive analysis discusses XSS vulnerabilities across three defensive levels: preventing code injection, implementing CSP to block execution, and minimizing damage post-compromise. The article demonstrates how context-specific escaping is critical, showing failures in naive HTML entity encoding and the need for attribute-aware and protocol-aware sanitization.

## Attack scenario (step by step)
1. Attacker identifies user input field (e.g., nickname) that gets output in multiple contexts without proper escaping
2. Attacker injects payload exploiting context-blind sanitization, such as closing HTML attributes with quotes and injecting event handlers
3. If basic escaping present, attacker uses JavaScript pseudo-protocol (javascript:) in href attributes to bypass tag-only sanitization
4. If CSP implemented, attacker crafts payload using whitelisted origins or finds CSP bypass via nonce/hash collision
5. Upon successful code execution, attacker pivots to higher-value targets (account takeover, financial transactions, data exfiltration)
6. Attacker aims to maximize damage by targeting sensitive operations available within XSS execution context

## Root cause
Context-agnostic input sanitization that treats all output locations identically despite requiring different escaping strategies. Developers often implement single-layer defense (e.g., HTML entity encoding) without recognizing that XSS prevention must adapt to context: HTML body content, attribute values, JavaScript strings, URL schemes, and CSS properties each require distinct handling.

## Attacker mindset
XSS attackers operate opportunistically across multiple attack surfaces. First, they probe for injection points and test sanitization robustness by varying payload syntax. When one approach fails, they shift context—moving from tag injection to attribute injection to protocol exploitation. The attacker views defensive layers as challenges to systematically overcome, escalating from arbitrary code execution to account takeover and financial fraud.

## Defensive takeaways
- Implement context-aware output encoding: use HTML entity encoding for body content, attribute encoding for attributes, JavaScript string escaping for JS contexts, URL encoding for URLs, and CSS escaping for stylesheets
- Never trust single-layer defense; combine input validation, output encoding, and Content Security Policy (CSP) as overlapping controls
- Use established libraries/frameworks with built-in encoding (e.g., htmlspecialchars in PHP, template auto-escaping in modern frameworks) rather than manual sanitization
- Define and enforce CSP policies restrictive enough to block inline scripts, unsafe-eval, and untrusted external sources
- Assume level-1 and level-2 controls may fail; implement level-3 mitigations such as Subresource Integrity (SRI), session binding, rate limiting on sensitive operations, and segregation of high-value functionality
- Conduct context-aware penetration testing specifically targeting different output locations and injection vectors
- Educate developers on why context matters; use code reviews to catch multi-context output without corresponding multi-context escaping
- Monitor for XSS exploitation post-deployment via CSP violation reports and anomalous user behavior

## Variant hunting
['Test all data output locations (body, attributes, script tags, event handlers, URLs) with context-specific XSS payloads', 'Identify user-controllable fields reflected in multiple contexts and validate each context receives appropriate encoding', 'Probe JavaScript pseudo-protocol handlers (javascript:, data:, vbscript:) in href, src, and form action attributes', 'Test for DOM-based XSS by tracing user input through JavaScript (location.hash, search parameters, postMessage) to DOM-altering APIs', 'Search for DOM-based sinks: innerHTML, document.write, eval(), setTimeout()/setInterval() with string arguments, and Function() constructor', 'Enumerate CSP policies for weaknesses: overly permissive directives, use of unsafe-inline or unsafe-eval, domain whitelisting without subdomain validation, and nonce/hash collisions', 'Test polyglot payloads that bypass multiple encoding schemes simultaneously', 'Hunt for second-order XSS via stored data in databases, caches, or logs that may be retrieved and output in different contexts', "Analyze framework-specific behavior: some frameworks auto-escape, others don't; identify gaps in auto-escaping coverage"]

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution
- T1566 - Phishing (via XSS-crafted malicious links)
- T1539 - Steal Web Session Cookie
- T1528 - Steal Application Access Token
- T1563 - Modify Authentication Process (via XSS-driven account manipulation)

## Notes
This writeup provides a layered defense framework essential for secure development. The multi-level approach (prevention → detection/blocking → damage control) reflects mature security thinking. Critical insight: naive developers believe single sanitization step suffices; the article proves context matters fundamentally. The Medium example demonstrates how XSS severity is business-contextual (account takeover vs. paywall bypass). Real-world impact: many frameworks still fail at context-aware escaping; developers must audit output locations. Testing implications: static scanning alone inadequate; dynamic testing must cover multiple output contexts and protocol handlers. The article implicitly warns against security theater (CSP without proper implementation) and emphasizes defense-in-depth necessity.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
