# Malstaller: Global Installation Process Hijacking via Registry Tampering for RCE and Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 165969 | https://hackerone.com/reports/165969
- **Submitted:** 2016-09-05
- **Reporter:** penrose
- **Program:** HackerOne (Vendor-Agnostic - Windows Ecosystem)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Privilege Escalation, Remote Code Execution, Registry Hijacking, Insecure Protocol Handler Registration, DLL/Binary Hijacking via HKCU
- **CVEs:** None
- **Category:** memory-binary

## Summary
Malstaller is a critical privilege escalation vulnerability affecting Windows installation processes where low-privileged users can tamper with HKEY_CURRENT_USER registry keys to hijack URL protocol handlers (http, https, FirefoxHTML, etc.) and execute arbitrary code with elevated administrator privileges. An attacker can intercept installer-triggered URL navigation or administrative tool execution to gain RCE and system-level access without requiring admin credentials initially.

## Attack scenario
1. Attacker with low-privilege user account on Windows 7 system identifies that target user has Firefox set as default browser
2. Attacker modifies HKCU registry keys for protocol handlers (http, https, FirefoxHTML, FirefoxURL) to point to attacker-controlled executable instead of Firefox
3. Administrator user initiates software installation which triggers UAC elevation prompt; administrator grants elevated privileges
4. During installation wizard, administrator clicks on external link (privacy policy, help link, etc.) which triggers URL protocol handler
5. Tampered registry key executes attacker's payload with inherited elevated privileges from installer process
6. Attacker achieves RCE and privilege escalation, can modify installation files, disable AV, exfiltrate data, or establish persistence

## Root cause
Installation processes and administrative tools rely on HKEY_CURRENT_USER registry hive to identify default protocol handlers and external resource paths, but fail to validate that these keys have not been tampered by unprivileged users. The elevation of privilege via UAC creates a trust boundary that inherits compromised HKCU settings, allowing low-privileged users to inject code into elevated execution contexts.

## Attacker mindset
Opportunistic privilege escalation targeting a fundamental Windows design assumption that HKCU is safe to use during elevated operations. Attacker recognizes that installer processes are commonly run by administrators and deliberately click external links, making this a reliable attack vector with high success probability and minimal detection risk.

## Defensive takeaways
- Never trust HKEY_CURRENT_USER registry values during elevated process execution; isolate elevated processes from user-modifiable registry hives
- Implement registry key integrity validation and whitelisting for protocol handlers before invoking external applications
- Use full absolute paths for external resources instead of relying on registry-based lookups that can be hijacked
- Apply principle of least privilege to installer processes; separate installation logic that requires elevation from installation UI that does not
- Monitor and alert on suspicious modifications to HKCU protocol handler registries, especially from non-admin processes
- Disable automatic URL navigation in installation wizards or require explicit user confirmation with visual verification of target URL
- Consider using protected registry keys or implementing registry redirection for elevated processes
- Educate administrators to avoid clicking external links in installer dialogs and use official vendor websites instead

## Variant hunting
Search for other Windows applications that: (1) run with elevated privileges via UAC, (2) reference HKCU registry keys for paths or handlers, (3) automatically invoke URLs or external executables, (4) trust default browser or protocol handler settings, (5) execute code during installation/uninstallation phases triggered by user interaction

## MITRE ATT&CK
- T1547.001
- T1548.002
- T1548.004
- T1112
- T1059.003
- T1059.001
- T1190
- T1566.002
- T1204.001

## Notes
Report demonstrates vendor-agnostic vulnerability affecting Windows ecosystem broadly. Attack requires local access but not initial admin privileges, making it suitable for post-exploitation or supply chain scenarios. Windows 7 explicitly verified; reporter indicates other Windows versions likely vulnerable. The elegance of this attack lies in leveraging legitimate installer behavior (clicking help/policy links) combined with implicit trust in user-writable registry hives during elevated execution. This represents a fundamental architectural weakness in Windows UAC model rather than isolated vendor vulnerability.

## Full report
<details><summary>Expand</summary>

Malstaller is a severe vulnerability that affects the installation process of an unknown number of software including many top-100 download software. The vulnerability affects Windows OS (WIN 7 verified vulnerable) users and variations of the attack can affect already installed software and native Windows OS tools.
Malstaller allows attackers to perform RCE and elevate privileges on the affected system corrupting or patching installations of various software with malicious code, blocking AV solutions, leaving a system unprotected or stealing sensitive information via URL sniffing. 

What can the attackers gain?

Malstaller allows attackers to perform RCE and elevate privileges on the affected system. An attacker with low privilege access to a Windows System (user) can intercept the installation/uninstallation process ( triggered by an elevated user) of software and execute his own code. Depending on the elevation level gained he can execute code as administrator, ultimately tampering the installation folder/files of the system or other system folders content. Of course he can execute any other malicious actions with his elevated privileges.

