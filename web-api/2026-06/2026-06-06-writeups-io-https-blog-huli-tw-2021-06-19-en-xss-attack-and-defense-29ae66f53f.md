# XSS Attacks and Defense: A Multi-Level Security Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Educational/Security Research
- **Bounty:** N/A - Educational Content
- **Severity:** high
- **Vuln types:** Stored XSS, Reflected XSS, DOM-based XSS, HTML Injection, Attribute Injection, JavaScript Protocol Injection
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
Comprehensive analysis of XSS vulnerabilities across three defense levels: preventing code injection, blocking code execution via CSP, and minimizing damage when XSS succeeds. The writeup demonstrates how context-aware escaping is critical, as naive approaches fail when user input appears in different contexts (HTML body, attributes, JavaScript, URLs).

## Attack scenario (step by step)
1. Attacker identifies user input field (nickname, avatar URL, link) that is rendered on page without proper sanitization
2. Attacker crafts payload appropriate to injection context (e.g., closing tag quotes for attributes, javascript: protocol for URLs)
3. Payload reaches page output and becomes part of HTML/JavaScript code structure
4. Browser parser interprets malicious payload as code rather than data
5. Injected script executes in victim's browser with same privileges as legitimate page code
6. Attacker steals session tokens, performs account takeover, or executes unauthorized actions

## Root cause
Insufficient input validation and context-unaware output encoding. Developers escape only basic characters (<>) without considering that different output contexts (HTML body, attributes, URLs, JavaScript strings) require different encoding schemes. Lack of defense-in-depth approach relying solely on escaping instead of CSP or other secondary controls.

## Attacker mindset
Opportunistic exploitation of common developer mistakes - recognizing that most developers only escape obvious characters and miss context-specific injection points (attributes, URLs, event handlers). Leveraging JavaScript pseudo-protocols and attribute breaking as alternative injection vectors when basic HTML escaping is present.

## Defensive takeaways
- Implement context-aware output encoding: use different encoding for HTML body, HTML attributes, JavaScript strings, and URL parameters
- Apply Defense in Depth: combine input validation, output escaping, CSP headers, and HTTPOnly cookie flags
- Use templating engines and frameworks with auto-escaping capabilities (not manual string concatenation)
- Implement Content Security Policy (CSP) to block inline scripts and restrict script sources as secondary defense
- For Level 3 defense, apply principle of least privilege: limit XSS blast radius via proper authentication, authorization, and CSRF tokens
- Validate protocol schemes in URLs (reject javascript:, data:, vbscript:)
- Use security headers (X-XSS-Protection, X-Content-Type-Options, X-Frame-Options) for additional browser-level protection
- Regular security testing including fuzzing with context-specific payloads

## Variant hunting
['Test attribute injection with various closing quote combinations: single quotes, double quotes, backticks in template literals', 'Probe URL contexts for protocol-based injection: javascript:, data:, vbscript:, file:, about: schemes', "Check JavaScript string contexts for escaping breaks: \\' vs \\\\ vs string terminators", 'Search for SVG/XML contexts requiring different escaping rules than HTML', 'Test mutation-based XSS where browser auto-corrects malformed HTML into executable code', 'Examine dynamically inserted content via innerHTML, eval(), or Function() constructors', 'Test CSS injection for expression evaluation and URL-based payloads in style attributes', 'Look for context-switching injection (output in attribute, switched to body context via browser behavior)']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204
- T1105

## Notes
Educational writeup emphasizing that XSS defense is not binary but exists on a spectrum of three levels. Key insight: escaping must be context-aware because the same special character has different meaning in HTML body vs attributes vs JavaScript vs URLs. The framework/language choice significantly impacts vulnerability surface - using frameworks with auto-escaping substantially reduces risk versus manual string concatenation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
