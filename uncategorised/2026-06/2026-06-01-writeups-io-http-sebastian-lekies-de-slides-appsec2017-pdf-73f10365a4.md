# PDF JavaScript Execution Vulnerability Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** AppSec 2017 - Sebastian Lekies Research
- **Bounty:** Unknown (Academic Research)
- **Severity:** HIGH
- **Vuln types:** Code Injection, Arbitrary Code Execution, JavaScript Execution in PDF, Client-Side Code Execution
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
This presentation document demonstrates vulnerabilities in PDF readers' handling of embedded JavaScript, allowing arbitrary code execution through malicious PDF files. The vulnerability exploits the fact that PDF readers interpret and execute JavaScript contained within PDF objects without proper sandboxing or user consent mechanisms.

## Attack scenario (step by step)
1. Attacker crafts a malicious PDF file with embedded JavaScript code in the JavaScript object catalog (/JavaScript /Names dictionary)
2. Attacker distributes the PDF via email, file sharing, or compromised website
3. Victim opens the PDF in a vulnerable PDF reader (Adobe Reader, Foxit, etc.)
4. PDF reader automatically parses and executes the embedded JavaScript without warning
5. JavaScript payload gains execution context and can steal data, modify content, or exploit further vulnerabilities
6. Attacker exfiltrates sensitive information or compromises the victim's system

## Root cause
PDF specification allows JavaScript execution within documents, and PDF readers implement insufficient security controls to prevent automatic execution of embedded scripts. The /JavaScript names dictionary in the PDF catalog enables script execution without explicit user interaction or permission prompt.

## Attacker mindset
Exploit the trust users place in PDF documents as seemingly static files while leveraging the powerful JavaScript engine embedded in PDF readers. Target users who open PDFs from untrusted sources, bypassing traditional file-based protections since PDFs are generally considered safe.

## Defensive takeaways
- Disable JavaScript execution in PDF readers by default (Adobe Reader: Edit > Preferences > JavaScript)
- Implement strict Content Security Policy and sandboxing for PDF document rendering
- Require explicit user consent before executing any scripts embedded in PDF documents
- Validate and sanitize all embedded scripts; implement allowlist-based script execution
- Educate users about risks of opening PDFs from untrusted sources
- Keep PDF reader software fully patched and updated
- Use dedicated PDF viewers without JavaScript capabilities for untrusted documents
- Implement endpoint detection and response (EDR) to monitor suspicious PDF reader behavior

## Variant hunting
Look for similar code injection vulnerabilities in other document formats (Office macros, Flash in PDFs, embedded media handlers), JavaScript execution in browser-based PDF viewers, and exploitation of PDF form submission capabilities.

## MITRE ATT&CK
- T1190
- T1059.007
- T1566.001
- T1204.002
- T1105

## Notes
This appears to be a research presentation (AppSec 2017) documenting PDF JavaScript vulnerabilities. The provided content is a PDF file structure with compressed stream objects containing slide content. Sebastian Lekies is known for security research on PDF vulnerabilities and browser sandbox escapes. This represents a well-known vulnerability class that has been exploited in real-world attacks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
