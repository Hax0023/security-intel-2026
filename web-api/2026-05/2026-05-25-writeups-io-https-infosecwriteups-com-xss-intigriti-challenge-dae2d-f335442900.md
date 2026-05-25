# XSS Intigriti Challenge 0523 - Reflect API Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Intigriti Bug Bounty Platform
- **Bounty:** Challenge-based (specific amount not disclosed in writeup)
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Insufficient Input Validation, Blacklist Bypass
- **Category:** web-api
- **Writeup:** https://infosecwriteups.com/xss-intigriti-challenge-dae2dba1cb4c

## Summary
A DOM-based XSS vulnerability in the Intigriti challenge 0523 was bypassed using the Reflect API to circumvent keyword blacklist filters. The challenge accepted user input in a 'xss' parameter that was dynamically loaded as a data URI script, but employed character whitelist and keyword blacklist filtering. The attacker used Reflect.set() to indirectly access and execute forbidden functions without using blacklisted keywords.

## Attack scenario (step by step)
1. Attacker identifies the challenge requires executing alert(document.domain) with no user interaction
2. Attacker analyzes the three validation constraints: length <100, character whitelist [a-zA-Z,'+\.()], and keyword blacklist of dangerous functions
3. Attacker notes that 'Reflect' is not in the blacklist despite being a powerful API
4. Attacker crafts payload using Reflect.set() to modify global properties and chain function access without using forbidden keywords
5. Attacker leverages the ECMA-262 specification hint to discover that Reflect methods can be used as property accessors/setters
6. Attacker submits the crafted Reflect-based payload which passes all filters and executes arbitrary JavaScript

## Root cause
The security filter relied on a blacklist approach for dangerous keywords while allowing the Reflect API, which provides indirect access to the same capabilities. The whitelist character restriction and length limit were insufficient to prevent sophisticated gadget chains using legitimate JavaScript APIs. The developers failed to anticipate meta-programming techniques available through standard ECMAScript features.

## Attacker mindset
The attacker understood that blacklist-based security is inherently flawed and sought legitimate APIs that could achieve the same outcome. Reading the ECMA-262 documentation hint led them to discover Reflect as an alternative pathway. The attacker recognized that character whitelisting could still construct complex expressions through method chaining and exploited the gap between what was blocked and what was allowed.

## Defensive takeaways
- Avoid blacklist-based security filters; use allowlist approaches for code/script execution
- Recognize that meta-programming APIs (Reflect, Proxy, etc.) can bypass traditional restrictions
- Implement content security policies (CSP) to prevent inline script execution
- Use static analysis tools to identify gadget chains in allowed APIs
- Consider disallowing dynamic script creation entirely (data: URIs, script.src manipulation)
- Apply defense-in-depth: combine multiple security layers rather than relying on a single filter
- Conduct threat modeling specifically for advanced JavaScript features and ECMAScript specifications
- Implement strict input validation with proven-safe parsing rather than character whitelisting

## Variant hunting
['Test if Proxy object is accessible and can intercept property access to reach blacklisted functions', 'Investigate other ES6+ features not mentioned in blacklist: Symbols, Generators, async/await chains', 'Check if template literals combined with whitelisted characters can construct forbidden words through computed properties', 'Analyze if chained method calls on Array.prototype or Object.prototype can access restricted APIs', 'Test if destructuring or spread operator combinations can bypass the character whitelist', 'Examine if Function.prototype methods (bind, call, apply alternatives) can be accessed through whitelisted APIs', 'Investigate eval alternatives: Function constructor accessed through indirect means, or indirect code execution via setTimeout bypasses']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (JavaScript)
- T1140 - Deobfuscate/Decode Files or Information

## Notes
This challenge exemplifies why security researchers recommend whitelisting over blacklisting. The hint about ECMA-262 was crucial in directing attention toward standardized JavaScript features that could bypass restrictions. The Reflect API bypass is particularly instructive because Reflect is a legitimate, documented API that provides indirect access to object property manipulation—exactly what many dangerous operations ultimately require. Real-world applications should avoid dynamic script creation entirely when possible, or if necessary, implement multiple validation layers and leverage CSP headers.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
