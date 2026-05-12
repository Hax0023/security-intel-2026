# WAF Bypass via CRLF Injection and DOM-XSS via Unicode Surrogate Pair Handling in CSS Selectors

## Metadata
- **Source:** HackerOne
- **Report:** 2921905 | https://hackerone.com/reports/2921905
- **Submitted:** 2025-01-04
- **Reporter:** clubbable
- **Program:** Doppler
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Web Application Firewall Bypass, CRLF Injection, DOM-based Cross-Site Scripting (DOM-XSS), Improper Unicode Character Handling, CSS Selector Injection
- **CVEs:** None
- **Category:** web-api

## Summary
The vulnerability comprises two interconnected issues: a CloudFlare WAF bypass using CRLF injection and newline characters to smuggle malicious payloads, and a DOM-XSS vulnerability in the ce.escapeSelector function due to incomplete handling of Unicode surrogate pairs. An attacker can bypass the WAF and then exploit the surrogate pair handling to inject JavaScript through CSS selectors.

## Attack scenario
1. Attacker crafts a payload containing CRLF characters and newlines to bypass CloudFlare's WAF detection rules: %22%3E%0D%0A%0D%0A%3Cx%20%27=%22foo%22%3E%3Cx%20foo=%27%3E%3Cimg%20src=x%20onerror=javascript:alert(`cloudfrontbypass`)//%27%3E
2. The WAF fails to detect the injection because it doesn't properly normalize or detect CRLF-based obfuscation techniques
3. Attacker then identifies that ce.escapeSelector() function uses charCodeAt() which doesn't properly handle Unicode surrogate pairs outside the BMP
4. Attacker crafts a malicious selector containing surrogate pairs like div[id="\uD83D\uDC4D;alert(1)//"] where the surrogate pair escaping is incomplete
5. The incomplete escaping allows the injected JavaScript payload to be interpreted as valid code rather than escaped text
6. JavaScript executes in the DOM context, allowing data exfiltration or session hijacking

## Root cause
Two separate but chained vulnerabilities: (1) CloudFlare WAF lacks proper CRLF normalization and newline filtering in query parameters, and (2) The ce.escapeSelector function uses charCodeAt() which returns individual 16-bit code units rather than the full Unicode codepoint, causing surrogate pairs (characters outside BMP) to be improperly escaped, allowing them to break out of the selector context

## Attacker mindset
An attacker researching WAF evasion techniques would test CRLF injection and character encoding methods. Upon discovering the WAF bypass, they would then probe the application's JavaScript for DOM-based vulnerabilities, eventually identifying the selector escaping weakness as a second exploitation vector. The combination allows both perimeter security bypass and internal application exploitation.

## Defensive takeaways
- Implement proper Unicode normalization (NFC/NFD) and handle all codepoints correctly, not just BMP characters
- Use codePointAt() instead of charCodeAt() for Unicode-safe string processing in escape functions
- Ensure WAF rules include CRLF normalization and filtering in all input vectors, not just common injection points
- Validate and escape selectors at the API boundary, not just in client-side JavaScript
- Use built-in DOM manipulation APIs (querySelector with proper escaping) or templating engines rather than string concatenation for selector construction
- Implement Content Security Policy (CSP) to mitigate DOM-XSS impact even if escaping fails
- Perform regular security audits of custom escaping and encoding functions against modern Unicode attack vectors

## Variant hunting
Search for other instances of charCodeAt() used in security-critical contexts (escaping, sanitization, validation). Test all WAF bypass via HTTP protocol smuggling (CRLF, LF-only, mixed case headers). Examine other jQuery or DOM manipulation functions that accept user input. Test other Unicode plane characters and edge cases in selector handling. Investigate if similar escaping issues exist in other parts of the codebase (HTML escaping, attribute escaping, etc.).

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1047 - Windows Management Instrumentation
- T1598 - Phishing for Information
- T1566 - Phishing
- T1203 - Exploitation for Client Execution

## Notes
The report demonstrates chained vulnerability exploitation: WAF bypass enables delivery of payload that would normally be blocked, then DOM-XSS in selector handling provides execution. The Unicode surrogate pair issue is particularly subtle as developers often assume charCodeAt() is sufficient for escaping. This affects any code processing selectors with user input. The CRLF bypass suggests the WAF may not be normalizing HTTP message boundaries correctly, a separate infrastructure issue.

## Full report
<details><summary>Expand</summary>

hello,

WAF :
 doppler uses cloudfare firewall to prevent unwanted malicous injections 
"https://share.doppler.com/ext/jquery/dist/jquery.min.js?c=%22%3Cscript%3Ealert(%27XSS%27)%3C/script%3E%22" by accessing the endpoint you'll get to know that!

But I found that this code "">%0D%0A%0D%0A<x '="foo"><x foo='><img src=x onerror=javascript:alert(`cloudfrontbypass`)//'>" bypass the cloud fare !
"https://share.doppler.com/ext/jquery/dist/jquery.min.js?c=%22%3E%0D%0A%0D%0A%3Cx%20%27=%22foo%22%3E%3Cx%20foo=%27%3E%3Cimg%20src=x%20onerror=javascript:alert(`cloudfrontbypass`)//%27%3E"
 it doesn't initiate the xss but I can able to bypass the WAF bypass!

DOM-XSS:
implementation of ce.escapeSelector is indeed vulnerable to DOM-based XSS due to its incomplete handling of Unicode characters, specifically surrogate pairs.

Here's why:

Surrogate Pairs:
Unicode uses surrogate pairs to represent characters outside the Basic Multilingual Plane (BMP).
A surrogate pair consists of two 16-bit code units that together represent a single character.
Incomplete Escaping:
The charCodeAt function returns the code unit at a specific index.
When dealing with a surrogate pair, charCodeAt will only return the code unit of the first or second surrogate, not the combined character.
This leads to incorrect escaping, as the hexadecimal representation of a single surrogate does not accurately represent the intended character.
XSS Exploitation:
An attacker could craft a malicious selector that includes a surrogate pair within it.
The incomplete escaping would allow the surrogate pair to be interpreted as part of the selector in unexpected ways.
This could potentially:
Manipulate the target of the selector, selecting unintended elements.
Inject JavaScript code into the selector, leading to arbitrary code execution within the context of the web page.
```
'div[id="\\uD83D\\uDC4D;alert(1)//"]'
```

## Impact

attackers can inject malicious code that steals sensitive user information like login credentials, personal details, and financial data.

</details>

---
*Analysed by Claude on 2026-05-12*
