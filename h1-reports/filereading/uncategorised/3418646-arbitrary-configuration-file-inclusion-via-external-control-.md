# Arbitrary Configuration File Inclusion via External Control of File Name or Path in curl

## Metadata
- **Source:** HackerOne
- **Report:** 3418646 | https://hackerone.com/reports/3418646
- **Submitted:** 2025-11-10
- **Reporter:** rootsecret3
- **Program:** curl/libcurl
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** CWE-73: External Control of File Name or Path, Arbitrary File Read, Arbitrary File Write, Configuration Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
A critical vulnerability exists in curl 8.15.0 where the --config option accepts user-controlled file paths without adequate validation, allowing attackers to execute arbitrary configuration directives. An attacker can trick users into running curl with a malicious configuration file, enabling local file read, arbitrary file write, and potential code execution. The vulnerability stems from insufficient path validation in the curlx_fopen function and direct processing of configuration file contents via the getparameter function.

## Attack scenario
1. Attacker creates a malicious .curlrc configuration file in a predictable location (e.g., /tmp/malicious.curlrc) containing directives like 'url = "file:///etc/passwd"' and 'output = "/tmp/stolen_passwd.txt"'
2. Attacker tricks or socially engineers a user into executing curl with the --config flag pointing to the malicious file
3. curl loads the configuration file without validating its origin or contents, and the curlx_fopen function opens the attacker-controlled path
4. The getparameter function processes each line from the malicious configuration, executing dangerous instructions such as reading sensitive files via file:// protocol
5. Arbitrary files are read from the system and written to attacker-specified locations, or network requests are made to internal resources via SSRF
6. Attacker gains access to sensitive credentials, system information, or achieves persistent code execution by overwriting shell startup files

## Root cause
Lack of adequate validation on the user-supplied configuration file path in the --config option. The vulnerability occurs at two levels: (1) the curlx_fopen function accepts the filename directly without validating its source or trustworthiness, and (2) the getparameter function blindly executes all directives from the configuration file without restrictions on dangerous operations like file:// URLs or output redirection.

## Attacker mindset
An attacker would recognize that users often run curl with configuration files, and that configuration files are typically read from trusted locations. By placing a malicious configuration file in a predictable location or manipulating PATH/environment variables, the attacker can achieve code execution or data exfiltration without requiring direct command-line access. The attacker exploits the implicit trust users place in configuration mechanisms.

