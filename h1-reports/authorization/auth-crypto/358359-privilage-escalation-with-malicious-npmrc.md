# Privilege Escalation via Malicious .npmrc onload-script

## Metadata
- **Source:** HackerOne
- **Report:** 358359 | https://hackerone.com/reports/358359
- **Submitted:** 2018-05-28
- **Reporter:** ginden
- **Program:** npm (Node Package Manager)
- **Bounty:** Not disclosed in report
- **Severity:** High
- **Vuln:** Privilege Escalation, Arbitrary Code Execution, Configuration File Injection
- **CVEs:** None
- **Category:** auth-crypto

## Summary
npm's onload-script configuration in .npmrc files is executed with the privileges of the user running npm, without any privilege separation or user awareness mechanisms. An attacker who can write to or control .npmrc can execute arbitrary Node.js code with elevated privileges, including root if the user runs 'sudo npm'.

## Attack scenario
1. Attacker publishes malicious npm package or compromises tutorial/documentation
2. Package/tutorial instructs user to run 'sudo npm' command in a controlled directory
3. Attacker has previously written malicious .npmrc to user's home directory or target folder (via low-privilege process or social engineering)
4. User executes npm command with sudo privileges while in or near attacker-controlled directory
5. npm process reads .npmrc and executes onload-script directive with root privileges
6. Arbitrary attacker payload executes with root access, achieving full system compromise

## Root cause
npm's onload-script feature (line 236 in lib/npm.js) executes JavaScript specified in .npmrc files without privilege separation, user confirmation, or validation of configuration file source/trustworthiness. The feature inherits the execution context of the parent npm process.

## Attacker mindset
An attacker recognizes that npm configuration files are often overlooked by users and that many developers use sudo with npm out of convenience or habit. By hiding malicious configuration in seemingly legitimate repositories or tutorials, and leveraging the widespread practice of running npm with elevated privileges (~30% of surveyed users), the attacker can achieve reliable code execution as root with minimal user interaction.

## Defensive takeaways
- Never run npm or package managers with sudo unless absolutely necessary; use proper permission management instead
- Audit .npmrc files in home directory and project directories for unexpected onload-script entries
- Review npm configuration before executing npm commands: use 'npm config list' to inspect active configuration
- Implement strict npm CLI security practices: disable onload-script execution in privileged contexts or add confirmation prompts
- Use npm's --onload-script='' flag as temporary workaround to disable onload-script execution
- Apply principle of least privilege: configure npm to run without root access when possible
- Validate source of npm configuration files and project repositories before running package manager commands
- Monitor for suspicious .npmrc modifications, particularly in home directories or shared systems

## Variant hunting
Similar privilege escalation vectors in other package managers (pip, gem, composer) that support configuration hooks
Execution of other npm lifecycle hooks (prepare, postinstall) with elevated privileges under different conditions
Privilege escalation through other configuration files that support script execution (e.g., .yarnrc in Yarn)
Abuse of npm's 'user' flag in .npmrc combined with onload-script for privilege escalation chains
Supply chain attacks leveraging .npmrc injection in widely-used tutorial repositories or documentation
Cross-platform variations where .npmrc behavior differs on Windows vs Unix-like systems

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (through malicious npm packages/tutorials)
- T1547 - Boot or Logon Initialization Scripts (onload-script execution on npm invocation)
- T1548 - Abuse Elevation Control Mechanism (sudo misuse)
- T1574 - Hijack Execution Flow (through configuration file injection)
- T1036 - Masquerading (hiding malicious .npmrc in legitimate projects)
- T1566 - Phishing (social engineering to run npm in attacker-controlled directory)

## Notes
Report dates from April-May 2018, affecting npm versions 3.10-6.0. The vulnerability demonstrates how widely-used development tools can amplify privilege escalation risk when configuration mechanisms lack safety guardrails. npm's delayed response indicates the complexity of patching such features without breaking legitimate use cases. The ~30% survey showing sudo npm usage highlights the severity of this vulnerability in real-world scenarios. This bug class is particularly dangerous in CI/CD pipelines and shared development environments.

## Full report
<details><summary>Expand</summary>

Hello.

I'm forwarding to you my conversation with npm staff regarding security issue. It allows to escalate to root privilages of victim using either:

a) basic social engineering - convincing victim to run npm in attacker-controlled folder (eg. repository), including such innocent ones like "npm help" or "npm whoami"  
b) low-privilage process with access to writing files  

I believe that impact of this bug can be high, if someone is able to hijack well-positioned tutorial.

Michał Wadas  

  

---------- Forwarded message ----------  


**Jon Lamendola** (npm)

May 22, 12:19 PDT

Hello Michal,

We're reviewing the impact of changing this behavior and still discussing internally how we might move forward. We understand that it's a risk, but it is also a feature that people use, so we need to fully understand the consequences of making major changes to it before we do. Unfortunately, this can take some time to analyze.

In the meantime, you can alias npm to something like npm --onload-script="" "$@" for a temporary workaround.

Thanks again for reporting this to us.

**Michał Wadas**

May 21, 07:05 PDT

Hi.

Is there any update on this?

**Michał Wadas**

Apr 26, 16:32 PDT

Just noticed - if attacker can control .npmrc (either by writing it from low-privilage script or tricking user into using sudo npm in infected folder), he can set user flag in .npmrc too.

**Jon Lamendola** (npm)

Apr 26, 11:36 PDT

Hello Michal,

Thanks for reporting this to us. I agree, this is a legitimate concern, and I will pass this on to the npm CLI team for discussion.

**Michał Wadas**

Apr 26, 09:54 PDT

Source of issue:

* onload-script is run with privilages of user running npm, in npm process.  
* User can be unaware of .npmrc behaviour

I have pin-pointed it to line 236 in lib/npm.js file in master tree.
Attack scenario:

* Attacker tricks victim into running "sudo npm" in folder (or descendant of folder) with malicious .npmrc
** This can be achieved in many ways - eg. by writing to $HOME/.npmrc from low-privilaged application or tricking victim to open infected directory  
** Example: tutorial asks user to clone git repository, configure it and then run "sudo npm i -g eslint"  
** Example 2: attacker publish malicious code to npm. Code writes to $HOME/.npmrc. Then, attacker can just wait for anyone running sudo npm.
* Then npm runs arbitrary Node.js script with arbitrary permissions

Proposed actions:

* Ignore onload-script when run as super user  
* Ask for confirmation before running onload-script  
* Run onload-script in separate process with lower privilages (it's already supported for other scripts in npm - [https://docs.npmjs.com/misc/<wbr>scripts#user</wbr>](https://docs.npmjs.com/misc/scripts#user) )

These actions should limit scope of attack.

Quick survey in group of Polish programmer showed that around ~30% of npm users use sudo npm

All versions of npm between 3.10 and 6.0 are confirmed to be vulnerable.

Thanks for your attention,  
Michał Wadas

## Impact

Attacker can reliably run arbitrary code with user privilages if he is able to write to .npmrc.

If user use "sudo npm" in folder with malicious .npmrc, attacker can run arbitrary code with root privilages.

</details>

---
*Analysed by Claude on 2026-05-24*
