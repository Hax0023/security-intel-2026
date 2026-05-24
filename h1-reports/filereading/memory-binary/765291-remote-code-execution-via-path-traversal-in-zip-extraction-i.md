# Remote Code Execution via Path Traversal in NextCloud Extract App Zip Extraction

## Metadata
- **Source:** HackerOne
- **Report:** 765291 | https://hackerone.com/reports/765291
- **Submitted:** 2019-12-27
- **Reporter:** emilvirkki
- **Program:** NextCloud (Hansson IT VM image - Extract app)
- **Bounty:** None (third-party app vulnerability, reporter noted ineligibility)
- **Severity:** critical
- **Vuln:** Path Traversal, Arbitrary File Write, Remote Code Execution, Insufficient Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Extract app in NextCloud fails to validate file paths during zip extraction, allowing authenticated attackers to write arbitrary files to the server via path traversal sequences. By crafting a malicious zip file and manipulating the extraction directory parameter, an attacker can overwrite critical application files (e.g., App.php) and achieve remote code execution with www-data privileges.

## Attack scenario
1. Attacker creates a malicious zip file containing a modified version of a critical NextCloud file (e.g., apps/files/App.php) with embedded PHP code
2. Attacker uploads the zip file to the NextCloud instance as an authenticated user
3. Attacker initiates extraction via the Extract app UI but intercepts the request
4. Attacker modifies the request parameters to include path traversal sequences (../../../../) in the directory parameter, pointing to the NextCloud application directory
5. Attacker submits the modified request, causing the Extract app to write the malicious file to the application's lib directory, overwriting the legitimate App.php
6. Attacker accesses the application and triggers execution of the malicious code via a crafted URL parameter (e.g., poc_cmd), achieving RCE with www-data privileges

## Root cause
The Extract app's extractHere.php endpoint does not properly validate or sanitize the 'directory' parameter before using it in zip extraction operations. The application fails to check for path traversal sequences (../) and does not restrict extraction to user-specific directories, allowing files to be written outside intended locations.

## Attacker mindset
An authenticated attacker with file upload privileges exploits insufficient path validation in a file extraction utility to escape the intended extraction sandbox. The attacker leverages the web server's execution context (www-data user) to achieve persistent code execution, treating the Extract app as a trusted but poorly-validated pathway to arbitrary file write capabilities.

## Defensive takeaways
- Implement strict path validation on all user-supplied directory and filename parameters; reject or normalize path traversal sequences
- Use a whitelist approach for allowed extraction directories, restricting extraction to user-specific folders with canonicalized paths
- Validate zip file contents before extraction; check that extracted file paths are within the intended target directory
- Apply principle of least privilege: run web server and file operations with minimal necessary permissions
- Implement proper input sanitization and use secure file handling APIs that prevent directory traversal (e.g., ZipArchive with proper path validation)
- Require CSRF tokens for file operations and validate them server-side
- Monitor and alert on suspicious file write patterns, especially to application directories
- Regularly audit third-party apps for security vulnerabilities before including them in official distributions

## Variant hunting
Search for other file extraction/decompression features in NextCloud or similar platforms that may not validate extraction paths
Audit other third-party NextCloud apps that handle file uploads and directory parameters for similar path traversal issues
Test archive manipulation in other applications (RAR, 7z handlers) for equivalent path traversal vulnerabilities
Look for similar patterns in other PHP applications using $_POST['directory'] or similar parameters without normalization
Examine symlink handling in extraction routines that may allow traversal via symbolic link creation
Test for zip slip vulnerabilities in frameworks that handle compressed files (Python zipfile, Java ZipInputStream, etc.)

## MITRE ATT&CK
- T1190
- T1491
- T1565
- T1547

## Notes
This vulnerability demonstrates the risks of including third-party applications in official distributions without thorough security audits. The attack chain requires authentication but is easily exploitable by low-privileged users. The vulnerability allows not just data exfiltration but persistent code execution, making it critical despite the reporter's willingness to waive rewards. The use of path traversal to overwrite application files is a particularly effective exploitation vector against PHP-based applications where code execution flows from file writes.

## Full report
<details><summary>Expand</summary>

I realise this doesn't qualify for a reward, as it's a vulnerability in a third-party app, but as the app is part of the "official" VM image provided by Hansson IT, I think it's well worth fixing.

The Extract app doesn't validate the path or filename of a zip file to be extracted, allowing an attacker to create or overwrite arbitrary files.

How to reproduce
===

Install NextCloud using the VM image with default settings (with the extra security options).

Create a new user with no user group and log in as that user.

Upload the payload zip file (nextcloud-shell.zip, attached) to the root folder (or wherever you like). It contains a modified version of apps/files/App.php, necessary for getting the payload to run.

Click the "Extract here" option for the nextcloud-shell.zip and intercept the request. Modify the **request body** so the request looks something like the following. You need to replace "normaluser" with the username of the user you created in (2):

```
POST /index.php/apps/extract/ajax/extractHere.php HTTP/1.1
Host: 192.168.100.32
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: */*
Accept-Language: fi-FI,fi;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
requesttoken: lv0G5+K7v/a3w30wOMyR35SvBgF35GHmiuoejP+8u7g=:w5s+qIPUj8aAohdpWojkiazdVXYRkwyp47t8ypHy/+4=
OCS-APIREQUEST: true
X-Requested-With: XMLHttpRequest
Content-Length: 55
Origin: https://192.168.100.32
DNT: 1
Connection: close
Cookie: ocmmdvtkydkx=1u2e2imt5h7g0pimv84eoqnfco; oc_sessionPassphrase=MXmMNXhcE3%2FpbZla9mKTYIS18lYG49cMP8lTHFrJfGe1jLxHd2hHfg8vYs1O6hFjv2IbkI31jhMeJnajKWNYzIb7G3f9UNiFmyKJwAbzPWLKY594ScipzPr6u%2BN9SUp3; __Host-nc_sameSiteCookielax=true; __Host-nc_sameSiteCookiestrict=true; nc_username=normaluser; nc_token=FkBWj5z2dOJS0v4putAyW2oL7tAEOc9Q; nc_session_id=1u2e2imt5h7g0pimv84eoqnfco

nameOfFile=../../../../../../mnt/ncdata/normaluser/files/nextcloud-shell.zip&directory=/../../../../var/www/nextcloud/apps/files/lib&external=0
```

Open the following URL (replace host ip with your actual install) and observe how the current user and group are printed: `https://192.168.100.32/apps/files/?dir=/&poc_cmd=whoami`. You can obviously change the poc_cmd parameter to run any command you like.

## Impact

The attacker can run any commands with the privileges of the www-data user. This allows the attacker to access and modify all the files and personally identifiable information in the installation.

</details>

---
*Analysed by Claude on 2026-05-24*
