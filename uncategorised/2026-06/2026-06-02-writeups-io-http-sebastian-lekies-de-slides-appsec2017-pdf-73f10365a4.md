# PDF Document with Embedded JavaScript - AppSec 2017 Presentation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** N/A - Educational/Research Material
- **Bounty:** N/A
- **Severity:** MEDIUM
- **Vuln types:** Arbitrary Code Execution, PDF JavaScript Execution, Malicious Document Delivery
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
A PDF document containing embedded JavaScript code that can be executed by PDF readers, potentially allowing arbitrary code execution. This appears to be an educational presentation on PDF attack vectors at AppSec 2017. The document structure references JavaScript objects that could be leveraged for malicious purposes if crafted with malicious payloads.

## Attack scenario (step by step)
1. Attacker crafts a malicious PDF with embedded JavaScript in the /JavaScript object references
2. PDF is distributed via email or hosted on a website for download
3. Victim opens the PDF in a vulnerable PDF reader (Adobe Reader, etc.)
4. PDF reader automatically executes the embedded JavaScript without explicit user consent
5. JavaScript payload executes with the privileges of the PDF reader process
6. Attacker achieves code execution, data exfiltration, or system compromise

## Root cause
PDF specification allows embedding and execution of JavaScript code within documents. Many PDF readers enable JavaScript execution by default without requiring explicit user permission, creating an attack surface for malicious code execution.

## Attacker mindset
Target users who trust PDF documents as static content but do not realize they can contain executable code. Leverage the general perception of PDFs as safe documents to deliver malware or exploit vulnerable PDF readers. Educational/research demonstrations show proof-of-concept for security awareness.

## Defensive takeaways
- Disable JavaScript execution in PDF readers by default or require explicit user approval
- Keep PDF reader software fully patched and updated
- Implement sandboxing for PDF reader processes to limit code execution impact
- Use static content analysis tools to detect suspicious JavaScript in PDFs before opening
- Educate users that PDFs can contain executable code and should be treated with caution
- Restrict PDF reader capabilities and disable unnecessary features like external content loading

## Variant hunting
Search for PDFs with /JavaScript objects, /AcroForm fields, /OpenAction triggers, embedded Flash objects, or suspicious /EmbeddedFile references. Look for PDFs that auto-execute on open or contain obfuscated JavaScript code using filters like FlateDecode or ASCII85Decode.

## MITRE ATT&CK
- T1566.001
- T1203
- T1204.002
- T1059.007

## Notes
This appears to be educational/research material from a security conference presentation, not an actual vulnerability report. The PDF structure is typical for presentations with FlateDecode streams and JavaScript references. Real-world exploitation depends on PDF reader vulnerabilities and user interaction. Sebastian Lekies is a known researcher in PDF security attack vectors.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
