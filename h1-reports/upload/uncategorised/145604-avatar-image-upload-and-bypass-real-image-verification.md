# Avatar Image Upload - Bypass Image Verification and Upload Arbitrary File Types

## Metadata
- **Source:** HackerOne
- **Report:** 145604 | https://hackerone.com/reports/145604
- **Submitted:** 2016-06-18
- **Reporter:** dremos
- **Program:** HackerOne (self-hosted/private program)
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Arbitrary File Upload, Insufficient File Type Validation, Magic Number/MIME Type Bypass, Remote Code Execution (potential)
- **CVEs:** None
- **Category:** uncategorised

## Summary
The avatar upload functionality in /core/controller/avatarcontroller.php performs insufficient MIME type validation, allowing attackers to upload PHP files disguised as JPEG/PNG images. While the uploaded file is renamed on the server (mitigating immediate RCE risk), the underlying validation can be bypassed by embedding executable code within valid image files.

## Attack scenario
1. Attacker creates a polyglot file containing valid JPEG data with embedded PHP code (e.g., phpinfo())
2. The malicious file passes MIME type validation because it legitimately identifies as image/jpeg
3. Attacker uploads the file through the avatar upload form in the web application
4. File is stored on the server (currently mitigated by automatic renaming to avatar_upload)
5. If web server is misconfigured or if file is renamed with executable extension, PHP code could execute
6. Attacker achieves remote code execution or information disclosure through embedded PHP functions

## Root cause
The application relies solely on MIME type checking via the `$image->mimeType()` function without validating file content or using additional verification methods. MIME type can be spoofed by embedding PHP code within valid image data, or by manipulating file headers. No restriction on actual file extension is enforced during upload.

## Attacker mindset
An attacker recognizes that image verification is weak and attempts to create polyglot files that are valid images while containing executable code. The attacker understands that MIME type detection can be bypassed and explores whether file renaming protections can be circumvented through server misconfiguration or application logic flaws.

## Defensive takeaways
- Implement multi-layered file validation: check MIME type, magic bytes/file signatures, and file extension independently
- Use binary content inspection libraries to verify actual file type, not just headers
- Store uploaded files outside webroot or in a directory with execution disabled (disable PHP execution)
- Implement strict Content-Type headers for uploaded files (e.g., Content-Disposition: attachment)
- Use allowlist approach for file extensions rather than blocklist
- Re-encode/sanitize images using image processing libraries (GD, ImageMagick) to remove embedded code
- Apply principle of least privilege: never allow arbitrary file execution in upload directories
- Log and monitor suspicious upload patterns (polyglot files, large image files, multiple uploads)

## Variant hunting
Check if other file upload forms (profile pictures, documents, etc.) have similar MIME validation gaps
Test for double extension bypass (e.g., file.php.jpg) in the upload mechanism
Verify if uploaded files can be accessed with different extensions (e.g., avatar_upload.php if file structure allows)
Investigate if image processing libraries are used; unpatched image libraries can execute code
Check for null byte injection if older PHP versions are used
Test SVG upload if accepted, as SVG can contain JavaScript
Examine if uploaded files inherit executable permissions from parent directory

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1105 - Ingress Tool Transfer
- T1059 - Command and Scripting Interpreter
- T1608 - Obtain Capabilities (upload malicious file)
- T1027 - Obfuscated Files or Information (polyglot files)

## Notes
The researcher notes that current server-side renaming (to 'avatar_upload') provides temporary mitigation against direct code execution, but the fundamental vulnerability remains exploitable if: (1) web server configuration allows execution in upload directory, (2) file renaming logic changes, or (3) race conditions exist. This is a classic example of relying on filename obfuscation rather than proper security controls. The vulnerability demonstrates the danger of single-factor file validation and highlights that MIME type alone is insufficient for security-critical file uploads.

## Full report
<details><summary>Expand</summary>

Hi

We can bypass Avatar Upload image verification and extension  uploading a php file or any other extension binding a valide  jpeg image  , there is no risk for the moment because the avatar is renamed to avatar_upload on the remote server , but it ll be nice to secure this part of code .

Example  
---------------
here is the same file with two different extension : 

http://91.121.108.101/image1.jpg
http://91.121.108.101/image1.php      <== execute php code inside the image 

1) download image1.jpg

2) as you can see  if you open the file image1.jpg  file on notepad it hide php code ( phpinfo(); function in this case .

3) rename image1.jpg to image1.php  , and try to upload it on the avatar upload form , it pass the verification  .

This verification is not enought in this  file :  /core/controller/avatarcontroller.php  


	if ($image->valid()) {
				$mimeType = $image->mimeType();
				if ($mimeType !== 'image/jpeg' && $mimeType !== 'image/png') {
					return new DataResponse(
						['data' => ['message' => $this->l->t('Unknown filetype')]],
						Http::STATUS_OK,
						$headers
					);
				}




</details>

---
*Analysed by Claude on 2026-05-24*
