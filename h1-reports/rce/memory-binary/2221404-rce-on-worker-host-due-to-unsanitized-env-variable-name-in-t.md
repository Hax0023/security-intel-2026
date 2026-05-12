# RCE on worker host due to unsanitized environment variable names in Taskcluster task definitions

## Metadata
- **Source:** HackerOne
- **Report:** 2221404 | https://hackerone.com/reports/2221404
- **Submitted:** 2023-10-23
- **Reporter:** ebrietas
- **Program:** Mozilla Client Security Bug Bounty (Taskcluster/community-tc.services.mozilla.com)
- **Bounty:** Not explicitly stated in report
- **Severity:** critical
- **Vuln:** Command Injection, Insufficient Input Validation, Remote Code Execution
- **CVEs:** None
- **Category:** memory-binary

## Summary
Taskcluster's worker code fails to sanitize environment variable names in task definitions before passing them to podman commands, allowing arbitrary command execution on the worker host. The custom shell.escape function properly sanitizes most parameters (image names, commands, artifact paths) but is not applied to environment variable names. Community-tc.services.mozilla.com allows any valid GitHub user to create tasks in example worker groups, making this vulnerability directly exploitable.

## Attack scenario
1. Attacker creates a GitHub account and authenticates to community-tc.services.mozilla.com
2. Attacker navigates to the task creation interface and crafts a malicious task definition
3. Attacker injects shell metacharacters and arbitrary commands as environment variable names (e.g., 'test2 --help ; whoami ; ls -lah ;')
4. Attacker submits the task to an accessible worker queue (e.g., proj-misc/tutorial)
5. The Taskcluster worker processes the task and constructs a podman command without properly escaping the env variable names
6. Arbitrary commands execute on the worker host with the worker process privileges before the container is even launched

## Root cause
The shell.escape function from the shell package is applied to user-supplied parameters like image names, commands, and artifact paths, but the implementation fails to apply the same sanitization to environment variable names during podman command construction. This creates an inconsistency in input validation where only certain parameters receive protection.

## Attacker mindset
An attacker with basic GitHub credentials recognizes that the publicly accessible community Taskcluster instance accepts task definitions from any valid user. By analyzing the task definition schema and testing shell escape mechanisms, the attacker discovers that environment variable names bypass sanitization. The attacker exploits this to execute reconnaissance commands (whoami, ls) on the worker host, potentially leading to privilege escalation, lateral movement, or worker compromise.

## Defensive takeaways
- Apply consistent input validation across all user-supplied parameters in task definitions, not selectively to certain fields
- Use allowlists for environment variable names (alphanumeric and underscore only) rather than blacklist-based escaping
- Sanitize all data that influences command construction, including variable names, not just values
- Implement defense-in-depth: run workers in containers or VMs with strict process isolation to limit blast radius of RCE
- Restrict access to public Taskcluster instances to authenticated users with explicit grants, avoiding blanket permissions
- Add security testing to verify that all injection vectors are covered by sanitization functions
- Consider using structured data formats (JSON-based APIs) instead of shell command construction to avoid injection entirely

## Variant hunting
Check if command field escaping can be bypassed with newlines or null bytes
Test artifact paths, image names, and command arguments for similar escaping gaps
Examine other task payload fields (labels, volumes, ports) for sanitization coverage
Look for similar command injection vulnerabilities in other Taskcluster components (queue, auth, provisioner)
Test if escaping can be bypassed through Unicode normalization or encoding tricks
Investigate whether other worker backends (EC2, Kubernetes) have the same vulnerability

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter
- T1203: Exploitation for Client Execution
- T1610: Deploy Container
- T1078: Valid Accounts

## Notes
This vulnerability demonstrates the critical importance of comprehensive input validation. The fact that shell.escape was implemented but not universally applied to all relevant fields suggests a gap in security architecture review. The public nature of community-tc.services.mozilla.com and lack of granular access controls amplified the exploitability. The researcher's initial uncertainty about whether to report it under the Mozilla Client bug bounty indicates potential confusion about scope boundaries for infrastructure vulnerabilities.

## Full report
<details><summary>Expand</summary>

## Summary:
This issue affects Taskcluster's worker code and not  just this instance but I did not see an easy way to report the vulnerability as well since I was unsure if this would qualify for the  Mozilla Client bug bounty. The task cluster definition attempts to escape parameters that are passed to the podman command prior to running the container to execute the task, the custom shell.escape function (https://github.com/taskcluster/shell/blob/master/shell.go)  is quite robust and is used on most user supplied parameters including docker image name, commands to run , and artifact path which prevents trivial command execution however it is not applied on the environment variable name itself allowing for command execution on the worker host.  Additionally, the community-tc.services.mozilla.com instance allows for any valid user to utilize an example worker group which allows for RCE on the worker host.


## Steps To Reproduce:

1. Create a github account if you do not have one and then login to https://community-tc.services.mozilla.com/ 
2. Visit https://community-tc.services.mozilla.com/tasks/create to create a new task. Copy and paste the following definition and then click the green save icon to run your task:
```yaml
retries: 0
created: '2023-10-23T08:10:11.044Z'
deadline: '2023-10-23T11:10:11.044Z'
expires: '2024-10-23T11:10:11.044Z'
taskQueueId: proj-misc/tutorial
projectId: none
tags: {}
scopes: []
payload:
  env:
# Commands to run in here
    test2 --help ; whoami ; ls -lah ;: '--help'
  image: ubuntu:latest
  command:
    - /bin/bash
    - '-c'
    - 'echo hello'
  maxRunTime: 5000
extra: {}
metadata:
  name: example-task
  description: An **example** task
  owner: name@example.com
  source: https://community-tc.services.mozilla.com/tasks/create
schedulerId: taskcluster-ui
```

{F2795414}

3. 
Wait for your task to run (it should fail) and then view the live logs to check for the output of the commands. 
{F2795415}

## Impact

## Summary:
Command execution outside of the intended container for the worker.

</details>

---
*Analysed by Claude on 2026-05-11*
