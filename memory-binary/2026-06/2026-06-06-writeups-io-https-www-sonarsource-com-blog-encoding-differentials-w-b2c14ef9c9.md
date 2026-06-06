# Encoding Differentials: Character Set Mismatches Leading to XSS

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** SonarSource Research
- **Bounty:** Not specified - Research/Educational publication
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Charset Confusion, Encoding Differential, Character Set Mismatch
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials occur when different layers of a web application interpret the same byte sequence under different character sets, allowing attackers to bypass input validation filters. When HTTP responses lack explicit charset declarations in Content-Type headers, browsers fall back to auto-detection or meta tags, enabling attackers to inject malicious payloads such as XSS or SQL injection that evade security filters designed for a specific encoding.

## Attack scenario (step by step)
1. Attacker identifies a web application that serves HTML responses without explicit charset in Content-Type header
2. Attacker crafts malicious payload that appears safe under UTF-8 (the assumed encoding) but contains executable JavaScript when decoded as an alternative charset (e.g., UTF-16, ISO-8859-x)
3. Browser receives response without charset specification and attempts auto-detection
4. Browser interprets the bytes using a different character encoding than what input validation filters expected
5. Input validation filters pass the payload because they analyzed it under UTF-8 encoding
6. Browser renders the payload using alternative charset, successfully executing the injected JavaScript

## Root cause
Failure to explicitly declare character encoding in Content-Type HTTP headers combined with reliance on browser auto-detection mechanisms and meta tags. This creates a window where validation logic and browser rendering can interpret the same byte sequences differently, bypassing security controls.

## Attacker mindset
An attacker would systematically identify missing or weak charset declarations and exploit the gap between validation encoding and browser rendering encoding. By understanding character encoding specifications and browser charset fallback behavior, an attacker can craft polyglot payloads that pass filters but execute in browsers.

## Defensive takeaways
- Always explicitly declare charset in Content-Type headers (e.g., 'charset=utf-8') rather than relying on browser auto-detection
- Validate and encode input using the same character set throughout the entire application stack (browser, server, database)
- Implement Content-Type headers that cannot be overridden by browser MIME-sniffing or meta tag manipulation
- Use charset specifications in meta tags as a secondary measure, not primary defense
- Perform static analysis of source code to detect missing or inconsistent charset declarations
- Apply input validation that accounts for multiple character encodings, not just the intended one
- Avoid relying on charset headers alone; enforce charset consistency at application logic level

## Variant hunting
Search for similar encoding confusion vulnerabilities in: UTF-16 encoding confusion attacks, GBK/Big5 multi-byte encoding exploitation, HTML5 charset override techniques, BOM (Byte-Order Mark) manipulation bypassing filters, polyglot payloads exploiting encoding differentials in different templating engines or web frameworks, and mXSS (mutated XSS) techniques leveraging encoding differences.

## MITRE ATT&CK
- T1190
- T1071.001
- T1140

## Notes
This is a sophisticated encoding-based bypass technique that demonstrates how seemingly minor configuration omissions (missing charset attribute) can create exploitable security gaps. The vulnerability class 'encoding differentials' represents a category of attacks that exploit inconsistencies between how different system layers interpret byte sequences. Presented at TROOPERS24 conference, indicating high-value security research.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
