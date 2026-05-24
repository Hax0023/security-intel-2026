# Arbitrary File Upload to Amazon S3 via HackerOne UI

## Metadata
- **Source:** HackerOne
- **Report:** 7929 | https://hackerone.com/reports/7929
- **Submitted:** 2014-04-17
- **Reporter:** leander
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Unrestricted File Upload, Insufficient File Type Validation, Malware Distribution Vector
- **CVEs:** None
- **Category:** uncategorised

## Summary
The HackerOne platform allowed users to upload arbitrary files (including executable malware) to Amazon S3 buckets through the web UI without proper file type validation or restrictions. This could enable malware distribution, phishing attacks, and abuse of trusted AWS domains for delivering malicious payloads.

## Attack scenario
1. Attacker crafts a malicious executable payload (e.g., MSF reverse shell)
2. Attacker obfuscates the filename with innocent-looking extensions (e.g., image.jpg.exe or document.pdf.exe)
3. Attacker uploads the file through HackerOne's file upload functionality
4. File is stored on hackerone-attachments.s3.amazonaws.com, a trusted AWS domain
5. Attacker shares the S3 URL in reports or comments, leveraging domain reputation
6. Victims download and execute the file, believing it's a legitimate attachment from a trusted source

## Root cause
Insufficient input validation on file uploads - the application failed to enforce file type restrictions, verify file content against declared MIME types, or prevent executable file uploads. The whitelist validation either didn't exist or was easily bypassed through extension manipulation.

## Attacker mindset
Opportunistic abuse of platform infrastructure for malware distribution; leveraging trusted domain reputation to increase successful infection rates; exploiting user trust in HackerOne's security stance.

## Defensive takeaways
- Implement strict whitelist-based file type validation checking both extension AND MIME type/magic bytes
- Reject executable file types (.exe, .bat, .cmd, .com, .scr, .vbs, .js, etc.) at upload
- Use Content-Disposition: attachment headers with filename sanitization to prevent browser execution
- Consider Content-Security-Policy headers to prevent inline script execution
- Implement malware scanning (e.g., VirusTotal, ClamAV) on uploaded files
- Display clear warnings for downloaded files from S3, similar to external link warnings
- Store uploads on separate domains not associated with main application domain
- Implement file size limits and rate limiting on uploads
- Log and monitor file uploads for abuse patterns

## Variant hunting
Check for similar bypass techniques: double extensions (.exe.jpg), null byte injection (.exe%00.jpg), case variation (.EXE), polyglot files combining image+executable headers, archive files (.zip, .rar) containing executables, scripting languages (.ps1, .vbs, .jar), and MIME type mismatches.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.001 - Phishing: Spearphishing Attachment
- T1204.002 - User Execution: Malicious File
- T1608.004 - Obtain Capabilities: Malware

## Notes
Early-stage report (2014) demonstrating fundamental file upload vulnerability. Reporter appropriately demonstrated risk without full exploitation and suggested proportionate fixes. The inclusion of an actual payload filename shows proof-of-concept. Platform's response and remediation not detailed in writeup but likely included file type restrictions and possibly Content-Disposition headers.

## Full report
<details><summary>Expand</summary>

Hi,

It seems one is able to upload arbitrary files to Amazon Webservices through the UI.

This allows for uploading malware such as [msf-payload-x86.jpg.exe](https://hackerone-attachments.s3.amazonaws.com/production/000/006/741/bf60ba068e72e767b93d3fa35c89a36639dd1f19/msf-payload-x86.jpg.exe?AWSAccessKeyId=AKIAJFXIS7KJADBA4QQA&Expires=1397769394&Signature=aoXXsjuCqUjReIFLzMtXYyMO5us%3D) or whatever.

Beyond free hosting this could potentially be used to entice teams into downloading stuff they probably don't want.

Actual exploitation would likely depend on obfuscating the filename to look more innocent, general human errors, a certain trust in files being served from `hackerone-attachments.*.amazonaws.com` or separate issues entirely.

I could imagine this to be working as intended but still believe it would be good to consider restrictions even if the result is to not enforce any.

I would propose to at least consider displaying a warning similar to the (excellent) one displayed when visiting an external link.

HTH,

-leander

</details>

---
*Analysed by Claude on 2026-05-24*
