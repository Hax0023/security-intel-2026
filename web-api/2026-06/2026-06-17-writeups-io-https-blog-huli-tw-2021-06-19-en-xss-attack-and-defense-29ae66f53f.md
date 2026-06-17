# XSS Attacks and Defense: A Multi-Level Security Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Educational/General Security
- **Bounty:** N/A - Educational Article
- **Severity:** HIGH
- **Vuln types:** Cross-Site Scripting (XSS), HTML Injection, Attribute-based XSS, JavaScript Protocol Injection
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
A comprehensive security analysis examining XSS vulnerabilities across three defense levels: preventing code injection, mitigating injected code execution via CSP, and minimizing damage from successful exploitation. The article demonstrates how context-specific escaping is critical, as generic escaping of <> characters is insufficient when user input appears in HTML attributes or JavaScript contexts.

## Attack scenario (step by step)
1. Attacker identifies a user input field (e.g., nickname) that is rendered in multiple contexts without proper context-aware escaping
2. Attacker crafts payload considering the specific rendering context, such as a quote character to break out of an HTML attribute
3. Payload like '" onload="alert(1)' closes the alt attribute and injects an event handler in an img tag
4. If escaping only covers <> but not quotes, the attribute-based XSS succeeds
5. JavaScript pseudo-protocols like javascript: can be injected in href attributes to execute code on click
6. Successful exploitation allows account takeover, financial fraud, or data exfiltration depending on application functionality

## Root cause
Insufficient context-aware output encoding and overly simplistic escaping strategies that fail to account for multiple rendering contexts (HTML body, HTML attributes, JavaScript code, URL protocols)

## Attacker mindset
Attackers recognize that developers often implement basic escaping (e.g., <> only) and exploit context-specific weaknesses. They understand that different contexts require different escape characters and can craft payloads that bypass incomplete sanitization by using quotes, event handlers, or protocol handlers.

## Defensive takeaways
- Implement context-aware escaping: different escape rules for HTML body, attributes, JavaScript, CSS, and URLs
- Never trust user input; validate at intake and encode at output
- Implement multiple defense layers: prevent injection (Level 1), restrict execution via CSP (Level 2), and minimize damage via authorization/isolation (Level 3)
- Use framework-provided sanitization functions (e.g., htmlspecialchars in PHP) rather than manual escaping
- Block JavaScript pseudo-protocols in href attributes or validate against whitelisted URL schemes
- Apply defense-in-depth: CSP headers, HttpOnly cookies, CORS policies, and principle of least privilege
- Regularly audit rendering code for all contexts where user input appears

## Variant hunting
['Search for URL rendering in href, src, action attributes without protocol validation', 'Identify all user-controlled variables in template rendering and check escape function usage', 'Test for stored XSS in user profile fields, comments, and settings that are displayed to other users', 'Examine JavaScript event handlers (onload, onerror, onclick) in dynamically constructed HTML', 'Check for DOM-based XSS in client-side JavaScript that manipulates innerHTML with user data', 'Test SVG and XML contexts which may have different escaping requirements than HTML', 'Look for data attributes or JSON encoding contexts where standard HTML escaping is insufficient']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539

## Notes
This is an educational writeup rather than a bug bounty report. It provides valuable security analysis but lacks specific vulnerability details, affected systems, or proof-of-concept code. The multi-level defense framework is excellent for security training: Level 1 (prevention), Level 2 (containment via CSP), Level 3 (damage control). The article emphasizes that escaping is context-dependent and demonstrates why naive implementations fail.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
