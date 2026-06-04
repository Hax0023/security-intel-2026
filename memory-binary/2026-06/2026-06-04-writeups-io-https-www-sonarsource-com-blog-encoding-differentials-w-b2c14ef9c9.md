# Encoding Differentials: Character Set Mismatches as XSS Vector

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** General Web Security (SonarSource Research)
- **Bounty:** N/A - Research Publication
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Charset Mismatch, Encoding Differential, mXSS (mutation XSS)
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials arise when different application layers interpret byte sequences using different character sets, allowing attackers to bypass input validation filters. Missing or inconsistent charset declarations enable browsers to auto-detect encodings, permitting malicious payloads like XSS and SQL injection to evade security controls designed for a specific character encoding.

## Attack scenario (step by step)
1. Attacker identifies a web application with a Content-Type header lacking explicit charset declaration (e.g., 'text/html' without 'charset=utf-8')
2. Browser receives HTTP response and cannot determine encoding from Content-Type header; begins auto-detection or assumes default encoding (often ISO-8859-1 or windows-1252)
3. Attacker crafts malicious payload using byte sequences that remain benign in the assumed encoding but decode to dangerous characters (e.g., XSS tags) when re-interpreted with UTF-16 or other encodings
4. Input validation filter processes the payload under one encoding (e.g., UTF-8) and allows it through, not recognizing the malicious code
5. Browser re-decodes the response body using auto-detected or meta-tag-specified encoding, transforming the benign bytes into executable XSS payload
6. JavaScript executes in victim's browser with full access to sensitive data and session cookies

## Root cause
Developers fail to explicitly declare charset in Content-Type headers, relying instead on browser auto-detection or meta tags. This creates ambiguity when multiple encoding interpretations are possible, especially when input validation occurs at a layer using a different assumed encoding than the browser. The HTML5 spec allows browsers to recover from missing charset information via auto-detection, enabling exploitation.

## Attacker mindset
An attacker exploiting encoding differentials views the gap between server-side validation encoding assumptions and browser-side decoding behavior as an opportunity. By crafting payloads that remain benign under one encoding but malicious under another, they bypass filters. The attacker relies on the browser's fault-tolerant behavior and the prevalence of missing charset declarations in real-world applications.

## Defensive takeaways
- Always explicitly declare charset in Content-Type headers at the HTTP layer (e.g., 'Content-Type: text/html; charset=utf-8')
- Validate and sanitize input using the same encoding consistently across all application layers
- Use Content-Security-Policy (CSP) headers to mitigate XSS impact even if encoding bypasses occur
- Avoid relying solely on meta tags or Byte-Order Marks for charset specification; prioritize HTTP headers
- Implement static analysis tools (like Sonar) to detect missing or inconsistent charset declarations before deployment
- Test with multiple character encodings during security testing to identify encoding-based bypasses
- Consider restricting accepted character encodings to UTF-8 only to reduce attack surface

## Variant hunting
Look for encoding differentials in: (1) JSON responses without charset declarations; (2) API endpoints returning HTML or templated content; (3) legacy applications using non-UTF-8 encodings; (4) partial HTML fragments served without meta tags; (5) form submission handlers that validate input under UTF-8 but output under different encodings; (6) cached responses where charset may be stripped by middleware; (7) databases returning data in encodings differing from HTTP response charset.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (JavaScript execution via XSS)
- T1566.002 - Phishing: Spearphishing Link (delivery of malicious encoded payload)

## Notes
This is a foundational research piece by SonarSource presented at TROOPERS24. The vulnerability class 'encoding differentials' is not widely recognized in threat models but represents a sophisticated bypass technique. The paper emphasizes the importance of explicit charset declaration and consistent encoding assumptions across the entire stack. Notably, browsers' fault-tolerant auto-detection behavior—designed for user experience—directly enables this attack vector. The technique overlaps with mutation XSS (mXSS) but focuses specifically on charset-based mutations.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
