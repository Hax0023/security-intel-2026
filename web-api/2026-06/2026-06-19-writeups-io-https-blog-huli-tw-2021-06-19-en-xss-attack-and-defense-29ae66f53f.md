# XSS Attacks and Defense: A Multi-Level Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Educational/General Security
- **Bounty:** N/A - Educational writeup
- **Severity:** high
- **Vuln types:** Stored XSS, Reflected XSS, DOM-based XSS, HTML Injection, Attribute-based XSS, JavaScript Protocol XSS
- **Category:** web-api
- **Writeup:** https://blog.huli.tw/2021/06/19/en/xss-attack-and-defense/

## Summary
Comprehensive analysis of XSS vulnerabilities across three defensive levels: preventing code injection through input validation and context-aware escaping, mitigating execution via Content Security Policy, and minimizing damage post-compromise. The article demonstrates how inadequate escaping in different contexts (HTML body, attributes, URLs) enables multiple XSS attack vectors despite attempted defenses.

## Attack scenario (step by step)
1. Attacker identifies input field (e.g., user nickname) that is rendered without proper context-aware escaping
2. Attacker crafts payload considering output context (HTML attribute, JavaScript, URL protocol)
3. Attacker injects payload such as HTML event handler in attribute (" onload="alert(1)) or JavaScript protocol (javascript:alert(1))
4. When data is rendered in vulnerable context, parser interprets attacker-controlled syntax as executable code
5. Browser executes injected code with victim's session privileges, enabling account takeover or financial fraud
6. If CSP is present, attacker attempts bypass techniques or exploits CSP weaknesses in policy configuration

## Root cause
Insufficient context-aware output encoding combined with the assumption that single escaping method (e.g., escaping <>) is universally sufficient. Different output contexts (HTML body, attributes, JavaScript strings, URLs) have different parsing rules requiring context-specific encoding. Developers fail to recognize that the same user input requires different escaping depending on where it is rendered.

## Attacker mindset
Methodical exploitation through context analysis. Attackers recognize that naive escaping leaves gaps—if < and > are escaped but attribute delimiters are not, attributes become injection points. They test multiple contexts within the same page and exploit URL protocols (javascript:, data:) as alternative code execution paths. At higher levels, they assume code execution is possible and focus on damage maximization (account takeover, financial theft) rather than code injection itself.

## Defensive takeaways
- Implement context-aware output encoding: use different escaping functions for HTML body, attributes, JavaScript, URLs, and CSS contexts
- Apply the principle 'Never trust user input' consistently at all data boundaries
- Use whitelisting for URL protocols in href/src attributes to block javascript: and data: URIs
- Deploy Content Security Policy (CSP) with strict directives (no-inline-script, script-src, object-src) as a secondary defense layer
- Implement defense-in-depth: assume code injection can occur and add tertiary controls to minimize damage (CSRF tokens, transaction verification, account isolation)
- Validate input at source but rely on output encoding as primary XSS defense, not input validation alone
- Use security libraries with built-in context-aware encoding (e.g., OWASP ESAPI) rather than manual escaping
- Recognize CSP as mitigation, not prevention—budget for post-compromise defensive measures
- Test escaping across multiple contexts within single page (body, attributes, event handlers, URLs)

## Variant hunting
Search for similar multi-level defense analysis articles discussing: (1) context-specific encoding weaknesses in frameworks like Django, Rails, Laravel; (2) CSP bypass techniques using script gadgets or blob URIs; (3) Real-world examples of inadequate escaping in attribute contexts across popular CMSs; (4) JavaScript protocol exploitation in modern browsers; (5) Interaction between client-side template injection and XSS; (6) DOM-based XSS resulting from jQuery or vanilla JS manipulation of user input; (7) Event handler injection in SVG and MathML contexts; (8) CSS property injection through unsanitized style attributes.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204
- T1539
- T1005
- T1056

## Notes
This is an educational security article rather than a bug bounty submission. It provides foundational analysis of XSS defense tiers rather than reporting a specific vulnerability. The article's framework (three defensive levels) is pedagogically valuable for understanding XSS as a spectrum of concerns rather than a single attack type. The emphasis on context-aware escaping addresses a critical gap in developer understanding. No specific vulnerable code or program is analyzed, making this a reference material for researchers and developers rather than a bounty report.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
