# Full Path Disclosure via Error in Deck Card Attachment Deletion

## Metadata
- **Source:** HackerOne
- **Report:** 1354334 | https://hackerone.com/reports/1354334
- **Submitted:** 2021-09-29
- **Reporter:** ctulhu
- **Program:** Nextcloud (Deck Application)
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Error-Based Information Disclosure
- **CVEs:** CVE-2022-24906
- **Category:** web-api

## Summary
An unhandled exception in the Deck application's attachment deletion endpoint reveals the full filesystem path of the Nextcloud installation through verbose error messages in the HTTP response. When attempting to delete a non-existent or invalid card attachment, the server returns a 500 error with a complete stack trace including absolute file paths.

## Attack scenario
1. Attacker identifies the Nextcloud instance running the Deck application at target domain
2. Attacker crafts a DELETE request to the attachment endpoint with an invalid card ID or attachment reference (e.g., /apps/deck/cards/11/attachment/file:1)
3. Server processes the request and encounters an unhandled exception in DeckShareProvider.php when attempting to retrieve share information
4. Exception handler returns 500 Internal Server Error response containing full stack trace with absolute file paths (e.g., /var/www/[redacted]/custom_apps/deck/lib/...)
5. Attacker extracts filesystem structure information from the error response
6. Attacker uses this information to map the application structure and identify potential attack surfaces or misconfigurations

## Root cause
The attachment deletion endpoint does not properly validate input parameters before attempting operations. When an invalid attachment reference is processed, the exception handling mechanism exposes the full exception object including file paths and line numbers in the JSON response body instead of returning a generic error message.

## Attacker mindset
Information gathering and reconnaissance. The attacker is mapping the target infrastructure to understand the application structure and identify potential weaknesses. Full path disclosure helps identify whether custom applications are installed, their locations, and the overall server architecture.

## Defensive takeaways
- Implement input validation on all API endpoints before processing file operations
- Never expose exception details, file paths, or stack traces in API responses sent to clients
- Configure error handlers to return generic messages to clients while logging detailed errors server-side only
- Implement proper exception handling in all service layers to catch and transform exceptions before response serialization
- Use centralized error response formatting that strips sensitive information
- Validate card IDs and attachment references against database constraints before attempting operations
- Implement authentication and authorization checks before even attempting to process file deletion requests

## Variant hunting
Test other file operation endpoints (upload, download, copy, move) for similar path disclosure
Check other Deck endpoints that interact with files or attachments for verbose error responses
Review all API endpoints in other Nextcloud apps (Tasks, Notes, Calendar) for similar exception disclosure patterns
Test with various invalid input formats to trigger different exception types and stack traces
Check if error details are also exposed in other response formats (XML, HTML) or headers
Attempt to trigger errors at different layers (database, filesystem, sharing) to map complete application structure

## MITRE ATT&CK
- T1592 - Gather Victim Host Information (system information disclosure)
- T1589 - Gather Victim Identity Information (application structure reconnaissance)
- T1598 - Phishing for Information (reconnaissance)

## Notes
This is a low-severity issue on its own but valuable for reconnaissance. The actual file paths appear to be redacted in the public report (shown as ██████), indicating the program may have sanitized the original disclosure. The vulnerability demonstrates poor exception handling practices and insufficient input validation. The issue is specific to invalid attachment deletion attempts; successful deletions may not trigger this error path.

## Full report
<details><summary>Expand</summary>

## Summary:

An error in deck cards when deleting an attachment reveals the full path of the website.

```
DELETE /apps/deck/cards/11/attachment/file:1 HTTP/2
Host: ctulhu.me/nc
Sec-Ch-Ua: "Chromium";v="93", " Not;A Brand";v="99"
Accept: application/json, text/plain, */*
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36
Sec-Ch-Ua-Platform: "macOS"
Origin: https://ctulhu.me/nc
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
```

### Response

```
HTTP/2 500 Internal Server Error
Date: Wed, 29 Sep 2021 07:42:43 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 2057
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Pragma: no-cache
Cache-Control: no-cache, no-store, must-revalidate
Content-Security-Policy: default-src 'none';base-uri 'none';manifest-src 'self';frame-ancestors 'none'
Feature-Policy: autoplay 'none';camera 'none';fullscreen 'none';geolocation 'none';microphone 'none';payment 'none'
X-Robots-Tag: none
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
X-Download-Options: noopen
X-Frame-Options: SAMEORIGIN
X-Permitted-Cross-Domain-Policies: none
X-Robots-Tag: none
X-Xss-Protection: 1; mode=block
Cf-Cache-Status: DYNAMIC
Server: cloudflare
Cf-Ray: 69639391d9741f21-FRA
Alt-Svc: h3=":443"; ma=86400, h3-29=":443"; ma=86400, h3-28=":443"; ma=86400, h3-27=":443"; ma=86400

{"status":500,"message":"There was an error retrieving the share. Maybe the link is wrong, it was unshared, or it was deleted.","exception":{"\u0000OC\\HintException\u0000hint":"","\u0000*\u0000message":"There was an error retrieving the share. Maybe the link is wrong, it was unshared, or it was deleted.","\u0000Exception\u0000string":"","\u0000*\u0000code":0,"\u0000*\u0000file":"\/var\/www\/██████████\/custom_apps\/deck\/lib\/Sharing\/DeckShareProvider.php","\u0000*\u0000line":586,"\u0000Exception\u0000trace":[{"file":"\/var\/www\/████████\/custom_apps\/deck\/lib\/Service\/FilesAppService.php","line":140,"function":"getShareById","class":"OCA\\Deck\\Sharing\\DeckShareProvider","type":"-\u003E"},{"file":"\/var\/www\/█████\/custom_apps\/deck\/lib\/Service\/AttachmentService.php","line":339,"function":"extendData","class":"OCA\\Deck\\Service\\FilesAppService","type":"-\u003E"},{"file":"\/var\/www\/██████████\/custom_apps\/deck\/lib\/Controller\/AttachmentController.php","line":96,"function":"delete","class":"OCA\\Deck\\Service\\AttachmentService","type":"-\u003E"},{"file":"\/var\/www\/███████\/lib\/private\/AppFramework\/Http\/Dispatcher.php","line":217,"function":"delete","class":"OCA\\Deck\\Controller\\AttachmentController","type":"-\u003E"},{"file":"\/var\/www\/███████\/lib\/private\/AppFramework\/Http\/Dispatcher.php","line":126,"function":"executeController","class":"OC\\AppFramework\\Http\\Dispatcher","type":"-\u003E"},{"file":"\/var\/www\/█████\/lib\/private\/AppFramework\/App.php","line":156,"function":"dispatch","class":"OC\\AppFramework\\Http\\Dispatcher","type":"-\u003E"},{"file":"\/var\/www\/██████████\/lib\/private\/Route\/Router.php","line":301,"function":"main","class":"OC\\AppFramework\\App","type":"::"},{"file":"\/var\/www\/██████\/lib\/base.php","line":1000,"function":"match","class":"OC\\Route\\Router","type":"-\u003E"},{"file":"\/var\/www\/█████████\/index.php","line":36,"function":"handleRequest","class":"OC","type":"::"}],"\u0000Exception\u0000previous":null}}
```

## Steps To Reproduce:
[add details for how we can reproduce the issue]

* 0.) setup burpsuite
* 1.) go to $website/apps/deck and pick any cards
* 2.)  attach a file to the card and delete it
* 3.) On burp suite go to proxy > http history > find the request
* 4.) send the request to repeater and run the request again

## Impact

Full path disclosure

</details>

---
*Analysed by Claude on 2026-05-24*
