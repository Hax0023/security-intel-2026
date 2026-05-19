# XSS Attacks and Defense: A Multi-Level Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Educational/General Security
- **Bounty:** N/A
- **Severity:** High
- **Vuln types:** Stored XSS, Reflected XSS, DOM-based XSS, HTML Injection, Attribute Injection, JavaScript Code Injection
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
A comprehensive analysis of XSS vulnerabilities across three defensive levels: preventing code injection, implementing CSP to block execution, and minimizing damage post-compromise. The writeup demonstrates how attackers can bypass naive escaping by exploiting context-specific injection points such as HTML attributes, JavaScript pseudo-protocols, and event handlers.

## Attack scenario (step by step)
1. Attacker identifies user input field (e.g., nickname) that is rendered without proper escaping
2. Attacker injects payload like <script>alert(1)</script> or " onload="alert(1) depending on rendering context
3. If output is in HTML attribute context, attacker closes attribute quote and injects event handler (e.g., " onload="alert(1))
4. If CSP is not implemented, injected JavaScript executes in victim's browser within application context
5. Attacker gains ability to steal session tokens, hijack accounts, or exfiltrate sensitive data
6. If CSP is bypassed or missing, attacker escalates to account takeover or financial fraud (e.g., Medium paywall bypass)

## Root cause
Insufficient input validation and context-aware output encoding. Developers apply generic escaping (e.g., only escaping < and >) without considering the specific output context (HTML body, attributes, JavaScript, URL schemes). Different contexts require different escaping strategies.

## Attacker mindset
Exploit the gap between developers' assumptions about escaping and actual attack surface. Identify multiple injection points in the same data field based on rendering context. Progressively test escaping robustness by varying payload format. Once code execution is achieved, pivot to higher-value attacks like account compromise or financial exploitation.

## Defensive takeaways
- Implement context-aware output encoding: use different escaping functions for HTML body, HTML attributes, JavaScript strings, and URL schemes
- Apply input validation as defense-in-depth but do not rely solely on it; output encoding is critical
- Deploy Content Security Policy (CSP) with strict directives to prevent inline script execution and restrict script sources
- Assume breach and implement defense-in-depth: even if XSS executes, limit damage via strong authentication, CSRF tokens, SameSite cookies, and privilege separation
- Use security-focused templating engines that enforce automatic context-aware escaping
- Regularly audit all output locations where user data appears, especially in attribute contexts
- For high-value operations (account changes, payments), require additional authentication factors beyond session token verification

## Variant hunting
Search for similar context-aware injection bypasses in other applications: test nickname/profile fields rendered in img alt attributes, href attributes with javascript: protocol, and data attributes. Examine whether frameworks auto-escape in templates. Test payloads like onfocus=, onmouseover=, oninput= in different attribute contexts. Check if CSP is present and if strict-dynamic or script-src nonce is implemented.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539
- T1550

## Notes
This is an educational writeup rather than a disclosed vulnerability in a specific program. It provides a tiered defense model: Level 1 (prevent injection via escaping), Level 2 (execute via CSP), Level 3 (minimize damage post-compromise). The article emphasizes that escaping strategy is context-dependent, and a single escaping approach fails across multiple output contexts. Real-world impact varies by application: Medium platform vulnerability could lead to account takeover or payment fraud.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
