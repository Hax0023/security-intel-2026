# Remote File Inclusion (RFI) in Slack Photo Upload Feature

## Metadata
- **Source:** HackerOne
- **Report:** 14092 | https://hackerone.com/reports/14092
- **Submitted:** 2014-05-30
- **Reporter:** coolboss
- **Program:** Slack
- **Bounty:** Unknown
- **Severity:** Medium
- **Vuln:** Remote File Inclusion, Server-Side Request Forgery (SSRF), Improper Input Validation, URL Parameter Manipulation
- **CVEs:** None
- **Category:** memory-binary

## Summary
A Remote File Inclusion vulnerability exists in Slack's photo upload and cropping feature where the 'url' parameter accepts arbitrary external URLs without proper validation. An authenticated attacker can manipulate the URL parameter to load and display images from any external source, potentially enabling phishing attacks, malware distribution, or SSRF exploitation.

## Attack scenario
1. Attacker authenticates to their Slack workspace and navigates to the photo change endpoint (/account/photo)
2. Attacker initiates the file upload process and captures the redirect to the crop page containing the 'url' parameter
3. Attacker modifies the 'url' parameter value to point to a malicious or third-party external image source
4. Slack server processes the request and fetches the image from the attacker-controlled URL without validation
5. Attacker can supply URLs to malicious content, internal network resources, or use the server as a proxy for SSRF attacks
6. Depending on implementation, attacker may also inject payloads within image metadata or trigger server-side processing vulnerabilities

## Root cause
Insufficient input validation and lack of URL allowlisting on the 'url' parameter in the photo cropping endpoint. The application trusts user-supplied URL parameters without verifying that URLs point only to legitimately uploaded temporary files from the expected storage location (S3 bucket).

## Attacker mindset
An authenticated user seeks to bypass file upload restrictions by directly manipulating URL parameters. The attacker realizes the application constructs URLs to external content without validation and exploits this to load arbitrary remote content, potentially for phishing integration, malware hosting, or reconnaissance of internal systems.

## Defensive takeaways
- Implement strict URL validation and allowlisting - only permit URLs from the expected S3 bucket and specific URL patterns
- Validate that uploaded file URLs match the format of legitimately generated temporary upload URLs with checksums or tokens
- Use opaque file identifiers (UUIDs/tokens) instead of allowing arbitrary URL parameters
- Implement Content Security Policy headers to restrict image loading origins
- Add rate limiting and monitoring on photo upload endpoints to detect abuse
- Validate image content server-side (magic bytes) rather than relying on user-supplied URLs
- Consider using signed URLs with expiration times for temporary file access

## Variant hunting
Check other file upload features in Slack (profile pictures, channel icons, file attachments) for similar RFI patterns
Test other endpoints accepting 'url' parameters (webhooks, integrations, embeds, previews)
Investigate if SSRF can be chained with internal service enumeration or metadata service access
Examine if image processing libraries (ImageMagick, etc.) are vulnerable to polyglot attacks via URL-fetched content
Test for TOCTOU race conditions between URL validation and actual file fetch
Check if user-supplied URLs are logged or stored, enabling indirect XSS or injection attacks

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1557 - Man-in-the-Middle
- T1598 - Phishing
- T1566 - Phishing
- T1105 - Ingress Tool Transfer

## Notes
This is a classic RFI/SSRF vulnerability in a high-profile application. The vulnerability is authenticated but still significant as it bypasses the intended upload flow. The severity depends on what the application does with fetched URLs - if it processes image metadata, extracts EXIF data, or displays content to other users, the impact increases substantially. The report lacks technical depth regarding actual impact and potential chaining vectors.

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
