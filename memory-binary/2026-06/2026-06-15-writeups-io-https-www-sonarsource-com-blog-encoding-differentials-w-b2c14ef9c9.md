# Encoding Differentials: Charset Mismatches Enabling XSS and Injection Attacks

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** General web applications (not specific program)
- **Bounty:** Not specified - Educational/Research
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), SQL Injection, Encoding Differential, Character Set Mismatch, Input Validation Bypass
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials occur when different layers of web applications interpret byte sequences under different character sets, allowing attackers to bypass input validation filters. Missing or mismatched charset declarations across the HTTP Content-Type header, HTML meta tags, and browser auto-detection enable attackers to inject malicious payloads like XSS or SQL injection that filters fail to detect.

## Attack scenario (step by step)
1. Attacker identifies a web application with missing charset attribute in Content-Type header
2. Browser falls back to auto-detection or meta tag charset, which differs from server's actual encoding
3. Attacker crafts payload exploiting the encoding differential (e.g., using UTF-16 or alternative encodings)
4. Input validation filter interprets payload under one charset while browser renders it under another
5. Malicious JavaScript or SQL executes because the two layers interpret the byte sequence differently
6. Attacker achieves XSS execution, session hijacking, or database compromise depending on context

## Root cause
Developers fail to explicitly declare character sets at all application layers (HTTP headers, HTML meta tags, database). Browsers perform lenient auto-detection when charset is missing, and different encoding schemes can represent the same malicious payload in ways that bypass charset-specific filters. The inconsistency between where encoding is declared and how it's validated creates exploitable gaps.

## Attacker mindset
Exploit framework and browser inconsistencies rather than application logic flaws. Leverage the fact that developers assume consistent encoding throughout the stack. Use character encoding knowledge to craft payloads that appear benign to one layer (filter) but malicious to another (browser renderer). This is a sophisticated technique requiring deep understanding of encoding mechanics and browser behavior.

## Defensive takeaways
- Always explicitly declare charset in Content-Type header (e.g., charset=utf-8)
- Include charset meta tag in HTML head as defense-in-depth
- Validate and filter payloads after decoding with explicitly specified charset
- Use consistent character encoding across all application layers: HTTP, HTML, database
- Avoid relying solely on Content-Type headers as browsers can override them
- Implement input validation that accounts for multiple possible encodings
- Use static analysis tools to detect charset misconfigurations before production
- Test security filters with payloads in alternative encodings (UTF-16, UTF-32, etc.)
- Apply output encoding appropriate to the context (HTML, JavaScript, URL, CSS)

## Variant hunting
['Test applications for missing charset declarations in all HTTP responses', 'Probe for charset-based XSS payloads using UTF-16, UTF-32, and Asian multibyte encodings', 'Attempt SQL injection payloads using alternative character sets to bypass WAF filters', 'Check for Byte-Order Mark (BOM) injection opportunities at document beginnings', 'Look for meta charset conflicts with Content-Type headers', 'Test polyglot payloads that are valid in multiple encodings', 'Investigate mXSS (mutated XSS) techniques leveraging encoding differentials', 'Fuzz charset values to find application-specific parsing inconsistencies']

## MITRE ATT&CK
- T1190
- T1203
- T1189
- T1566

## Notes
This is an educational writeup from SonarSource presented at TROOPERS24 conference. The vulnerability class (encoding differentials) represents a gap between encoding specification and validation, exploitable when developers don't explicitly manage charset at all layers. The key insight is that missing charset information forces browsers into auto-detection mode, which differs from how validation filters interpret the same bytes. This is not a traditional single vulnerability but a class of configuration weaknesses that enable multiple injection attacks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
