# PDF JavaScript Execution and Security Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** AppSec 2017 Conference - Sebastian Lekies Presentation
- **Bounty:** Not specified (conference presentation/research)
- **Severity:** High
- **Vuln types:** Arbitrary Code Execution, JavaScript Execution in PDF, PDF Embedded Script Execution
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
This PDF document contains embedded JavaScript code within its structure, demonstrating the attack surface of PDF readers that execute JavaScript. The vulnerability allows attackers to embed malicious scripts within PDF files that execute when opened by vulnerable PDF readers, potentially leading to system compromise or data exfiltration.

## Attack scenario (step by step)
1. Attacker crafts a PDF document with embedded JavaScript in the /JavaScript catalog entry
2. Malicious script is encoded within the PDF stream objects with FlateDecode compression to obfuscate content
3. PDF is distributed via email, file sharing, or drive-by download to target users
4. Victim opens PDF in a vulnerable PDF reader (Adobe Reader, Firefox, etc.) that executes JavaScript
5. JavaScript executes with privileges of the PDF reader, allowing file access or system calls
6. Attacker achieves code execution, data theft, or further system compromise

## Root cause
PDF specification allows JavaScript execution within documents for interactive features. Insufficient sandboxing and overprivileged JavaScript execution in PDF readers fails to properly restrict access to file system and system APIs. Compression (FlateDecode) obfuscates malicious content from basic static analysis.

## Attacker mindset
Leveraging trusted document format (PDF) to bypass security perimeter defenses. Using legitimate PDF features (JavaScript support) as attack vector. Relying on user trust in documents and security gaps in popular PDF readers. Obfuscating payload through compression to evade detection.

## Defensive takeaways
- Disable JavaScript execution in PDF readers by default unless required
- Implement strict Content Security Policy for PDF JavaScript contexts
- Use sandboxing to isolate PDF renderer processes with minimal privileges
- Apply principle of least privilege to PDF JavaScript API access (file I/O, system calls)
- Maintain updated PDF reader software with security patches
- Implement static analysis to detect suspicious JavaScript patterns in PDFs
- Use allow-list approach for legitimate PDF features rather than block-list
- Educate users about risks of opening PDFs from untrusted sources
- Monitor and audit JavaScript execution logs in PDF readers

## Variant hunting
Search for PDFs containing /JavaScript entries in catalog, look for encoded streams with suspicious function calls (getURL, launchURL, createSocket), examine PDFs with multiple stages of obfuscation (compression + encryption), identify PDFs attempting to access file:// protocol or system APIs

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution
- T1566.001 - Phishing: Spearphishing Attachment
- T1059.007 - Command and Scripting Interpreter: JavaScript/JScript
- T1547 - Boot or Logon Autostart Execution
- T1027 - Obfuscated Files or Information

## Notes
This appears to be a PDF copy of AppSec 2017 conference slides by Sebastian Lekies on PDF security vulnerabilities. The content demonstrates research on PDF attack vectors. The binary stream data contains FlateDecode compressed content typical of PDF structures. This is educational/research material highlighting risks in PDF readers rather than an active exploit sample.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
