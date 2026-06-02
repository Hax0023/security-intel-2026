# PayPal Demo Node.js Code Injection via Dust.js Template Engine

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Remote Code Execution (RCE), Code Injection, Template Injection, Unsafe use of eval(), Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
A critical RCE vulnerability was discovered in demo.paypal.com where user-supplied input passed unsafely to Dust.js template engine's 'if' helper, which uses JavaScript eval() for expression evaluation. By exploiting type confusion in Node.js query parameter parsing (converting strings to arrays), the attacker bypassed HTML character encoding protections to achieve arbitrary code execution.

## Attack scenario (step by step)
1. Attacker performs parameter fuzzing on demo.paypal.com and observes different error responses for backslash (\) and newline (%0a) characters
2. Attacker identifies Dust.js templating engine from error messages and analyzes its source code, discovering unsafe eval() in 'if' helpers
3. Attacker notes that dangerous characters are HTML-encoded (quotes become &#39;), preventing direct string breakout
4. Attacker exploits Node.js query parameter parsing by sending array syntax (device[]=value) instead of strings, bypassing the escaping function
5. Attacker crafts payload: ?device[]=x&device[]=y'-require('child_process').exec('curl...') -' which concatenates into unescaped JavaScript code
6. Attacker executes arbitrary system commands (exfil /etc/passwd) with application privileges

## Root cause
Multiple compounding issues: (1) Use of eval() for template expression evaluation, (2) HTML entity encoding that only works on strings, not arrays, (3) Lack of type validation before passing user input to escaping functions, (4) No input validation or sanitization before template processing

## Attacker mindset
Systematic fuzzer discovers unexpected application behavior, performs reconnaissance through error messages and source code analysis, identifies type confusion in parameter handling as bypass technique, and leverages language-specific features (Node.js array parsing) to circumvent security controls.

## Defensive takeaways
- Never use eval() for expression evaluation; use safe expression parsers or sandboxed environments
- Validate and normalize input types before any processing or encoding
- Apply encoding/escaping consistently regardless of input type (string, array, object)
- Implement strict Content Security Policy (CSP) to prevent code injection
- Use template engines with sandboxed/safe evaluation by default
- Perform security review of dependencies (Dust.js, qs module) and their known vulnerabilities
- Implement input validation whitelist rather than blacklist
- Use security linters to detect eval() usage patterns

## Variant hunting
["Search for other uses of Dust.js 'if' helpers in legacy PayPal applications", 'Test array parameter handling ([]=) against other template injection points', 'Investigate other Node.js applications using qs module with unsafe template engines', 'Look for similar type confusion vulnerabilities in query parameter parsing', "Check for eval() usage in other template helpers (not just 'if')", 'Test other dangerous characters that might bypass entity encoding on non-string types', 'Review other PayPal subdomains (staging, sandbox) for same vulnerable pattern']

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1020
- T1083

## Notes
This is a landmark bug bounty finding that demonstrates the danger of combining multiple seemingly minor flaws: unsafe eval() + insufficient escaping + type confusion. The attacker's systematic approach (fuzzing → error analysis → source review → bypass engineering) is exemplary. The vulnerability class (template injection via type confusion) has become a recurring pattern in Node.js applications. PayPal's response with $10K bounty suggests they took it seriously. The writeup is from August 2016, highlighting how legacy template engines remain dangerous years after discovery.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