Variations of the same attack can hijack the use of native windows administrative tools like for example “perfmon.exe” or “mmc.exe”. The specific scenario exploits the fact that tools that need administrative level authority in order to execute, rely on resources accessible/editable by simple users under the HKEY_CURRENT_USER hive. The attacker hijacks the execution of an administrative level tool and injects his code which runs with elevated privileges.

Who is vulnerable and when?

Windows 7 OS users are vulnerable to this attack. Other versions of Windows OS seem to be vulnerable. 
The attack can take place during:
•	Installation of software
•	Execution of software (if run as admin)
•	Uninstallation of software 
The attack can take place without user interaction. These are the cases where an installation of uninstallation process automatically redirect user to a URL thus activating automatically the injected code with elevated privileges.

Replication of the attack

It is possible for an attacker that has limited user privileges (not admin) to hijack the installation process of your executable via tampering registry keys belonging to HKCU Hive. Typically installers require admin privileges (UAC) to install the tool properly but "unfortunately" trust registry keys that can be tampered by underprivileged users in order to perform certain actions. The specific registry keys targetted in this exploit are mainly used to identify the default browser (path of the browser) chosen by the user.
An attacker can tamper these registry keys and replace them, pointing to malicious software, triggering a code execution with elevated privileges during the installation/uninstallation or elevated execution of software. This can lead to attacker escalating privileges and at the same time tampering the installation itself opening a window to more dangerous attacks.

Here are the steps to replicate the attack:
On Windows 7 OS install Firefox Browser (set as default browser) (The attack is also possible with other browsers. This parameter is needed in order to know which registry key to tamper)

Step 1: Tempering Registry Keys
Attacker (with low privileges) tampers the content of the following registry keys:
•	[HKEY_CURRENT_USER\Software\Classes\https\shell\open\command]
•	[HKEY_CURRENT_USER\Software\Classes\http\shell\open\command]
•	[HKEY_CURRENT_USER\Software\Classes\FirefoxHTML\shell\open\command]
•	[HKEY_CURRENT_USER\Software\Classes\FirefoxURL\shell\open\command]

With value:
"C:\Users\{CURRENTUSERNAME_EDIT_HERE}\Desktop\malstaller.bat" "%1"
The value above points to the code the attacker wants to be executed with elevated privileges and can be of any file type including .exe, .vbs, .bat etc. 

Step 2: Attack script
Create a simple .bat file named malstaller.bat on the Desktop folder of the user. This script will perform the RCE with elevated privileges. (In reality these files would have been hidden on a different folder). 
Example content of malstaller.bat:

REM Malstaller Attack 2016
set arg1=%1
REM RCE with ELEVATION (Capturing URLs and saving to admin space)
echo %date% : %1 >> C:\mal_log.txt
REM Opening URL not to raise suspicion
"C:\Program Files (x86)\Mozilla Firefox\firefox.exe" -osint -url "%1"

Step 3: Attack replication
Victim administrator: 
•	Installs software
•	Executes software (as admin)
•	Uninstalls software 

UAC window pops up asking for privileged access which the admin provides.
At this point the user (victim) is navigated through various panels with installation/uninstallation options. In case he clicks on any of the external links like for example the Privacy policy he unconsciously triggers the attacker’s script (malstaller.bat) with elevated privileges (RCE & Privilege Escalation). 
In our case the script will create a file named mal_log.txt under C:\, a protected admin folder.
The file will contain the Date and URL that was clicked to trigger the attack in order to easily identify the vulnerable program.

Examples of Vulnerable Software 

The following software are just some indicative examples of popular software vulnerable to this attack. The full list is unknown. Links that trigger the attack scripts are highlighted with red squares.

Verified List (RCE with Elevated Privileges)
AV: AVG, Avira, MalwareBytes, Microsoft Security Essentials, McAfee
Readers: Foxit
WEB: Wamp Server, TeamViewer
General Purpose: Winrar, Winzip, VLC
Windows Native: perfmon, mmc

Check the Annex Section attached for a collection of PoC images of vulnerable software.

Disclaimer: All tests were made using the latest versions of the tools depicted above. Downloads were made using direct links from the official websites of each tool.

How can I check if my installer or software is vulnerable?

Follow the “Replication of attack guide” and while installing/uninstalling or running any software try to click on all possible links that would trigger a browser to open. If the script is activated, check mal_log.txt to find the newly created log. If a new entry is present that the installer/uninstaller or software is vulnerable to this type of attack.

Mitigation

Never trust/rely on resources (registry keys) that can be tampered by underprivileged users when executing a privileged action like the installation/uninstallation of software.
Use HKEY_LOCAL_MACHINE Hive instead to identify browsers and navigate to URLs.
If you need to link your installer app to an external link (ex. privacy policy page) use a non-elevated executable first and only when real installation/uninstallation starts ask to elevate privileges.

Who else can be affected?

The number of software/tools that are vulnerable to this attack are unknown. The number of users impacted by this attack is also hard to define.

</details>

---
*Analysed by Claude on 2026-05-12*
