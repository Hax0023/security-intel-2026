# PDF JavaScript Execution and Security Analysis (AppSec 2017)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Academic/Security Research - Sebastian Lekies AppSec 2017
- **Bounty:** N/A - Academic Research
- **Severity:** HIGH
- **Vuln types:** Arbitrary Code Execution, JavaScript Execution in PDF, Unsafe PDF Features
- **Category:** uncategorised
- **Writeup:** http://sebastian-lekies.de/slides/appsec2017.pdf

## Summary
This PDF presentation appears to contain embedded JavaScript objects within the PDF structure, demonstrating attack vectors through PDF JavaScript execution capabilities. The presentation likely covers vulnerabilities in how PDF readers handle JavaScript within PDF documents, enabling arbitrary code execution on systems that process untrusted PDFs.

## Attack scenario (step by step)
1. Attacker crafts a malicious PDF containing JavaScript within the /JavaScript object reference in the PDF catalog
2. Victim opens the PDF in a vulnerable PDF reader (Adobe Reader, Foxit, etc.) that enables JavaScript execution
3. PDF reader automatically executes embedded JavaScript without user awareness or consent
4. JavaScript payload accesses file system, exfiltrates data, or installs malware on victim's machine
5. Attack succeeds silently with limited user-visible indicators of compromise
6. Attacker maintains persistence or completes data theft objective

## Root cause
PDF specification includes JavaScript support for interactive features, but PDF readers often execute JavaScript with insufficient sandboxing and without explicit user permission, creating an execution environment with access to system resources.

## Attacker mindset
Attacker seeks to weaponize PDF delivery mechanism as trusted document format to bypass user suspicion, exploiting automatic JavaScript execution to achieve code execution on high-value targets (enterprises, governments) through spear-phishing or watering hole attacks.

## Defensive takeaways
- Disable JavaScript execution in PDF readers by default, require explicit user opt-in
- Implement strict sandboxing for all JavaScript executed within PDF context
- Use allowlisting for JavaScript APIs available to PDF scripts, restrict file system access
- Implement Content Security Policy-like restrictions for PDF JavaScript
- Educate users about risks of opening untrusted PDF documents
- Apply security patches promptly for PDF reader vulnerabilities
- Use alternative document formats without embedded scripting capabilities
- Deploy endpoint detection to monitor suspicious PDF reader behavior
- Implement application whitelisting to restrict PDF reader execution scope

## Variant hunting
Hunt for: PDFs with /JavaScript references in catalog or page annotations; PDFs using /OpenAction or /AA (additional actions) with JavaScript; PDFs with obfuscated JavaScript payloads; PDFs exploiting PDF specification edge cases in JavaScript APIs; PDFs chaining multiple JavaScript handlers; Polymorphic PDF structures evading static detection

## MITRE ATT&CK
- T1190
- T1566.001
- T1204.002
- T1059.007
- T1547
- T1218

## Notes
Sebastian Lekies is prominent security researcher specializing in web and application security. This appears to be a research presentation on PDF security rather than disclosure of new vulnerability. The raw PDF structure shows typical obfuscated content streams (FlateDecode compression). JavaScript in PDFs represents significant attack surface often overlooked by end users who perceive PDFs as passive document format.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
