# Encoding Differentials: Charset Mismatches Enabling XSS and SQL Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** SonarSource Security Research
- **Bounty:** Not specified (educational/research)
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), SQL Injection, Encoding Differential, Charset Mismatch, Input Validation Bypass
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials occur when different layers of a web application interpret byte sequences under different character sets, allowing attackers to bypass input validation filters. Missing or mismatched charset declarations across HTTP headers, meta tags, and database layers create security gaps where malicious payloads like XSS or SQL injection can be smuggled past security controls. Browser charset auto-detection, when charset information is missing, compounds the vulnerability by allowing attackers to control how content is interpreted.

## Attack scenario (step by step)
1. Attacker observes that a web application's HTTP response lacks explicit charset declaration in the Content-Type header
2. Attacker crafts a payload containing bytes that are valid in one encoding but interpreted differently in another (e.g., UTF-8 vs UTF-16)
3. The payload bypasses server-side input validation filters designed for UTF-8, which fail to recognize the malicious sequence
4. Browser receives response and, lacking charset specification, triggers auto-detection or falls back to a different charset assumption
5. Browser interprets the bytes under the different charset, reconstructing the malicious payload into executable JavaScript or SQL
6. Payload executes in victim's browser (XSS) or is executed by database (SQL injection), compromising the application

## Root cause
Developers fail to explicitly declare character sets at every layer of the application stack (HTTP headers, HTML meta tags, database). Reliance on browser auto-detection and implicit charset assumptions creates conditions where different system components interpret the same byte sequence differently. The missing charset attribute in Content-Type headers forces browsers to guess encoding, introducing controllable ambiguity.

## Attacker mindset
Exploit the gap between encoding expectations at different layers. Attack filters and validation logic by using encoding transformations that survive server-side checks but are reconstructed as malicious code by the browser. Leverage non-strict browser behavior and auto-detection as a feature, not a bug, to smuggle payloads that appear benign in one encoding but dangerous in another.

## Defensive takeaways
- Always explicitly declare charset (charset=utf-8) in Content-Type HTTP headers; never rely on browser auto-detection
- Include charset declaration in HTML meta tags as a secondary defense layer
- Ensure consistent character encoding across all layers: HTTP headers, HTML documents, server-side processing, and database
- Implement input validation that accounts for multiple possible character encodings, not just the expected default
- Avoid relying on Content-Type headers alone, as they can be overridden or ignored by certain browsers or intermediaries
- Use static analysis tools to detect charset-related misconfigurations before deployment to production
- Test security controls with various character encodings to identify validation bypasses
- Set appropriate HTTP security headers (Content-Security-Policy) as defense-in-depth against encoding-based XSS

## Variant hunting
Search for: applications missing charset in Content-Type headers; input validation filters that only handle single encodings; discrepancies between declared and actual encoding across response layers; use of deprecated character encodings (windows-125x, GBK, Big5) that increase differential interpretation risks; partial HTML responses without meta charset declarations; database default character sets mismatched with application encoding; framework defaults that omit charset specification

## MITRE ATT&CK
- T1190
- T1203
- T1059

## Notes
Presented at TROOPERS24 conference. This is a sophisticated attack class requiring understanding of character encoding mechanics and browser behavior. The vulnerability is particularly dangerous because it bypasses common input validation approaches that assume single-encoding context. Byte-Order Mark (BOM) can override explicit charset declarations, adding another layer of complexity. The root issue stems from the disconnect between server intent and browser interpretation when encoding information is ambiguous or missing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
