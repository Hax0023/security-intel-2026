# PayPal demo.paypal.com Node.js Code Injection (RCE) via Dust.js Template Engine

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** PayPal
- **Bounty:** $10,000
- **Severity:** critical
- **Vuln types:** Code Injection, Remote Code Execution, Template Injection, Unsafe use of eval(), Type Confusion
- **Category:** memory-binary
- **Writeup:** http://artsploit.blogspot.com/2016/08/pprce2.html

## Summary
A Node.js application on demo.paypal.com used the Dust.js templating engine which internally used JavaScript eval() for evaluating 'if' helper expressions. By exploiting type confusion through array parameters that bypassed string sanitization, an attacker could inject arbitrary JavaScript code and achieve remote code execution.

## Attack scenario (step by step)
1. Attacker performs parameter fuzzing and notices different error responses for backslash (\) and newline (%0a) characters
2. Through error messages, attacker identifies the use of Dust.js templating engine with 'if' helpers
3. Attacker discovers that Dust.js uses eval() to evaluate complex expressions in 'if' conditionals
4. Attacker notes that single and double quotes are HTML-encoded by the application's sanitization function
5. Attacker exploits type confusion by sending array parameters (device[]=value) which bypass the string sanitization since the escape function only operates on strings, not arrays
6. Attacker crafts a payload that injects JavaScript code to execute system commands (curl with cat /etc/passwd) using require('child_process').exec()

## Root cause
The vulnerability stems from multiple layers of security failures: (1) Use of eval() in Dust.js 'if' helper for expression evaluation, (2) Incomplete input sanitization that only escaped quotes for string types but didn't validate parameter types, (3) Node.js qs module parsing array syntax which bypassed type assumptions in the sanitization code, (4) Lack of parameterized/safe templating mechanisms

## Attacker mindset
Methodical fuzzer who discovered the vulnerability through systematic parameter testing, recognized the framework from error messages, analyzed open-source library code on GitHub, understood Node.js type handling and qs parsing behavior, then creatively exploited type confusion to bypass insufficient sanitization. The attacker demonstrated deep knowledge of both common web vulnerabilities and Node.js-specific quirks.

## Defensive takeaways
- Never use eval() or similar dynamic code execution functions with user input, regardless of sanitization attempts
- Sanitize all input based on expected type before processing, not just string escaping; validate parameter types explicitly
- Use safe template engines that don't allow arbitrary code execution or use strict sandboxing
- When using expression evaluators, use safe libraries like jexl or expression-evaluator instead of eval()
- Apply defense in depth: sanitize at multiple layers (type validation, encoding, templating restrictions)
- Keep dependencies updated; the old version of Dust.js had this unsafe 'if' helper implementation
- Disable or heavily restrict access to require() and child_process modules in templating contexts
- Use security linters and SAST tools to flag eval() usage patterns
- Implement Content Security Policy and runtime security monitoring to detect exec() calls

## Variant hunting
Search for other applications using old Dust.js versions with 'if' helpers. Look for similar eval()-based template engines (Jade, EJS with eval, Handlebars with custom helpers). Hunt for other Node.js applications that parse array parameters and use incomplete sanitization. Check for other frameworks that escape strings but don't validate parameter types before escaping. Test for similar type confusion vulnerabilities in query parameter parsing across different frameworks.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1203 - Exploitation for Client Execution
- T1598 - Phishing for Information (reconnaissance phase)

## Notes
This is a particularly elegant vulnerability that exploits the intersection of multiple security issues. The attacker leveraged deep understanding of Node.js internals (qs parsing creating arrays) and open-source library internals (Dust.js eval usage) to craft a minimal bypass of insufficient sanitization. The $10,000 bounty reflects PayPal's appreciation for responsibly disclosed RCE on their infrastructure. Published August 2016, demonstrating that even well-resourced companies can miss these kinds of contextual type-confusion vulnerabilities. The blogpost is from Michael Stepankin (artsploit), a respected security researcher known for similar findings.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
