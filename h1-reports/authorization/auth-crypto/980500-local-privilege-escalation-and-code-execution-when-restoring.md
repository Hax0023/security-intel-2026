# Local Privilege Escalation and Code Execution via Directory Junction Attack in Acronis True Image Quarantine Restore

## Metadata
- **Source:** HackerOne
- **Report:** 980500 | https://hackerone.com/reports/980500
- **Submitted:** 2020-09-12
- **Reporter:** z3ron3
- **Program:** Acronis True Image
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Privilege Escalation, Directory Traversal, TOCTOU (Time-of-check-time-of-use), Symlink/Junction Attack, Arbitrary File Write
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Acronis True Image's Quarantine Restore feature is vulnerable to directory junction attacks, allowing unprivileged users to restore files to arbitrary protected locations. By creating a directory junction pointing to sensitive directories like Windows Startup folders or system directories, attackers can achieve arbitrary file writes and execute code with SYSTEM privileges.

## Attack scenario
1. Attacker creates a folder and places a file containing EICAR test string to trigger antivirus detection
2. Attacker modifies the detected file with malicious content (e.g., calc.exe execution) before quarantine completes
3. Attacker initiates quarantine action which moves the file to Acronis quarantine storage
4. Attacker deletes the original folder and creates a directory junction from the original location to a sensitive target (e.g., Startup, System32)
5. Attacker restores the quarantined file via Acronis Restore feature, which follows the junction to write to the protected target location
6. Malicious file executes with elevated privileges when the system boots or when associated processes run as SYSTEM

## Root cause
The Quarantine Restore feature fails to validate that the original file path has not been replaced with a directory junction or symbolic link between quarantine time and restore time. The vulnerability exists in the TOCTOU window where the file location can be manipulated after detection but before restoration.

## Attacker mindset
An attacker seeks to bypass antivirus protections and Windows filesystem permissions by leveraging a trusted application's privileged operations. By manipulating the filesystem between detection and restoration, the attacker exploits the Restore feature's trust in the original path, achieving arbitrary file writes to protected system locations and ultimately SYSTEM-level code execution.

## Defensive takeaways
- Implement real-time validation of file paths during restore operations to detect and reject directory junctions, symbolic links, and mount points
- Store full filesystem metadata (inode numbers, junction status) at quarantine time and validate during restore to detect path substitution attacks
- Use Windows API functions like GetFinalPathNameByHandle() to resolve the true target of any path before file operations
- Implement file path normalization and canonical form validation before any restore operation
- Perform restore operations with minimal required privileges, not SYSTEM level, to limit blast radius
- Add filesystem monitoring to detect suspicious junction creation near quarantined file locations
- Validate file integrity and prevent TOCTOU conditions by using atomic operations or exclusive locks during detection-to-restore window
- Restrict restore operations to their original locations without following any filesystem redirection

## Variant hunting
Search for similar vulnerabilities in: Windows Defender quarantine restore, other antivirus quarantine features, backup/recovery software restore functions, Windows file recovery tools, system restore points, and any privileged file operation utilities that rely on stored path information without re-validation.

## MITRE ATT&CK
- T1548.004 - Abuse Elevation Control Mechanism: Elevated Execution with Prompt
- T1190 - Exploit Public-Facing Application
- T1547.001 - Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder
- T1036.006 - Masquerading: Rename System Utilities
- T1611 - Escape to Host

## Notes
This is a sophisticated privilege escalation chain exploiting the implicit trust placed in quarantine metadata. The vulnerability requires local access but leads to SYSTEM-level code execution. The EICAR test file demonstrates proof-of-concept with minimal detection evasion. The attack's timeline flexibility (TOCTOU window) makes it practical in real-world scenarios. Acronis scheduler component's SYSTEM privileges amplifies impact.

## Full report
<details><summary>Expand</summary>

