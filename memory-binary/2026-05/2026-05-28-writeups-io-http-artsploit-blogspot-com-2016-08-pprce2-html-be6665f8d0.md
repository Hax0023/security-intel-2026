# PayPal Node.js Code Injection via Dust.js Template Engine (RCE)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Code Injection, Remote Code Execution, Template Injection, Unsafe use of eval(), Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
PayPal's demo application used Dust.js templating engine which internally evaluated user-supplied input through JavaScript eval() in the 'if' helper function. By exploiting type confusion through array parameters and bypassing character sanitization, an attacker could inject arbitrary JavaScript code and achieve remote code execution on the server.

## Attack scenario (step by step)
1. Attacker performs parameter fuzzing and observes different error responses for backslash and newline characters, indicating server-side template processing
2. Attacker identifies Dust.js templating engine through error messages and recognizes it uses eval() for 'if' helper expression evaluation
3. Attacker discovers character sanitization replaces single and double quotes with HTML entities to prevent string escaping
4. Attacker leverages Node.js qs module behavior to convert parameter to array type (device[]=value) which bypasses string-based sanitization
5. Attacker crafts payload with array parameter containing quote character and JavaScript payload: device[]=x&device[]=y'-require('child_process').exec('curl...')-'
6. Server evaluates the injected code within eval(), executing arbitrary shell commands with application privileges

## Root cause
Multiple security failures: (1) Use of unsafe eval() for template expression evaluation, (2) Incomplete input sanitization that only handles string type inputs but not arrays, (3) No server-side template injection protections, (4) Trust in client parameter type assumptions without validation

## Attacker mindset
Methodical fuzzer who performs comprehensive parameter testing to identify error conditions and information disclosure. Investigates error messages to understand technology stack, reviews open-source library code to find eval-based vulnerabilities, and exploits type system quirks (array vs string) to bypass security controls.

## Defensive takeaways
- Never use eval() or equivalent dynamic code evaluation on user input, even with sanitization
- Implement input validation and sanitization at type level - validate input types explicitly before processing
- Use safe templating engines that don't eval expressions (use expression parsers instead)
- Apply defense in depth: sanitize at multiple layers including type validation
- Regularly audit third-party library versions for known vulnerabilities
- Implement strict Content Security Policy and disable JavaScript eval where possible
- Perform negative testing with various parameter formats (arrays, nested objects, type variations)

## Variant hunting
['Search for other uses of Dust.js or similar templating engines with eval-based helpers in PayPal applications', 'Test other templating engines (EJS, Jade, Handlebars) for similar eval-based vulnerabilities', 'Fuzz other parameters on PayPal endpoints for type confusion and template injection patterns', 'Check if similar qs module type confusion affects other Node.js applications with sanitization bypasses', 'Hunt for other eval() calls in Node.js backend code that may have incomplete sanitization', 'Test array parameter handling on other endpoints that process user input through templating']

## MITRE ATT&CK
- T1190
- T1059
- T1203
- T1593

## Notes
This is a textbook example of defense in depth failure. The application attempted to block dangerous characters but failed to account for type polymorphism in JavaScript. The qs module's automatic array parsing combined with eval-based templating created a critical vulnerability. The researcher's systematic fuzzing approach and knowledge of Node.js internals were key to discovering and exploiting this issue. Published in August 2016.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
