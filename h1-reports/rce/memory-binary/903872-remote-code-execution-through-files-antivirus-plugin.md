# Remote Code Execution through Files_Antivirus Plugin Configuration Injection

## Metadata
- **Source:** HackerOne
- **Report:** 903872 | https://hackerone.com/reports/903872
- **Submitted:** 2020-06-20
- **Reporter:** pabl00nicarres
- **Program:** OwnCloud
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Arbitrary Code Execution, Command Injection, Unsafe Command Execution, Privilege Escalation, Information Disclosure
- **CVEs:** None
- **Category:** memory-binary

## Summary
The files_antivirus plugin in OwnCloud allows authenticated administrators to achieve Remote Code Execution by injecting an arbitrary executable path (PHP interpreter) into the antivirus scanner configuration. The plugin fails to validate or sanitize the configured antivirus binary path, executing user-supplied files through the specified interpreter with application-level privileges.

## Attack scenario
1. Attacker obtains or compromises OwnCloud administrator credentials
2. Attacker downloads the configuration report from the admin dashboard to enumerate sensitive paths including datadirectory and PHP interpreter location
3. Attacker uploads a file containing PHP code to the OwnCloud file storage system
4. Attacker navigates to the Protection settings and modifies the clamscan binary path to point to the PHP interpreter (e.g., /usr/bin/php)
5. Attacker configures the first argument to reference the previously uploaded PHP file
6. Upon saving or triggering antivirus scan, the system executes the PHP code through the configured interpreter with application privileges

## Root cause
The files_antivirus plugin does not validate, sanitize, or restrict the configured antivirus scanner binary path. The application blindly executes whatever path is specified in the configuration combined with uploaded file paths, allowing path traversal and arbitrary executable substitution. Additionally, configuration reports expose absolute file paths and system information to authenticated users without proper access controls.

## Attacker mindset
An insider threat or compromised admin account holder leverages trusted administrative access to reconfigure security mechanisms as attack vectors. By weaponizing the antivirus configuration interface, the attacker converts a legitimate system feature into an RCE gadget, assuming the developers did not validate the binary path or consider malicious admin behavior.

## Defensive takeaways
- Implement strict whitelist validation for antivirus binary paths; only allow known safe executables from system directories
- Use absolute path validation and symbolic link resolution to prevent path traversal attacks
- Restrict configuration reports to exclude or redact sensitive paths (datadirectory, interpreter paths, absolute file locations)
- Implement command execution with minimal privileges and use allow-lists for permitted binaries rather than user-supplied paths
- Apply principle of least privilege: separate antivirus configuration permissions from file upload permissions
- Use shell_exec/proc_open alternatives that prevent command injection (e.g., exec with argument array)
- Implement audit logging for all antivirus configuration changes by administrators
- Enforce code review processes for plugins handling system command execution
- Consider sandboxing or containerization of antivirus scanning processes

## Variant hunting
Similar vulnerabilities likely exist in other OwnCloud plugins that accept executable paths or system commands as configuration (backup plugins, external storage integrations, media processors). Search for user-supplied path concatenation in shell_exec(), proc_open(), passthru(), or system() calls. Review any admin interface that accepts file paths, interpreter paths, or binary names without validation.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1078 - Valid Accounts
- T1548 - Abuse Elevation Control Mechanism
- T1203 - Exploitation for Client Execution
- T1569 - System Services

## Notes
This vulnerability requires administrator-level access, limiting the attack surface but presenting significant risk in multi-tenant or compromised admin scenarios. The researcher's observation about design philosophy is apt—administrative access should not directly grant code execution capability. The vulnerability is particularly severe because it exploits a legitimate security feature (antivirus integration) as the attack vector, likely bypassing many security monitoring tools.

## Full report
<details><summary>Expand</summary>

Hi,
I would like to report a Remote Code Execution in OwnCloud. 
The flaw is exploitable as an authenticated user and level of privileges required is "Administrator".
Vulnerable component is the plugin "files_antivirus", freely downloadable via the market and available in owncloud github repository at  
+ https://github.com/owncloud/files_antivirus.

Environment used: LAMP stack . Owncloud version:  10.4.1.3.
Considerations: In owncloud separation between application/database/system layer is cleary a (good) design choice and neither an Administrator user in a default configuration scenario is supposed to upload custom code if not provided with shell access level.
POC: Below the steps to reproduce the issue and get code execution:
+ Login in owncloud as Administrator.
+ If not installed, go to marketplace and install the aforementioned "files_antivirus" plugin.
+ Download the config report from the general menu. {F875798}
+ Open the report, all sensitive infos are stripped but absolute paths are still there. We're mostly interested in the config value "datadirectory" in order to understand where exactly the uploaded files are. Other interesting values are in the "enviroment structure, where we can get the php interpreter path (just an example, this can be done with bash etc.). {F876062}
+ Go to "Files" and upload a file with php code, extension is not relevant.
{F876139}
+ Go to "Protection" and, using the previously obtained path from the config report, set the clamscan av path with the PHP interpreter path. The first argument will be the file with php code we just uploaded (the use of escapeshellarg function is not relevant here, we're not injecting shell arguments/commands). {F876153}
+ Save the new config, ignore the error about the scan that cannot be executed and verify that the PHP code was successfully executed.

Kind Regards
Paolo Serracino

## Impact

Depends from the environment, an attacker who is able to get admin creds could use this flaw to move laterally, steal cloud metadata infos and so on.

</details>

---
*Analysed by Claude on 2026-05-12*
