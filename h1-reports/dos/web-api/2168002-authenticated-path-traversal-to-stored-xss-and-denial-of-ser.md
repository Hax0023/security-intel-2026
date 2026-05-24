# Authenticated path traversal to Stored XSS and Denial-of-Service in phpBB emoji import

## Metadata
- **Source:** HackerOne
- **Report:** 2168002 | https://hackerone.com/reports/2168002
- **Submitted:** 2023-09-17
- **Reporter:** shin24
- **Program:** phpBB
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Stored Cross-Site Scripting (XSS), Denial-of-Service, Insufficient Input Validation, Race Condition
- **CVEs:** None
- **Category:** web-api

## Summary
phpBB's emoji import functionality in acp_icons.php lacks proper input sanitization on the 'pak' parameter, allowing authenticated administrators to perform path traversal attacks. This can be exploited to cause DoS by reading blocking files like /proc/self/fd/1, and combined with a race condition on file uploads, to import malicious emoji containing stored XSS payloads that execute in all users' browsers.

## Attack scenario
1. Attacker obtains authenticated admin access to phpBB instance
2. Attacker sends POST request to emoji import endpoint with malicious 'pak' parameter pointing to /proc/self/fd/X (file descriptors created during upload processing)
3. Attacker spams multiple file upload requests simultaneously to create temporary files in /proc/self/fd/
4. Attacker uses race condition to import malicious emoji file before it is deleted by the system
5. Malicious emoji file contains XSS payload in the SMILEY_IMG field without proper escaping
6. When users view emoji on any page of the forum, the stored XSS payload executes in their browsers, enabling cookie theft, session hijacking, or malware distribution

## Root cause
Multiple security flaws: (1) The 'pak' parameter is passed directly to PHP's file() function without sanitization or path validation, (2) No verification that uploaded emoji files are legitimate before import, (3) SMILEY_IMG data is stored and rendered without HTML entity encoding, (4) Race condition exists where temporary uploaded files can be imported before cleanup, (5) Error messages leak information about file existence on the filesystem

## Attacker mindset
A sophisticated authenticated attacker recognizing that administrative upload functionality creates temporary files with predictable locations, exploiting race conditions and insufficient input validation to achieve persistent code execution across all forum users while simultaneously demonstrating path traversal capabilities for DoS impact.

## Defensive takeaways
- Implement strict whitelist validation for file paths - reject any path containing traversal sequences like '..' or absolute paths
- Use PHP functions like realpath() to resolve and validate that the final path is within an expected directory
- HTML entity encode all user-controlled data before output in HTML context, especially data stored in database
- Implement proper file upload handling: validate file types, store uploads outside webroot, use cryptographically random filenames
- Add timing delays or token-based verification between file upload and import operations to prevent race conditions
- Avoid exposing system error messages that reveal file existence or filesystem structure
- Sanitize CSV/import file data with strict parsing rules and data type validation
- Implement rate limiting on import operations to mitigate DoS attacks
- Use security headers like CSP to limit XSS impact if stored XSS occurs

## Variant hunting
Look for similar path traversal patterns in other file import functionality (avatars, themes, extensions). Check for race conditions in other upload-then-process workflows. Search for unescaped database content rendered in admin panels. Test other emoji/icon management features for similar validation bypasses. Review other ACP modules using file() function for similar vulnerabilities.

## MITRE ATT&CK
- T1190
- T1083
- T1499
- T1190
- T1083
- T1547
- T1059

## Notes
Report lacks specific bounty amount and CVE/patch information. The race condition exploitation requires precise timing and is environment-dependent. DoS impact varies based on server configuration and proxy behavior - more severe with single-threaded or sequential request processing proxies. Requires authentication, limiting attack surface but still critical for compromised admin accounts or privilege escalation scenarios.

## Full report
<details><summary>Expand</summary>

# Denial-of-Service
The vulnerabiity lies on the line `552` of `acp_icons.php`file, when importing emoji from a file we can tell phpBB which file to import from via the paramter `pak`, without any sanitization, the `pak` paramter gets passed dirrectly to `file` the file function, which attemp to read the content of the file to an array.
{F2705838}
Because of the check, reading files like /etc/passwd would not be possible, but if we try to read files like /proc/self/fd/1, the request will hang, a TCP connection will be kept open, the will bring lots of burden to the server. More over, in the case when phpBB is behind a proxy, which may process concurrent request one by one, in this case, if the previous request has not finished, the the rest of requests will have to wait for it to timeout, causing a Denial-of-Service

