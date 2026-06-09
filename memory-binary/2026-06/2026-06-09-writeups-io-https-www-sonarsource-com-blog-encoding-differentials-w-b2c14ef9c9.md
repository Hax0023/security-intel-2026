# Encoding Differentials: Character Set Mismatches Enable XSS and SQL Injection Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** SonarSource Research
- **Bounty:** N/A - Educational/Research
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), SQL Injection, Charset/Encoding Differential, Input Validation Bypass, Character Encoding Confusion
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Character encoding differentials occur when different application layers (browser, server, database) interpret byte sequences under different character sets, allowing attackers to smuggle malicious payloads past input validation filters. Missing or mismatched charset declarations enable browsers to auto-detect encodings, which attackers can exploit to inject XSS, SQL injection, or other payloads that appear benign under one encoding but become malicious under another.

## Attack scenario (step by step)
1. Attacker identifies a web application with missing charset attribute in Content-Type header
2. Attacker crafts malicious payload designed to appear as safe characters under browser's auto-detected encoding (e.g., UTF-16 or GBK)
3. Browser receives response and auto-detects incorrect character encoding due to missing charset declaration
4. Malicious payload gets decoded as executable JavaScript or SQL syntax under the auto-detected encoding
5. Input validation filters designed for UTF-8 fail to recognize the dangerous payload in its alternate encoding
6. Payload bypasses server-side filters and executes as XSS or SQL injection in database context

## Root cause
Developers omit explicit charset declarations at multiple stack layers (HTTP header, meta tag, database connection), forcing browsers to perform auto-detection or use fallback encoding schemes. This creates a differential where the same byte sequence has different semantic meaning depending on which character set interprets it.

## Attacker mindset
Exploit the gap between how browsers interpret bytes (often through fallible auto-detection) versus how server-side validation logic processes them. By crafting payloads that are harmless in one encoding but malicious in another, attackers bypass encoding-aware filters that only check for threats in expected character sets.

## Defensive takeaways
- Always explicitly declare charset in Content-Type HTTP header (e.g., charset=utf-8)
- Include meta charset declaration in HTML head as defense-in-depth
- Validate and sanitize input independently of character encoding assumptions
- Configure database connections with explicit character sets to prevent encoding confusion
- Avoid relying solely on Content-Type headers, which browsers may override or auto-detect past
- Use static analysis tools to detect missing or inconsistent charset declarations
- Test input validation logic against multiple character encodings (UTF-8, UTF-16, GBK, Big5, etc.)
- Implement encoding normalization before applying security filters
- Be aware of Byte-Order Mark (BOM) which takes precedence over charset attributes

## Variant hunting
Search codebases for: (1) HTTP response handlers without explicit charset parameters, (2) HTML templates missing meta charset tags, (3) Database connection strings without collation/charset specifications, (4) Input validation functions that assume single character encoding, (5) Content served with application/octet-stream or missing Content-Type entirely, (6) Java/Python applications using default platform encoding instead of explicit UTF-8, (7) Legacy code with ISO-8859-1 or windows-125x charset declarations.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution (XSS variant)
- T1083 - File and Directory Discovery (charset scanning)
- T1012 - Query Registry (character encoding detection)
- T1027 - Obfuscation or Encoding

## Notes
This research was presented at TROOPERS24 conference. The vulnerability chain demonstrates that security is not just about logic but also about consistent interpretation of data across layers. The browser's lenient auto-detection behavior, while improving user experience, creates a surface for exploitation. Critical insight: missing charset information forces browsers to guess, and attackers can influence that guess through payload crafting. The differential nature means filters working correctly in one encoding may fail in another.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