## Defensive takeaways
- Implement strict validation and sanitization of file paths passed via command-line arguments, including canonicalization and whitelist checks for allowed directories
- Restrict dangerous operations in configuration files (e.g., file:// protocol access, arbitrary output redirection) or require explicit user consent for sensitive actions
- Use secure defaults for configuration file locations and reject loading configuration files from world-writable directories like /tmp
- Implement a warning system that alerts users when curl is about to load configuration files from non-standard locations
- Apply principle of least privilege: when curl is run by web servers or other services, restrict its file access permissions
- Perform security audits on parsing logic for configuration files, testing with adversarial inputs to prevent injection attacks
- Consider requiring explicit opt-in for potentially dangerous configuration options rather than allowing them by default

## Variant hunting
Look for similar vulnerabilities in other utilities that accept configuration files via command-line arguments (wget, git, ssh, etc.). Search for cases where file paths are derived from user input without proper validation. Investigate whether environment variables (e.g., CURL_HOME, HOME) can be manipulated to load configuration files from attacker-controlled locations. Test for symlink attacks where configuration files are symbolic links to sensitive system files.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1574: Hijack Execution Flow
- T1083: File and Directory Discovery
- T1005: Data from Local System
- T1041: Exfiltration Over C2 Channel
- T1543: Create or Modify System Process
- T1059: Command and Scripting Interpreter

## Notes
The report explicitly states that AI tools were used only for summarization, CVSS calculation, and report structure drafting, not for exploit code generation or vulnerability discovery. The vulnerability is particularly dangerous because curl is a widely-used utility in scripts, automation, and containers. The attack surface is large given curl's prevalence in development and production environments. The writeup demonstrates the vulnerability with a clear proof-of-concept but stops short of showing more sophisticated attacks like code execution via shell startup file overwriting or SSRF attacks against internal services.

## Full report
<details><summary>Expand</summary>

## Summary:
The Arbitrary Configuration File Inclusion (ACFI) vulnerability was identified in the curl utility via the --config <file> option. This flaw is a form of External Control of File Name or Path (CWE-73), occurring due to the lack of adequate validation on the user-supplied configuration file path.

An attacker can leverage this weakness to:
Trick a user into executing curl with a malicious configuration file located at an arbitrary path (e.g., /tmp/malicious.curlrc).

Significantly control curl's behavior, including setting dangerous options such as url = "file:///" and output = "...".

The impact is Critical, potentially allowing the attacker to perform a Local File Read of sensitive files like /etc/passwd and an Arbitrary File Write to arbitrary locations on the victim's system.

"I confirm that I performed the vulnerability discovery and core technical analysis manually. However, AI tools (such as Gemini/ChatGPT) were utilized solely for summarizing the findings, calculating the CVSS score, and drafting the formal report structure based on my raw technical data. AI was not used to generate the exploit code or perform the scan/discovery."

## Affected version
curl/libcurl version :  8.15.0
platform : x86_64-pc-linux-gnu

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1.  create a malicious configuration file :
Open the terminal and run the following command to create a file named /tmp/malicious.curlrc. This file will instruct curl to read the /etc/passwd file and save it to /tmp/stolen_passwd.txt.

echo 'url = "file:///etc/passwd"' > /tmp/malicious.curlrc
echo 'output = "/tmp/stolen_passwd.txt"' >> /tmp/malicious.curlrc

  2. and then Run curl and direct it to use the configuration file you just created using the --config

curl --config /tmp/malicious.curlrc

  3. Then we check whether the file /tmp/stolen_passwd.txt has been successfully created and contains the contents of /etc/passwd.

cat /tmp/stolen_passwd.txt

The results are in.

curl executes instructions from configuration files without warning, reads sensitive local files (/etc/passwd), and writes them to a location specified by the attacker (/tmp/stolen_passwd.txt).

This proves that attackers can read arbitrary local files and write to locations accessible to users running curl

## Supporting Material/References:
This vulnerability stems from the way curl parses configuration files without adequate path validation.

source file: /curl/src/

The curlx_fopen function is called with a filename that is directly controlled by the user via the --config argument.
vulnerable lines of code : 
file = curlx_fopen(filename, FOPEN_READTEXT);

Execution point (sink): Each line of the configuration file is then processed by the `getparameter` function, which executes malicious instructions such as `url` and `output`.
code :
res = getparameter(option, param, &usedarg, config, max_recursive);

  * [attachment / reference]
 CWE-73: External Control of File Name or Path

## Impact

## Summary: The impact of this vulnerability is Critical, as it gives attackers the ability to perform several dangerous actions on the target system, depending on the access rights of the user running curl.

 1. Sensitive Information Disclosure:
An attacker can read any file accessible to the user. This
includes, but is not limited to:
* User Credentials: Private SSH keys (~/.ssh/id_rsa), shell
history files (~/.bash_history), API tokens, or cloud credentials stored in ~/.aws/credentials.
* Application Secrets: Configuration files containing database passwords, API keys, or other sensitive data.
* System Data: Files such as /etc/passwd or system logs that can be used for user enumeration and system mapping.

 2. File Modification and Potential Code Execution (Arbitrary File Write & Code Execution):
  By using output parameters in configuration files, attackers can write or overwrite files in permitted locations. Attack scenarios
  include:
* Achieving Persistent Code Execution: Overwriting startup shell files such as ~/.bashrc or ~/.profile to insert malicious commands that will be executed every time a user logs in.
* Planting a Web Shell: If curl is run by the web server, attackers can write PHP files or other scripts to the web directory
(/var/www/html/shell.php), which gives them remote shell access.
* Compromising System Integrity: Overwriting important files that can cause Denial of Service (DoS).

3. SSRF (Server-Side Request Forgery) Attack:
  An attacker can force the server to make network requests to internal resources that are not accessible from the outside. By setting url = “http://169.254.169.254/latest/meta-data/” (in an AWS environment) or url = “http://localhost:8080/admin”, attackers can scan the internal network and steal data from internal services.

Overall, this vulnerability compromises the three pillars of security: Confidentiality, Integrity, and potentially Availability of the system.

</details>

---
*Analysed by Claude on 2026-05-24*
