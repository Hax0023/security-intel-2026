# XSS without Parentheses and Semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** PortSwigger Research
- **Bounty:** N/A - Research Publication
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, JavaScript Code Execution
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute arbitrary JavaScript and call functions without using parentheses or semicolons, bypassing common input sanitization filters. The method leverages the onerror handler combined with throw statements to pass arguments and execute code, with variations for different browser engines.

## Attack scenario (step by step)
1. Attacker identifies a target application filtering parentheses and semicolons in user input
2. Attacker crafts XSS payload using onerror assignment within throw statement: <script>{onerror=alert}throw 1337</script>
3. Alternative approach: Attacker embeds onerror assignment inside throw expression: <script>throw onerror=alert,'payload'</script>
4. For eval-based attacks on Chrome, attacker prefixes string with '=' to bypass 'Uncaught' prefix: <script>{onerror=eval}throw'=alert\x281337\x29'</script>
5. For Firefox compatibility, attacker creates Error object literal with required properties (lineNumber, columnNumber, fileName, message) to avoid 'uncaught exception' prefix
6. Payload executes arbitrary JavaScript code bypassing filter protections

## Root cause
Input sanitization filters that only blacklist parentheses and semicolons fail to account for alternative JavaScript syntax patterns using onerror handlers, throw statements, and block statements to achieve function execution without explicit parentheses or statement terminators.

## Attacker mindset
Security researchers and penetration testers discovering filter evasion techniques through understanding JavaScript's flexible syntax. Motivation is to demonstrate gaps in client-side sanitization and inform defensive measures. Approach involves methodical testing of language features and cross-browser behavior analysis.

## Defensive takeaways
- Implement server-side output encoding/escaping rather than relying on blacklist-based input filtering
- Use Content Security Policy (CSP) with strict directives (script-src 'none') to prevent inline script execution
- Apply comprehensive allowlist-based sanitization if client-side filtering is required, not character-based blacklists
- Understand that banning specific characters (parentheses, semicolons) is insufficient as JavaScript has multiple syntax patterns for code execution
- Consider DOM-based XSS context-aware sanitization libraries (DOMPurify) that understand JavaScript syntax variations
- Employ server-side validation and not just client-side filters which are easily bypassed
- Test XSS filters against polyglot and syntax-variation payloads

## Variant hunting
Researchers should investigate: alternative onerror/throw combinations with other event handlers (onload, oninput); variations using async/await syntax; combinations with template literals; use of eval alternatives (Function constructor without parentheses); browser-specific exception handling differences; combinations with HTML5 event attributes; nested block statements for further obfuscation; use of comma operators to chain expressions.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059.007 - Command and Scripting Interpreter: JavaScript
- T1047 - Windows Management Instrumentation
- T1204.001 - User Execution: Malicious Link

## Notes
This research demonstrates the danger of character-based input filtering as a primary security control. The technique's effectiveness varies by browser (Chrome vs Firefox), showing importance of understanding browser-specific JavaScript exception handling. The discovery process involved methodical syntax exploration and using browser developer tools (Hackability Inspector) to reverse-engineer object properties.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
