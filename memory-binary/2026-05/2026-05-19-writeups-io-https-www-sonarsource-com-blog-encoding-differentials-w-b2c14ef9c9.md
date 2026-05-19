# Encoding Differentials: Charset-Based Security Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** SonarSource Security Research
- **Bounty:** N/A - Research Publication
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), SQL Injection, Encoding Differential, Charset Confusion, Mutation XSS (mXSS)
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials occur when different layers of a web application interpret byte sequences under different character sets, enabling attackers to bypass input validation filters. Missing or conflicting charset declarations across the HTTP Content-Type header, meta tags, and Byte-Order Marks allow browsers to auto-detect encodings, potentially converting filtered payloads into executable code. This vulnerability class demonstrates how charset mismatches between browser, server, and database layers create exploitable security gaps.

## Attack scenario (step by step)
1. Attacker identifies a web application missing explicit charset declaration in Content-Type header (e.g., 'text/html' without 'charset=utf-8')
2. Browser defaults to auto-detection or a non-standard charset (e.g., UTF-16, GBK, ISO-8859-1) instead of intended UTF-8
3. Attacker crafts payload with bytes that appear benign in server's validation encoding but render as malicious code in browser's interpreted charset
4. Payload passes server-side filters that validated against different byte representations
5. Browser decodes malicious bytes under detected charset, reconstructing XSS or injection payload
6. Arbitrary JavaScript executes in victim's browser or SQL injection succeeds against database

## Root cause
Missing or conflicting charset specifications force browsers to implement auto-detection heuristics, decoupling the validation charset from execution charset. This creates an encoding differential where byte sequences have different interpretations across layers. Three prioritized fallback mechanisms (BOM > Content-Type header > meta tag) combined with browser lenience enable exploitation when initial charset context is absent.

## Attacker mindset
An attacker recognizes that security filters operate on character representations after decoding, then exploit the encoding process itself. By crafting payloads that remain filtered in one charset but transform into malicious content when interpreted through a different charset, they bypass validation entirely. The attacker leverages browser auto-detection as a feature, not a limitation, to force reinterpretation of their payload.

## Defensive takeaways
- Explicitly declare charset in Content-Type header for all HTTP responses (charset=utf-8 preferred)
- Validate and enforce consistent character encoding at all application layers (HTTP, server processing, database storage)
- Include charset meta tags in HTML templates as defense-in-depth, but do not rely solely on them
- Avoid relying on browser auto-detection; never assume default encodings
- Implement input validation and output encoding using the same explicit charset throughout the stack
- Use static analysis tools to detect charset misconfigurations before production deployment
- Test XSS/injection filters with payloads across multiple character encodings (UTF-16, GBK, ISO-8859-1, etc.)
- Do not allow user control over charset parameters in responses
- Monitor and sanitize Byte-Order Marks in user-supplied content

## Variant hunting
Investigate other encoding schemes supported by browsers (UTF-16LE/BE, ISO-2022-JP, EUC-KR) for differential encoding bypasses. Examine APIs that perform encoding/decoding at different stack layers (JavaScript TextDecoder vs. server-side decoders). Test mixed-charset responses where portions use different encodings. Analyze multi-byte character encodings (GBK, Big5) where single bytes may be reinterpreted as parts of different characters. Review database-level charset configurations and collation settings for secondary injection vectors.

## MITRE ATT&CK
- T1190
- T1090
- T1027
- T1083

## Notes
This research was presented at TROOPERS24 conference. The vulnerability class demonstrates that security controls must account for encoding layers explicitly rather than relying on implicit browser behavior. Encoding differentials represent a form of polyglot payload construction where the same bytes have multiple valid interpretations. SonarSource's static analysis approach enables detection of charset misconfigurations in source code before exploitation. The vulnerability highlights how defense-in-depth encoding specifications are critical; no single layer (HTTP header, meta tag, or BOM) is sufficient without explicit management.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
