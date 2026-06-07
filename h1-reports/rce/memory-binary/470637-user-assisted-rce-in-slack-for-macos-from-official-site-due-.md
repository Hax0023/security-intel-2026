# User-assisted RCE in Slack for macOS via Improper Quarantine Meta-attribute Handling

## Metadata
- **Source:** HackerOne
- **Report:** 470637 | https://hackerone.com/reports/470637
- **Submitted:** 2018-12-21
- **Reporter:** metnew
- **Program:** Slack
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Improper Resource Validation, Missing Security Attribute, Gatekeeper Bypass, Quarantine Attribute Bypass
- **CVEs:** None
- **Category:** memory-binary

## Summary
Slack's macOS direct download functionality fails to set the com.apple.quarantine extended attribute on downloaded files, allowing .terminal files to bypass Gatekeeper security checks. Attackers can deliver executable .terminal files that execute arbitrary shell commands without triggering security warnings when opened by users.

## Attack scenario
1. Attacker crafts a malicious exploit.terminal file containing shell commands disguised as a harmless XML text file
2. Attacker sends the exploit.terminal file to victim via Slack DM or channel
3. Victim opens the file via Slack's 'Open' button or from Finder using Shift+Click
4. macOS fails to display Gatekeeper quarantine warnings since com.apple.quarantine attribute is missing
5. Terminal application immediately executes embedded shell commands with user-level privileges
6. Arbitrary code execution achieved with no security prompts or user awareness

## Root cause
Slack's direct download implementation does not set the com.apple.quarantine extended file attribute on downloaded files. This attribute is essential for macOS Gatekeeper to identify and warn users about potentially dangerous downloaded executables. .terminal files are executable by default and bypass Gatekeeper checks when this attribute is absent.

## Attacker mindset
An attacker recognizes that Slack is a trusted communication platform where users may lower their guard. By leveraging the direct download feature's missing security attribute combined with .terminal files' deceptive appearance and auto-executable nature, the attacker achieves low-friction code execution that appears legitimate to unsuspecting victims.

## Defensive takeaways
- Always set com.apple.quarantine extended attribute on files downloaded from the internet, regardless of file type or source
- Implement file download security consistently across all delivery mechanisms (direct downloads, API responses, etc.)
- Validate that macOS security frameworks are properly invoked for all user-accessible file operations
- Test application behavior against Gatekeeper at different security levels, especially 'AppStore only' mode
- Consider sandboxing or restricting download functionality to safer mechanisms provided by the OS
- Educate users about verifying file sources and not opening unexpected executable files (terminal, shell, scripts) from messaging platforms

## Variant hunting
Search for similar quarantine attribute bypass in other macOS applications that handle downloads: browsers, email clients, file sharing apps (Dropbox, Google Drive), document viewers, and messaging platforms. Check for inconsistent quarantine handling between native OS features and application-specific download paths. Investigate other executable file types that might bypass Gatekeeper (.app, .scpt, .sh, .command).

## MITRE ATT&CK
- T1566.002
- T1204.002
- T1059.001
- T1036.005
- T1218.002

## Notes
Critical distinction: Slack from AppStore was not vulnerable due to proper quarantine attribute handling. Only the direct download version exhibited the vulnerability. This highlights the importance of using OS-provided distribution mechanisms and testing across different deployment methods. The vulnerability requires user interaction but exploits user trust in the Slack platform and deceptive file presentation.

## Full report
<details><summary>Expand</summary>

## Summary

### **GateKeeper/Quarantine bypass for downloaded files**

Lack of `com.apple.quarantine` meta-attribute for downloaded files allows a remote attacker to send an executable file that won't be checked by Gatekeeper .

### File opening **doesn't trigger native alerts** from GateKeeper/Quarantine

> Downloaded executable files lack `com.apple.quarantine` meta-attribute => no alerts about launching an executable from the web will appear.

### Code execution after opening

Opening a downloaded `.terminal` file in Slack via "Shift + Click"  (or in Finder) immediately leads to running attacker's code on a target device.

### `.terminal` file

1. Opening leads to command execution.
2. Looks safe - XML file.
3. Downloaded `.terminal` file **couldn't be opened** if application sets quarantine meta-attribute properly. However, Slack (Direct Download) doesn't do that.

## Attack scenario

1. Attacker sends `exploit.terminal` to the victim. File looks like a plaintext file in preview.
2. Victim opens `exploit.terminal` file via "Shift + Click" (or via Finder)
3. No alert from Gatekeeper about unsigned executable
4. No alert about running executable file downloaded from the web
5. Shell commands from `exploit.terminal` get executed with user-level privileges.

## Version

Decribed scenario is reproducible in Slack 3.3.3 Direct Download.
Slack from AppStore has correct quarantine rules and isn't vulnerable.

## Additional details

`exploit.terminal` attached + Screencast attached.

### Quarantine
macOS is build in such way that OS will ask user before opening any downloaded and potentially launchable (in default setup) files. This rule applies to `.terminal` files too.

### TL;DR: 
- no quarantine -> `exploit.terminal` is launchable in 1 click without warning a user with popups
- quarantine -> no immediate launch for all files (2 popups) +  no RCE is possible if GateKeeper level set to "AppStore only"

## Impact

## Impact

Attacker could send a crafted `.terminal` file to the victim, which will be executed immediately after opening this file via "Open" button or in Finder. 

The attack scenario requires a certain level of user interaction. 
But the file looks safe and the victim doesn't expect that it'll be launched immediately

### Additional Impact

GateKeeper bypass allows running arbitrary apps in environments hardened with Gatekeeper settings set to "AppStore only".

</details>

---
*Analysed by Claude on 2026-06-07*
