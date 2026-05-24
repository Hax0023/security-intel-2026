# Pixel Flood Attack leads to Application level DoS

## Metadata
- **Source:** HackerOne
- **Report:** 970760 | https://hackerone.com/reports/970760
- **Submitted:** 2020-08-30
- **Reporter:** mr_vrush
- **Program:** cs.money
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Denial of Service (Application Level), Resource Exhaustion, Insufficient Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can upload extremely high-resolution images (64K x 64K pixels) to the support chat attachment feature, causing server resource exhaustion and returning 502 Bad Gateway errors for all users attempting to upload images simultaneously. This application-level DoS affects legitimate customer support interactions and has demonstrated ~1.2 minutes of downtime affecting multiple concurrent users.

## Attack scenario
1. Attacker creates or obtains a specially crafted image file with extremely high pixel dimensions (64K x 64K or similar)
2. Attacker authenticates to cs.money platform and navigates to the support chat feature
3. Attacker clicks on attachments and uploads the high-resolution pixel flood image
4. Server begins processing the resource-intensive image, consuming CPU and memory
5. Simultaneously, legitimate users attempt to upload normal images to support chat from different accounts/connections
6. Server becomes exhausted and returns 502 Bad Gateway errors to all users, disrupting support functionality

## Root cause
The application lacks proper input validation and resource limits on image uploads in the support chat feature. Specifically: (1) No maximum pixel dimension validation on uploaded images, (2) No image processing timeout or resource quota per user/session, (3) Synchronous image processing without queue management, (4) No rate limiting on concurrent image uploads

## Attacker mindset
Attacker demonstrates responsible disclosure awareness by noting DoS is typically out of scope but frames this as application-level impact affecting real customers. Motivation appears to be highlighting a practical vulnerability affecting service availability rather than malicious disruption. Attacker provides structured reproduction steps and comparative evidence showing legitimate users are impacted.

## Defensive takeaways
- Implement strict image dimension limits (e.g., max 4K x 4K or 8192 x 8192 pixels) with server-side validation before processing
- Add file size limits in addition to pixel dimension limits
- Implement asynchronous image processing with job queues and timeouts to prevent blocking operations
- Add per-user rate limiting on file uploads (e.g., max 5 uploads per minute)
- Implement resource quotas and graceful degradation when server load exceeds thresholds
- Add monitoring and alerting for unusually large image uploads
- Consider client-side validation and preview to catch extreme dimensions early
- Implement request timeouts and circuit breakers for image processing operations

## Variant hunting
Look for similar resource exhaustion vectors in other file upload features: document uploads, profile pictures, media attachments in messages. Test other content types (PDFs with excessive pages, videos with extreme dimensions, archives with compression bombs). Check if other endpoints lack resource limits (email attachments, bulk imports). Investigate if similar pixel flood attacks work on image resizing/thumbnail generation endpoints.

## MITRE ATT&CK
- T1499.004 - Application Exhaustion Flood
- T1499 - Endpoint Denial of Service
- T1190 - Exploit Public-Facing Application

## Notes
Reporter explicitly acknowledges DoS is typically out of scope but argues this qualifies as application-level DoS with real user impact. The evidence of simultaneous legitimate user failures strengthens the report. References to similar reports (752073, 752010) suggest this may be part of a pattern. Key evidence: 502 responses from both attacker and legitimate user, demonstrating collateral damage to availability. Timeline shows ~1.2 minutes of confirmed downtime.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello Team,
      I had gone through your policy and I saw that DoS is out of scope but I am not sure about Application level DoS. The another reason to report  this attack because it affects  real customers who want to chat with your support team. I had tested this with two accounts 

1. From Account 1 I had tried to send 64K * 64K resolution image 
2. Simultaneously from Account 2 I had tried to  send normal image (with different Internet Connection).
3. The response was 502 for both images.

## Steps To Reproduce:
1.  Go to cs.money and login with Account1, Login Account2 on different device with different Internet Connection.
2.  Now Find Support symbol.
3.  Click on attachments and upload "lottapixel.jpg"  from Account1. 
4. Simultaneously upload normal image from Account2.  


## Supporting Material/References:
https://hackerone.com/reports/752073
https://hackerone.com/reports/752010
If you need more information please let me know.

  * [attachment / reference]
From: Device 1,  Account1 
Image "lottapixel.jpg" is Payload
Image "502.PNG" is proof of attack is successful.

From: Device 2, Account2
Image "upload timing from account2.png" and "Account2.png"  is proof that real users are also affected.

## Impact

Real User are not able to send images to the support team.  It affects to the availability  of resource.  I had recorded 1.2 min downtime. 
Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
