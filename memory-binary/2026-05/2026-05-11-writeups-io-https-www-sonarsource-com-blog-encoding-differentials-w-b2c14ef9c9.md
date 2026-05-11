# Encoding Differentials: Character Set Mismatches in Web Applications

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** SonarSource Research
- **Bounty:** Not applicable - Educational research publication
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), SQL Injection, Character Encoding Confusion, mXSS (Mutation XSS), Input Validation Bypass
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials occur when different application layers interpret byte sequences under different character sets, allowing attackers to bypass input validation filters. Missing or mismatched charset declarations across HTTP headers, meta tags, and databases create security gaps that enable malicious payload smuggling such as XSS and SQL injection attacks.

## Attack scenario (step by step)
1. Attacker identifies web application serving HTML without explicit charset in Content-Type header
2. Browser auto-detects character encoding (potentially different from server's intended encoding) or relies on meta tag charset
3. Attacker crafts payload that appears benign in one encoding but contains malicious code when decoded in the browser's chosen encoding
4. Input validation filters on server check payload against their expected charset, missing the malicious interpretation
5. Browser decodes payload in its auto-detected or meta-tag-specified charset, revealing malicious JavaScript or SQL syntax
6. XSS executes in victim's browser or SQL injection compromises database integrity/confidentiality

## Root cause
Browsers implement lenient character encoding detection (auto-detection, byte-order marks, meta tags) when explicit charset declarations are missing. This creates a differential interpretation gap where server-side validation uses one charset interpretation while browsers may use another, especially when charset information is absent or ambiguous in HTTP responses.

## Attacker mindset
Exploit the gap between strict server-side validation (if it occurs at all) and lenient browser-side decoding. Target applications with missing or incomplete charset declarations, particularly those relying solely on Content-Type headers that lack charset attributes. Abuse browser auto-detection mechanisms to obfuscate malicious payloads that pass validation filters.

## Defensive takeaways
- Explicitly declare charset (preferably UTF-8) in Content-Type header for all HTTP responses
- Do not rely solely on HTTP headers; include charset meta tag in HTML documents as defense-in-depth
- Implement input validation that accounts for multiple potential character encodings and normalizes inputs
- Use static analysis tools (like Sonar) to detect missing or mismatched charset declarations in source code
- Validate and normalize character encoding at database layer independently
- Consider using UTF-8 exclusively across entire application stack to eliminate encoding confusion
- Test input filters against payloads encoded with alternative charsets (UTF-16, ISO-8859-x, GBK, etc.)

## Variant hunting
['Test applications using legacy charset declarations (ISO-8859-1, windows-1252) for differential interpretation', 'Investigate multi-byte encodings (UTF-16 with BOM, Big5, GBK) for null-byte injection and filter evasion', 'Check for inconsistent charset declarations across different response types (API vs HTML vs JavaScript)', 'Search for applications missing charset on JSON/XML responses that browsers might sniff as HTML', 'Examine error pages and edge cases where charset fallback mechanisms trigger', 'Test WAF/filter rules against payloads using alternative encodings that decode identically']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1083 - File and Directory Discovery
- T1566 - Phishing
- T1598 - Phishing for Information

## Notes
This research was presented at TROOPERS24 conference. The vulnerability class is subtle and often overlooked because proper charset declaration is sometimes treated as non-critical by developers. Encoding differentials are particularly dangerous because they bypass input validation that assumes consistent character interpretation. The three-level charset resolution priority (BOM > Content-Type > meta tag) creates multiple exploitation vectors. Static analysis is critical for detecting these configuration issues before deployment.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
