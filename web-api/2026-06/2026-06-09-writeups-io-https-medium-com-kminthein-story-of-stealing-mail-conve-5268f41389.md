# Stored XSS in Mail.ru and myMail iOS Applications via SVG File Upload

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Mail.ru
- **Bounty:** $1000
- **Severity:** Critical
- **Vuln types:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Unsafe File Upload, Cross-Application Scripting (CAS)
- **Category:** web-api
- **Writeup:** https://medium.com/kminthein/story-of-stealing-mail-conversation-contacts-in-mail-ru-and-mymail-ios-applications-via-xss-1e49c4ed560

## Summary
A stored XSS vulnerability in Mail.ru and myMail iOS applications (v12.2.1) allowed attackers to inject malicious JavaScript code via crafted SVG image files. When users viewed the malicious SVG attachment, the JavaScript would execute with application privileges, enabling exfiltration of sensitive data including email conversations, contacts, and payment information from the application's SQLite database.

## Attack scenario (step by step)
1. Attacker crafts a malicious SVG file containing embedded JavaScript code that accesses the file system
2. Attacker sends the SVG file as an email attachment to a target Mail.ru/myMail user
3. Target user opens the email and views/previews the SVG image attachment within the application
4. The malicious JavaScript executes in the context of the Mail.ru application, bypassing sandbox restrictions
5. The script discovers the application's data directory path and locates the mail_cache.sq3 SQLite database
6. The entire database file containing emails, contacts, and sensitive data is exfiltrated to the attacker's server

## Root cause
The application failed to properly validate and sanitize SVG file uploads before rendering them. SVG files were processed as trusted content without restricting script execution, allowing embedded JavaScript to execute within the application's security context with access to local file systems.

## Attacker mindset
The researcher demonstrated sophisticated persistence and technical depth by: (1) recognizing that basic XSS impact would be dismissed, (2) conducting extensive file system reconnaissance to identify high-value targets, (3) using XSS itself to dynamically discover application paths, (4) developing a working exploit despite technical obstacles, and (5) creating a complete data exfiltration proof-of-concept rather than settling for theoretical impact.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) to prevent inline script execution in file attachments
- Sanitize and validate all uploaded files, particularly media files like SVG that can contain scripts
- Use sandboxed contexts for rendering untrusted content (iframes with restricted permissions)
- Disable scripting in SVG renderers or use specialized SVG parsers that strip executable content
- Apply principle of least privilege - limit file system access from web/attachment contexts
- Implement proper access controls on sensitive SQLite databases
- Use code signing and integrity verification for local files
- Conduct security testing of file upload and rendering mechanisms across all file types
- Monitor and log file access patterns for anomalies

## Variant hunting
['Test other vector-based file formats (PDF, EPS, XAML) for similar script injection vulnerabilities', 'Check if other Mail.ru properties (VK.com, etc.) have similar SVG processing vulnerabilities', 'Investigate whether other messaging/email iOS apps have similar file upload validation issues', 'Test polyglot files (SVG + image) that may bypass file type validation', 'Check if server-side email rendering also processes SVG with script execution', 'Test if other XML-based formats (XML, SOAP) allow script injection in the same application', 'Investigate attachment preview functionality across different content types']

## MITRE ATT&CK
- T1190
- T1199
- T1566.001
- T1059.007
- T1005
- T1020
- T1041

## Notes
The vulnerability demonstrates the critical security risk of rendering untrusted file formats within mobile applications. Notable aspects: (1) Mail.ru disputed the classification as 'Stored XSS' vs 'Cross-Application Scripting', suggesting potential disagreement on vulnerability taxonomy; (2) The researcher's use of a jailbroken iPhone to understand the file system structure was crucial for developing a real-world impact PoC; (3) The ability to dynamically discover file paths via XSS itself shows sophisticated exploit chaining; (4) Affecting 100+ million users made this a high-impact vulnerability; (5) The $1000 bounty appears low given the severity and scope of the vulnerability.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
