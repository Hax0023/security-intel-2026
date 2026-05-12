# Arbitrary File Reading leads to RCE in Pulse Secure SSL VPN

## Metadata
- **Source:** HackerOne
- **Report:** 678496 | https://hackerone.com/reports/678496
- **Submitted:** 2019-08-21
- **Reporter:** sp1d3rs
- **Program:** Pulse Secure SSL VPN
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln:** Arbitrary File Reading, Path Traversal, Pre-authentication vulnerability, Credential Exposure, Remote Code Execution, Command Injection
- **CVEs:** CVE-2019-11510, CVE-2019-11542, CVE-2019-11539, CVE-2019-11538, CVE-2019-11508, CVE-2019-11540
- **Category:** memory-binary

## Summary
Pulse Secure SSL VPN is vulnerable to pre-authentication arbitrary file reading via path traversal (CVE-2019-11510), allowing attackers to extract plaintext credentials from the local database. These credentials can then be used to authenticate and exploit a post-authentication command injection vulnerability (CVE-2019-11539) to achieve remote code execution as root.

## Attack scenario
1. Attacker discovers a Pulse Secure SSL VPN instance exposed on the internet
2. Attacker exploits CVE-2019-11510 path traversal to read `/data/runtime/mtmp/lmdb/dataa/data.mdb` containing plaintext VPN credentials without authentication
3. Attacker extracts valid username and password from the credential store
4. Attacker authenticates to the VPN using the stolen credentials
5. Attacker exploits CVE-2019-11539 post-authentication command injection to execute arbitrary system commands
6. Attacker achieves remote code execution as root and gains access to protected intranet resources

## Root cause
Improper input validation on the path traversal parameter combined with insufficient access controls; credentials stored in plaintext in the local database; command injection in authenticated endpoints without proper input sanitization

## Attacker mindset
An attacker recognizes that pre-authentication file read access provides a path to obtain valid credentials, which can then be leveraged with post-authentication vulnerabilities to achieve full system compromise. This chaining of multiple CVEs demonstrates the high-value nature of initial file read access in security contexts.

## Defensive takeaways
- Implement strict input validation and canonicalization for all file path parameters, rejecting path traversal sequences before processing
- Enforce authentication and authorization checks before allowing any file read operations on sensitive system files
- Encrypt sensitive credentials at rest using strong encryption with proper key management
- Sanitize and validate all command injection sensitive functions, use parameterized execution methods instead of shell interpretation
- Apply principle of least privilege - run VPN services with minimal required permissions, not as root
- Implement Web Application Firewall (WAF) rules to detect and block path traversal attempts
- Maintain current patch levels and security updates from vendors immediately upon release
- Monitor for suspicious file access patterns to local database files
- Implement network segmentation to limit impact of VPN compromise

## Variant hunting
Search for other path traversal patterns in Pulse Secure SSL VPN endpoints; audit other endpoints in the `/dana-na/` path hierarchy; test other sensitive file locations accessible via path traversal; examine command injection points in other authenticated administrative functions; verify if other credential storage mechanisms exist; test if similar vulnerabilities exist in related Pulse Secure products

## MITRE ATT&CK
- T1190
- T1552
- T1078
- T1021
- T1059
- T1087
- T1040
- T1005

## Notes
This report chains multiple CVEs (CVE-2019-11510, CVE-2019-11539) to demonstrate a complete attack path from unauthenticated access to root RCE. The vulnerability was patched on 2019-04-25 but the report shows instances still running vulnerable versions. The use of `--path-as-is` flag in curl is critical to bypass path normalization. This represents a critical infrastructure risk as SSL VPNs are often critical security boundaries.

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
*Analysed by Claude on 2026-05-12*
