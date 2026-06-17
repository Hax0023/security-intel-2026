# Encoding Differentials: Charset-Based Security Gaps in Web Applications

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** SonarSource Research
- **Bounty:** N/A - Research/Educational
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), SQL Injection, Charset Mismatch/Encoding Differential, Input Validation Bypass, Character Encoding Confusion
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials occur when different layers of a web application interpret byte sequences under different character sets, allowing attackers to smuggle malicious payloads past filters. Missing or mismatched charset declarations across browsers, servers, and databases create security gaps that enable XSS and SQL injection attacks through character encoding confusion.

## Attack scenario (step by step)
1. Attacker identifies a web application missing charset specification in Content-Type headers
2. Browser auto-detects or assumes an alternative character encoding (e.g., UTF-16, GBK, ISO-8859-1)
3. Attacker crafts payload using multi-byte or encoding-specific characters that bypass server-side filters designed for UTF-8
4. Server-side validation sees benign bytes in UTF-8 interpretation while browser renders malicious JavaScript in alternate encoding
5. XSS payload executes in victim's browser due to encoding differential between validation and rendering layers
6. Alternative attack vector: SQL injection bypasses occur when database uses different charset than application validation layer

## Root cause
Browsers implement lenient charset auto-detection when explicit charset is missing from HTTP headers or meta tags, allowing multiple valid interpretations of the same byte sequence. Combined with server-side validation that assumes a single encoding, this creates a semantic gap where payloads pass filters but execute as malicious code.

## Attacker mindset
Exploit the inconsistency between how different application layers interpret byte sequences by leveraging browser charset auto-detection and multi-byte encoding quirks. Target applications with inconsistent charset declaration to craft payloads that appear benign during validation but execute maliciously in the browser's interpreted encoding.

## Defensive takeaways
- Explicitly declare charset attribute in Content-Type headers (e.g., charset=utf-8) on all responses
- Include <meta charset> tags in HTML documents for defense-in-depth
- Validate and sanitize input at every layer using consistent, explicitly-defined character encoding
- Avoid relying solely on Content-Type headers which can be overridden by browser auto-detection
- Implement consistent charset handling across browser, server, and database layers
- Use static analysis tools to detect charset misconfigurations before production deployment
- Test applications with multiple character encodings to identify encoding differential vulnerabilities
- Prefer UTF-8 consistently across all application layers to reduce encoding confusion

## Variant hunting
Search for: applications missing charset in Content-Type headers; inconsistent character encoding between frontend and backend validation; use of auto-detecting encodings; multi-byte character handling in input filters; applications supporting legacy charsets (GBK, Big5, ISO-8859-x); mXSS (mutated XSS) vectors through encoding confusion; database encoding mismatches with application layer

## MITRE ATT&CK
- T1190
- T1053
- T1083
- T1059

## Notes
This research highlights a fundamental browser compatibility feature (charset auto-detection) that conflicts with security assumptions in server-side validation. The vulnerability class is subtle because it relies on semantic differences rather than implementation bugs. Presented at TROOPERS24 conference. The missing charset attribute appears minor but represents a critical security control failure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
