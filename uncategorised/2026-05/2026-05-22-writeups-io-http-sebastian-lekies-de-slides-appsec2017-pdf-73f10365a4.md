# PDF JavaScript Execution and Security Risks in Document Handlers

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Unknown - Academic/Research Presentation
- **Bounty:** No bounty (Academic research material)
- **Severity:** High
- **Vuln types:** Arbitrary Code Execution, JavaScript Execution in PDFs, Unsafe Document Processing, Embedded Malicious Scripts
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
This PDF contains embedded JavaScript functionality within the document structure, demonstrating how PDF readers can execute arbitrary code when processing malicious PDFs. The vulnerability allows attackers to leverage JavaScript execution capabilities in PDF viewers to compromise system security and user data.

## Attack scenario (step by step)
1. Attacker crafts a malicious PDF with embedded JavaScript in the /JavaScript catalog entry
2. PDF is distributed via email, file sharing, or compromised websites to target users
3. Victim opens the PDF with a vulnerable PDF reader (Adobe Reader, etc.)
4. PDF reader automatically executes the embedded JavaScript without explicit user consent
5. Malicious script performs unauthorized actions: file access, data exfiltration, exploit delivery, or privilege escalation
6. Attacker gains control over victim system or extracts sensitive information

## Root cause
PDF specification allows JavaScript execution for legitimate document automation purposes, but this feature is exploited by attackers. PDF readers fail to properly sandbox or restrict JavaScript execution, and lack adequate user warnings about code execution.

## Attacker mindset
Exploit the trust users place in document files (PDFs appear benign) combined with automatic JavaScript execution in PDF readers. Leverage the PDF format's capability to embed code as a delivery mechanism for malware, enabling targeted attacks against specific user groups via seemingly innocent documents.

## Defensive takeaways
- Disable JavaScript execution in PDF readers by default; require explicit user opt-in per document
- Implement strict sandboxing for any PDF JavaScript execution with limited API access
- Display prominent warnings when PDFs attempt to execute scripts, showing source and intent
- Keep PDF readers updated with latest security patches and disable vulnerable features
- Use alternative document formats (HTML, DOCX with proper security controls) when JavaScript is unnecessary
- Implement content security policies and restrict PDF file origins in enterprise environments
- Educate users about risks of opening PDFs from untrusted sources
- Apply principle of least privilege to PDF reader process permissions

## Variant hunting
Look for similar attack vectors in: Microsoft Office macros, Flash embedded in PDFs, OLE objects in documents, SVG files with JavaScript, XML-based document formats with script support, and browser plugins processing document formats. Search for PDF samples with JavaScript in VirusTotal using 'type:pdf javascript' queries.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution
- T1566 - Phishing (Email Attachment)
- T1204 - User Execution of Malicious File
- T1059 - Command and Scripting Interpreter (JavaScript)

## Notes
This appears to be academic research material from Sebastian Lekies on application security. The PDF itself demonstrates the vulnerability it discusses - containing JavaScript capabilities in its structure. This is a foundational attack vector still actively exploited in 2024. PDF-based attacks remain effective because users perceive PDFs as safe, read-only documents despite their scripting capabilities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
