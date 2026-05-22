# Encoding Differentials: Character Set Mismatches Leading to XSS Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** SonarSource Security Research
- **Bounty:** Not specified - Security research publication
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Character Encoding Mismatch, Input Validation Bypass, HTTP Response Splitting
- **Category:** memory-binary
- **Writeup:** https://www.sonarsource.com/blog/encoding-differentials-why-charset-matters/

## Summary
Encoding differentials occur when different layers of a web application interpret the same byte sequence under different character sets, allowing attackers to bypass input validation filters. Missing or incorrect charset declarations in HTTP Content-Type headers force browsers to auto-detect encoding, enabling attackers to inject malicious payloads like XSS that pass filters expecting a specific encoding.

## Attack scenario (step by step)
1. Attacker identifies a web application missing explicit charset attribute in Content-Type header (e.g., 'text/html' without 'charset=utf-8')
2. Browser defaults to auto-detection or fallback encoding when parsing the response body
3. Attacker crafts payload using alternate character encoding (e.g., UTF-16, ISO-8859-1, GBK) that encodes XSS payload differently
4. Input validation filter expects UTF-8 and fails to detect the malicious payload in alternate encoding
5. Browser's auto-detection or <meta charset> tag interprets the bytes as the alternate encoding, successfully executing JavaScript
6. XSS payload executes in victim's browser, compromising session or stealing credentials

## Root cause
Browsers implement lenient charset handling to improve user experience, using auto-detection when charset information is missing. This creates a gap between what validation filters expect (specific encoding) and what browsers actually interpret (auto-detected or alternate encoding). Three fallback mechanisms exist: Byte-Order Mark, Content-Type charset attribute, and <meta> charset tag—any mismatch creates exploitability.

## Attacker mindset
Exploit trust assumptions in encoding layers. By forcing encoding mismatch between filter and browser interpretation, attackers bypass defenses that assume consistent encoding. This leverages browser leniency as a feature, not a bug, turning auto-detection into an attack vector.

## Defensive takeaways
- Always explicitly declare charset in Content-Type headers (e.g., 'text/html; charset=utf-8')
- Include charset in <meta> tags as defense-in-depth, particularly for partial HTML responses
- Validate input using the exact character encoding the browser will use, not an assumed encoding
- Implement validation filters that handle multiple encodings or normalize to a single canonical form before validation
- Use Content-Security-Policy headers to limit XSS impact regardless of encoding bypasses
- Avoid relying solely on Content-Type headers; attackers can override with <meta> tags or Byte-Order Marks
- Implement static analysis tools to detect missing or misconfigured charset declarations
- Test security filters against payloads in alternative encodings (UTF-16, GBK, etc.)

## Variant hunting
Search for: (1) HTML responses without charset attributes across all endpoints; (2) Input filters that assume single encoding; (3) Database operations with charset mismatches between application and DB; (4) APIs returning JSON/XML without explicit charset; (5) Partial HTML snippets injected into pages without charset context; (6) Legacy applications using windows-125x or ISO-8859-1; (7) User-controlled content served without charset encoding; (8) Frameworks with auto-detected charset handling.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1071 - Application Layer Protocol
- T1059 - Command and Scripting Interpreter
- T1566 - Phishing

## Notes
This is a sophisticated encoding-based security differential. The vulnerability relies on intentional browser lenience (auto-detection) colliding with validation assumptions. Presenters at TROOPERS24 demonstrated 'From ASCII to UTF-16' techniques. The attack surface includes any charset mismatch in the stack: browser↔server, server↔database, validation filter↔rendering engine. Particularly dangerous for mXSS (mutation XSS) scenarios. SonarSource static analysis can detect misconfigured charsets pre-deployment.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
