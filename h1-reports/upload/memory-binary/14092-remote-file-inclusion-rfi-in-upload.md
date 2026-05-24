# Remote File Inclusion (RFI) in Slack Photo Upload Feature

## Metadata
- **Source:** HackerOne
- **Report:** 14092 | https://hackerone.com/reports/14092
- **Submitted:** 2014-05-30
- **Reporter:** coolboss
- **Program:** Slack
- **Bounty:** Unknown
- **Severity:** medium
- **Vuln:** Remote File Inclusion, Insufficient Input Validation, URL Parameter Manipulation
- **CVEs:** None
- **Category:** memory-binary

## Summary
Slack's photo upload feature contains an RFI vulnerability where the 'url' parameter in the crop photo page accepts arbitrary external image URLs without proper validation. An authenticated attacker can manipulate this parameter to load and display images from any external source, potentially enabling SSRF or content injection attacks.

## Attack scenario
1. Attacker authenticates to their Slack workspace (e.g., pran3hiva.slack.com)
2. Attacker navigates to the photo change functionality at /account/photo
3. Attacker initiates file upload and proceeds to the crop photo page
4. Attacker observes the 'url' parameter containing the S3 temporary image path
5. Attacker modifies the 'url' parameter to point to an external image (e.g., google.co.in logo or malicious server)
6. Slack application fetches and displays the external image without validation, confirming RFI capability

## Root cause
The application fails to validate and restrict the 'url' parameter to trusted sources (S3 bucket). It accepts any URL provided by the user and fetches remote content server-side without whitelist enforcement or domain restrictions.

## Attacker mindset
Initial reconnaissance of upload functionality to identify parameter manipulation opportunities. Recognition that the 'url' parameter is user-controlled and directly influences server-side image fetching. Exploitation to demonstrate arbitrary external content loading and potential escalation to SSRF or internal resource access.

## Defensive takeaways
- Implement strict URL whitelist validation - only allow URLs from trusted storage services (e.g., specific S3 buckets)
- Use URL parsing and domain validation to reject external URLs
- Implement Content Security Policy (CSP) headers to restrict image sources
- Apply server-side request filtering (SSRF protection) to prevent access to internal/cloud metadata endpoints
- Validate file URLs before fetching - verify they match expected patterns and origins
- Consider generating temporary signed URLs with expiration instead of exposing raw S3 paths
- Add request rate limiting on image fetch operations
- Log and monitor suspicious URL parameter values for security auditing

## Variant hunting
Check other file upload features (document, avatar, workspace logo) for similar RFI patterns
Test if 'url' parameter accepts file:// URIs (local file access)
Attempt to access internal metadata endpoints (e.g., 169.254.169.254 for cloud credentials)
Test for SSRF to internal services (Redis, databases, admin interfaces)
Check if URL parameter reflects in error messages (XSS potential)
Test with encoded URLs (double encoding, null bytes) to bypass validation
Verify if the vulnerability exists across different Slack workspaces and domains

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is an authenticated vulnerability requiring valid Slack credentials. The practical impact depends on what content can be loaded and how it's processed. Potential escalation vectors include SSRF for internal network reconnaissance, credential harvesting if the application downloads and processes malicious content, or social engineering via injected content. The vulnerability demonstrates the importance of strict input validation on file handling operations, especially when URLs are involved.

## Full report
<details><summary>Expand</summary>

Hello,

Everysite has a RFI vulnerability.
Everysite i.e *.slack.com is having this vulnerability.

Proof of concept / Steps to Reproduce :
=================================

1. Sign in to your account on slack eg. I signed in https://pran3hiva.slack.com
2. Now, go to 'Change photo'. i.e https://pran3hiva.slack.com/account/photo
3. Now, select file to upload.
4. Click on upload image.
5. You will be redirected to 'Crop Photo'.
6. Note the url 
eg.
https://pran3hiva.slack.com/account/photo?url=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fslack-files2%2Favatar-temp%2F2014-05-30%2F2364428212.jpg

Note the 'url' parameter.

7. Change it to desired.
8. I changed it to --> https://pran3hiva.slack.com/account/photo?url=https://www.google.co.in/images/srpr/logo11w.png

Now, image from site will be loaded.

Hence, RFI :D
I have attached 2 screen-shots. POC.
Hope, you patch this one. :)

If you have any questions you may ask me.

Thank You,
Pranav


</details>

---
*Analysed by Claude on 2026-05-24*
