# XSS Attacks and Defense: A Multi-Level Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Educational/General Security
- **Bounty:** N/A - Educational writeup
- **Severity:** HIGH
- **Vuln types:** Stored XSS, Reflected XSS, DOM-based XSS, HTML Injection, Attribute Injection, JavaScript Protocol Injection
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
Comprehensive analysis of XSS vulnerabilities across three defense levels: preventing code injection, blocking code execution via CSP, and minimizing damage when code execution occurs. The writeup demonstrates various escaping pitfalls and context-specific vulnerabilities that arise from improper output encoding in different HTML contexts.

## Attack scenario (step by step)
1. Attacker identifies a nickname field rendered without proper escaping in HTML content
2. Attacker injects <script>alert(1)</script> and payload executes when other users view the profile
3. Attacker notices nickname is also rendered in img alt attribute and uses " onload="alert(1) to break out of attribute context
4. Attacker bypasses basic escaping by exploiting context-specific encoding failures (attributes vs text nodes vs URLs)
5. If CSP is implemented, attacker uses javascript: protocol in href attributes to execute code within policy restrictions
6. With successful code execution, attacker escalates to account takeover, session hijacking, or financial fraud on platforms with sensitive operations

## Root cause
Developers apply uniform escaping rules (e.g., only escaping <>  or &) without understanding that different HTML contexts (text content, attributes, URLs, JavaScript) require distinct encoding strategies. Lack of context-aware output encoding and failure to validate/sanitize URLs for dangerous protocols like javascript:

## Attacker mindset
Opportunistic exploitation of implementation gaps. Attackers recognize that developers often implement basic escaping but fail to account for all contexts where user input appears. They methodically test different injection points and encoding contexts, gradually escalating from simple tag injection to attribute breakout and protocol-based attacks.

## Defensive takeaways
- Implement context-aware output encoding: HTML text content, HTML attributes, JavaScript strings, CSS, and URLs each require different escaping strategies
- Use established libraries and frameworks with built-in XSS protection rather than implementing custom escaping logic
- Validate and sanitize user input at input boundaries, particularly for URLs - whitelist known-safe protocols and reject javascript: and data: URIs
- Implement Content Security Policy (Level 2 defense) as defense-in-depth even when input validation is in place
- Design with least privilege in mind (Level 3 defense): prevent account takeover, restrict sensitive operations from XSS context, implement CSRF tokens
- Use templating engines that enforce automatic context-appropriate escaping by default
- Regular security testing including input fuzzing with polyglot payloads across multiple injection points
- Educate developers on the nuances of XSS - it's not just about sanitizing <> characters

## Variant hunting
['Test all user input fields (nicknames, comments, descriptions, URLs, email) in different HTML contexts (text, attributes, href, src, style, event handlers)', 'Probe for SVG/XML-based XSS bypassing HTML-only protections', 'Test CSS injection in style attributes and <style> tags when escaping is incomplete', 'Attempt protocol-based attacks: javascript:, data:, vbscript: in href, src, form action attributes', 'Test for encoding bypasses: double encoding, Unicode encoding, mixed encoding, HTML entity encoding chains', "Check if CSP is actually enforced and test for policy bypass via unsafe domains or 'unsafe-inline' in nonce/hash implementations", 'Test for DOM-based XSS through client-side JavaScript processing of user input', 'Enumerate sensitive operations reachable via XSS (password reset, account transfer, financial transactions) for impact escalation']

## MITRE ATT&CK
- T1190
- T1499
- T1583
- T1598
- T1608
- T1657

## Notes
This is a foundational educational writeup rather than a specific vulnerability report. The multi-level defense framework is valuable: Level 1 (prevent injection via context-aware encoding), Level 2 (block execution via CSP), Level 3 (minimize damage via design and operational security). The key insight is that 'escaping' is not one-size-fits-all; developers must understand their context (attribute vs text vs URL vs JavaScript) to escape correctly. The writeup emphasizes the gap between what developers think they're protecting against and what actually needs protection.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