## Summary
Acronis True Image has an Antivirus functionality which provides real-time protection and signature-based defenses against viruses and malwares. The Quarantine  has a Restore feature which can be used to restore quarantined files back to their original location if the user is sure that the file is not a threat. 
The Restore file feature makes sure to stop Symlink attack successfully but it is vulnerable to Directory junction attack.
After more testing, I was able to create or modify any file on the system with attacker controlled data that a normal user does not have access to thus resulting in a Local Privilege Escalation vulnerability.


## Steps To Reproduce
[ 1 ] - Create a new folder anywhere on the system.
I created a folder named 'eicar' on my system.  %userprofile% is a Windows environment variable for the user folder which is '**C:\Users\Gr33n**' in my case.
`mkdir %userprofile%\Desktop\eicar`

{F985003}


[ 2 ] - Write the EICAR test string to a file you want to replace or write as the target file as a fake virus for Acronis AV to detect. (eicar.bat in this case)
`echo|set /p="X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*" > %userprofile%\Desktop\eicar\eicar.bat`

{F985007}

After writing EICAR string to a file in 'eicar' folder, Acronis AV will detect it as a threat and will await for instructions wheather to trust the file or quarantine it.

{F985009}


[ 3 ] - Before choosing the Quarantine option, we must change the contents of the detected eicar.bat file.
I will change the contents of eicar.bat file with a simple 'calc' command which opens Microsoft Calculator when executed in a batch file.
`echo calc > %userprofile%\Desktop\eicar\eicar.bat`

{F985012}

[ 4 ] - Click on Quarantine option in the Acronis AV threat detected overlay.

{F985019}

The edited eicar.bat will be moved into Acronis AV's Quarantine folder.

[ 5 ] - Delete the whole eicar folder as it a prerequisite for creating Directory Junction.
`rmdir /S /Q %userprofile%\Desktop\eicar`

{F985021}

[ 6 ] - Create a Directory Junction from the 'eicar' folder to any target folder you want to write to but don't have permission for.
I chose '**C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp**' folder in Windows which executes any programs in it on system start as the logged in user. This means logging in as SYSTEM will execute the program from SYSTEM privileges.

{F985022}

[ 7 ] - Restore the quarantined 'eicar.bat' file from Acronis AV Quarantine.

{F985025}

Acronis AV will restore the 'eicar.bat' to its original location but due to the Directory Junction from that folder to 'Startup' folder, the 'eicar.bat' file will be restored in 'Startup' folder.

{F985030}


## Note

{F985065}

From Acronis AV's settings, I chose 'Block and notify' as Action on detection so that I could easily get screenshots for the demonstration of this report and it is the option that most people prefer.
The vulnerability will also work when 'Quarantine' option is selected if attacker controlled data is written in detected file (eicar.bat) in a short time frame before Acronis AV moves the file into Quarantine which requires a little bit of trial an error.


## Recommendations
Detect Directory Junction on file's origin folder and stop the restore process.

## Impact

##Denial of Service (DoS)
Using the above demonstrated vulnerability, an attacker can corrupt important files which are necessary for the working of the Acronis AV thus denying user from using its protection.

An attacker can also corrupt important files which are necessary for Windows to boot such as '**C:\Windows\System32\drivers\pci.sys**' file. User won't be able to boot into Windows if this file gets corrupted resulting into a DoS attack.

##SYSTEM level Code execution
 [ 1 ] - I saw that Acronis AV users a 'schedul2.exe' application which executes '**C:\Program Files (x86)\Acronis\Agent\bin\adp-rest-util.exe**' with SYSTEM privileges so I tried the above demonstrated attack on 'adp-rest-util.exe' and was able to execute attacker controlled command as SYSTEM as it can seen in the Process Monitor.

{F985043}

[ 2 ] - Attacker can plant malicious DLL files for applications running as SYSTEM or Acronis components itself in directories of DLL search order and the malicious DLL will be loaded when the application is launched resulting in SYSTEM level code execution.

</details>

---
*Analysed by Claude on 2026-05-24*
