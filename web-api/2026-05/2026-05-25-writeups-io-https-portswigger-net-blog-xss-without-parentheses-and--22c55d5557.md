# XSS without Parentheses and Semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** PortSwigger Research
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, WAF Evasion
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
Researcher discovered a technique to execute JavaScript and call functions without using parentheses or semicolons by leveraging the onerror handler combined with throw statements. The technique works across different browsers by using creative syntax variations including block statements, expression syntax, and Firefox-specific Error object properties to bypass input filters.

## Attack scenario (step by step)
1. Attacker identifies a web application that filters parentheses and semicolons in user input
2. Attacker crafts a payload using the onerror/throw technique: <script>{onerror=alert}throw 1337</script>
3. The payload bypasses the filter because it contains no parentheses or semicolons
4. JavaScript parser executes the script, setting the onerror handler to the alert function
5. The throw statement triggers the onerror handler, passing 1337 as the argument
6. The alert function executes with attacker-controlled data, demonstrating code execution

## Root cause
Input filters that only blacklist parentheses and semicolons fail to account for alternative JavaScript syntax patterns. The onerror event handler provides a legitimate mechanism to execute functions with arguments passed via exception objects, circumventing traditional function call syntax restrictions.

## Attacker mindset
An attacker recognizes that security filters often target specific syntax patterns rather than underlying functionality. By understanding how exception handlers work and alternative expression syntax, they identify creative ways to achieve the same execution goals using allowed characters. This reflects a deeper understanding of JavaScript semantics beyond surface-level syntax.

## Defensive takeaways
- Avoid blacklist-based input validation; use whitelist approaches for dangerous contexts
- Understand that parentheses and semicolons are not the only way to execute code in JavaScript
- Implement Content Security Policy (CSP) to restrict inline script execution entirely
- Consider that event handlers like onerror present execution vectors even without function call syntax
- Apply context-aware output encoding rather than relying on character-level filters
- Test filter bypasses by studying alternative JavaScript syntax patterns
- Use a Web Application Firewall with semantic understanding of code, not just pattern matching

## Variant hunting
Security researchers should investigate: alternative exception handlers (onload, oninput), other throw mechanisms, similar patterns in eval-based injection chains, error object property manipulation across browsers, variations using template literals or spread operators, and whether other browsers handle error message prefixes differently than Chrome and Firefox.

## MITRE ATT&CK
- T1190
- T1567

## Notes
This research demonstrates the principle that filter evasion requires understanding both what you're filtering and why. The technique leverages legitimate JavaScript features in unintended ways. Browser-specific behavior differences (Chrome's 'Uncaught' prefix vs Firefox's 'uncaught exception') required different payloads, showing importance of cross-browser testing. Published May 2019, updated March 2020.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
