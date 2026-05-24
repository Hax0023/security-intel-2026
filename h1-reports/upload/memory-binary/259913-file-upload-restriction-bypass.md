# File Upload Restriction Bypass - Unrestricted imgnum Parameter Leading to DoS

## Metadata
- **Source:** HackerOne
- **Report:** 259913 | https://hackerone.com/reports/259913
- **Submitted:** 2017-08-14
- **Reporter:** ok_bye_now
- **Program:** LISTSERV
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Improper Input Validation, Unrestricted File Upload, Denial of Service, Lack of Rate Limiting
- **CVEs:** None
- **Category:** memory-binary

## Summary
LISTSERV 16.0 allows authenticated users to bypass the 10-logo upload limit by manipulating the imgnum parameter in POST requests. An attacker can upload unlimited images with arbitrary imgnum values, potentially exhausting server disk space and causing application denial of service.

## Attack scenario
1. Attacker creates an account on vulnerable LISTSERV instance and navigates to Newsletter Profile settings
2. Attacker uploads a legitimate logo image through the web interface to understand the normal upload flow
3. Attacker intercepts the POST request in a proxy tool and identifies the imgnum parameter (normally 1-10)
4. Attacker modifies imgnum parameter to arbitrary values (e.g., 'cow', '9999', 'x' repeated) and replays request multiple times
5. Attacker crafts automated script to repeatedly upload images with different imgnum values, filling server disk space
6. Server experiences denial of service as disk space is exhausted, impacting all users' ability to upload content

## Root cause
The application fails to validate and enforce the imgnum parameter to only accept values 1-10. Input validation is missing on the server-side, allowing arbitrary strings/numbers to be used as image identifiers, with no corresponding storage quota enforcement or duplicate prevention.

## Attacker mindset
An authenticated user seeks to disrupt service for all users by exhausting server resources. The attacker recognizes that client-side restrictions (dropdown limited to 1-10) can be bypassed by directly manipulating HTTP parameters, requiring only basic proxy interception knowledge.

## Defensive takeaways
- Implement strict server-side whitelist validation for imgnum parameter (accept only 1-10)
- Enforce per-user storage quotas to prevent unlimited uploads regardless of parameter manipulation
- Implement rate limiting on upload endpoints to prevent abuse
- Use deterministic file naming based on user ID and slot number rather than user-supplied values
- Log and monitor abnormal upload patterns (multiple uploads in short timeframe)
- Overwrite existing images rather than creating new files when slot already occupied
- Never trust client-side restrictions; validate all parameters server-side
- Implement disk space monitoring and alerts for abnormal usage patterns

## Variant hunting
Check if other file upload functions have similar parameter validation issues (profile pictures, document uploads, etc.)
Test numeric parameters in other modules for integer overflow/underflow possibilities
Investigate if imgnum parameter is logged or could lead to path traversal (e.g., imgnum='../../../')
Test if authenticated users can modify imgnum for other users' uploads
Check if the vulnerability applies to other LISTSERV versions and components

## MITRE ATT&CK
- T1190
- T1499

## Notes
This is a straightforward input validation bypass requiring authentication. The impact is significant (DoS via resource exhaustion) but requires active exploitation. The fix is simple: whitelist validation. The writeup demonstrates good reproduction steps and clear proof-of-concept methodology.

## Full report
<details><summary>Expand</summary>

**Summary:**
A file upload function allows users to specify their own file name on the server, which allows a user to upload as many images as they would like, potentially causing an Application Denial of Service.

**Description:**
The listserv 16.0 server at http://████████ allows users to upload their own logos for their own newsletter. The user can upload up to 10 logos. If you capture the request in a proxy such as Burp Suite Pro, you can examine the POST request and see that imgnum parameter is set at 1-10 based on what logo the user specified. It is possible to modify that parameter to whatever you want. For example; any word or number and that image can be retrieved by browsing to the link provided after it is uploaded. This would allow a user to upload as many images/logos as they want to potentially causing a Application Denial of Service if they were able to fill up the server hard drive. 

## Impact
Denial of Service

## Step-by-step Reproduction Instructions

1. Navigate to http://█████████ and create an account.
2.  Go to Preferences after you login and choose the "Newsletter Profile" tab.
3. On the logos option, keep the default "Slot 1" selected and hit browse to choose an image to upload. 
4.  No go to the bottom and choose Update.
5. In your proxy tool, replay the request with the imgnum paramter changed to "cow" or 50 or whatever you want. 
6. Append the same value to the end of the image data (logo parameter) in the POST request. 
7. Replay the modified request.
8. Navigate to http://█████/scripts/wa.cgi?VL&Y=9e44b517&imgnum=<INSERT MODIFIED VALUE HERE> 
9. For example, if you used "cow", you would navigate to http://█████████/scripts/wa.cgi?VL&Y=9e44b517&imgnum=cow
10. To verify, download the image and look at the image in a text editor, you should see the appended value at the end of the image file.

You many need to change the Y parameter in the URI for your account, this will be displayed after you upload your logo through the web interface.

## Product, Version, and Configuration (If applicable)
LISTSERV 16.0
## Suggested Mitigation/Remediation Actions
Only allow values 1-10 for the imgnum parameter and overwrite images if there is one with that number already.

</details>

---
*Analysed by Claude on 2026-05-24*
