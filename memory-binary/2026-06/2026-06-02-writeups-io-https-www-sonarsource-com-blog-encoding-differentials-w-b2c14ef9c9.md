# Encoding Differentials: Charset-Based XSS and Injection Vulnerabilities

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Sonar/SonarSource Research
- **Bounty:** Research/Educational (No specific bounty mentioned)
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), SQL Injection, Encoding Differential Attack, Character Set Mismatch, Input Validation Bypass
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials occur when different application layers interpret byte sequences under different character sets, allowing attackers to smuggle malicious payloads past validation filters. Missing or mismatched charset declarations in HTTP headers, meta tags, and databases enable browsers to auto-detect encodings, which attackers can exploit to bypass XSS and SQL injection protections.

## Attack scenario (step by step)
1. Attacker identifies web application without explicit charset declaration in Content-Type header
2. Attacker crafts HTTP response with malicious JavaScript payload encoded in alternative charset (e.g., UTF-16, ISO-8859-1)
3. Browser encounters missing/invalid charset and performs auto-detection, interpreting bytes under attacker-controlled encoding
4. Input validation filter expecting UTF-8 encoded payload fails to detect XSS payload due to encoding differential
5. Browser re-interprets payload in detected charset and renders malicious JavaScript in user's context
6. XSS executes with user's session privileges, potentially stealing credentials or performing unauthorized actions

## Root cause
Developers fail to explicitly declare character encoding at all application layers (HTTP headers, HTML meta tags, database). Browser auto-detection and charset resolution order prioritize Byte-Order Mark, then Content-Type header, then meta tags—creating ambiguity when multiple or none are specified. Input validation assumes single encoding, unable to handle differential interpretations.

## Attacker mindset
Exploit the gap between encoding assumptions at different layers. By deliberately crafting payloads in alternative character encodings, bypass signature-based filters and WAF rules designed for UTF-8. Leverage browser auto-detection as an unintended feature to decode malicious content that validators rejected. This is a sophisticated attack requiring understanding of character encoding internals and browser behavior.

## Defensive takeaways
- Always explicitly declare charset in Content-Type header (e.g., charset=utf-8) for all HTTP responses
- Include <meta charset="UTF-8"> tag in HTML head as defense-in-depth
- Never rely solely on Content-Type headers; browsers may override or ignore them
- Validate and normalize input encoding before applying security filters
- Implement charset validation to reject unexpected character encodings
- Use static analysis tools (like Sonar) to detect missing charset declarations in source code
- Configure servers to enforce strict charset handling; disable auto-detection where possible
- Test input validation filters with multiple character encodings (UTF-16, ISO-8859-1, GBK, etc.)
- Apply security controls consistently across all layers (browser, server, database)
- Use Content-Security-Policy headers to mitigate XSS even if payload bypasses validation

## Variant hunting
Search for similar encoding differential attacks in: UTF-16 BOM-based bypasses, double-encoding chains, multi-byte character set mutations (GBK, Big5), homograph attacks via encoding, internationalized domain names (IDN) exploitation, charset switching in AJAX/API responses, encoding differentials in JSON/XML parsers, database encoding mismatches causing stored XSS, URL encoding interactions with character sets

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1059

## Notes
This research was presented at TROOPERS24 conference. The vulnerability is particularly insidious because it exploits browser standards-compliance (auto-detection for user experience) as an attack surface. Organizations using WAFs/signature-based detection may be especially vulnerable if their rules assume UTF-8. The encoding differential concept extends beyond XSS to SQL injection and other injection attacks where validators depend on single encoding assumption.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
