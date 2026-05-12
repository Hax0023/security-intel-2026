# 2-Click Remote Code Execution in Evernote Android via Path Traversal in Attachment Filename

## Metadata
- **Source:** HackerOne
- **Report:** 1377748 | https://hackerone.com/reports/1377748
- **Submitted:** 2021-10-21
- **Reporter:** hulkvision_
- **Program:** Evernote
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Path Traversal, Arbitrary File Write, Remote Code Execution, Improper Input Validation, Insecure Deserialization of Untrusted Data
- **CVEs:** None
- **Category:** memory-binary

## Summary
Evernote Android app fails to sanitize attachment filenames extracted from Content-Disposition HTTP headers, allowing attackers to write files to arbitrary locations using path traversal sequences. By renaming an attachment to include traversal characters (e.g., '../../../lib-1/libjnigraphics.so'), an attacker can overwrite native libraries in the app's lib directory, achieving remote code execution when the shared note is accessed by a victim.

## Attack scenario
1. Attacker uploads a malicious native library (.so file) disguised as 'libjnigraphics.so' to an Evernote note
2. Attacker renames the attachment via Evernote's rename function to include path traversal payload: '../../../lib-1/libjnigraphics.so'
3. Attacker shares the note with victim via invitation and generates shareable link (app deeplink or web link)
4. Victim clicks the malicious link (first click), opening the shared note in Evernote app
5. Victim clicks on the attachment to view/download it (second click)
6. Malicious native library is written to /data/data/com.evernote/lib-1/ instead of cache directory, overwriting legitimate library
7. Upon app restart, Evernote loads the attacker-controlled native library, achieving code execution with app privileges

## Root cause
The Evernote Android application extracts attachment filenames directly from the Content-Disposition HTTP response header without sanitization or validation. The download handler in React Native code (compiled to Hermes bytecode) fails to restrict path traversal sequences and allows arbitrary file placement using relative path components. No canonical path resolution or filename validation is performed before writing files to disk.

## Attacker mindset
Attackers identified a critical input validation gap in a widely-used productivity application by leveraging cross-component vulnerabilities (Java + React Native). By chaining the legitimate rename feature with unsanitized header parsing, they discovered a high-impact RCE vector requiring minimal user interaction. The use of native libraries as payload demonstrates sophisticated understanding of Android app architecture and how untrusted dependencies trigger code execution.

## Defensive takeaways
- Always sanitize and validate filenames extracted from HTTP headers (Content-Disposition, Content-Type, etc.) using whitelist-based approach
- Implement canonical path resolution to detect and reject path traversal sequences (../, .., etc.) before file operations
- Use constant/hardcoded download directories without path manipulation based on user input
- Apply same validation rigor to all components (Java, React Native, native code) - security boundaries can be bypassed through cross-layer attacks
- Implement file integrity verification for critical assets like native libraries before loading
- Use security managers or SELinux policies to restrict file write access to designated directories only
- Review all previous fixes for similar vulnerabilities to ensure they address root cause across all code paths

## Variant hunting
Check if other attachment-handling features (backup, export, sync) have similar path traversal issues
Audit other header-derived values (Content-Type, Last-Modified, custom headers) for injection vulnerabilities
Test if the vulnerability works with encoded traversal sequences (URL-encoded, double-encoded, Unicode normalization)
Verify if symlink creation is possible to bypass directory restrictions
Check if similar path traversal exists in notebook rename or note title handling
Test zip extraction functionality for path traversal (if Evernote supports bulk downloads)
Investigate if file permissions set during download could enable privilege escalation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (Social engineering via share links)
- T1574.001 - Hijack Execution Flow: DLL Search Order Hijacking (native library replacement)
- T1036.004 - Masquerading: Masquerade File Type
- T1571 - Non-Standard Port

## Notes
This vulnerability is distinct from the prior report #1362313 which involved unsanitized _display_name from content:// URIs. This attack vector specifically targets Content-Disposition header parsing in the React Native layer, demonstrating that framework-level fixes may not propagate across language boundaries. The 2-click requirement and use of legitimate sharing features make this highly practical for mass exploitation. The fact that malicious library loading occurs on app restart suggests the attacker can achieve persistence and potentially access encrypted note contents.

## Full report
<details><summary>Expand</summary>

This vulnerability is similar to my previous reported vulnerability #1362313 , in here also weakness is path transversal  vulnerability which helps me to acheive code execution but the root cause is different.

some part of this app is written in java and some parts are written in react native. 

In evernote we can share notes and notebooks with others. In  notes we can also add attachments and there is option to rename the added attachment. When renaming i founded that special characters are not restricted,for example file uploaded with name `libjnigraphics.so`  can be renamed to `../../../lib-1/libjnigraphics.so` and when the attachment is downloaded it is downloaded with filename `../../../lib-1/libjnigraphics.so`.
The evernote android app also does not sanitize the received filename, so when user clicks on attachment,instead of attachment getting downloaded in `/data/data/com.evernote/cache/preview/:UUID/` this directory it is downloaded into   `/data/data/com.evernote/lib-1/libjnigraphics.so` which results into remote code execution.

> #1362313 report vulnerability root cause was that the app was not sanatizing the value of `_display_name ` from the provider of received `content://` uri that  resulted into ACE.

> This report's  root cause is that app is extracting attachment filename from `content-disposition` header  eg:- `content-disposition: attachment; filename="../../../lib-1/libjnigraphics.so"`  and the evernote app is  not sanatizing the received filename from the response header. 
The attachment download logic is written in react-native and the source file is compiled into hermes javascript bytecode, so i am not able to show the exact vulnerable code like i did in my last report.

The conclusion i reached was that fixing this report #1362313 bug will not fix this vulnerability so i am writing a new report.




## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Add the native-library poc file to a note {F1489257}
  2. Rename the attachment to `../../../lib-1/libjnigraphics`.
  2. Invite the victim to your note.

  Step 2 is needed,i don't know why `Shareable link` feature is not working on evernote android app without sending an invitation
 3. Click on 3 dots > copy internal link > copy web link OR copy app link(which is android deeplink and can be triggred from websites)
 4. Send link to victim and open the link (1st click)
 5. Click on attachment when note is opened (2nd click)
 6. Close the evernote app and open it again.
From adb shell run nc 127.0.0.1 6666
* use physical device because i have provided the arm64 architecture native library

>POC VIDEO
{F1489256}

## Impact

remote code execution in evernote android app with 2 clicks.

</details>

---
*Analysed by Claude on 2026-05-12*
