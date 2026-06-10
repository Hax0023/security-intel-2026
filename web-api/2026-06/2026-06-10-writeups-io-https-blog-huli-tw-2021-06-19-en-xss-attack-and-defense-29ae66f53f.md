# XSS Attacks and Defense: A Multi-Level Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Educational/General Security Research
- **Bounty:** N/A - Educational writeup
- **Severity:** high
- **Vuln types:** Stored XSS, Reflected XSS, DOM-based XSS, HTML Injection, Attribute-based XSS, JavaScript Protocol XSS
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
Comprehensive analysis of XSS vulnerabilities and defensive strategies across three levels: preventing code injection, preventing code execution via CSP, and minimizing damage from successful XSS. The writeup demonstrates context-specific escaping requirements and highlights how incomplete sanitization in different HTML contexts (attributes, text nodes, URL protocols) can lead to XSS exploitation.

## Attack scenario (step by step)
1. Attacker identifies user-controlled input field (e.g., nickname) that is rendered on page without proper sanitization
2. Attacker injects payload such as <script>alert(1)</script> or HTML attribute escape like " onload="alert(1)
3. Attacker manipulates the context where payload is rendered (e.g., within HTML attribute vs text node) to bypass basic < and > escaping
4. If basic escaping exists, attacker uses context-specific payloads like javascript: protocol in href attributes or event handlers
5. Payload executes in victim's browser when page is viewed, allowing session hijacking, credential theft, or account takeover
6. If CSP is implemented, attacker attempts CSP bypass techniques or exploits application functionality with XSS to steal sensitive data

## Root cause
Insufficient input validation and context-unaware output encoding. Developers implement simplistic escaping (only <> characters) without considering that different HTML contexts require different escaping strategies. Failure to recognize that user input can appear in HTML tag attributes, JavaScript code blocks, URL protocols, and CSS contexts—each requiring distinct sanitization approaches.

## Attacker mindset
Methodical reconnaissance of output contexts; testing for layered defenses; adapting payloads to bypass context-specific filters; leveraging browser parsing behavior and protocol handlers (javascript:, data:, vbscript:) to circumvent naive sanitization; escalating from code execution to account takeover or financial fraud.

## Defensive takeaways
- Implement context-aware output encoding: use different escaping functions based on where user data is rendered (HTML body, attributes, JavaScript, CSS, URL)
- Never trust user input; validate and sanitize at entry points using whitelist approaches when possible
- Use templating engines that provide automatic context-aware escaping (Jinja2, Twig, etc.)
- Implement Content Security Policy (CSP) as second-level defense to restrict inline scripts and limit script sources
- Disable dangerous protocols in href attributes (javascript:, data:, vbscript:) via URL validation
- Apply principle of least privilege: limit what XSS payload can accomplish even if execution occurs (third-level defense)
- Use HttpOnly and Secure flags on cookies to prevent session theft via XSS
- Implement sub-resource integrity (SRI) for external scripts
- Regular security testing including payload variation across contexts

## Variant hunting
['Test escaping bypass in different HTML contexts: tag attributes (onclick, onload, src), href protocols, data attributes', 'Enumerate event handlers available in target browser version (onload, onerror, onmouseover, ontouchstart)', 'Test protocol handlers: javascript:, data:, vbscript:, file:, about:', 'Investigate HTML5 event handlers and exotic attributes that may execute code', 'Test for DOM-based XSS by tracing user input through JavaScript (location.hash, postMessage, etc.)', 'Look for double-encoding bypasses or encoding-specific filters', 'Test mutation XSS (mXSS) where browser HTML parser behavior differs from sanitizer expectations', 'Identify stored XSS in secondary output locations (logs, analytics, email notifications)', 'Test CSP bypass vectors: nonce reuse, unsafe-eval, unsafe-inline in specific directives']

## MITRE ATT&CK
- T1190
- T1059
- T1204.001
- T1566.002
- T1072
- T1539
- T1005

## Notes
This is an educational security writeup, not a specific bug bounty submission. It provides a framework for understanding XSS defense in layers: Layer 1 (input validation/output encoding), Layer 2 (CSP and execution prevention), Layer 3 (damage limitation). The article emphasizes that single-function escaping is insufficient and developers must understand the parser's behavior in different contexts. Real-world exploitation severity depends on what attackers can do with code execution (account takeover, privilege escalation, financial fraud). The writeup references context-specific escaping requirements but appears incomplete (cuts off mid-discussion about URL protocols).

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
