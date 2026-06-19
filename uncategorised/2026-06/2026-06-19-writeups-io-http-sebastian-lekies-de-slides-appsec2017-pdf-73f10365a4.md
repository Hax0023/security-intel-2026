# PDF JavaScript Execution and Security Implications

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Academic/Security Research (AppSec 2017 Conference)
- **Bounty:** N/A - Academic Research Presentation
- **Severity:** HIGH
- **Vuln types:** JavaScript Execution in PDF, Code Execution, Client-Side Script Injection
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
This presentation discusses JavaScript execution capabilities embedded within PDF documents, demonstrating how malicious scripts can be embedded in PDF files and executed by PDF readers. The vulnerability allows attackers to execute arbitrary code when users open seemingly innocent PDF files.

## Attack scenario (step by step)
1. Attacker crafts a malicious PDF file with embedded JavaScript code in the document catalog or page objects
2. Attacker distributes the PDF through email, file sharing, or compromised websites
3. Victim downloads and opens the PDF using a vulnerable PDF reader (Adobe Reader, etc.)
4. PDF reader automatically parses and executes the embedded JavaScript without user consent
5. Malicious script gains access to system resources, file system, or initiates network connections
6. Attacker achieves code execution, data exfiltration, or system compromise

## Root cause
PDF specification allows embedded JavaScript in document objects (/JavaScript dictionary in catalog). PDF readers automatically execute scripts without adequate sandboxing or user warnings, treating PDFs as trusted content containers.

## Attacker mindset
Target unsuspecting users who trust PDF as a safe document format. Leverage automatic script execution to bypass user vigilance. Use social engineering combined with technical exploit for maximum impact.

## Defensive takeaways
- Disable JavaScript execution in PDF readers by default
- Implement strict Content Security Policy for PDF content
- Use sandboxing for PDF rendering with minimal privilege elevation
- Require explicit user consent before executing embedded scripts
- Maintain updated PDF reader software with security patches
- Educate users about risks of opening PDFs from untrusted sources
- Implement file type validation and signature checking
- Monitor PDF files for suspicious JavaScript patterns during security scanning

## Variant hunting
Search for PDFs with /JavaScript, /AcroForm, /OpenAction, /AA (Additional Actions) objects. Look for obfuscated or encoded JavaScript using FlateDecode filters. Check for embedded URLs or network connections in PDF scripts. Analyze PDFs opened from email or suspicious sources.

## MITRE ATT&CK
- T1190
- T1204
- T1566
- T1059

## Notes
This is an academic research presentation from AppSec 2017 by Sebastian Lekies analyzing PDF security. The PDF itself contains compressed content streams demonstrating the vulnerability being discussed. The research highlights a fundamental design flaw in PDF specification where scripts are executed automatically without proper isolation or user control.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
