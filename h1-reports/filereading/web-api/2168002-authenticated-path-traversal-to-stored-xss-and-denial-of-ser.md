# Authenticated Path Traversal to Stored XSS and Denial-of-Service in phpBB Icon/Emoji Import

## Metadata
- **Source:** HackerOne
- **Report:** 2168002 | https://hackerone.com/reports/2168002
- **Submitted:** 2023-09-17
- **Reporter:** shin24
- **Program:** phpBB
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Path Traversal, Stored Cross-Site Scripting (XSS), Denial-of-Service (DoS), Race Condition, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
An authenticated attacker can exploit unsanitized file path input in phpBB's emoji import functionality to trigger DoS by reading special files like /proc/self/fd/1, import malicious emoji files via race condition to achieve stored XSS, and enumerate file existence through error message differences. The vulnerability chain allows complete compromise of forum integrity and user sessions.

## Attack scenario
1. Attacker authenticates to phpBB admin panel with emoji import permissions
2. Attacker sends POST request to acp_icons.php with pak parameter pointing to /proc/self/fd/1 or similar special files causing request to hang indefinitely
3. Request timeout exhausts server resources and blocks subsequent requests on single-threaded or proxy-based deployments, causing DoS
4. Simultaneously, attacker spams file upload requests to create temporary files with file descriptors in /tmp
5. Attacker uses race condition to trigger emoji import from /proc/self/fd/X before temporary file is deleted
6. Malicious emoji file containing XSS payload (e.g., 'onmouseover=alert()') is imported and stored, triggering on all pages displaying emojis

## Root cause
The pak parameter in acp_icons.php line 552 is passed directly to PHP's file() function without path sanitization or validation, and emoji data fields (SMILEY_IMG) are not HTML-encoded before storage and rendering. The application also trusts user-controlled file paths for import operations.

## Attacker mindset
A disgruntled administrator or insider with low-level access seeks maximum impact by chaining multiple vulnerabilities: first disabling the forum via DoS, then implanting persistent XSS payload to steal admin credentials and deface content. The race condition technique demonstrates sophisticated exploitation knowledge.

## Defensive takeaways
- Implement strict path validation and whitelisting for file imports; reject any paths containing ../, /proc/, /sys/, or other sensitive directories
- HTML-encode all user-controlled data before database storage and rendering, especially emoji metadata fields
- Implement request rate limiting and timeout protection to prevent single requests from exhausting server resources
- Use secure file upload handling with atomic operations and proper cleanup, avoiding race conditions on temporary files
- Add server-side file type verification beyond extension checking (magic number validation)
- Implement CSRF protection on file import operations (already present but may be bypassable)
- Log and alert on suspicious file path access attempts in import functions
- Restrict emoji import functionality to specific trusted administrators only
- Use Content-Security-Policy headers to mitigate stored XSS impact

## Variant hunting
Check all file upload/import functionality in admin panels for similar path traversal (styles, themes, extensions, language packs)
Test other data fields imported from user-supplied files for XSS and injection vulnerabilities
Examine other PHP file() function usages throughout codebase for unsanitized path input
Test race conditions on other temporary file operations in upload handlers
Check if similar path traversal exists in backup/restore functionality
Review other admin ACP modules for information disclosure via error message differences

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (path traversal in web interface)
- T1083 - File and Directory Discovery (path traversal for file enumeration)
- T1499 - Endpoint Denial of Service (resource exhaustion via /proc/self/fd)
- T1567 - Exfiltration Over Web Service (potential data theft via XSS)
- T1059 - Command Line Interface (proc filesystem access)
- T1012 - Query Registry (information disclosure via error messages)
- T1087 - Account Discovery (admin access via XSS/cookie theft)
- T1657 - Stored XSS payload delivery

## Notes
This is a sophisticated multi-stage attack combining path traversal, race conditions, and XSS. The attacker's use of /proc/self/fd demonstrates deep understanding of Linux process internals. The race condition exploitation for bypassing file upload restrictions is particularly creative. Requires authentication but can be leveraged by low-privilege users with emoji management permissions.

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
