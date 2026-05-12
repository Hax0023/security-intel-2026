# Remote Code Execution via Malicious Image Upload in Basecamp Profile Image Function

## Metadata
- **Source:** HackerOne
- **Report:** 365271 | https://hackerone.com/reports/365271
- **Submitted:** 2018-06-13
- **Reporter:** gammarex
- **Program:** Basecamp
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Arbitrary File Upload, Remote Code Execution, Insufficient Input Validation, Insecure Deserialization, Command Injection
- **CVEs:** CVE-2017-8291
- **Category:** memory-binary

## Summary
Basecamp's profile image upload function accepts PostScript/EPS files renamed as .gif without proper validation, which are processed by ImageMagick/GraphicsMagick and passed to Ghostscript. A vulnerability in the Ghostscript version (CVE-2017-8291) allows remote command execution through specially crafted PostScript files. An attacker can upload a malicious image file to gain arbitrary code execution on the server.

## Attack scenario
1. Attacker crafts a malicious PostScript/EPS file containing shell commands (e.g., ping command or reverse shell)
2. Attacker renames the PostScript file with a .gif extension to bypass basic file type checks
3. Attacker uploads the disguised file through Basecamp's profile image upload feature
4. Server-side image processing triggers ImageMagick/GraphicsMagick to process the file
5. ImageMagick detects PostScript magic header ('%!') and delegates to Ghostscript for interpretation
6. Vulnerable Ghostscript version executes the embedded shell commands, providing attacker with remote code execution

## Root cause
Multiple security failures: (1) No magic byte/file signature validation on uploaded files, (2) Reliance on file extension (.gif) for type detection, (3) Unsafe delegation to Ghostscript without security restrictions, (4) Use of vulnerable Ghostscript version with CVE-2017-8291 command execution flaw

## Attacker mindset
Attacker identifies that image upload endpoints often lack robust validation and discovers that ImageMagick processes multiple file formats including PostScript. Attacker leverages known Ghostscript CVE to achieve RCE with minimal interaction—just uploading a file with correct extension.

## Defensive takeaways
- Validate uploaded files by magic bytes/file signatures, not just extensions
- Implement strict file type allowlisting for uploads
- Disable PostScript/EPS/vector format processing in ImageMagick via policy.xml (disable 'PS', 'EPS', 'PDF')
- Keep all image processing libraries and dependencies (ImageMagick, Ghostscript) fully patched
- Run image processing in isolated/sandboxed environment with minimal privileges
- Use safe image processing libraries or cloud services (AWS Rekognition, Cloudinary) instead of local ImageMagick
- Implement Content-Security-Policy and serve uploaded content from separate domain
- Log and monitor file upload activities for suspicious patterns

## Variant hunting
Search for similar upload functionality in other Basecamp products or integrations; test other file formats that might bypass extension checks (TIFF, SVG, PDF); investigate if other image processing endpoints exist; check for similar ImageMagick delegation vulnerabilities in competing services

## MITRE ATT&CK
- T1190
- T1199
- T1566
- T1203
- T1059

## Notes
This vulnerability chain exploits trust assumptions at multiple layers: file extension trust, format detection trust, and library security. The use of deprecated/vulnerable Ghostscript functionality for image conversion is a known ImageMagick security anti-pattern. CVE-2017-8291 demonstrates how 'feature' complexity in image libraries can create exploitation pathways. Report demonstrates excellent security research by showing PoC and providing clear remediation steps.

## Full report
<details><summary>Expand</summary>

A critical flaw in Basecamp's profile image upload function leads to remote command execution. Images are converted on the server side, but not only image files but also PostScript/EPS files are accepted (if renamed to .gif). This is probably due to ImageMagick / GraphicsMagick being used for image conversion, which calls a PostScript interpreter (Ghostscript) if the input file starts with '%!'. The used Ghostscript version however has a security bug (CVE-2017-8291) leading to remote command execution.

/Proof of concept/: Upload the attached rce.gif file as profile image (change the `ping -c1 attacker.com' to some other shell command).

/Mitigation/: Upgrade Ghostscript; also, before processing uploaded images make sure they are real image files (e.g. based on magic header)

## Impact

Gain a remote shell; from here start exploitation/privilege escalation

</details>

---
*Analysed by Claude on 2026-05-11*
