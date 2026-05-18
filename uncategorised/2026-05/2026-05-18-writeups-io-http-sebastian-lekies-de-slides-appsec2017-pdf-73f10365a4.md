# PDF-based Attack Surface Analysis - AppSec 2017

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Unknown (Academic/Conference Presentation)
- **Bounty:** N/A - Research/Educational
- **Severity:** MEDIUM
- **Vuln types:** Arbitrary Code Execution, PDF JavaScript Execution, Malicious PDF Delivery
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
This PDF document contains embedded JavaScript capabilities through the /Names dictionary with /JavaScript reference, demonstrating the attack surface of PDF readers that execute embedded scripts. The document structure shows how PDF files can be weaponized to execute arbitrary code when opened in vulnerable PDF viewers. Sebastian Lekies' AppSec 2017 presentation discusses PDF-based attack vectors and exploitation techniques.

## Attack scenario (step by step)
1. Attacker crafts malicious PDF with JavaScript embedded in the /Names /JavaScript object structure
2. Attacker distributes PDF via email, watering hole, or malicious download link
3. Target opens PDF in vulnerable PDF reader (Adobe Reader, older versions)
4. PDF reader automatically parses and executes embedded JavaScript without user confirmation
5. Malicious script gains execution context with user privileges and PDF reader permissions
6. Attacker achieves code execution, data exfiltration, or system compromise

## Root cause
PDF specification allows embedded JavaScript execution through /JavaScript names dictionary entry. PDF readers traditionally auto-execute scripts without sufficient security checks or user warnings. FlateDecode compressed streams obscure malicious payloads from static analysis.

## Attacker mindset
Leverage trusted document format (PDF) as delivery mechanism for code execution. PDFs appear innocuous and are commonly used in business/educational contexts, bypassing user suspicion. JavaScript in PDFs executes in privileged context with access to file system and system functions depending on reader permissions and settings.

## Defensive takeaways
- Disable JavaScript execution in PDF readers by default or require explicit user consent
- Implement strict Content Security Policy for PDF rendering engines
- Validate and sandbox PDF JavaScript execution environment
- Use updated PDF readers with security patches against known JavaScript exploits
- Implement application-level checks to detect suspicious PDF structures before opening
- Monitor for unusual PDF characteristics (embedded scripts, large streams, suspicious object references)
- Educate users on risks of opening PDFs from untrusted sources
- Consider blocking JavaScript entirely in PDF readers if business use case permits

## Variant hunting
['Search for PDFs with /JavaScript in /Names dictionary across internal document repositories', 'Hunt for PDF files with FlateDecode compressed streams containing JavaScript keywords', 'Monitor email gateways for PDFs with embedded script objects', 'Analyze PDF metadata and catalog structures for obfuscation techniques', 'Test PDF readers against malicious samples to identify exploit chains', 'Examine alternative JavaScript delivery in PDFs: /AA (additional actions), /OpenAction, form XFA scripts']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.001 - Phishing: Spearphishing Attachment
- T1203 - Exploitation for Client Execution
- T1204.002 - User Execution: Malicious File
- T1059.007 - Command and Scripting Interpreter: JavaScript
- T1218 - System Binary Proxy Execution

## Notes
This appears to be a research presentation document rather than a traditional bug bounty report. The PDF itself demonstrates PDF attack surface through its structural composition. Real-world exploitation depends on PDF reader version, security settings, and operating system. Adobe Reader has historically been primary target due to market share and feature-rich JavaScript engine.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
