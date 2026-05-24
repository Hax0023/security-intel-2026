# Unrestricted File Upload Leading to RCE in express-cart

## Metadata
- **Source:** HackerOne
- **Report:** 343726 | https://hackerone.com/reports/343726
- **Submitted:** 2018-04-26
- **Reporter:** patrickrbc
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Unrestricted File Upload, Path Traversal, Remote Code Execution, Insufficient Input Validation
- **CVEs:** CVE-2018-3758
- **Category:** memory-binary

## Summary
express-cart v1.1.5 contains multiple critical file upload vulnerabilities in the /admin/file/upload endpoint that allow authenticated administrators to upload arbitrary files to any server path, including executable code. An attacker with admin privileges can exploit path traversal, lack of file type validation, and absence of file size restrictions to achieve remote code execution by overwriting critical application files like app.js.

## Attack scenario
1. Attacker gains administrator credentials through phishing, credential stuffing, or social engineering
2. Attacker navigates to the admin file upload interface or directly crafts a POST request to /admin/file/upload
3. Attacker bypasses file type validation by uploading malicious JavaScript with a spoofed image/png Content-Type header
4. Attacker uses path traversal payload (../../) in the 'directory' parameter to write the file outside intended upload directory
5. Attacker uploads malicious app.js or other critical file to the application root directory, replacing legitimate code
6. Upon next application restart or file inclusion, the malicious JavaScript executes with application privileges, establishing web shell access

## Root cause
The upload handler fails to implement multiple security controls: (1) User-supplied directory paths are not validated or sanitized, allowing path traversal attacks; (2) File types are not restricted despite being an image upload feature; (3) File sizes are unchecked, enabling resource exhaustion; (4) No whitelist of allowed upload locations; (5) Insufficient trust boundary enforcement for privileged users

## Attacker mindset
A malicious administrator or compromised admin account holder would systematically identify that the upload endpoint accepts arbitrary paths and file types. They would recognize that replacing app.js or other entry point files would lead to code execution. The attacker would craft a polyglot file or simple JavaScript payload, use path traversal to escape the uploads directory, and achieve persistent access to the underlying server.

## Defensive takeaways
- Implement strict whitelist validation for upload directories - never use user-supplied paths directly
- Validate file extensions and MIME types on both client and server side; use magic number verification, not just extension/Content-Type
- Store uploaded files outside the web root or in a non-executable directory with .htaccess/web.config restrictions
- Implement file size limits and rate limiting to prevent DoS attacks
- Use randomized filenames and remove user-controlled naming from upload mechanism
- Apply principle of least privilege - even admin users should have restricted upload capabilities
- Implement proper access controls ensuring only intended user types can access upload endpoints
- Set appropriate file permissions (644 or read-only) on uploaded files to prevent execution
- Use Content-Disposition: attachment headers when serving uploads to prevent browser interpretation
- Log and monitor all file upload activities for suspicious patterns

## Variant hunting
Look for similar unrestricted upload endpoints in Node.js e-commerce platforms (WooCommerce plugins, PrestaShop modules, custom shopping carts). Search for other /admin/*/upload paths, file management APIs, and avatar/profile image upload features that may share the same validation weaknesses. Examine other npm packages with file handling in their admin panels, particularly those handling product management, media libraries, or document uploads.

## MITRE ATT&CK
- T1190
- T1434
- T1083
- T1047
- T1105

## Notes
This vulnerability requires prior authentication with administrative privileges, reducing but not eliminating risk given credential compromise possibilities. The vulnerability is particularly critical in e-commerce contexts where admin accounts may be targets for account takeover attacks. The reporter did not contact maintainers or open issues, suggesting this may be an unpatched legacy version. The specific version (1.1.5) and npm package should be checked for patch availability.

## Full report
<details><summary>Expand</summary>

I would like to report an unrestricted file upload in express-cart.

It allows a user with administrative privileges to upload a file to any path.

# Module

**module name:** express-cart
**version:** 1.1.5
**npm page:** `https://www.npmjs.com/package/express-cart`

## Module Description

expressCart is a fully functional shopping cart built in Node.js (Express, MongoDB) with Stripe, PayPal and Authorize.net payments.

# Vulnerability

## Vulnerability Description

A privileged user can use the upload functionality to gain access to the server.

The application offers the possibility of uploading product images. However, there are many problems with the way it handles these uploads.

Firstly, it uses a path provided by the user. This path is not validated, therefore, it would allow the user to upload the file to any path on the hosting server.

Secondly, it does not restrict the type of the file being uploaded, therefore, it would allow the user to upload a malicious file to gain access to the server.

Finally, it does not restrict the size of the file. This would allow to easily exhaust the host resources and consequently produce a DoS.
  
## Steps To Reproduce:

There are many ways this vulnerability could be exploited. Supposing our goal would be to establish access to the host machine, we could replace the *app.js* file with a malicious JavaScript that would give us a web shell.

Once you have administrator privileges you can use a request similar to:

```
POST /admin/file/upload HTTP/1.1
Host: localhost:1111
Referer: http://localhost:1111/
Content-Type: multipart/form-data; boundary=---------------------------1099055603892737061752875043
Cookie: [ADMINISTRATOR_COOKIE]

-----------------------------1099055603892737061752875043
Content-Disposition: form-data; name="upload_file"; filename="app.js"
Content-Type: image/png

[MALICIOUS_JAVASCRIPT]
-----------------------------1099055603892737061752875043
Content-Disposition: form-data; name="productId"

5ae2228d995e3e5d7c96474d
-----------------------------1099055603892737061752875043
Content-Disposition: form-data; name="directory"

../../
-----------------------------1099055603892737061752875043
Content-Disposition: form-data; name="saveButton"

-----------------------------1099055603892737061752875043--
```

# Wrap up

- I contacted the maintainer to let them know: [N] 
- I opened an issue in the related repository: [N]

## Impact

This vulnerability would allow a privileged user to gain access in the hosting machine.

</details>

---
*Analysed by Claude on 2026-05-24*
