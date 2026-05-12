# Arbitrary File Reading leads to RCE in Pulse Secure SSL VPN via CVE-2019-11510 and CVE-2019-11539

## Metadata
- **Source:** HackerOne
- **Report:** 696276 | https://hackerone.com/reports/696276
- **Submitted:** 2019-09-17
- **Reporter:** sp1d3rs
- **Program:** Pulse Secure
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Arbitrary File Reading, Path Traversal, Cleartext Credential Storage, Command Injection, Remote Code Execution
- **CVEs:** CVE-2019-11510, CVE-2019-11542, CVE-2019-11539, CVE-2019-11538, CVE-2019-11508, CVE-2019-11540
- **Category:** memory-binary

## Summary
Pulse Secure SSL VPN instances were vulnerable to pre-authentication arbitrary file reading (CVE-2019-11510) via path traversal, combined with post-authentication command injection (CVE-2019-11539). An unauthenticated attacker could read sensitive files including credentials stored in cleartext, then leverage those credentials to execute arbitrary commands as root.

## Attack scenario
1. Attacker identifies vulnerable Pulse Secure SSL VPN instance via reconnaissance
2. Attacker exploits CVE-2019-11510 path traversal to read /etc/passwd and other sensitive files without authentication
3. Attacker locates and reads configuration files containing plaintext VPN credentials
4. Attacker authenticates to VPN using harvested credentials
5. Attacker exploits CVE-2019-11539 post-authentication command injection vulnerability
6. Attacker achieves remote code execution as root user with full VPN and intranet access

## Root cause
Improper input validation in the dana-na path handling allowing path traversal bypasses, combined with credentials stored in plaintext configuration files and insufficient input sanitization in command processing functions.

## Attacker mindset
An attacker targeting corporate infrastructure would recognize the VPN as a high-value target. The pre-auth file reading vulnerability bypasses authentication entirely, and discovering plaintext credentials provides an easy escalation path. The combination creates a critical attack chain requiring no prior access.

## Defensive takeaways
- Implement strict input validation and canonicalization for all file path parameters
- Never store credentials in plaintext; use encrypted vaults with strong key management
- Apply principle of least privilege - avoid running VPN services as root
- Implement proper output encoding and parameterized commands to prevent injection attacks
- Maintain security patch management with immediate updates for critical VPN vulnerabilities
- Use Web Application Firewalls to detect and block path traversal patterns
- Implement authentication/authorization checks before any file access operations

## Variant hunting
Search for similar path traversal patterns in other Pulse Secure modules, examine other VPN solutions for cleartext credential storage, investigate whether other services using the dana framework have similar vulnerabilities, test for alternative command injection vectors in post-auth functions.

## MITRE ATT&CK
- T1190
- T1083
- T1078
- T1059
- T1555
- T1021

## Notes
This report chains multiple CVEs from the 2019 Orange Tsai research presentation. The vulnerability was patched on 2019-04-25. The attack requires no pre-existing access, making it extremely dangerous. The researcher was appropriately cautious about IP blocking by changing VPN endpoints during testing.

## Full report
<details><summary>Expand</summary>

##Description
Hello. Some time ago, researcher Orange Tsai from DEVCORE team had a talk on Defcon/BlackHat regarding Pulse Secure SSL VPN vulnerabilities fixed on 2019/4/25:
**CVE-2019-11510 - Pre-auth Arbitrary File Reading**
CVE-2019-11542 - Post-auth Stack Buffer Overflow
**CVE-2019-11539 - Post-auth Command Injection**
CVE-2019-11538 - Post-auth Arbitrary File Reading
**CVE-2019-11508 - Post-auth Arbitrary File Writing**
CVE-2019-11540 - Post-auth Session Hijacking

Link to the slides: https://i.blackhat.com/USA-19/Wednesday/us-19-Tsai-Infiltrating-Corporate-Intranet-Like-NSA.pdf

I discovered that `https://██████████` instance is vulnerable to described vulnerabilities.

##POC

Reading `/etc/passwd` via CVE-2019-11510:
```
curl -i -k --path-as-is https://██████████/dana-na/../dana/html5acc/guacamole/../../../../../../etc/passwd?/dana/html5acc/guacamole/
```
```
root:x:0:0:root:/:/bin/bash
nfast:x:0:0:nfast:/:/bin/bash
bin:x:1:1:bin:/:
nobody:x:99:99:Nobody:/:
dns:x:98:98:DNS:/:
term:x:97:97:Telnet/SSH:/:
web80:x:96:96:Port 80 web:/:
rpc:x:32:32:Rpcbind Daemon:/var/cache/rpcbind:/sbin/nologin
```
█████

The RCE can be achieved with this chain:
1) Pulse Secure stores credentials in the cleartext.
2) Attacker reads credentials  and authorizes on VPN
3) Attacker exploits CVE-2019-11539 - Post-auth Command Injection achieving RCE as root.

##Suggested fix
Update the Pulse Secure SSL VPN software.

##Note
If you experience timeout errors when reproducing, try to change your IP/VPN

## Impact

Remote code execution as root (by reading plaintext credentials and then exploiting CVE-2019-11539 - Post-auth Command Injection) and accessing intranet behind VPN.
You can see here example report to Twitter by Orange Tsai: https://hackerone.com/reports/591295

</details>

---
*Analysed by Claude on 2026-05-12*
