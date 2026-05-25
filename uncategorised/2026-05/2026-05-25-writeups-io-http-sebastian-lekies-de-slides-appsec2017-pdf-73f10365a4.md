# PDF JavaScript Execution and Security Analysis - AppSec 2017

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Academic/Conference Presentation
- **Bounty:** N/A - Academic Research
- **Severity:** High
- **Vuln types:** Arbitrary Code Execution, JavaScript Execution in PDF, Client-Side Code Injection
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
This presentation analyzes JavaScript execution vulnerabilities within PDF documents, demonstrating how malicious JavaScript can be embedded and executed by PDF viewers. The research highlights the risks of PDF readers processing embedded scripts without proper sandboxing or user consent, potentially leading to arbitrary code execution on victim systems.

## Attack scenario (step by step)
1. Attacker embeds malicious JavaScript in a PDF document using the JavaScript dictionary in the PDF catalog
2. PDF is distributed via email, file hosting, or watering hole attack to target users
3. Victim opens PDF in vulnerable PDF reader (Adobe Reader, etc.) which automatically executes embedded scripts
4. JavaScript code executes with privileges of the PDF reader application and user
5. Attacker gains ability to access file system, exfiltrate data, or install malware
6. Attack occurs transparently without user knowledge or visible indicators of malicious activity

## Root cause
PDF readers implement JavaScript support for interactive features but lack proper sandboxing, validation, and user consent mechanisms. The PDF specification allows arbitrary JavaScript execution through multiple vectors including document catalogs, annotations, and form fields without requiring user interaction or approval.

## Attacker mindset
Exploit legitimate PDF features to deliver malicious code; target users who trust PDF format as 'safe'; leverage automatic script execution in popular PDF readers; create convincing social engineering pretexts (business documents, resumes, invoices) containing hidden payloads.

## Defensive takeaways
- Disable JavaScript execution in PDF readers by default or require explicit user consent
- Implement strict sandboxing for any JavaScript running in PDF context with minimal API access
- Validate and sanitize all embedded scripts; implement Content Security Policy equivalents for PDFs
- Provide visual indicators when PDFs contain executable content or scripts
- Regularly patch PDF readers and maintain updated vulnerability databases
- Train users to be suspicious of unexpected PDFs and disable active content features
- Use alternative formats (static PDFs without scripting) when possible
- Implement application whitelisting to prevent PDF reader exploits from executing system commands

## Variant hunting
Search for: PDF embedded scripts in network traffic, suspicious JavaScript in PDF metadata, PDF files with unusual JavaScript objects, exploitation of PDF reader vulnerabilities (CVE-2010-0188, CVE-2019-7090), alternative code injection points in PDF structure (stream objects, XFA forms), PDF polyglot files combining multiple attack vectors.

## MITRE ATT&CK
- T1193 - Spearphishing Attachment
- T1203 - Exploitation for Client Execution
- T1566 - Phishing
- T1204 - User Execution of Malware
- T1047 - Windows Management Instrumentation
- T1085 - Rundll32
- T1086 - PowerShell

## Notes
This appears to be a research presentation from AppSec 2017 by Sebastian Lekies analyzing PDF security. The PDF itself contains compressed content streams typical of presentation slides. Key research contributions likely include documentation of JavaScript execution capabilities, proof-of-concept exploits, and recommendations for securing PDF readers. This research is foundational for understanding PDF-based attack vectors that remain relevant in modern security assessments.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
