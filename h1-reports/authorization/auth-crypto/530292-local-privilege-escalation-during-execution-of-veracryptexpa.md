# Local Privilege Escalation via UAC Bypass in VeraCryptExpander.exe

## Metadata
- **Source:** HackerOne
- **Report:** 530292 | https://hackerone.com/reports/530292
- **Submitted:** 2019-04-06
- **Reporter:** penrose
- **Program:** VeraCrypt
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Privilege Escalation, UAC Bypass, Registry Hijacking, Insecure Shell Protocol Handler, Local Code Execution
- **CVEs:** CVE-2019-19501
- **Category:** auth-crypto

## Summary
VeraCryptExpander.exe executes elevated processes that open URLs using shell protocol handlers defined in HKCU (user-controlled) registry keys rather than secure system-wide HKLM keys. An attacker with local access can modify HKEY_CURRENT_USER registry entries for browser protocol handlers to execute malicious code with elevated privileges when the user clicks the 'Homepage' button. This results in a complete UAC bypass allowing arbitrary code execution in an elevated context.

## Attack scenario
1. Attacker with local user access modifies HKCU registry keys for multiple browser protocol handlers (ChromeHTML, FirefoxHTML, IE.HTTP, HTTPS, etc.) to point to attacker-controlled executable
2. Attacker crafts malicious batch file or executable that performs privileged operations (write to protected directories, create scheduled tasks, etc.)
3. Victim runs VeraCryptExpander.exe with elevated privileges (manifest specifies requestedExecutionLevel as asInvoker or higher)
4. Victim clicks the 'Homepage' button which attempts to open a URL using shell protocol handler
5. Windows resolves the protocol handler from HKCU registry and executes the attacker's malicious script with inherited elevated privileges
6. Attacker gains code execution with full administrative rights, bypassing UAC entirely

## Root cause
The application manifest allows elevation and the WinMain.cpp implementation uses ShellExecute or similar APIs to open URLs, which resolve protocol handlers from HKCU registry hive (user-writable) instead of HKLM (system-wide, restricted). The developer failed to validate or sanitize the registry source before executing shell commands with elevated privileges.

## Attacker mindset
An attacker recognizes that HKCU registry is writable by unprivileged users and sees the opportunity to intercept shell protocol execution happening within an elevated process context. By poisoning user-controlled registry handlers, the attacker hijacks the execution flow without needing admin rights to modify system hives, achieving privilege escalation through a trusted application.

## Defensive takeaways
- Never open URLs or execute shell commands from elevated processes without first validating handlers against system-wide (HKLM) registry only, not HKCU
- Avoid ShellExecute/ShellExecuteEx for handling URLs; implement explicit whitelist of allowed protocols and handlers
- If elevation is required, implement it only for specific operations; avoid blanket process elevation for the entire application
- Use CreateProcessAsUser with explicit handler validation rather than shell protocol handlers
- Implement manifest with requestedExecutionLevel as 'asInvoker' and request elevation only when needed via UAC prompts
- Regularly audit code paths that execute external processes to ensure they don't trust user-writable registry or environment variables
- Test all user-facing buttons/actions for unexpected registry lookups or shell command execution

## Variant hunting
Search for similar patterns in other applications: any elevated process that (1) opens URLs/URIs, (2) reads from HKCU for handlers, (3) uses ShellExecute/registry-based dispatching, (4) has elevation manifest. Look for unvalidated protocol handler execution in Citrix, VPN clients, system utilities, and backup software. Check for filetype associations being read from HKCU without HKLM validation.

## MITRE ATT&CK
- T1548.002
- T1547.001
- T1112
- T1036
- T1059.003
- T1190

## Notes
This vulnerability demonstrates a classic privilege escalation chain: (1) HKCU registry is user-writable, (2) elevated process trusts HKCU entries, (3) no validation of handler source. Affects both Windows 7 and Windows 10. Windows 10 adds slightly more friction (requiring user to change default browser) but remains fully exploitable. The PoC is straightforward and requires no exploitation tools beyond registry modification, making it highly practical. Reports references MITRE T1088 (deprecated, now T1548.002 for UAC bypass).

## Full report
<details><summary>Expand</summary>

## Summary:
Your VeraCryptExpander.exe is vulnerable to a Local Privilege Escalation (UAC BYPASS) during execution. The issue is located here:
https://github.com/veracrypt/VeraCrypt/blob/a108db7c85248a3b61d0c89c086922332249f518/src/ExpandVolume/VeraCryptExpander.manifest 
https://github.com/veracrypt/VeraCrypt/blob/a108db7c85248a3b61d0c89c086922332249f518/src/ExpandVolume/WinMain.cpp

The issue is detected on the fact that you launch a web page  through an elevated process but trust the link to be opened by an app specified by registry keys belonging to HKCU Hive (current user domain) and not an elevated HIVE set like HKEY_LOCAL_MACHINE. It is possible for an attacker that has limited admin privileges (not full admin with UAC) to hijack the execution of you code by tampering specific registry keys linked to browsers and elevate his privileges ultimately tampering your installation folder by writing malicious code in it or replacing binaries with his own.

