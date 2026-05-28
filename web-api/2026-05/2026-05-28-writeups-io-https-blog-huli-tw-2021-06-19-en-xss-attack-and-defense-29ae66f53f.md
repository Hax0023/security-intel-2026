# XSS Attacks and Defense: A Multi-Level Security Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Educational/General Security
- **Bounty:** N/A - Educational article
- **Severity:** High
- **Vuln types:** Stored XSS, Reflected XSS, DOM-based XSS, HTML Injection, Attribute-based XSS, JavaScript Protocol XSS
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
Comprehensive analysis of XSS vulnerabilities across three defensive levels: preventing code injection, mitigating injected code execution via CSP, and damage limitation post-compromise. The article demonstrates how context-specific escaping is critical, as different output contexts (HTML, attributes, JavaScript, URLs) require different sanitization approaches.

## Attack scenario (step by step)
1. Attacker identifies user input field (nickname) that is rendered without proper escaping
2. Attacker injects malicious payload like '<script>alert(1)</script>' or event handler attributes
3. If basic HTML escaping only (<>), attacker uses attribute context escape: '" onload="alert(1)' to break out of attributes
4. If input-level defenses fail, attacker executes JavaScript in browser context of victim users
5. If CSP blocks inline scripts, attacker uses alternative vectors like javascript: protocol in URLs or DOM manipulation
6. If all XSS is prevented, attacker focuses on account takeover or privilege escalation using legitimate XSS vectors

## Root cause
Insufficient context-aware output encoding and reliance on single-layer defense. Developers often implement only basic HTML entity encoding without accounting for multiple output contexts (HTML content, attributes, JavaScript, URLs), where different special characters pose risks.

## Attacker mindset
Systematic exploitation of defense gaps by testing multiple injection vectors across different contexts. Attackers recognize that basic escaping is insufficient and probe for context-specific weaknesses (attribute breakout, protocol handlers). They operate with layered thinking: if one defense fails, exploit the next level until code execution is achieved.

## Defensive takeaways
- Implement context-aware output encoding: use different escaping rules for HTML content, HTML attributes, JavaScript strings, CSS, and URLs
- Apply defense-in-depth: combine input validation, output encoding, CSP headers, and HttpOnly cookies
- Use security libraries and frameworks that provide automatic context-aware escaping rather than manual implementation
- Implement Content Security Policy (CSP) to block inline scripts and restrict code execution sources
- Assume code injection will occur and plan Layer 2 defenses (CSP, sandbox restrictions) and Layer 3 defenses (CSRF tokens, rate limiting, account isolation)
- Conduct context analysis of all user data output locations and map appropriate escaping functions
- Use allowlists for URLs in href attributes to prevent javascript: protocol attacks
- Implement subresource integrity (SRI) and CSP script-src directives to prevent injected script execution

## Variant hunting
['Test all output contexts: check if escaping varies between HTML body, attribute values, href attributes, event handlers, and script content', 'Probe for attribute breakout using quotes and special characters in all user-controlled attributes (alt, title, data-*, etc.)', 'Test protocol handlers: javascript:, data:, vbscript: in href, src, formaction, and other URL attributes', 'Search for DOM XSS by tracing user input through JavaScript (location.hash, innerHTML, appendChild)', 'Test event handlers in different HTML elements and contexts', 'Look for double encoding or nested encoding bypasses', 'Test mutation-based XSS with SVG and MathML contexts', 'Check for XSS in error messages, redirects, and 404 pages']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (via XSS-injected malicious links)
- T1203 - Exploitation for Client Execution
- T1204 - User Execution (clicking XSS-injected links)
- T1539 - Steal Web Session Cookie (via XSS)
- T1185 - Man in the Browser (XSS-based session hijacking)

## Notes
This is an educational security article rather than a traditional bug bounty writeup. It provides valuable framework for understanding XSS as a multi-layered problem requiring multi-layered defense. The article emphasizes that developers must understand context-aware escaping - a common gap where developers implement one escaping method universally when different contexts (HTML, attributes, JavaScript, URLs) require different approaches. The three-level defense model (prevent injection → prevent execution → limit damage) represents mature security thinking applicable beyond XSS to other vulnerability classes.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
