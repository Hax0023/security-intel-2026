# XSS Attacks and Defense: A Multi-Level Security Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Educational/General Security Knowledge
- **Bounty:** N/A - Educational Article
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), HTML Injection, Attribute-based XSS, JavaScript Code Injection, JavaScript Protocol Injection
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
This article provides a comprehensive framework for understanding XSS vulnerabilities across three defensive levels: preventing code injection, mitigating execution through CSP, and minimizing damage post-compromise. It demonstrates how context-specific escaping is critical, as improper handling of user input in different contexts (HTML content, attributes, URLs) enables multiple attack vectors.

## Attack scenario (step by step)
1. Attacker identifies an input field where user data is reflected without proper sanitization (e.g., nickname field)
2. Attacker crafts a payload such as <script>alert(1)</script> or attribute-based payload like " onload="alert(1)
3. When the application renders this data without context-appropriate escaping, the payload becomes part of the HTML/JavaScript
4. Victim views the affected page and the injected code executes in their browser context
5. Attacker escalates from XSS to account takeover or unauthorized actions (session stealing, privilege abuse)
6. If CSP is bypassed or insufficient, attacker achieves arbitrary code execution within the application context

## Root cause
Insufficient input validation and context-unaware output encoding. Developers often apply blanket escaping rules (e.g., only escaping < and >) without considering the specific context where data is rendered (HTML content vs. attributes vs. URLs vs. JavaScript strings). Different contexts require different escaping strategies.

## Attacker mindset
Attackers recognize that escaping is not one-size-fits-all and exploit context-specific weaknesses. They test multiple injection points and payload variations, understanding that attribute injection and JavaScript protocol handlers bypass naive < > filtering. Advanced attackers chain XSS with session theft or financial fraud to maximize impact.

## Defensive takeaways
- Implement context-aware output encoding tailored to where data is rendered (HTML body, attributes, URLs, JavaScript strings, CSS)
- Never rely solely on blacklist-based filtering; use whitelist validation where possible
- Apply Content Security Policy (CSP) as a secondary defense layer to prevent inline script execution
- Use security-focused libraries and frameworks with built-in escaping mechanisms (e.g., PHP htmlspecialchars, template engines with auto-escaping)
- Validate and sanitize URLs, blocking JavaScript pseudo-protocols (javascript:, data:, vbscript:)
- Design defenses assuming XSS will occur; implement measures to limit damage (SameSite cookies, CSRF tokens, account isolation, financial transaction confirmation)
- Conduct context-specific security testing for each input/output combination

## Variant hunting
Search for reflected and stored XSS in form inputs, user profile fields, search parameters, and comment sections. Identify secondary injection points where user data is rendered in multiple contexts. Test JavaScript protocol injection in href/src attributes. Examine how frameworks handle template rendering and whether auto-escaping is enabled. Look for mixed content scenarios where different escaping rules apply.

## MITRE ATT&CK
- T1190
- T1499
- T1598
- T1566

## Notes
This is an educational security article, not a bug bounty report. It provides foundational knowledge on XSS attack vectors and defense-in-depth strategies. The article emphasizes that single-layer defense is insufficient; organizations should implement defense across multiple levels (input validation, output encoding, CSP, damage limitation). The distinction between different XSS contexts and appropriate escaping methods is critical for developers implementing security controls.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
