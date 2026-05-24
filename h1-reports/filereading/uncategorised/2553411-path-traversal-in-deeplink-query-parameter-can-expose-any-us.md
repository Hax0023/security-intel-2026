# Path Traversal in Deeplink Query Parameter Exposes Private User Data to Public Directory

## Metadata
- **Source:** HackerOne
- **Report:** 2553411 | https://hackerone.com/reports/2553411
- **Submitted:** 2024-06-16
- **Reporter:** fr4via
- **Program:** Basecamp
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Insecure Deeplink Handling, Arbitrary File Write, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Basecamp Android application (v4.8.6) improperly handles deeplink parameters, allowing attackers to exploit a path traversal vulnerability via the 'filename' query parameter. This enables arbitrary file writes to shared device directories, exposing private user data to third-party applications with basic storage permissions.

## Attack scenario
1. Attacker crafts a malicious deeplink URL containing path traversal sequences (e.g., https://3.basecamp.com/5195267/reports/progress?filename=/../../../../../../sdcard/Download/disclosure.txt)
2. Attacker embeds the malicious link in a Basecamp comment, project, or other location where users can interact with it
3. Victim clicks the link within the Basecamp app, triggering the deeplink handler
4. Application processes the 'filename' parameter without sanitization and writes sensitive data to the traversed directory path
5. Sensitive user data (reports, private files) is written to a publicly accessible shared directory like /sdcard/Download/
6. Third-party applications with READ/MANAGE_EXTERNAL_STORAGE permissions can now access and exfiltrate the exposed private data

## Root cause
The deeplink handler fails to validate and sanitize the 'filename' query parameter before using it in file write operations. No path normalization or boundary checks prevent directory traversal sequences (../) from escaping intended directories.

## Attacker mindset
An attacker with access to Basecamp (as a team member or public participant) can silently compromise all users who click the malicious link. The one-click nature and embedding capability in collaborative features make this a practical social engineering vector with no user interaction beyond a click.

## Defensive takeaways
- Implement strict input validation on all deeplink parameters, rejecting path traversal sequences (.., /, absolute paths)
- Use a whitelist approach for filename parameters, allowing only alphanumeric characters and safe delimiters
- Canonicalize file paths and verify they remain within the intended base directory using File.getCanonicalPath()
- Store sensitive user data in private app-specific directories (Context.getFilesDir() or Context.getCacheDir()) rather than shared storage
- Request explicit user confirmation before writing files to shared directories
- Implement deeplink intent filters with explicit verification of source and parameters
- Apply principle of least privilege: minimize permissions requested and enforce scoped storage restrictions
- Regular security audits of all deeplink handlers and file operations

## Variant hunting
Search for other deeplink handlers accepting file path parameters (install, export, download, save, report parameters)
Audit all file write operations preceded by user-controllable input from intents, URLs, or bundle extras
Test deeplinks with encoded traversal sequences (%2e%2e, %252e%252e) to bypass basic filters
Check for similar vulnerabilities in other Basecamp-owned apps or API endpoints handling file operations
Examine backup/restore features that may accept file path parameters
Review content sharing and file export dialogs for path injection vulnerabilities

## MITRE ATT&CK
- T1190
- T1566
- T1566.002
- T1204.001
- T1005
- T1041

## Notes
This is a critical risk despite moderate technical complexity because: (1) one-click exploitation with no user security warnings, (2) embedding in collaborative features enables mass distribution, (3) affects all users with basic Android storage permissions, (4) exposes highly sensitive work data. The vulnerability demonstrates why deeplinks should never handle file paths directly. Android scoped storage mitigations may limit but not eliminate risk on older target SDKs.

## Full report
<details><summary>Expand</summary>

```java
[------------------------------------Package Details---------------------------------------]:
|    Application Name  :Basecamp
|    Package Name      :com.basecamp.bc3
|    Version code      :380
|    Version Name      :4.8.6
|    Mimimum SDK       :28
|    Target  SDK       :34
|    Max SDK           :None
|    Sha256            :124861dde5cbb9a38d0994c3ca994fbbe5bae83b79621b7e476a0aa78bb711f2
[------------------------------------------------------------------------------------------]
````

## Summary

It was found that the basecamp.bc3 app can be forced to expose the user's private info (any), to the device's shared directory which is accessible by any 3p app with READ/MANAGE external storage permissions. 


## Technical details

The application declares to its android manifest that it handles deeplinks of the form: https://3.basecamp.com/* . The particular deeplink can "take" an additional parameter, called "filename" which is used by the app to save the file locally.  By using a textbook path traversal exploit, it is possible to force the app to save the file to any directory, including ones which are shared and thus accessible by 3rd party apps. 


## Steps to reproduce

The following link stores the user's progress report to the /sdcard/Download/disclosure.txt file:

<a href="https://3.basecamp.com/5195267/reports/progress?filename=/../../../../../../../../../../sdcard/Download/disclosure.txt">click me</a>


Since basecamp supports link within comments/projects e.t.c. , it is possible to add a malicious link, literally anywhere:

{F3360970}

## Impact

An attacker can send/add a malicious link which can expose user's private and files to 3rd party entities.

</details>

---
*Analysed by Claude on 2026-05-24*
