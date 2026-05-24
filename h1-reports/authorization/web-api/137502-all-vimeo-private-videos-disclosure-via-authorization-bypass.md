# All Vimeo Private Videos Disclosure via Authorization Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 137502 | https://hackerone.com/reports/137502
- **Submitted:** 2016-05-10
- **Reporter:** opnsec
- **Program:** Vimeo
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Authorization Bypass, Information Disclosure, Broken Access Control, Improper Error Handling
- **CVEs:** None
- **Category:** web-api

## Summary
A critical authorization bypass vulnerability in Vimeo's share endpoint (`/[VIDEO_ID]?action=share`) leaked authentication tokens for private videos in error responses. An unauthenticated attacker could obtain the secret token parameter (`s=[SECRET]`) from the config file URL exposed in error messages, granting complete access to any private video including download links and metadata. The vulnerability affected all private video types regardless of ownership or access restrictions.

## Attack scenario
1. Attacker identifies a Vimeo private video ID through various reconnaissance methods
2. Attacker sends HTTP request to `https://vimeo.com/[VIDEO_ID]?action=share` with `X-Requested-With: XMLHttpRequest` header (AJAX request)
3. Server returns error response indicating lack of access, but includes the video config file URL containing the secret token parameter `s=[SECRET]`
4. Attacker extracts the token from error message and constructs authorized request to `https://player.vimeo.com/video/[VIDEO_ID]/config?s=[SECRET]`
5. Config file is returned containing video metadata, direct video file URLs, and owner information
6. Attacker gains full access to private video content for viewing and downloading

## Root cause
Dual-layered authorization flaw: (1) The share endpoint exposed sensitive config tokens in error responses without proper access validation, and (2) The config endpoint accepted and honored tokens without re-validating user access rights to the video. Server-side error handling included the protected resource's authentication token when rejecting unauthorized requests.

## Attacker mindset
An opportunistic attacker exploiting information disclosure in error messages to bypass access controls. The vulnerability requires minimal effort—no authentication needed, no session hijacking, no exploitation of complex logic flaws. The attacker recognized that the server was leaking the exact credential needed to access protected resources within its rejection message, turning a denial into an authorization.

## Defensive takeaways
- Never include sensitive tokens, authentication parameters, or resource identifiers in error responses, especially for unauthorized access attempts
- Implement defense-in-depth: validate access rights at multiple layers (share endpoint AND config endpoint), not just once
- Ensure authentication tokens are properly bound to user sessions and re-validate permissions when tokens are presented to protected resources
- Audit all AJAX endpoints for improper error handling that may leak security-sensitive information
- Implement proper access control checks before constructing any response, regardless of whether the response is an error or success
- Log and monitor for patterns of 'error response mining' where attackers deliberately trigger errors to extract information
- Sanitize error messages to exclude any tokens, URLs with parameters, or resource identifiers that could be repurposed for attacks

## Variant hunting
Search for similar AJAX endpoints with `?action=` parameters that may expose tokens in error responses. Examine other share/embed functionality endpoints. Review API responses across delete, update, and other protected operations that might leak identifiers. Test whether other private resource types (audio, documents, images) have similar issues. Check if the token parameter `s=[SECRET]` is used in other Vimeo endpoints beyond `/config`.

## MITRE ATT&CK
- T1190
- T1110
- T1555
- T1526

## Notes
Report demonstrates excellent vulnerability analysis with clear POC, technical breakdown, and mitigation recommendations. The vulnerability is particularly severe because: (1) no authentication required, (2) affects all private videos universally, (3) requires minimal technical skill to exploit, (4) grants complete access including download capability, (5) has multiple variants likely across platform. The researcher responsibly created a password-protected POC demonstrating awareness of disclosure sensitivity.

## Full report
<details><summary>Expand</summary>

Hello,

There is a vulnerability in `https://vimeo.com/[VIDEO_ID]?action=share` that makes all Vimeo private videos available to anybody.

POC link :
http://opnsec.com/vimeo/vl/videoLeak.php?video=[VIDEO_ID]

POC requirements :
- No need to be logged in Vimeo
- Because of sensitivity of this, I put a password on the POC :
username : vimeo
password : aS3cr3tP4$$wrD7854123

POC instructions :
1. Open the POC link replacing `[VIDEO_ID]` by any Vimeo private video id (I believe all type of private videos are vulnerable)
2. Enter the username and password as per requirements 
3. If the Vimeo video id is correct, no matter the status of the video, the video should start playing.

---------

Technical description :

`https://vimeo.com/[VIDEO_ID]?action=share` is an Ajax link used to ask Vimeo for the "Share" code to embed the video
Because it is Ajax, the server is only replying if the `Header X-Requested-With is set to XMLHttpRequest`.

If the Attacker send this request with a [VIDEO_ID] of a private video that he don't have access to, the server reply with an error message. However, this message contains the link to the `config` file of the private video including a `token parameter s=[SECRET]` which will grant the attacker access to the config file.
The config file contains all the info about the video including the actual video file links, video title, owner vimeo account, ... which means that the attacker has complete access to the video.

Example of config file with `token parameter s=[SECRET] `
```
https://player.vimeo.com/video/165266592/config?autoplay=0&byline=0&bypass_privacy=1&context=Vimeo%5CController%5CClipController.main&default_to_hd=1&portrait=0&title=0&s=bb016a22af815053eb54XXXXXXX019d8_1462989197
```
------
Vulnerability Mitigation 

To resolve this issue, the `https://vimeo.com/[VIDEO_ID]?action=share` server should not include the token parameter `s=[SECRET]` of the config file in the error response of `https://vimeo.com/[VIDEO_ID]?action=share`if the user doesn't have right to access the video.
There is a good chance this vulnerability is present in other links, especially other Ajax links.

In addition, if that is possible, the `https://player.vimeo.com/video/[VIDEO_ID]/config` config file server should also check that the user has valid right to access the video even if he has a correct `s=[SECRET]` token

-------------

Here is the source code of `http://opnsec.com/vimeo/vl/videoLeak.php`

If you need more info or if the POC doesn't work feel free to contact me.

Regards,

Enguerran Gillier
&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;
&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;&#x2588;

</details>

---
*Analysed by Claude on 2026-05-24*