In the progress of testing, i use the default HTTP server of PHP, which simulate exactly what a one-by-one request processing proxy would do.
Request:
```
POST /adm/index.php?i=acp_icons&mode=smilies&current=delete HTTP/1.1
Host: 127.0.0.1:8082
sec-ch-ua: "Chromium";v="113", "Not-A.Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Content-Type: application/x-www-form-urlencoded
Referer: http://127.0.0.1:8082/adm/index.php?i=acp_icons&mode=smilies
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: csrftoken=Ky6rB5uThxl3PwYd6EScmT9WXYiH6rGe; sessionid=hmrhwwo5hj5abu4kqgln2let1x9zudbr; phpbb3_83bmg_u=2; phpbb3_83bmg_k=zalvonnyh1lr16og; phpbb3_83bmg_sid=3ba797a8668f6db1639ac6939d91f96e
Connection: close
Content-Length: 137

action=import&pak=../../../../../../../../../proc/self/fd/1&form_token=b2655d5f0c9edb201328b799a61777b26cef16a5&creation_time=1694960302
```
Result timed-out and no response received:
{F2705858}

This vulnerability can also help an authenticated attacker know which file exist on server by observe the response message, if the file is not found, the error from `$user->lang['PAK_FILE_NOT_READABLE']` would trigger and result in different message than `$user->lang['WRONG_PAK_TYPE']`(when the file exist but has invalid format)
# Stored XSS
When testing the emoji import, i also observe that the `SMILEY_IMG` isn't sanitized or escaped
{F2705870} 
So we can import a malicious emoji file containing the XSS payload, everyone who access the sites (posting section, comment section, admin section, ...) that emoji presents will trigger the XSS payload, leading to web defacement, cookie stealing, malware attack, ... 
```
'icon_e_biggrin.gif', '15', '17', '1', 'Very Happy', ':D',
'icon_e_biggrin.gif', '15', '17', '1', 'Very Happy', ':-D',
'icon_e_biggrin.gif', '15', '17', '1', 'Very Happy', ':grin:',
'icon_e_smile.gif', '15', '17', '1', 'Smile', ':)',
'icon_e_smile.gif', '15', '17', '1', 'Smile', ':-)',
'icon_e_smile.gif', '15', '17', '1', 'Smile', ':smile:',
'icon_e_wink.gif', '15', '17', '1', 'Wink', ';)',
'icon_e_wink.gif', '15', '17', '1', 'Wink', ';-)',
'icon_e_wink.gif', '15', '17', '1', 'Wink', ':wink:',
'icon_e_sad.gif', '15', '17', '1', 'Sad', ':(',
'icon_e_sad.gif', '15', '17', '1', 'Sad', ':-(',
'icon_e_sad.gif', '15', '17', '1', 'Sad', ':sad:',
'icon_e_surprised.gif', '15', '17', '1', 'Surprised', ':o',
'icon_e_surprised.gif', '15', '17', '1', 'Surprised', ':-o',
'icon_e_surprised.gif', '15', '17', '1', 'Surprised', ':eek:',
'icon_eek.gif', '15', '17', '1', 'Shocked', ':shock:',
'icon_e_confused.gif', '15', '17', '1', 'Confused', ':?',
'icon_e_confused.gif', '15', '17', '1', 'Confused', ':-?',
'icon_e_confused.gif', '15', '17', '1', 'Confused', ':???:',
'"onmouseover=alert() ><script>alert()</script>', '17', '18', '1', 'POC', ':POC:',
```
The problem is, if the attacker has no file access permission, how would he be able to import emoji from files? In here, i abused the function of PHP that it will create an tmp file in /tmp and has an file descriptor pointing at it (in my case was /proc/self/fd/10) when php process an uploading, then we will spam a lot of upload attachment request and in the same time, use race condition to import the file before it's deleted. Below i record a short video, spaming the upload request and use a small php file which emulate the behavior of the import function for demonstration purpose, i would be quite the same with the real function but if i turn on to many tab for race condition and also the recorder, i laptop will explose...

{F2705889}

The final result:
{F2705893}

## Impact

The impact for both DoS and XSS has been mentioned above

# Mitigation
I suggest HTML entity encoding data from emoji before show to client, limiting the folder of which user can import the emoji from.

</details>

---
*Analysed by Claude on 2026-05-24*
