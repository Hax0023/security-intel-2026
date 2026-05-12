# XSS in PDF Viewer via CVE-2018-5158 (Outdated PDF.js)

## Metadata
- **Source:** HackerOne
- **Report:** 819863 | https://hackerone.com/reports/819863
- **Submitted:** 2020-03-16
- **Reporter:** skewbed
- **Program:** Unknown (HackerOne report 819863)
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Arbitrary Code Execution, Insecure Library Version
- **CVEs:** CVE-2020-8155, CVE-2018-5158
- **Category:** web-api

## Summary
An outdated version of PDF.js library used in the application's PDF viewer is vulnerable to CVE-2018-5158, allowing attackers to execute arbitrary JavaScript code through a malicious PDF file. The vulnerability has been confirmed working in Safari 13.0.5 and Firefox 74.0, enabling XSS attacks when users view crafted PDF documents.

## Attack scenario
1. Attacker crafts a malicious PDF file embedding JavaScript payload that exploits CVE-2018-5158 vulnerability in PDF.js
2. Attacker distributes the PDF through email, social engineering, or malicious links targeting application users
3. User opens the malicious PDF in the application's web-based PDF viewer
4. PDF.js processes the document and fails to properly sanitize the malicious payload
5. JavaScript payload executes in the context of the user's browser session with access to the application's DOM and cookies
6. Attacker can steal session tokens, perform unauthorized actions, or redirect user to malicious sites

## Root cause
The application uses an outdated version of PDF.js library (vulnerable to CVE-2018-5158) without proper input validation or sandboxing. The vulnerability exists in PDF.js's handling of embedded JavaScript in PDF documents, allowing script execution without adequate security controls.

## Attacker mindset
Opportunistic attacker leveraging known public vulnerability (CVE-2018-5158) to compromise users through trusted document format. The use of PDF as attack vector exploits user trust in documents and bypasses some security perceptions.

## Defensive takeaways
- Immediately upgrade PDF.js library to a patched version that addresses CVE-2018-5158
- Implement a Software Composition Analysis (SCA) tool to track vulnerable dependencies and receive security alerts
- Disable JavaScript execution in PDF viewer if not required for functionality
- Implement strict Content Security Policy (CSP) headers to prevent inline script execution
- Run PDF viewer in a sandboxed iframe with minimal permissions
- Validate and sanitize all PDF content before rendering
- Implement regular security audits and dependency updates as part of CI/CD pipeline
- Monitor browser console and network logs for suspicious activity during PDF rendering

## Variant hunting
Search for other outdated JavaScript libraries used for document processing (e.g., older versions of pdf-lib, pdfkit). Check for similar version-based vulnerabilities in other PDF viewers or document processing tools. Test whether other embedded content types (SVG, images with metadata) have similar execution paths.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (JavaScript)
- T1566 - Phishing (PDF attachment delivery)
- T1203 - Exploitation for Client Execution
- T1041 - Exfiltration Over C2 Channel

## Notes
Reporter noted that CORS policy blocked attempts to fetch external code, indicating some security controls were in place but insufficient. The vulnerability's cross-browser behavior (working in Safari/Firefox but not Chrome) suggests browser-specific PDF handling differences. Reporter was unable to test against desktop client, which may have different implications. Public PoC available from Mozilla bug tracker indicates widespread awareness of vulnerability.

## Full report
<details><summary>Expand</summary>

An outdated version of PDF.js in use allows for the CVE-2018-5158 vulnerability.

When the payload PDF is shown in the supplied PDF viewer, it can execute arbitrary JavaScript.

I have tested the payload PDF, and it is working in the Safari 13.0.5 (the latest version) and Firefox 74.0 (the latest version). Although, it does not work in the latest version of Chrome.

I could not find a way to test it on the desktop client. I assume that it would use the system PDF viewer.

Modifying the payload to fetch other code was luckily blocked because of a CORS policy.

The payload is from [https://bugzilla.mozilla.org/show_bug.cgi?id=1452075](https://bugzilla.mozilla.org/show_bug.cgi?id=1452075).
I have also included the PDF in the attachments.

The payload can be seen in action by checking the JavaScript console. It says "Hello, this is code running in" followed by the path to file where the vulnerability is.

## Impact

An attacker could execute arbitrary JavaScript code on a web browser when a PDF containing an exploit is opened.

</details>

---
*Analysed by Claude on 2026-05-12*
