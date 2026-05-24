# Node.js Installer Local Privilege Escalation via Insecure Directory Permissions

## Metadata
- **Source:** HackerOne
- **Report:** 1211160 | https://hackerone.com/reports/1211160
- **Submitted:** 2021-05-28
- **Reporter:** deepsurface-robert
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insecure File Permissions, PATH Hijacking, DLL Hijacking, Local Privilege Escalation
- **CVEs:** CVE-2021-22921, CVE-2021-29221, CVE-2021-22117
- **Category:** auth-crypto

## Summary
Node.js installer on Windows creates installation directories with overly permissive BUILTIN\Users Allow * permissions, enabling unprivileged local users to write arbitrary files. The installation directory is added to the system PATH, allowing attackers to drop malicious executables (e.g., npm.exe) that execute with elevated privileges when invoked by higher-privileged users, or to perform DLL hijacking attacks against node.exe.

## Attack scenario
1. Attacker creates or obtains account with local user privileges on Windows system
2. Attacker identifies Node.js installation directory with insecure permissions (e.g., C:\tools with BUILTIN\Users Allow *)
3. Attacker verifies installation directory is in system PATH environment variable
4. Attacker crafts malicious executable and drops it into Node installation directory with name matching command precedence (e.g., npm.exe before npm.cmd)
5. Privileged user executes command (npm, npx, or other PATH-dependent command)
6. Malicious executable executes with privileges of the privileged user who invoked the command

## Root cause
Node.js installer on Windows does not properly restrict file permissions on installation directories. The directory inherits overly permissive ACLs (BUILTIN\Users Allow *) from parent drive, allowing any local user to create, modify, or delete files. Additionally, the installer adds this unprotected directory to the system PATH, creating multiple escalation vectors.

## Attacker mindset
An unprivileged local attacker seeks persistence and privilege escalation. By exploiting installation directory permissions, they can achieve code execution in elevated contexts without requiring administrative access. The attacker recognizes that system administrators and privileged processes frequently execute commands from PATH, making this a reliable vector for privilege escalation.

## Defensive takeaways
- Restrict file permissions on installation directories to prevent modification by unprivileged users (use NTFS ACLs to grant only necessary groups write access)
- Avoid adding installation directories to system-wide PATH if they are writable by unprivileged users; use absolute paths or restricted PATH entries instead
- Implement installer-time permission validation to ensure installation directories have secure ACLs before adding them to PATH
- Monitor and audit file permission inheritance to prevent overly permissive permissions from being inherited by application directories
- Educate system administrators about the risks of custom installation directories with inherited parent directory permissions
- Implement application-level verification of executable integrity before execution to mitigate DLL hijacking attacks
- Use code signing and signature verification for critical executables to prevent untrusted executable substitution

## Variant hunting
Search for other Windows installers that add directories to PATH without securing permissions (particularly software management tools, development frameworks, runtime environments)
Examine DLL search order for other applications to identify additional DLL hijacking vectors in shared installation directories
Review installer behavior for applications that create user-writable directories in common locations (C:\Program Files, C:\tools, etc.)
Investigate hybrid scenarios where multiple applications share installation directories with inherited permissive ACLs
Analyze Windows service installations that depend on executables in user-writable directories within PATH

## MITRE ATT&CK
- T1547.001
- T1574.001
- T1574.008
- T1059.003
- T1548.002
- T1543.003

## Notes
This vulnerability mirrors CVE-2021-22117 discovered in RabbitMQ by DeepSurface Security team in May 2021, indicating a systemic issue in how software installers handle directory permissions on Windows. The attack is particularly effective because privileged users typically execute commands from PATH without verifying executable origin. Windows executable search order (.exe before .cmd) is exploited for reliable code execution precedence. The vulnerability requires local access but no authentication, making it a concern for shared systems, development environments, and systems where unprivileged users have accounts.

## Full report
<details><summary>Expand</summary>

Node is vulnerable to local privilege escalation attacks under certain conditions on Windows platforms. More specifically, improper configuration of permissions in the installation directory allows an attacker to perform two different escalation attacks: PATH and DLL hijacking.  

To demonstrate this flaw, we first download the latest version of Node from https://nodejs.org/en/download/. At the time of writing, this was node version 14.17.0. 

We follow the standard installation steps, except for the installation directory, which we change to `C:\tools`. This directory can either be created through the installer GUI, or through `mkdir C:\tools`. 

{F1318095}

We also select the option in a later step to “automatically install the necessary tools”. 

In the screenshot below, note the improper permissions, `BUILTIN\Users Allow *`, on the installation directory, which are inherited from the drive root. This gives any local user the ability to create arbitrary files in the installation directory. 

{F1318096}

This unprotected directory has also been added to the system `PATH` variable, allowing an attacker to drop malicious executables in that directory and have them executed by other users in certain circumstances. (Note that you may have to start a new powershell instance to see the `PATH` change.)

{F1318097}

To fully demonstrate the implications of this vulnerability, first create a new unprivileged user. Then, as this user, drop a malicious exe into the `C:\tools` directory and rename it to `npm.exe`. For testing purposes, you can simply do `cp node.exe npm.exe`. Note that the same could be done for `npx`. 

Windows will search for a program with the `.exe` extension first, meaning that the malicious npm.exe will take precedence over `npm.cmd`. 

Now, as the privileged user, try running `npm`. This should drop you into the node shell, demonstrating how an attacker could run a malicious executable. 

{F1318098}

A writable PATH directory would also allow an attacker to hijack the execution of any commands that come later in the path. From the default node installation, this would include chocolatey, a software management tool for Windows. However, such a vulnerability could also affect all programs installed in the future as well. 

Aside from the `PATH` vulnerability, the insecure permissions configured could also allow an attacker to perform a DLL hijacking attack against the `node.exe`. Using [Process Monitor](https://docs.microsoft.com/en-us/sysinternals/downloads/procmon), we can confirm that node attempts to load a number of DLLs from the unprotected folder. 

{F1318099}

For more information on DLL hijacking attacks, see our [blog post](https://deepsurface.com/deepsurface-security-advisory-local-privilege-escalation-in-erlang-on-windows-cve-2021-29221/). 

It is worth noting that a very similar problem was discovered in RabbitMQ and reported by the DeepSurface Security research team. The RabbitMQ team fixed this issue in May 2021. For more information, see: [CVE-2021-22117](https://tanzu.vmware.com/security/cve-2021-22117).

## Impact

A locally  unprivileged attacker could perform a local privilege escalation attack through PATH and DLL hijacking.

</details>

---
*Analysed by Claude on 2026-05-24*
