# Acronis True Image Local Privilege Escalation via Insecure Folder Permissions

## Metadata
- **Source:** HackerOne
- **Report:** 908162 | https://hackerone.com/reports/908162
- **Submitted:** 2020-06-25
- **Reporter:** theevilbit
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure File Permissions, Local Privilege Escalation, Unsafe LaunchDaemon Configuration, Improper Installation Security
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image installs application files with insecure permissions when using drag-and-drop installation. LaunchDaemons execute binaries and scripts from the application folder as root, allowing an admin user to replace executables and achieve trivial privilege escalation. Multiple LaunchDaemon services are affected including prl_stat, mms_mini, mobile_backup_server, mobile_backup_status_server, and schedul2.

## Attack scenario
1. Admin user obtains access to the system (may be unprivileged initially)
2. Admin discovers LaunchDaemon plist files in /Library/LaunchDaemons/com.acronis.* that reference executables in /Applications/Acronis True Image.app/
3. Admin verifies the application folder has world-writable or admin-writable permissions due to drag-and-drop installation method
4. Admin replaces target executable (e.g., prl_stat, schedul2) with malicious binary containing privilege escalation payload
5. LaunchDaemon triggers at scheduled interval (StartInterval) or on boot (RunAtLoad=true)
6. Malicious binary executes with root privileges, establishing persistent root access or executing arbitrary commands as root

## Root cause
The application uses drag-and-drop installation method which does not properly set restrictive file permissions on the application bundle. LaunchDaemon plists reference executables within this insufficiently protected directory without integrity validation. The application folder should be owned by root:wheel with restrictive permissions (755 or 700), but drag-and-drop installation leaves them user-modifiable.

## Attacker mindset
An attacker with admin credentials seeks straightforward privilege escalation to root. The drag-and-drop installation weakness is trivial to exploit - no code injection, patching, or vulnerability discovery required. The attacker simply replaces a binary and waits for the LaunchDaemon to execute it. Multiple trigger points (scheduled intervals and boot-time execution) provide high reliability.

## Defensive takeaways
- Always use package installers (PKG format on macOS) rather than drag-and-drop for applications that need elevated privileges or register LaunchDaemons
- Set restrictive ownership and permissions on application bundles: root:wheel 755 (or 700 for sensitive parts) to prevent modification by non-root users
- Implement code signing and verify signatures before executing binaries from LaunchDaemon plists
- Avoid storing executables in user-accessible directories; use /Library/PrivilegedHelperTools or similar protected paths for privileged executables
- Validate file integrity (checksums/notarization) before LaunchDaemon execution rather than trusting file location alone
- Audit all LaunchDaemon definitions to ensure they only reference protected binaries with proper ownership
- Consider using Service Management API (SMJobBless or newer alternatives) for privilege elevation instead of LaunchDaemons launching user-modifiable binaries

