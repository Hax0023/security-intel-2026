# 2-Click Remote Code Execution in Evernote Android via Path Traversal in Attachment Filename

## Metadata
- **Source:** HackerOne
- **Report:** 1377748 | https://hackerone.com/reports/1377748
- **Submitted:** 2021-10-21
- **Reporter:** hulkvision_
- **Program:** Evernote
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Path Traversal, Insecure File Download, Arbitrary File Write, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
Evernote Android app fails to sanitize attachment filenames extracted from Content-Disposition HTTP headers, allowing attackers to use path traversal sequences to write malicious native libraries into the app's lib directory. When a victim clicks a shared note link and downloads the renamed attachment, the native library is loaded during app restart, achieving remote code execution.

## Attack scenario
1. Attacker uploads a malicious native library (e.g., libjnigraphics.so) to a note as an attachment
2. Attacker renames the attachment using path traversal characters (e.g., to ../../../lib-1/libjnigraphics.so)
3. Attacker shares the note via invitation or generates a shareable link with embedded deeplink
4. Victim clicks the shared link (1st click), opening the note in Evernote Android app
5. Victim clicks on the attachment to download it (2nd click), which gets written to /data/data/com.evernote/lib-1/ instead of the intended cache directory
6. Victim closes and reopens the Evernote app, triggering loading of the malicious native library and achieving code execution

## Root cause
The React Native download logic in Evernote extracts the filename from the Content-Disposition HTTP response header without sanitizing path traversal sequences. The app fails to validate or normalize the filename before writing to disk, allowing arbitrary file placement within the application's private data directory.

## Attacker mindset
Attacker recognized that while a previous report (#1362313) focused on content:// URI provider sanitization, this vulnerability exploits a different code path in the React Native layer. By understanding the app's architecture split between Java and React Native components, the attacker identified an unpatched attack surface and demonstrated that fixing one vulnerability does not necessarily fix similar issues in other code paths.

## Defensive takeaways
- Always sanitize and validate filenames from untrusted sources (HTTP headers, user input, URIs)
- Implement path traversal prevention by rejecting filenames containing '..' or absolute paths
- Use a whitelist of allowed characters in filenames or normalize paths before file operations
- Ensure consistent security controls across all code paths (Java, native, and React Native components)
- Verify that attachment downloads are restricted to intended directories using canonical path resolution
- Implement code review processes that account for multi-layered architecture (native, Java, React Native)
- Consider code signing or verification for native libraries loaded from potentially untrusted sources

## Variant hunting
Search for similar patterns in other applications that: (1) download files with filenames from HTTP headers without sanitization, (2) use React Native with uncompiled/bytecode-obfuscated native bridge code, (3) split security logic across multiple runtime environments, (4) support collaborative features allowing filename manipulation before sharing, (5) load dynamic libraries from application private directories

## MITRE ATT&CK
- T1190
- T1566
- T1059
- T1525
- T1036

## Notes
The vulnerability requires victim interaction (2 clicks) but with minimal social engineering. The attacker must use invitation-based sharing rather than shareable links on Android. The React Native code is compiled to Hermes bytecode, preventing direct source code analysis. The vuln demonstrates that fixing one instance of a vulnerability class does not guarantee all instances are patched when code spans multiple architectural layers.

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
*Analysed by Claude on 2026-05-24*
