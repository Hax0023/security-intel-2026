# XSS without parentheses and semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** PortSwigger Research / General Web Security
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, JavaScript Code Execution
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique discovered to execute JavaScript functions without using parentheses or semi-colons, exploiting the onerror handler and throw statement. This bypasses filters that block parentheses and semi-colons by leveraging JavaScript exception handling and object literal syntax.

## Attack scenario (step by step)
1. Attacker identifies a web application filtering parentheses and semi-colons in user input
2. Attacker crafts payload using onerror handler with throw statement: <script>{onerror=eval}throw'=alert\x281337\x29'</script>
3. JavaScript engine creates exception, triggering onerror handler without requiring parentheses
4. Attacker uses object literals with Error prototype properties to bypass Firefox exception prefixing: {lineNumber:1,columnNumber:1,fileName:1,message:'alert\x281\x29'}
5. Payload executes arbitrary JavaScript code (alert, data exfiltration, etc.) despite filter restrictions
6. Application vulnerable to XSS due to incomplete input validation strategy

## Root cause
Incomplete input validation that blocks specific characters (parentheses, semi-colons) but fails to account for alternative JavaScript execution patterns using exception handlers, throw statements, and object literals. The onerror handler mechanism provides an implicit function call without requiring parenthesis syntax.

## Attacker mindset
Bypass-focused: searching for alternative syntax and language features that achieve the same execution goal. Understanding JavaScript semantics deeply to find edge cases where normal restrictions don't apply. Experimental approach—testing exception handling behavior across browsers to identify differences that can be weaponized.

## Defensive takeaways
- Blocklist-based input filtering is insufficient; use allowlist validation with strict encoding rules
- Understand that blocking specific characters doesn't prevent code execution—restrict dangerous functions (eval, onerror assignments) contextually
- Apply Content Security Policy (CSP) to prevent inline script execution entirely
- Implement server-side template escaping and client-side DOM-based XSS protections
- Recognize that JavaScript has multiple code execution primitives beyond function calls—test alternative patterns
- Test filters against browser-specific behaviors and exception handling edge cases
- Use output encoding appropriate to context (HTML, JavaScript, URL encoding) rather than input filtering alone

## Variant hunting
Search for similar bypass techniques involving: (1) other error handlers (onload, onerror variations), (2) template literals and expression evaluation without parentheses, (3) Proxy objects and implicit function invocation, (4) HTML5 event handler attribute bypasses, (5) Service Worker and Web Worker message passing without traditional function syntax, (6) Browser-specific exception handling differences in other environments (Safari, Edge)

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a foundational XSS bypass research post rather than a traditional bug report. The techniques described represent general JavaScript language features that can be chained to circumvent insufficient input validation. The Firefox vs Chrome exception prefix differences highlight the importance of testing across browsers. The research emphasizes that security through character blacklisting is fundamentally flawed—attackers will exploit legitimate language semantics.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
