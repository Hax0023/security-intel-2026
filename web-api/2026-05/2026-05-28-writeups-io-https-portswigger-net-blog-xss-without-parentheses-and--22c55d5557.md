# XSS without parentheses and semi-colons

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** PortSwigger Research
- **Bounty:** N/A - Research/Educational
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Filter Bypass, JavaScript Injection
- **Category:** web-api
- **Writeup:** https://portswigger.net/blog/xss-without-parentheses-and-semi-colons

## Summary
A technique to execute arbitrary JavaScript without using parentheses or semi-colons by leveraging the onerror handler combined with throw statements. The method uses object literals with Error prototypes to bypass character-based filters that attempt to prevent XSS attacks.

## Attack scenario (step by step)
1. Attacker identifies a web application filtering parentheses and semi-colons in user input
2. Attacker crafts XSS payload using onerror assignment within throw statement: <script>{onerror=eval}throw'=alert\x281337\x29'</script>
3. Input validation allows the payload through because it contains no parentheses or semi-colons
4. Browser executes the script, setting onerror handler to eval function
5. Throw statement creates exception with malicious string, triggering onerror handler
6. Eval function executes the exception message as JavaScript code, executing arbitrary commands

## Root cause
Filter-based input validation relying on blacklisting specific characters (parentheses, semi-colons) rather than whitelisting safe constructs or properly sanitizing JavaScript contexts. Developers assumed these characters were necessary for function execution.

## Attacker mindset
Security researchers discovering that character-level filters are insufficient for preventing code execution. The attacker views exception handling mechanisms as alternative execution paths when traditional methods are blocked, demonstrating creative abuse of language features.

## Defensive takeaways
- Avoid character-based blacklist filtering for XSS prevention; use context-aware output encoding instead
- Implement Content Security Policy (CSP) to restrict script execution and eval usage
- Use allowlist validation rather than blacklist filtering for user input
- Encode output based on context (HTML, JavaScript, URL, CSS)
- Disable or restrict eval() and related dynamic code execution functions
- Conduct thorough security testing against creative bypass techniques, not just common patterns
- Apply defense-in-depth with multiple security layers

## Variant hunting
Search for alternative exception handling mechanisms (Promise rejection handlers, async/await error handlers), other statement types that bypass semicolon requirements (if/else blocks, loops), alternative function invocation methods (tagged templates, Proxy handlers), and browser-specific exception prefixing behaviors across different environments.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1203 - Exploitation for Client Execution

## Notes
This is an educational security research publication demonstrating filter bypass techniques. The technique exploits fundamental JavaScript language features (onerror handlers, throw statements, object literals) that cannot be disabled without breaking legitimate functionality. Firefox and Chrome handle exception formatting differently, requiring context-specific payloads. The research highlights why security controls must operate at semantic/semantic levels rather than purely syntactic filtering.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
