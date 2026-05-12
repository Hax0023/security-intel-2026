# Remote Code Execution via Path Traversal in NextCloud Extract App

## Metadata
- **Source:** HackerOne
- **Report:** 765291 | https://hackerone.com/reports/765291
- **Submitted:** 2019-12-27
- **Reporter:** emilvirkki
- **Program:** NextCloud (Extract App - Third-party)
- **Bounty:** No reward (third-party app vulnerability)
- **Severity:** CRITICAL
- **Vuln:** Path Traversal, Arbitrary File Write, Remote Code Execution, Insufficient Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Extract app in NextCloud fails to validate zip file extraction paths, allowing authenticated attackers to write arbitrary files to the filesystem. By crafting a malicious zip with path traversal sequences and modifying extraction requests, an attacker can overwrite application code (e.g., App.php) and achieve remote code execution with www-data privileges.

## Attack scenario
1. Attacker creates a zip file containing a malicious version of /apps/files/lib/App.php with embedded PHP shell code
2. Attacker uploads the zip to a NextCloud instance and initiates extraction through the web interface
3. Attacker intercepts the HTTP request to /apps/extract/ajax/extractHere.php and modifies the 'directory' parameter to include path traversal sequences (../../../../var/www/nextcloud/apps/files/lib/)
4. Attacker also manipulates the 'nameOfFile' parameter to reference the uploaded zip from a traversed path
5. The Extract app processes the request without validating the destination path and overwrites legitimate application files
6. Attacker accesses the modified application file through the web interface, triggering PHP execution of the injected shell code

## Root cause
The Extract app's extractHere.php endpoint does not implement path validation or canonicalization checks before extracting zip file contents. It accepts user-supplied directory parameters without verifying they resolve to intended locations, enabling directory traversal attacks that bypass intended file storage boundaries.

## Attacker mindset
An authenticated user with file upload capabilities seeks to escalate privileges by replacing core application logic. The attacker recognizes that zip extraction logic often fails to sanitize paths and leverages this to escape user-specific directories and reach application code directories executable by the web server process.

## Defensive takeaways
- Implement strict path validation using realpath() and ensure resolved paths remain within intended extraction directories
- Use whitelist-based validation for zip extraction destinations rather than blacklist approaches
- Reject any zip entries containing '..', absolute paths, or symbolic links before extraction
- Run zip extraction with minimal privileges and in isolated/sandboxed environments when possible
- Validate user input against both the 'directory' and 'nameOfFile' parameters independently
- Implement proper access controls to prevent unauthorized directory traversal manipulation in API requests
- Consider disallowing zip extraction to sensitive application directories entirely

## Variant hunting
Search for similar path traversal vulnerabilities in other file archiving operations (tar, rar, gzip extraction), backup restoration functionality, file management features that accept user-supplied paths, and any file operation endpoints that concatenate user input with file paths without canonicalization.

## MITRE ATT&CK
- T1190
- T1083
- T1105
- T1059

## Notes
This vulnerability required authenticated access but could be exploited by low-privilege users. The reporter ethically disclosed despite no monetary reward due to inclusion in official VM image. The attack elegantly combines multiple weaknesses: path traversal, lack of input validation, and execution of user-supplied code paths. The use of request interception to modify parameters demonstrates the importance of server-side validation independence from client-side controls.

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
*Analysed by Claude on 2026-05-12*
