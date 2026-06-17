# PDF Security Analysis - AppSec 2017 Presentation by Sebastian Lekies

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Unknown - Academic/Conference Materials
- **Bounty:** None - Educational content
- **Severity:** Medium
- **Vuln types:** Embedded JavaScript in PDF, Potential PDF Exploit Vector, Client-side Code Execution
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
A PDF presentation file contains embedded JavaScript objects within its structure, potentially allowing execution of malicious scripts when opened in vulnerable PDF readers. The presence of /JavaScript references and Names dictionary indicates the PDF was designed to demonstrate PDF security vulnerabilities or attack techniques at AppSec 2017.

## Attack scenario (step by step)
1. Attacker crafts a malicious PDF with embedded JavaScript in the document catalog and object streams
2. Victim opens the PDF in a vulnerable PDF reader application (Adobe Reader, etc.)
3. PDF reader automatically parses and executes the embedded JavaScript without user consent
4. JavaScript payload gains access to victim's filesystem, network resources, or local system depending on reader permissions
5. Attacker exfiltrates sensitive data or delivers additional malware payloads
6. Attack leaves minimal forensic evidence as it occurs during normal PDF viewing

## Root cause
PDF specification allows embedding of JavaScript code which PDF readers may execute with insufficient sandboxing or security controls. The /Names dictionary with /JavaScript references enables automatic script execution. Legacy PDF readers often prioritize compatibility over security, executing embedded scripts with high privileges.

## Attacker mindset
Exploit trust users place in PDF documents combined with weak sandbox implementations in popular PDF readers. Use PDF as a delivery mechanism for sophisticated attacks since it appears benign. Target users who disable JavaScript in browsers but have it enabled in PDF readers.

## Defensive takeaways
- Disable JavaScript execution in PDF readers by default
- Implement strict Content Security Policy for PDF processing
- Use sandboxed PDF rendering engines with minimal privilege escalation paths
- Prompt users before executing any scripts embedded in PDF documents
- Keep PDF reader software updated to patch JavaScript execution vulnerabilities
- Educate users about PDF security risks and suspicious document sources
- Use alternative formats (static images, HTML) when JavaScript functionality is not required
- Monitor PDF readers for suspicious object streams and JavaScript references

## Variant hunting
Search for PDFs with: (1) /JavaScript references in Names dictionary, (2) AA (Additional Actions) dictionaries with event triggers, (3) OpenAction triggers that execute on document open, (4) Embedded Flash objects in PDF streams, (5) Launch actions pointing to executables, (6) Form XDP/XFA components with script execution, (7) Suspicious stream filters combined with JavaScript objects

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204.002 - User Execution: Malicious File
- T1566.001 - Phishing: Spearphishing Attachment
- T1203 - Exploitation for Client Execution
- T1559.003 - Inter-Process Communication: Distributed Component Object Model

## Notes
This appears to be Sebastian Lekies' presentation material on PDF vulnerabilities from AppSec 2017. The PDF itself demonstrates the vulnerability it discusses - containing JavaScript objects in its structure. This is educational content meant to illustrate real attack vectors. Not an actual bug bounty submission but rather security research documentation. The FlateDecode compression obscures the exact JavaScript payload, but the presence of /JavaScript names and structured object references indicates intentional demonstration of PDF exploitation techniques.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
