# Arbitrary File Reading leads to RCE in Pulse Secure SSL VPN via CVE-2019-11510 and CVE-2019-11539

## Metadata
- **Source:** HackerOne
- **Report:** 695005 | https://hackerone.com/reports/695005
- **Submitted:** 2019-09-14
- **Reporter:** sp1d3rs
- **Program:** Pulse Secure SSL VPN
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Arbitrary File Reading, Path Traversal, Command Injection, Cleartext Credential Storage, Pre-authentication Remote Code Execution
- **CVEs:** CVE-2019-11510, CVE-2019-11542, CVE-2019-11539, CVE-2019-11538, CVE-2019-11508, CVE-2019-11540
- **Category:** memory-binary

## Summary
The Pulse Secure SSL VPN instance is vulnerable to pre-authentication arbitrary file reading (CVE-2019-11510) due to improper path validation in the dana-na endpoint, combined with cleartext credential storage and post-authentication command injection (CVE-2019-11539). An unauthenticated attacker can chain these vulnerabilities to achieve remote code execution as root on the VPN appliance.

## Attack scenario
1. Attacker crafts malicious request using path traversal bypass with --path-as-is flag to the vulnerable dana-na endpoint
2. Attacker reads /etc/passwd and other sensitive files containing cleartext credentials via CVE-2019-11510
3. Attacker extracts valid VPN credentials from plaintext configuration files
4. Attacker authenticates to the VPN using stolen credentials
5. Attacker exploits post-authentication command injection vulnerability (CVE-2019-11539) in a vulnerable endpoint
6. Attacker executes arbitrary commands as root user, gaining full control of the VPN appliance and access to protected intranet

## Root cause
Insufficient input validation and improper path normalization in the dana-na/html5acc endpoint allowing directory traversal bypass using ../sequences combined with the --path-as-is curl flag. Additionally, credentials stored in plaintext and lack of command input sanitization in post-auth functionality.

## Attacker mindset
Opportunistic attacker leveraging publicly disclosed vulnerabilities from high-profile security conferences (BlackHat/DEFCON). The multi-step attack chain exploiting multiple CVEs demonstrates sophisticated understanding of attack surface and privilege escalation techniques targeting enterprise VPN infrastructure.

## Defensive takeaways
- Implement strict input validation and canonicalize all file paths before access, rejecting requests with ../ sequences
- Apply principle of least privilege - never store credentials in plaintext, use encrypted storage with proper key management
- Enforce strong authentication mechanisms beyond password-based VPN access
- Implement rate limiting and anomaly detection on file access patterns
- Sanitize and validate all command inputs, use allowlists for permitted commands
- Disable HTTP methods that permit path traversal techniques (enforce proper URL handling)
- Segment VPN infrastructure from sensitive internal systems
- Apply security patches immediately for pre-authentication vulnerabilities
- Monitor for exploitation attempts including unusual file access patterns and parameter variations

## Variant hunting
Search for similar path traversal patterns in other Pulse Secure endpoints (dana/, admin/, etc.). Investigate other parameters accepting file paths. Test for authenticated command injection in different POST endpoints handling system configuration. Check for credential exposure in other configuration files or backup locations. Examine error messages for information disclosure.

## MITRE ATT&CK
- T1190
- T1080
- T1078
- T1059
- T1021
- T1566
- T1040
- T1005

## Notes
This report chains together multiple CVEs disclosed by Orange Tsai (DEVCORE) at BlackHat USA 2019. CVE-2019-11510 is the critical pre-auth arbitrary file read that enables the attack chain. The vulnerability affects widely-deployed enterprise VPN infrastructure, making it high-value target. Report redacts target domain but indicates successful exploitation. Fixes were released 2019-04-25, yet many organizations remained unpatched at time of report submission.

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
███████
█████████
██████████
████
█████
██████
███████
████████
███████
```

The RCE can be achieved with this chain:
1) Pulse Secure stores credentials in the cleartext.
2) Attacker reads credentials  and authorizes on VPN
3) Attacker exploits CVE-2019-11539 - Post-auth Command Injection achieving RCE as root.

##Suggested fix
Update the Pulse Secure SSL VPN software.

## Impact

Remote code execution as root (by reading plaintext credentials and then exploiting CVE-2019-11539 - Post-auth Command Injection) and accessing intranet behind VPN.
You can see here example report to Twitter by Orange Tsai: https://hackerone.com/reports/591295

</details>

---
*Analysed by Claude on 2026-05-12*
