# Arbitrary File Reading leads to RCE in Pulse Secure SSL VPN via CVE-2019-11510 and CVE-2019-11539

## Metadata
- **Source:** HackerOne
- **Report:** 696276 | https://hackerone.com/reports/696276
- **Submitted:** 2019-09-17
- **Reporter:** sp1d3rs
- **Program:** Pulse Secure
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Arbitrary File Reading, Path Traversal, Command Injection, Cleartext Credential Storage, Remote Code Execution
- **CVEs:** CVE-2019-11510, CVE-2019-11542, CVE-2019-11539, CVE-2019-11538, CVE-2019-11508, CVE-2019-11540
- **Category:** memory-binary

## Summary
The Pulse Secure SSL VPN instance is vulnerable to pre-authentication arbitrary file reading (CVE-2019-11510) via path traversal, allowing attackers to read sensitive files including credentials stored in cleartext. These credentials can then be used to authenticate and exploit post-authentication command injection (CVE-2019-11539) to achieve remote code execution as root.

## Attack scenario
1. Attacker discovers publicly accessible Pulse Secure SSL VPN instance at target domain
2. Attacker leverages CVE-2019-11510 path traversal vulnerability using crafted curl request with --path-as-is flag to bypass path normalization
3. Attacker traverses directory structure using /../ sequences to read /etc/passwd and locate credential storage files
4. Attacker extracts plaintext credentials from configuration files accessible via the arbitrary file reading vulnerability
5. Attacker authenticates to VPN using stolen credentials, bypassing authentication controls
6. Attacker exploits CVE-2019-11539 post-authentication command injection vulnerability to execute arbitrary commands as root user

## Root cause
Insufficient input validation and path normalization in the dana-na endpoint handler allows directory traversal. Additionally, Pulse Secure stores VPN credentials in plaintext on the system, and command injection filters are inadequate in authenticated endpoints.

## Attacker mindset
An attacker seeking access to corporate intranet resources would recognize the high-value target of an unpatched VPN gateway. By chaining multiple vulnerabilities together, they can escalate from unauthenticated file reading to authenticated RCE with root privileges, enabling full network compromise.

## Defensive takeaways
- Immediately patch Pulse Secure SSL VPN to April 25, 2019 release or later
- Implement strict input validation and path canonicalization before processing file paths
- Encrypt all credential storage; never store credentials in plaintext on disk
- Apply defense-in-depth: disable HTTP_BYPASS and enforce proper URI parsing
- Implement command injection filters and parameterization for all authenticated endpoints
- Restrict access to VPN management endpoints via network segmentation and authentication
- Monitor for suspicious path traversal attempts (../ sequences) in access logs
- Use Web Application Firewall (WAF) rules to block path traversal patterns

## Variant hunting
Search for other Pulse Secure endpoints that may bypass path normalization (check all /dana-* paths)
Identify other configuration files readable via CVE-2019-11510 that may contain credentials (system.xml, config files)
Test for similar path traversal vulnerabilities in other VPN appliances (Fortinet, Cisco, Check Point)
Look for additional command injection points in other authenticated endpoints beyond those documented in CVE-2019-11539
Check for similar cleartext credential storage in other Pulse Secure configuration locations
Research if earlier versions of Pulse Secure have unpatched variants of these issues

## MITRE ATT&CK
- T1190
- T1083
- T1021
- T1078
- T1059
- T1087
- T1552
- T1021.002

## Notes
This report demonstrates a critical vulnerability chain affecting Pulse Secure SSL VPN. The vulnerabilities (CVE-2019-11510, CVE-2019-11539, CVE-2019-11542, CVE-2019-11538, CVE-2019-11508, CVE-2019-11540) were publicly disclosed by Orange Tsai at BlackHat/DEFCON 2019. The reporter identified an unpatched instance and responsibly disclosed it. The attack chain is particularly dangerous because it requires no user interaction and results in root-level code execution on a critical network perimeter device. The reporter notes timeout issues may occur based on attacker IP, suggesting possible rate limiting or IP-based restrictions on the target.

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
*Analysed by Claude on 2026-05-24*
