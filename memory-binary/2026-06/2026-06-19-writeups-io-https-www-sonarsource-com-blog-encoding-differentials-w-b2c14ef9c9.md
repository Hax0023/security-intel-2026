# Encoding Differentials: Charset Mismatches as Security Gaps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** SonarSource Security Research
- **Bounty:** Not specified (Research publication)
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), SQL Injection, Character Encoding Bypass, Input Validation Bypass, Charset Confusion
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials occur when different layers of a web application interpret byte sequences under different character sets, allowing attackers to bypass input validation filters. When Content-Type headers lack explicit charset declarations, browsers fall back to auto-detection or meta tags, enabling attackers to inject malicious payloads like XSS by manipulating character encoding interpretation across the stack.

## Attack scenario (step by step)
1. Attacker identifies a web application with missing charset attribute in Content-Type header
2. Browser defaults to auto-detection and interprets response using an unintended character encoding (e.g., UTF-16 instead of UTF-8)
3. Attacker crafts payload that is valid in the alternative encoding but bypasses server-side validation filters
4. Input validation layer interprets payload as safe UTF-8, but browser renders it as malicious code in the alternative encoding
5. Malicious JavaScript executes in victim's browser context when page is rendered
6. Attacker achieves arbitrary code execution, session hijacking, or credential theft

## Root cause
Developers fail to explicitly declare character sets at every application layer, relying on implicit defaults or HTTP headers that can be overridden. Browser fallback mechanisms (auto-detection, meta tags, BOM) create inconsistency between server-side validation expectations and client-side rendering, enabling encoding-based bypass techniques.

## Attacker mindset
An attacker recognizes that input validation systems typically assume a single encoding (usually UTF-8) and that mismatches between validation layer and rendering layer can be exploited. By understanding character encoding specifications and browser auto-detection behavior, they craft polyglot payloads valid in multiple encodings to evade filters and inject malicious content.

## Defensive takeaways
- Always explicitly declare charset in Content-Type headers (charset=utf-8 recommended)
- Avoid relying solely on HTTP headers; they can be overridden by browser auto-detection
- Include charset meta tags in HTML head as a secondary layer
- Be aware of Byte-Order Mark (BOM) precedence and potential exploitation
- Implement validation that accounts for encoding differentials and multiple character set interpretations
- Perform static analysis to detect missing or mismatched charset declarations across the stack
- Test input validation against payloads in alternative encodings (UTF-16, ISO-8859-x, GBK, Big5)
- Use strict encoding validation rather than relying on auto-detection

## Variant hunting
['UTF-16 encoding bypass where validation assumes UTF-8 byte patterns', 'Double-encoding attacks combined with charset confusion', 'BOM-based bypass techniques (U+FEFF prefix manipulation)', 'Asian character set exploitation (GBK, Big5) with overlong encoding sequences', 'Windows-125x encoding variants bypassing Latin-1 validation', 'Combination of charset confusion with mXSS (mutation-based XSS) techniques', 'Database charset mismatch between application and backend storage']

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This research demonstrates that security is not just about what data is processed, but how it is encoded and decoded across different layers. The attack surface includes the HTTP layer, browser parsing, DOM rendering, and database storage—each with potential charset interpretation differences. Similar to MIME-type sniffing vulnerabilities, browsers' user-friendly auto-detection mechanisms create security risks. Presented at TROOPERS24 conference.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
