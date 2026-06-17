# Bypassing XSS Filters: Techniques and Solutions

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Educational/General Web Security
- **Bounty:** Not applicable - educational article
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding, Blacklist-based Filter Evasion
- **Category:** web-api
- **Writeup:** https://infosecwriteups.com/bypassing-xss-filters-techniques-and-solutions-d6674029f1e9

## Summary
This article explores common XSS filter bypass techniques including length limits, event handler blocking, tag filtering, and character restrictions. It demonstrates how blacklist-based filtering approaches are inherently flawed and can be circumvented through encoding, alternative event handlers, and non-standard payload methods.

## Attack scenario (step by step)
1. Attacker identifies that target application implements a blacklist filter blocking common event handlers like 'onerror', 'onload', and 'onclick'
2. Attacker researches alternative event handlers not included in the blacklist (e.g., 'onmouseover', 'onfocus', 'onload' variants)
3. Attacker crafts payload using alternative event handler: '<img src=x onmouseover=alert(1)>'
4. Payload bypasses the blacklist filter and reaches the DOM
5. When user interacts with the malicious element, JavaScript executes in user's browser context
6. Attacker steals session cookies, redirects to phishing page, or performs actions on behalf of victim

## Root cause
Reliance on blacklist-based input filtering rather than whitelist-based validation and proper output encoding. Filters attempt to block known attack patterns but fail to account for the vast number of alternative XSS vectors and encoding bypasses available to attackers.

## Attacker mindset
Pragmatic and adaptive - understanding that any blacklist-based defense has gaps. Attacker focuses on finding unblocked alternatives: other event handlers, encoding schemes, HTML5 attributes, JavaScript APIs, or DOM-based execution paths. Views security measures as a puzzle to solve rather than a barrier.

## Defensive takeaways
- Implement whitelist-based input validation instead of blacklist filtering
- Use proper output encoding/escaping based on context (HTML, JavaScript, URL, CSS)
- Deploy Content Security Policy (CSP) headers to restrict script execution
- Use templating engines with automatic contextual escaping
- Validate and sanitize on both client and server sides
- Apply principle of least privilege to user-controlled data
- Use security libraries like DOMPurify for sanitization when necessary
- Implement HTTPOnly and Secure flags on cookies to prevent JavaScript access
- Regular security testing including fuzzing with XSS payloads
- Keep frameworks and libraries updated with latest security patches

## Variant hunting
Search for: alternative XSS event handlers (onmouseover, onfocus, onwheel), HTML5-specific attributes, SVG-based XSS, CSS expression injection, data URIs, JavaScript protocol handlers, DOM-based XSS in frameworks, mutation-based XSS, CSS injection leading to XSS, polyglot payloads, encoding variations (hex, unicode, UTF-7), case variation bypasses, null byte injection, comment-based obfuscation, argument injection in event handlers

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
This is an educational writeup rather than a specific bug bounty report. It functions as a security awareness article demonstrating fundamental XSS bypass principles. The code examples are simplified and illustrative. Real-world applications often use multiple security layers, making exploitation more complex. The article emphasizes that no single filter can block all XSS variations, reinforcing the need for defense-in-depth strategies including CSP, proper encoding, and secure coding practices.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