A file less malware that has hijacked the reghive altering or creating specific keys can hijack the execution of you binary and bypass UAC achieving full admin right.
Examples of malware using UAC bypass: https://attack.mitre.org/techniques/T1088/
The attack was successfully tested in both WIN 7 and WIN 10

## Steps To Reproduce:
Windows OS 7 (tested) for this example
Default browser Chrome (works with any default browser option just change the right reg)
User role ADMINISTRATOR - name of my user for the example is: TEMP
Step0. Create malicious script to elevate: malstaller.bat on desktop (attached)

Step1. Tamper Registry Keys - run add.bat attached after altering the current username
This action simulates an attacker (with low privilege admin) tampering the content of the following registry keys (no need for full admin rights). These keys are tampered to cover all cases of popular default browsers:

[HKEY_CURRENT_USER\Software\Classes\ChromeHTML\shell\open\command]
@="C:\Users\Temp\Desktop\malstaller.bat \"%1\""

[HKEY_CURRENT_USER\Software\Classes\ChromeURL\shell\open\command]
@="C:\Users\Temp\Desktop\malstaller.bat \"%1\""

[HKEY_CURRENT_USER\Software\Classes\FirefoxHTML\shell\open\command]
@="C:\Users\Temp\Desktop\malstaller.bat \"%1\""

[HKEY_CURRENT_USER\Software\Classes\FirefoxURL\shell\open\command]
@="C:\Users\Temp\Desktop\malstaller.bat \"%1\""

[HKEY_CURRENT_USER\Software\Classes\IE.HTTP\shell\open\command]
@="C:\Users\Temp\Desktop\malstaller.bat \"%1\""

[HKEY_CURRENT_USER\Software\Classes\IE.HTTPS\shell\open\command]
@="C:\Users\Temp\Desktop\malstaller.bat \"%1\""

[HKEY_CURRENT_USER\Software\Classes\HTTP\shell\open\command]
@="C:\Users\Temp\Desktop\malstaller.bat \"%1\""

[HKEY_CURRENT_USER\Software\Classes\HTTPS\shell\open\command]
@="C:\Users\Temp\Desktop\malstaller.bat \"%1\""

The path is altered to point to the malicious script that attacker wants to be elevated (UAC bypass attack/privilege escalation). This script can do anything like deleting/creating files under C:. Scheduling tasks etc.

Step2. To achieve/activate UAC bypass
Run VeraCryptExpander.exe and click on the button : "Homepage" on the higher top part of the window.
The execution in now hijacked (see video) and UAC bypass is achieved.

A one liner used in the video will place fake VeraCrypt2.exe (with putty.exe as PoC) under your installation folder and execute it with full admin priviledges.

Useful files of your installation can be tampered alternatively and used as backdoor.

Watch the video attached were a simple .bat script gains elevated admin privileges during your software execution and writes in admin space.

WINDOWS 10
User Role: Administrator

In order to successfully replicate the attack on Windows 10 the following steps must be followed (a little bit different from WIN 7) . As windows have changed some security setting you cannot alter the default browser for the attack to happen seamlessly. But win 10 users are still vulnerable. The difference is that after tampering reg keys to trap various browsers (not the current default) on the system in the affected system the victim must change the default browser to one that has been trapped for the exploit to happen.

In the example below on WIN 10 and with Default Browser assuming EDGE, we will trap IE. If after we alter reg keys executing the add.bat, the user chooses IE or any other browser in place as his default browser the exploit works as before.

Be Admin user logged in!
Step 1: Tamper or create registry keys for IE (or run add.bat) no UAC is needed to do so (your default browser is EDGE):

[HKEY_CURRENT_USER\Software\IE.HTTP\shell\open\command]
[HKEY_CURRENT_USER\Software\IE.HTTPS\shell\open\command]

With value:
"C:\Users{PLACE PROPER USER ACCOUNT NAME HERE}\Desktop\malstaller.bat" "%1"

Step 2: After step 1 is done and only then admin user chooses to set IE as default browser (your default browser is IE but in reality user has set our malicious script as default browser!!!).

Step3: Execute your vulnerable  software that triggers the execution of the malicious code with elevated privileges as before. click button "Homepage" 

Note:
If the tampered keys are already set for ex. IE (booby-trap set) and for some reason the admin users chooses to change default browser from ex. Edge to IE (booby-trapped) then the attack works smoothly.

Both add.bat and malstaller.bat need changes in the username and relative paths to work for you.

Fix:Remove any link/button to external web resources on elevated processes.

In CPP while inside an elevated process (UAC accepted), use:
void safeCall()
{
	system("explorer http://www.test.com");
}

Instead of:
void unsafeCall()
{
	ShellExecute(0, 0, L"http://www.test.com", 0, 0, SW_SHOW);
}
The safeCall() will trigger a new process to open the URL with less privileges, keeping you safe from the attack. Stupid workaround but it works if you need to keep the link.

## Impact

It is possible for an attacker that has limited admin privileges (not full admin with UAC) to hijack the execution of you code by tampering specific registry keys linked to browsers and elevate his privileges ultimately tampering your installation folder by writing malicious code in it or replacing binaries with his own. The installation of your software can be fully compromised.

</details>

---
*Analysed by Claude on 2026-05-24*
