# PDF JavaScript Execution and Security Analysis (AppSec 2017)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Academic/Conference Presentation
- **Bounty:** N/A - Educational Material
- **Severity:** High
- **Vuln types:** Arbitrary Code Execution, JavaScript Execution in PDF, Client-Side Code Injection
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
This is a conference presentation slide deck (likely containing embedded JavaScript in PDF format) demonstrating PDF-based attack vectors and security vulnerabilities. The PDF contains embedded JavaScript objects and potentially malicious code execution capabilities through PDF readers that support JavaScript.

## Attack scenario (step by step)
1. Attacker crafts a PDF document with embedded JavaScript code in the PDF catalog/names section
2. PDF is distributed to target users via email, file sharing, or compromised websites
3. When victim opens the PDF in a vulnerable PDF reader (Adobe Reader, etc.), the embedded JavaScript automatically executes
4. JavaScript payload can access document properties, interact with file system, or establish network connections
5. Attacker achieves code execution, data exfiltration, or further malware installation on victim's system
6. Minimal user interaction required - simply opening the PDF triggers the exploit

## Root cause
PDF specification allows embedding and execution of JavaScript code within PDF documents. Many PDF readers execute JavaScript by default without explicit user consent or adequate sandboxing, treating PDF files as trusted despite their untrusted origin.

## Attacker mindset
Attacker recognizes PDFs as effective delivery mechanisms for malicious payloads because: (1) PDFs are commonly used and trusted file formats, (2) JavaScript execution is enabled by default in many readers, (3) Users do not expect code execution from document formats, (4) PDF attachments bypass email security filters more easily than executables, (5) Cross-platform compatibility ensures wide target surface

## Defensive takeaways
- Disable JavaScript execution in PDF readers by default (Adobe Reader: Edit > Preferences > Security > Scripting)
- Use sandboxed or isolated PDF viewers that restrict JavaScript capabilities
- Implement strict Content Security Policy and disable unnecessary PDF features at organizational level
- Educate users about risks of opening PDFs from untrusted sources
- Keep PDF readers patched with latest security updates
- Use endpoint protection that detects suspicious PDF behavior
- Consider alternative document formats (HTML, Office) for distribution when possible
- Implement file scanning and analysis before allowing PDFs through email gateways

## Variant hunting
Hunt for: (1) PDFs with /JavaScript, /AcroForm, /OpenAction, or /AA (Additional Actions) objects, (2) Obfuscated JavaScript within PDF streams using compression/encoding, (3) PDFs triggering network requests or file system access, (4) Flash embedded in PDFs for alternative code execution, (5) PDFs exploiting known CVEs in PDF reader JavaScript engines, (6) Malicious PDFs using /EmbeddedFile for payload delivery

## MITRE ATT&CK
- T1190
- T1566.001
- T1204.002
- T1059.007
- T1203
- T1105
- T1078

## Notes
This appears to be Sebastian Lekies' AppSec 2017 presentation on PDF security vulnerabilities. The PDF itself is a legitimate academic presentation (not an actual attack), but demonstrates the attack surface. Key insight: PDF format complexity and feature richness (JavaScript, forms, embedded files, actions) creates significant security risks. Modern browsers increasingly disable PDF JavaScript execution, but standalone PDF readers remain vulnerable. Organizations should treat PDFs as code, not just documents.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
