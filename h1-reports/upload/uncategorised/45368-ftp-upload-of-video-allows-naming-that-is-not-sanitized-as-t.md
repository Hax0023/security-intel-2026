# FTP Upload Video Naming Lacks Sanitization Applied to Manual Entry

## Metadata
- **Source:** HackerOne
- **Report:** 45368 | https://hackerone.com/reports/45368
- **Submitted:** 2015-01-27
- **Reporter:** ba4fe4ca95021d367f8a574
- **Program:** Vimeo
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Improper Input Validation, Cross-Site Scripting (XSS), Inconsistent Security Controls
- **CVEs:** None
- **Category:** uncategorised

## Summary
FTP file uploads bypass filename sanitization that is applied to manually entered video names, allowing potentially malicious characters and XSS payloads to be stored as video names. While not immediately reflected in the current screenshot, the unsanitized filename could be exploited during subsequent operations involving the video name such as sharing, following, or linking.

## Attack scenario
1. Attacker authenticates to Vimeo Pro account with FTP access enabled
2. Attacker uploads a video file with specially crafted filename containing XSS payload: ""><img src=x onerror=alert(2)>.mp4
3. FTP upload bypasses validation and stores the filename as-is without sanitization
4. Video appears in user's library with unsanitized filename stored in database
5. When video is shared, linked, or interacted with (follow, like), the filename is rendered in HTML context without encoding
6. XSS payload executes in browser of user viewing the malicious video reference

## Root cause
Vimeo implements input validation and sanitization for video names submitted through the manual naming interface, but does not apply the same security controls to filenames received via FTP uploads. This inconsistency creates a validation bypass where the FTP upload handler accepts raw filenames without passing them through the same sanitization pipeline as user-provided names.

## Attacker mindset
An attacker with FTP access could systematically test various special characters and XSS payloads in filenames, knowing that the manual interface validation is bypassed. They would identify that while immediate rendering may not occur, the stored unsanitized value presents a time-delayed exploitation opportunity when the filename is rendered in other contexts like sharing pages.

## Defensive takeaways
- Implement centralized input validation for all entry points (manual upload, FTP, API, etc.) to ensure consistent security enforcement
- Apply filename sanitization uniformly before storage, not just before display
- Use allowlist approach for filename characters rather than blocklist
- HTML-encode all user-controlled data (including filenames) at output time regardless of storage
- Conduct security testing across all upload mechanisms, not just primary UI
- Use CSP headers to mitigate XSS impact as defense-in-depth
- Implement filename validation regex and test it across all input vectors

## Variant hunting
Check other file upload mechanisms (direct upload, drag-drop, mobile app) for similar bypasses
Test API endpoints for file uploads to see if they validate differently than UI
Try double-encoding or alternative encoding schemes in FTP filenames
Test other user-supplied fields accessible via FTP (descriptions, metadata) for similar gaps
Check if S3 direct uploads or other third-party upload services have similar issues
Look for similar patterns in other Vimeo features that accept external input

## MITRE ATT&CK
- T1190
- T1059

## Notes
The vulnerability is notable for highlighting an architectural inconsistency rather than a single validation failure. The fact that manual naming applies sanitization proves Vimeo was aware of the XSS risk, but failed to apply the same controls consistently. The reporter's observation about delayed rendering is valuable - demonstrating that even if the XSS isn't immediately visible, the unsanitized data in storage creates a future exploitation vector when rendered in different contexts.

## Full report
<details><summary>Expand</summary>

I have uploaded via ftp (Vimeo Pro account) a filename

""><img src = x onerror=alert(2)>".mp4

And as you can see in the screenshot it is put automatically as the name of the video. But I cannot put this name (""><img src = x onerror=alert(2)>".mp4) manually

So I think it needs the same sanitization of the name as it's done after the manual editing.

Even if the XSS is not reflected now (in this case) it can be when doing other actions involving the video name (sharing, follow, link, like etc)

</details>

---
*Analysed by Claude on 2026-05-24*