## Variant hunting
Search for other macOS applications using drag-and-drop installation with LaunchDaemon registration that execute binaries from /Applications/
Audit applications that register multiple LaunchDaemons with RunAtLoad=true or frequent StartInterval values for privilege escalation vectors
Test other Acronis products (Acronis Cyber Backup, Acronis Disaster Recovery) for identical permission flaws
Examine shell script execution via LaunchDaemon (mms_mini.sh, mobile_backup_server.sh) - these may have even weaker protections
Check for symlink vulnerabilities in application folder where admin could create symlinks to system binaries
Look for applications that install to user-writable locations (/Users/*/Applications/) and register system-wide LaunchDaemons
Test whether application updates maintain insecure permissions, enabling persistent exploitation

## MITRE ATT&CK
- T1547.014 - Boot or Logon Autostart Execution: Launch Agent/Daemon
- T1574.010 - Hijack Execution Flow: Privilege Escalation
- T1053.005 - Scheduled Task/Job: LaunchDaemon
- T1548.004 - Abuse Elevation Control Mechanism: Elevated Execution with Prompt
- T1098 - Valid Accounts (assuming admin account compromise)
- T1078.003 - Valid Accounts: Local Accounts

## Notes
Report indicates researcher submitted this through official service desk before H1 submission. macOS admin-to-root is correctly classified as valid privilege escalation scenario as admin users can modify system settings and install LaunchDaemons without requiring user password. Fix validation simple: verify permissions via 'ls -lR /Applications/Acronis*' show root:wheel ownership. The vulnerability is installation-method dependent, making it a supply chain/deployment security issue rather than code vulnerability. Multiple LaunchDaemons with RunAtLoad=true increase exploitation reliability.

## Full report
<details><summary>Expand</summary>

Note: This has been submitted via service desk earlier, and I got a call from Acronis customer service that it's up on H1 and I should submit it there as well.


All of the Acronis LaunchDaemons (except the price helper) which can be found here: `/Library/LaunchDaemons/com.acronis.*` start an app / script inside the `/Applications/Acronis True Image.app/` folder. As the installation happened with drag and drop, an admin user can replace any of the executables and achieve trivial privilege escalation to root.

Please note that on macOS admin to root is a valid privilege escalation scenario, as even if we don't know the user's password, we can get root. 

Here are all the insecure LauncDaemon files.

```
% cat /Library/LaunchDaemons/com.acronis.*
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>KeepAlive</key>
	<false/>
	<key>Label</key>
	<string>com.acronis.acep</string>
	<key>ProgramArguments</key>
	<array>
		<string>/Applications/Acronis True Image.app/Contents/MacOS/prl_stat</string>
		<string>for_scheduler</string>
	</array>
	<key>StartInterval</key>
	<integer>1209600</integer>
</dict>
</plist>
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>KeepAlive</key>
	<dict>
		<key>SuccessfulExit</key>
		<false/>
	</dict>
	<key>Label</key>
	<string>com.acronis.mms_mini</string>
	<key>ProgramArguments</key>
	<array>
		<string>/Applications/Acronis True Image.app/Contents/MacOS/mms_mini/mms_mini.sh</string>
	</array>
	<key>RunAtLoad</key>
	<true/>
</dict>
</plist>
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>KeepAlive</key>
	<dict>
		<key>SuccessfulExit</key>
		<false/>
	</dict>
	<key>Label</key>
	<string>com.acronis.mobile_backup_server</string>
	<key>ProgramArguments</key>
	<array>
		<string>/Applications/Acronis True Image.app/Contents/MacOS//mobile_backup_server/mobile_backup_server.sh</string>
	</array>
	<key>RunAtLoad</key>
	<true/>
</dict>
</plist>
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>KeepAlive</key>
	<dict>
		<key>SuccessfulExit</key>
		<false/>
	</dict>
	<key>Label</key>
	<string>com.acronis.mobile_backup_status_server</string>
	<key>ProgramArguments</key>
	<array>
		<string>/Applications/Acronis True Image.app/Contents/MacOS//mobile_backup_status_server/mobile_backup_status_server.sh</string>
	</array>
	<key>RunAtLoad</key>
	<true/>
</dict>
</plist>
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>KeepAlive</key>
	<dict>
		<key>SuccessfulExit</key>
		<false/>
	</dict>
	<key>Label</key>
	<string>com.acronis.scheduler</string>
	<key>ProgramArguments</key>
	<array>
		<string>/Applications/Acronis True Image.app/Contents/MacOS/schedul2</string>
	</array>
	<key>RunAtLoad</key>
	<true/>
	<key>WorkingDirectory</key>
	<string>/Applications/Acronis True Image.app/Contents/MacOS/</string>
</dict>
</plist>

```

Fix: Install the application with a pkg installer to ensure that the folder permissions are set to `root:wheel` and users can't modify files.

## Impact

Local privilege escalation

</details>

---
*Analysed by Claude on 2026-05-24*
