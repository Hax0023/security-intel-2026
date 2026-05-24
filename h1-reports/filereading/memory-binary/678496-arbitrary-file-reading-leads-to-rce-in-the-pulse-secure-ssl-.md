# Arbitrary File Reading leads to RCE in Pulse Secure SSL VPN

## Metadata
- **Source:** HackerOne
- **Report:** 678496 | https://hackerone.com/reports/678496
- **Submitted:** 2019-08-21
- **Reporter:** sp1d3rs
- **Program:** Pulse Secure SSL VPN
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Path Traversal, Arbitrary File Reading, Remote Code Execution, Credential Exposure, Command Injection
- **CVEs:** CVE-2019-11510, CVE-2019-11542, CVE-2019-11539, CVE-2019-11538, CVE-2019-11508, CVE-2019-11540
- **Category:** memory-binary

## Summary
A pre-authentication arbitrary file reading vulnerability (CVE-2019-11510) in Pulse Secure SSL VPN allows attackers to extract plaintext credentials from the LMDB database, which can then be used to authenticate and exploit a post-authentication command injection vulnerability (CVE-2019-11539) for remote code execution as root.

## Attack scenario
1. Attacker identifies an exposed Pulse Secure SSL VPN instance without authentication requirements
2. Attacker exploits path traversal vulnerability using specially crafted URI with `/../` sequences to bypass access controls
3. Attacker extracts sensitive files including `/data/runtime/mtmp/lmdb/dataa/data.mdb` containing plaintext VPN credentials
4. Attacker uses extracted credentials to authenticate to the VPN as a legitimate user
5. Attacker exploits post-authentication command injection vulnerability (CVE-2019-11539) to execute arbitrary commands
6. Attacker achieves remote code execution with root privileges and gains access to internal network resources

## Root cause
Insufficient input validation on URI path parameters allowing traversal sequences, combined with storage of credentials in plaintext and lack of input sanitization in command processing endpoints

## Attacker mindset
Opportunistic reconnaissance of internet-facing VPN appliances for unpatched instances; systematic exploitation of known vulnerability chains to escalate from unauthenticated file access to authenticated remote code execution with maximum privileges

## Defensive takeaways
- Implement strict input validation and normalization of URI paths before processing, blocking or rejecting traversal sequences
- Encrypt credentials at rest using strong encryption with secure key management practices
- Apply principle of least privilege for service accounts and isolate VPN appliances with network segmentation
- Implement authentication/authorization checks for all file access endpoints regardless of intended sensitivity
- Use parameterized queries and command builders to prevent injection vulnerabilities in authenticated endpoints
- Maintain current patch levels for all security appliances with automated update mechanisms
- Monitor file access patterns and command execution logs for suspicious traversal or injection attempts
- Deploy WAF rules to detect and block path traversal patterns in HTTP requests

## Variant hunting
Search for similar path traversal patterns in other VPN appliances (Cisco AnyConnect, Fortinet FortiClient, SonicWall); investigate other LMDB-based credential storage mechanisms; test for alternative authentication bypass chains using different file access paths; check for unauthenticated access to other sensitive endpoints beyond file reading

## MITRE ATT&CK
- T1190
- T1083
- T1555
- T1078
- T1059
- T1021
- T1566

## Notes
This is a critical vulnerability chain affecting Pulse Secure SSL VPN instances. The CVE-2019-11510 alone is severe due to pre-authentication access, but the combination with CVE-2019-11539 creates a complete compromise scenario. The fact that credentials are stored in plaintext is a significant security design flaw. The writeup references a BlackHat presentation by Orange Tsai from DEVCORE which provides additional technical details on the vulnerability class.

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

I discovered that https://████ instance is vulnerable to described vulnerabilities.

##POC
Extracting `/etc/passwd` as example:
```
curl -i -k --path-as-is https://██████/dana-na/../dana/html5acc/guacamole/../../../../../../etc/passwd?/dana/html5acc/guacamole/
```
{F561180}

The RCE can be achieved with this chain:
1) Pulse Secure stores credentials in the cleartext.
2) Attacker reads credentials via CVE-2019-11510 (it stored in the `/data/runtime/mtmp/lmdb/dataa/data.mdb`) and authorizes on VPN
3) Attacker exploits CVE-2019-11539 - Post-auth Command Injection achieving RCE as root.

##Suggested fix
Update the Pulse Secure SSL VPN software (also implementing certificate validation can harden access a bit if some similar CVEs will be discovered in future).

## Impact

Remote code execution as root (by reading plaintext credentials and then exploiting CVE-2019-11539 - Post-auth Command Injection) and accessing intranet behind VPN.

</details>

---
*Analysed by Claude on 2026-05-24*
