# Encoding Differentials: Charset Mismatches as XSS/Injection Vectors

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** General security research/SonarSource
- **Bounty:** N/A - Educational writeup
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), SQL Injection, Charset Confusion, Encoding Differential, Input Validation Bypass
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials occur when different layers of web applications interpret byte sequences under different character sets, allowing attackers to bypass input validation filters. Missing or mismatched charset declarations in HTTP headers, meta tags, and database configurations create security gaps where malicious payloads like XSS and SQL injection can be smuggled past security controls.

## Attack scenario (step by step)
1. Attacker identifies that server omits charset attribute from Content-Type header
2. Browser falls back to auto-detection, potentially inferring different charset than intended (e.g., UTF-16 instead of UTF-8)
3. Attacker crafts payload that is valid in the auto-detected charset but bypasses server-side filters designed for UTF-8
4. Browser interprets bytes under the wrong encoding, rendering the malicious payload executable (XSS) or interpretable (SQL injection)
5. Input validation filters that operate under UTF-8 assumption fail to detect dangerous sequences encoded differently
6. Payload executes client-side or is processed unsafely server-side, compromising application security

## Root cause
Inconsistent charset specification across three browser resolution mechanisms (BOM > Content-Type header > meta tag) combined with browser auto-detection fallback behavior and server-side filters assuming single encoding without explicit declaration at all layers

## Attacker mindset
Exploit the gap between how developers assume browsers will interpret content and how browsers actually handle missing encoding information. Use non-standard encodings to encode payloads that appear safe under one charset but execute differently under another. Leverage browser's lenient error recovery to bypass validation.

## Defensive takeaways
- Always explicitly declare charset=utf-8 in Content-Type header for all HTTP responses
- Set charset in meta tags as secondary defense, not primary
- Use Byte-Order Mark (BOM) as tertiary defense for UTF-8/UTF-16 responses
- Implement server-side input validation that is encoding-aware and normalizes input before filtering
- Use allowlist validation rather than blocklist patterns vulnerable to encoding tricks
- Configure database character set explicitly to match application encoding
- Test XSS and injection filters with various character encodings (UTF-16, ISO-8859-1, GBK, etc.)
- Disable browser auto-detection where possible via X-Content-Type-Options: nosniff header
- Use static analysis tools to detect missing or mismatched charset configurations
- Perform security testing with charset-fuzzing against input filters

## Variant hunting
Look for: (1) API endpoints returning JSON/XML without charset declaration, (2) Legacy applications using HTTP/1.0 without Content-Type headers, (3) Partial HTML responses (fragments) missing meta charset, (4) Form submissions with enctype but missing accept-charset, (5) Double UTF-8 encoding scenarios, (6) Applications using iconv or similar functions with mismatched charset parameters, (7) Database connections using different charset than application, (8) Reverse proxies or WAF rules validating UTF-8 only while browser interprets UTF-16

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1071 - Application Layer Protocol
- T1189 - Drive-by Compromise
- T1204.001 - User Execution: Malicious Link
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing for Information: Spearphishing Link

## Notes
This writeup was presented at TROOPERS24 conference. The attack exploits browser specifications' multi-stage charset resolution mechanism. The vulnerability exists at the intersection of browser behavior, web server configuration, and input validation assumptions. Modern static analysis (Sonar) can detect these misconfigurations. The technique is particularly effective because it exploits standardized lenient error recovery behavior in browsers, making it difficult to patch universally.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
