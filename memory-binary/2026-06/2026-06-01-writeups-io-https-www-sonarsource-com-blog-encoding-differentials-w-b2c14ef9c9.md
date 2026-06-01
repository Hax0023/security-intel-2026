# Encoding Differentials: Charset Mismatches Enable XSS and SQL Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** SonarSource Security Research
- **Bounty:** Not applicable - Research/Educational
- **Severity:** HIGH
- **Vuln types:** Cross-Site Scripting (XSS), SQL Injection, Charset Confusion, Encoding Differential, Character Set Mismatch
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials occur when different application layers interpret byte sequences using inconsistent character sets, allowing attackers to bypass input validation filters. When Content-Type headers lack explicit charset declarations, browsers perform auto-detection or fallback to alternative encoding sources (meta tags, BOM), creating opportunities to smuggle malicious payloads like XSS or SQL injection.

## Attack scenario (step by step)
1. Attacker identifies a web application with missing charset attribute in Content-Type header (e.g., 'text/html' without 'charset=utf-8')
2. Application implements input validation filters assuming UTF-8 encoding when processing user input or database queries
3. Attacker crafts a payload exploiting a different character encoding (e.g., UTF-16, ISO-8859-1, windows-1252) that bypasses the UTF-8-based filter
4. Browser receives response and auto-detects or uses meta tag charset, interpreting attacker's payload under the different encoding scheme
5. Filter validation passes because it evaluated the payload in UTF-8 context, but browser executes malicious code under the attacker's chosen encoding
6. XSS or SQL injection executes when the payload is rendered or processed by the browser/database in the unintended character set

## Root cause
Missing or inconsistent charset declarations across the HTTP response stack (Content-Type header, meta tags, BOM) combined with browsers' auto-detection behavior and fallback mechanisms. Developers fail to explicitly declare character sets, allowing encoding ambiguity that can be exploited by attackers who understand character encoding mechanics.

## Attacker mindset
Security researchers and sophisticated attackers recognize that modern browsers prioritize user experience over strict adherence to standards, implementing charset auto-detection and fallback behavior. By deliberately choosing alternative character encodings that render differently than the filter's assumed encoding, attackers can encode XSS/SQL injection payloads that evade input validation filters operating under different charset assumptions.

## Defensive takeaways
- Always explicitly declare charset in Content-Type HTTP headers (charset=utf-8 recommended)
- Include charset meta tag in HTML head: <meta charset="UTF-8">
- Validate and normalize character encoding at every layer (browser, server, database)
- Implement input validation that is encoding-aware and tests payloads under multiple character sets
- Avoid relying solely on Content-Type headers as browsers can auto-detect or override them
- Use static analysis tools to detect missing charset declarations in source code before production
- Consider using Content-Security-Policy headers to mitigate XSS even if encoding differentials exist
- Test application security with alternative character encodings (UTF-16, ISO-8859-1, etc.) during SAST/DAST

## Variant hunting
Search for applications using alternative character encodings (GBK, Big5, windows-125x, ISO-8859-xx families) without proper declaration. Investigate partial HTML responses (templates, API responses) that lack meta charset tags. Test mutation XSS (mXSS) scenarios where encoding differentials combine with DOM parsing to create secondary vulnerabilities. Examine legacy systems supporting older character sets that may have less rigorous validation frameworks.

## MITRE ATT&CK
- T1190
- T1203
- T1189
- T1083

## Notes
This represents a class of vulnerabilities emerging from the intersection of character encoding specifications and browser auto-detection heuristics. The TROOPERS24 conference talk 'From ASCII to UTF-16: Leveraging Encodings to Break Software' provides practical exploitation demonstrations. The vulnerability is particularly dangerous because it defeats encoding-agnostic input filters and is difficult to detect without encoding-aware security testing. SonarSource's static analysis approach enables detection at code review stage before deployment.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
