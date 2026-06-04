# PDF-based JavaScript Execution and Client-Side Security Vulnerabilities

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** AppSec 2017 Conference Presentation (Research/Educational)
- **Bounty:** Not Applicable - Academic Research Presentation
- **Severity:** HIGH
- **Vuln types:** Arbitrary Code Execution, JavaScript Injection in PDF, Client-Side Attack Vector, Unsafe PDF Handling
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
This PDF document contains embedded JavaScript capabilities through the PDF catalog structure, demonstrating how malicious actors can embed executable code within PDF files to compromise client systems. The presentation by Sebastian Lekies appears to focus on application security vulnerabilities related to PDF handling and JavaScript execution in PDF viewers.

## Attack scenario (step by step)
1. Attacker crafts a PDF file with embedded JavaScript in the /Names dictionary and /JavaScript object reference
2. PDF is distributed via email or hosted on a website, appearing as a legitimate document
3. Victim opens the PDF in a vulnerable PDF reader (Adobe Reader, browser-based PDF viewer, etc.)
4. PDF viewer automatically executes the embedded JavaScript code without explicit user consent
5. Malicious script gains access to local system functions, file system, or sensitive data available to the PDF viewer process
6. Attacker achieves code execution, data exfiltration, or system compromise depending on JavaScript capabilities and sandbox restrictions

## Root cause
PDF specification allows embedding JavaScript through the /JavaScript name tree and object references. PDF viewers may auto-execute scripts without proper sandboxing or user prompts. Insufficient input validation and overly permissive JavaScript APIs in PDF readers enable malicious code execution with elevated privileges.

## Attacker mindset
Leverage widely-trusted file formats (PDFs) to bypass user suspicion. Exploit the gap between user expectations (PDFs as passive documents) and technical reality (executable code containers). Target PDF reader vulnerabilities to achieve arbitrary code execution with minimal user interaction. Use social engineering to distribute malicious PDFs disguised as legitimate business documents.

## Defensive takeaways
- Disable JavaScript execution in PDF readers by default; require explicit user enablement per document
- Implement strict Content Security Policy for PDF JavaScript execution with minimal API surface
- Sandbox PDF viewer processes with reduced file system and system call access
- Implement code signing and integrity verification for embedded scripts in PDFs
- Deploy application whitelisting to restrict executable code execution from PDF processes
- Educate users about PDF security risks and the dangers of opening unsolicited PDF attachments
- Keep PDF viewers patched with latest security updates addressing JavaScript execution vulnerabilities
- Use alternative formats (HTML, Office documents with macros disabled) for sensitive document distribution

## Variant hunting
Search for other embedded objects in PDFs: /Flash, /XObject, /Launch actions, /SubmitForm, /ImportData, /EmbeddedFile. Investigate PDF readers beyond Adobe Reader (Firefox, Chrome, Safari viewers). Research PDF form-based attacks using /AcroForm fields. Analyze file type confusion attacks combining PDF with other formats. Examine PDF annotation-based code execution vectors.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution
- T1566.001 - Phishing: Spearphishing Attachment
- T1204.002 - User Execution: Malicious File
- T1547 - Boot or Logon Autostart Execution
- T1059.007 - Command and Scripting Interpreter: JavaScript

## Notes
This appears to be a research/educational presentation on PDF security rather than a traditional bug bounty write-up. The PDF structure shows compressed content streams typical of Google Slides exports. The presentation likely detailed methods for exploiting PDF readers and JavaScript execution vulnerabilities. Sebastian Lekies is known for research on browser and client-side security. The document itself demonstrates the attack vector it likely discusses - a PDF containing executable content.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
