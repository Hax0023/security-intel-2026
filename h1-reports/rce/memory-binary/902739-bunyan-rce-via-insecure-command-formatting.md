# bunyan - Remote Code Execution via Insecure Command Formatting

## Metadata
- **Source:** HackerOne
- **Report:** 902739 | https://hackerone.com/reports/902739
- **Submitted:** 2020-06-19
- **Reporter:** ahihi
- **Program:** bunyan (npm package)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Command Injection, Improper Input Validation, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
The bunyan logging library versions up to 1.8.12 contain a command injection vulnerability in the CLI tool that allows arbitrary command execution through unsanitized user input passed to the -p flag. An attacker can inject shell commands that will be executed with the privileges of the user running the bunyan CLI, leading to complete system compromise.

## Attack scenario
1. Attacker identifies that a system uses bunyan CLI tool and can be invoked with user-controlled arguments
2. Attacker crafts a malicious payload containing shell metacharacters and commands, e.g., -p "S'11;touch hacked ;'"
3. User or automated process runs bunyan with the attacker-supplied arguments
4. The bunyan CLI constructs a shell command string that includes the unsanitized input
5. The shell executes the injected commands alongside the intended bunyan functionality
6. Attacker achieves arbitrary code execution in the victim's environment with the privileges of the bunyan process

## Root cause
The bunyan CLI tool at bin/bunyan (line ~1224) directly interpolates user input from the -p parameter into a shell command without proper validation or escaping. The input is passed to a command execution function without sanitization, allowing shell metacharacters to break out of the intended command structure.

## Attacker mindset
An attacker would recognize that logging utilities are widely deployed and often called programmatically or via shell scripts. By targeting the CLI interface with command injection, they can achieve RCE with minimal complexity. The high npm download count (920k+ weekly) makes this an attractive target for mass exploitation.

## Defensive takeaways
- Never directly interpolate user input into shell commands; use parameterized execution APIs instead
- If shell execution is necessary, use functions like execFile() with argument arrays rather than shell string concatenation
- Implement strict input validation for all CLI parameters, whitelist allowed characters
- Avoid passing CLI arguments directly to command constructors; parse and validate first
- Use security linters and static analysis tools to detect command injection patterns
- Keep dependencies updated and monitor security advisories for widely-used packages like bunyan
- Run services with minimal required privileges to limit blast radius of RCE

## Variant hunting
Look for similar patterns in other logging libraries (winston, pino, log4js) where CLI tools accept user input for file paths, patterns, or process names. Check for command injection in monitoring tools, log aggregators, and any utility that constructs shell commands from CLI flags. Search for other uses of child_process.exec() or similar functions in popular npm packages without proper input sanitization.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1203 - Exploitation for Client Execution
- T1548 - Abuse Elevation Control Mechanism

## Notes
This is a critical vulnerability affecting a widely-used package with minimal complexity to exploit. The researcher did not contact the maintainer before disclosure, which could indicate responsible disclosure practices were not followed. The vulnerability likely affects all systems using bunyan CLI with untrusted input sources. Fixed in later versions by proper input sanitization or migration to parameterized command execution.

## Full report
<details><summary>Expand</summary>

I would like to report RCE in bunyan
It allows arbitrary commands remotely inside the victim's PC

# Module

**module name:** bunyan
**version:** 1.8.12
**npm page:** `https://www.npmjs.com/package/bunyan`

## Module Description

> Bunyan is a simple and fast JSON logging library for node.js services:

## Module Stats

[920,196] weekly downloads

# Vulnerability

## Vulnerability Description

> The issue occurs because a user input is formatted inside a command that will be executed without any check. https://github.com/trentm/node-bunyan/blob/master/bin/bunyan#L1224

## Steps To Reproduce:

> Run the following command
npm install bunyan
./node_modules/bunyan/bin/bunyan -p "S'11;touch hacked ;'"
> Recheck the files: now hacked has been created
## Patch

> Check input before command

## Supporting Material/References:

> State all technical information about the stack where the vulnerability was found

- [OPERATING SYSTEM VERSION]: Ubuntu 18.04
- [NODEJS VERSION]: v8.10.0
- [NPM VERSION]: 3.5.2

# Wrap up

> Select Y or N for the following statements:

- I contacted the maintainer to let them know: [Y/N] N 
- I opened an issue in the related repository: [Y/N] N

## Impact

RCE on bunyan.

</details>

---
*Analysed by Claude on 2026-05-12*
