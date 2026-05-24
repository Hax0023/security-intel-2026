# SVG File Upload XSS Vulnerability via HTML Elements in Concrete5 File Manager

## Metadata
- **Source:** HackerOne
- **Report:** 437863 | https://hackerone.com/reports/437863
- **Submitted:** 2018-11-09
- **Reporter:** hexife
- **Program:** Concrete5
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), File Upload Validation Bypass, Stored XSS
- **CVEs:** None
- **Category:** web-api

## Summary
Concrete5's file upload whitelist permits SVG files, but SVG format supports HTML elements including script tags. An attacker with administrator privileges can upload malicious SVG files containing embedded HTML/JavaScript that executes when the SVG is accessed directly in a browser, bypassing HTML upload restrictions. This results in stored XSS vulnerability within the application.

## Attack scenario
1. Attacker with administrator access creates a malicious SVG file containing HTML script tags with JavaScript payload
2. Attacker navigates to File Manager and uploads the crafted SVG file through the standard file upload interface
3. SVG file passes whitelist validation as it has permitted .svg extension despite containing dangerous HTML content
4. Attacker embeds or references the uploaded SVG file in application content (e.g., portfolio slides, image includes)
5. When legitimate users access the page containing the SVG reference or view the SVG directly, the browser executes embedded JavaScript
6. Attacker achieves arbitrary JavaScript execution, enabling session hijacking, credential theft, or malware distribution

## Root cause
Concrete5 implements file extension-based whitelist validation without inspecting file content. SVG format specification allows HTML elements including script tags, but this W3C-compliant feature was not considered during whitelist design. The application does not sanitize SVG content or enforce Content-Type headers that would prevent script execution.

## Attacker mindset
Administrator-level attacker recognizes that while HTML uploads are blocked, SVG format legitimately permits HTML content per W3C standards. This allows bypassing file type restrictions while maintaining plausible deniability. The attacker exploits the gap between file extension filtering and actual file content capabilities.

## Defensive takeaways
- Implement content-based file validation in addition to extension whitelisting (verify MIME type and file structure)
- Parse and sanitize SVG files to remove potentially dangerous elements (script, style, event handlers, foreign HTML elements)
- Serve uploaded SVG files with Content-Type: image/svg+xml and X-Content-Type-Options: nosniff headers to prevent script execution
- Use Content Security Policy (CSP) headers to restrict script execution from uploaded content
- Implement file upload sandboxing and serve user-uploaded content from separate domain to contain XSS impact
- Restrict file upload privileges to appropriate user roles only; avoid permitting administrators unrestricted file upload capabilities
- Conduct security review of all whitelisted file formats for unexpected embedded executable content capabilities

## Variant hunting
Similar bypass patterns exist in other applications: PDF files with embedded JavaScript, ZIP archives containing executable scripts, Office documents with macros, and other container formats. Any format that permits executable content (scripts, embedded objects) while having a seemingly 'safe' extension should be audited. Look for applications whitelisting: DOCX, XLSX, PDF, SVG, XML, WEBP with embedded content execution paths.

## MITRE ATT&CK
- T1190
- T1071
- T1566

## Notes
Report demonstrates practical exploitation through Concrete5's portfolio/slides feature. The vulnerability is particularly dangerous for administrator-class attackers as they have legitimate platform access. The W3C reference in the report strengthens the argument that SVG's HTML capability is intentional design, not accidental. Concrete5 likely patched this by implementing SVG sanitization libraries. The fix should remove dangerous elements while preserving legitimate SVG rendering capability.

## Full report
<details><summary>Expand</summary>

Concrete5 has the whitelist for restricting that malicious file is uploaded.
( concrete/config/concrete.php, Line no. 86~88 )

The extension whitelist allows to upload SVG file.

However, SVG can has the HTML elements in its code.
(Ref. https://www.w3.org/TR/SVG2/intro.html#W3CCompatibility )

If web browser accesses the SVG file that has the 'script' tag of HTML element  directly,
browser executes the JavaScript placed in SVG file.

Example SVG file likes below.
```
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 105">
<html><head><title>test</title></head><body><script>alert('xss');</script></body></html>
</svg>
```
It can be occur the XSS vulnerability.


* Test Scenario

1. Make the SVG
{F373015}

2. Login as administrator and select the File Manager feature.

3. Upload the file we made.
{F373008}

4. We can check the upload path in "Right click -> Properties"
{F373009}

5. For the test to triggering SVG file, we edit portfolio section.
Move to "portfolio > project Title #" and Edit / Add slides like this.
{F373010}

6. We can confirmed the execution of JavaScript in the SVG file.
{F373011}

Thank you for reading my report.

PS.
When I was the kid, My father gave me the crayon as the Christmas gift.

## Impact

Concrete5 prohibited  the upload the HTML files, but this method is bypass the file upload filtering.
Attacker who got the administrator authority can inject and hide malicious html tags to target service.

</details>

---
*Analysed by Claude on 2026-05-24*
