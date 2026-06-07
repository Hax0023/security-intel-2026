# XSS Attacks and Defense: A Multi-Level Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Educational/General Web Security
- **Bounty:** N/A - Educational Article
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), HTML Injection, HTML Attribute Injection, JavaScript Code Injection, DOM-based XSS
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
Comprehensive analysis of XSS vulnerabilities across three defense levels: preventing code injection, blocking execution via CSP, and minimizing damage post-compromise. The article demonstrates that simple escaping is insufficient and context-aware sanitization is required for different injection vectors.

## Attack scenario (step by step)
1. Attacker identifies input field (e.g., nickname) that reflects user input without proper escaping
2. Attacker tests basic XSS payload like <script>alert(1)</script> in nickname field
3. If basic escaping present, attacker crafts context-aware payload exploiting HTML attributes (e.g., " onload="alert(1)) or JavaScript protocol (javascript:alert(1))
4. Payload bypasses inadequate sanitization by exploiting different rendering contexts (HTML body vs. attributes vs. URLs)
5. Malicious script executes in victim's browser with full session privileges
6. Attacker exfiltrates session tokens, performs account takeover, or financial fraud

## Root cause
Developers implement generic escaping (e.g., htmlspecialchars) without understanding context-specific encoding requirements. Different output contexts (HTML body, attribute values, JavaScript strings, URL parameters) require different sanitization approaches. Single-layer defense fails when CSP is bypassed or misconfigured.

## Attacker mindset
Exploit the gap between developer assumptions and actual security requirements. Attackers recognize that simple < and > escaping is insufficient and probe for context-specific weaknesses. Multi-stage approach: first identify injection points, then craft payloads for specific contexts, finally leverage XSS for account compromise or financial theft.

## Defensive takeaways
- Implement context-aware output encoding (HTML, attribute, JavaScript, CSS, URL contexts require different escaping)
- Never rely on single escaping method; use framework-provided sanitization functions designed for specific contexts
- Deploy Content Security Policy (CSP) as second-level defense to prevent inline script execution
- Implement privilege separation and authentication checks even for XSS-compromised sessions
- Use HTTPOnly and Secure cookie flags to prevent session hijacking via XSS
- Apply defense-in-depth: input validation, output encoding, CSP, and post-exploitation controls
- Recognize three defense levels: prevention of injection, prevention of execution (CSP), and damage mitigation

## Variant hunting
['Test attribute injection in different HTML elements (img, a, div, form) with event handlers', 'Probe JavaScript protocol handlers (javascript:, data:, vbscript:) in link and form action attributes', 'Test CSS injection vectors and style attribute context escaping', 'Examine SVG and XML contexts for namespace-specific XSS', 'Check template injection when user input influences template rendering logic', 'Test DOM-based XSS where client-side JavaScript processes user input', 'Verify CSP bypass techniques (nonce leakage, unsafe-eval, trusted-types evasion)', 'Test polyglot payloads that work across multiple contexts']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1539 - Steal Web Session Cookie
- T1583 - Acquire Infrastructure
- T1598 - Phishing for Information
- T1204 - User Execution

## Notes
This is an educational article, not a specific bug report. It emphasizes that XSS defense is layered and that many developers misunderstand the nuances of output encoding. The article correctly identifies that htmlspecialchars alone is insufficient and that different contexts require different encoding schemes. The three-level defense model (prevention, mitigation via CSP, post-exploitation controls) represents security best practices. Key insight: developers often assume generic escaping functions handle all cases, leading to context-escape mismatches.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
