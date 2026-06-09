# PDF-based Attack Vector Analysis - AppSec 2017

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Unknown - Academic/Conference Presentation
- **Bounty:** N/A - Research/Educational Content
- **Severity:** HIGH
- **Vuln types:** Arbitrary JavaScript Execution, PDF Embedded Script Execution, Client-side Code Injection
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
This appears to be a presentation on PDF-based security vulnerabilities, specifically demonstrating how JavaScript can be embedded within PDF documents to execute arbitrary code. The PDF contains embedded JavaScript objects (reference 3 0 R in the Names dictionary) that enable script execution when the document is opened in vulnerable PDF readers.

## Attack scenario (step by step)
1. Attacker crafts a malicious PDF document with embedded JavaScript code in the /JavaScript object dictionary
2. Victim receives the PDF via email or downloads it from a compromised website
3. Victim opens the PDF in a vulnerable PDF reader (Adobe Reader, Firefox, Chrome, etc.)
4. The PDF reader automatically executes the embedded JavaScript without user consent or warning
5. JavaScript payload executes with the privileges of the PDF reader process, potentially accessing sensitive data or executing system commands
6. Attacker gains code execution, data exfiltration, or system compromise depending on payload and reader sandbox strength

## Root cause
PDF specification allows embedding and automatic execution of JavaScript objects. PDF readers by default execute scripts without explicit user consent or adequate sandboxing. The /Names dictionary references JavaScript objects that trigger execution upon document load or user interaction.

## Attacker mindset
An attacker would recognize PDFs as trusted file formats with high delivery success rates. By embedding malicious scripts, they bypass email filters and user suspicion. The attack is particularly effective because users expect PDFs to be passive documents. JavaScript in PDFs can interact with the file system, network, and external applications, making it a powerful vector for espionage or malware delivery.

## Defensive takeaways
- Disable JavaScript execution in PDF readers (Adobe Reader, browser PDF plugins) by default
- Implement strict Content Security Policy and sandboxing for PDF rendering engines
- Use updated PDF readers with security patches and disabled scripting features
- Educate users about the risks of opening PDFs from untrusted sources
- Implement email gateway filtering for suspicious PDF attachments with embedded scripts
- Use PDF analysis tools to detect and strip embedded JavaScript before user delivery
- Require explicit user confirmation before executing any scripts in PDFs
- Deploy EDR/XDR solutions to detect suspicious JavaScript execution from PDF processes

## Variant hunting
['Search for other PDF embedded object types: /Flash, /XObject, /RichMedia for similar exploitation patterns', 'Investigate PDF form submission features that could exfiltrate data or execute actions', 'Test PDF readers with OpenAction triggers that execute automatically without /JavaScript explicit calls', "Research PDF 'Launch' actions that can execute external applications or system commands", 'Examine PDF 3D annotations and embedded media handlers for code execution vectors', 'Test cross-origin resource requests from embedded PDFs for CORS bypass', 'Analyze Go/GoTo actions in PDF bookmarks for navigation-based exploitation']

## MITRE ATT&CK
- T1190
- T1204.002
- T1566.001
- T1059.007
- T0801

## Notes
This appears to be content from Sebastian Lekies' AppSec 2017 presentation on browser and PDF security. The PDF structure clearly shows JavaScript object references in the catalog. This represents a well-documented but still actively exploited vulnerability class. Modern PDF readers have largely mitigated this through sandboxing and script disabling, but legacy systems and misconfigured readers remain vulnerable. The presentation likely demonstrates the PDF format's inherent risks when processing is done without proper security controls.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
