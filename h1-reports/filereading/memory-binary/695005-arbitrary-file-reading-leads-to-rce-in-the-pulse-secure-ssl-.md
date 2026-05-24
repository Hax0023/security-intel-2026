# Arbitrary File Reading leads to RCE in Pulse Secure SSL VPN

## Metadata
- **Source:** HackerOne
- **Report:** 695005 | https://hackerone.com/reports/695005
- **Submitted:** 2019-09-14
- **Reporter:** sp1d3rs
- **Program:** Pulse Secure
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Arbitrary File Reading, Path Traversal, Credential Exposure, Command Injection, Remote Code Execution
- **CVEs:** CVE-2019-11510, CVE-2019-11542, CVE-2019-11539, CVE-2019-11538, CVE-2019-11508, CVE-2019-11540
- **Category:** memory-binary

## Summary
The Pulse Secure SSL VPN instance is vulnerable to CVE-2019-11510, allowing unauthenticated arbitrary file reading via path traversal. Combined with cleartext credential storage and post-auth command injection (CVE-2019-11539), an attacker can achieve remote code execution as root and access the protected corporate intranet.

## Attack scenario
1. Attacker exploits CVE-2019-11510 path traversal vulnerability using crafted URL with ../ sequences to bypass directory restrictions
2. Attacker reads sensitive files like /etc/passwd and configuration files containing plaintext VPN credentials
3. Attacker obtains valid VPN credentials stored in cleartext within accessible configuration files
4. Attacker authenticates to the VPN using stolen credentials
5. Attacker exploits CVE-2019-11539 post-auth command injection vulnerability to execute arbitrary system commands
6. Attacker achieves remote code execution with root privileges and gains access to corporate intranet resources

## Root cause
Insufficient input validation on file path parameters allowing traversal sequences; inadequate access controls on pre-auth endpoints; storage of credentials in plaintext; unsafe command processing in post-auth functionality

## Attacker mindset
An attacker can leverage public vulnerability disclosures and proof-of-concepts from security conferences to identify and exploit unpatched VPN endpoints, using multi-stage attack chains to escalate from read-only file access to full system compromise

## Defensive takeaways
- Implement strict input validation and canonicalization for file path parameters; reject or escape traversal sequences
- Enforce authentication requirements on all sensitive endpoints; avoid exposing pre-auth arbitrary file reading capabilities
- Never store credentials in plaintext; use encrypted vaults with proper access controls and encryption
- Sanitize and validate all command-line inputs; avoid dynamic command construction; use allowlists for permitted operations
- Implement prompt security patching processes for critical VPN infrastructure
- Apply principle of least privilege; avoid running VPN services as root
- Monitor and alert on suspicious file access patterns and unusual authentication followed by command execution

## Variant hunting
Search for similar path traversal vulnerabilities in other Pulse Secure components (portal, admin interfaces); examine other VPN appliances for cleartext credential storage; test for command injection in other parameter inputs; investigate other pre-auth endpoints for information disclosure

## MITRE ATT&CK
- T1190
- T1083
- T1005
- T1552
- T1021
- T1059
- T1078

## Notes
CVE-2019-11510 is a pre-auth vulnerability enabling unauthenticated file reading, making it exceptionally dangerous. The chain combining it with plaintext credential storage (CVE-2019-11508) and post-auth command injection (CVE-2019-11539) demonstrates the importance of addressing multiple vulnerabilities holistically. This vulnerability set was disclosed at Black Hat 2019 by Orange Tsai, indicating widespread researcher awareness and likely exploitation in the wild.

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
*Analysed by Claude on 2026-05-24*
