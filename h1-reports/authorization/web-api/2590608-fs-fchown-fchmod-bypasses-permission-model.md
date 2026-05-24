# fs.fchown/fchmod bypasses Node.js permission model

## Metadata
- **Source:** HackerOne
- **Report:** 2590608 | https://hackerone.com/reports/2590608
- **Submitted:** 2024-07-09
- **Reporter:** 4xpl0r3r
- **Program:** Node.js (HackerOne IBB)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Authorization Bypass, Permission Model Bypass, Privilege Escalation
- **CVEs:** CVE-2024-36137
- **Category:** web-api

## Summary
Node.js experimental permission model fails to validate operations on file descriptors, allowing fs.fchown() and fs.fchmod() to bypass permission restrictions. An attacker with a read-only file descriptor can modify file ownership and permissions despite --allow-fs-write restrictions being in place.

## Attack scenario
1. Attacker opens a file with read-only permissions using fs.open()
2. Application grants a read-only file descriptor to the attacker-controlled code
3. Attacker calls fs.fchown() with the read-only descriptor to change file ownership
4. Attacker calls fs.fchmod() with the read-only descriptor to modify file permissions
5. Permission model fails to validate operations against file descriptors
6. File ownership and permissions are modified despite --allow-fs-write restrictions

## Root cause
Node.js permission model operates on file paths rather than file descriptors. The fchown() and fchmod() functions accept file descriptors but do not perform permission checks against the descriptor's access level, allowing operations that should be restricted.

## Attacker mindset
An insider or compromised process with read-only file access seeks to escalate privileges by modifying file ownership or permissions to gain write access or execute privileged operations.

## Defensive takeaways
- Implement file descriptor-level permission validation in filesystem operations
- Validate that fchown/fchmod operations are consistent with the original file descriptor's access mode
- Add permission checks that track the 'how' (path vs descriptor) alongside the 'what' (file path)
- Thoroughly test permission model against all filesystem operations, not just path-based ones
- Consider blocking sensitive operations (chown, chmod) on file descriptors in sandboxed contexts

## Variant hunting
Search for other descriptor-based filesystem operations that bypass permission checks: fs.ftruncate(), fs.futimes(), fs.fdatasync(). Test permission models in other Node.js APIs that accept file descriptors. Check if similar issues exist in other permission-restricted contexts.

## MITRE ATT&CK
- T1548.001
- T1190
- T1552

## Notes
Vulnerability affects Node.js 20 and 21 with experimental permission model enabled. CVE-2024-36137 assigned. Reporter proposed 25% penalty reduction for experimental status and 50% reduction for proposed fix, resulting in 50% bounty modifier. This demonstrates the importance of validating security-sensitive operations across all code paths, not just the primary/documented ones.

## Full report
<details><summary>Expand</summary>

Hello IBB team, i would like to submit a report about Node.js vulnerability that i have reported to the Node.js team, which was assigned to CVE-2024-36137  and disclosed today. Please check #2472071.

Modifier: I have proposed a fix(-25% shouldn't be apllied) and the feature is experimental (-50%), so I believe the final ratio is 50%.

## Details:
A vulnerability has been identified in Node.js, affecting users of the experimental permission model when the --allow-fs-write flag is used.

Node.js Permission Model do not operate on file descriptors, however, operations such as `fs.fchown` or `fs.fchmod` can use a "read-only" file descriptor to change the owner and permissions of a file.

This vulnerability affects all users using the experimental permission model in Node.js 20 and Node.js 21.

Please note that at the time this CVE was issued, the permission model is an experimental feature of Node.js.

## Impact

Node.js Permission Model do not operate on file descriptors, however, operations such as `fs.fchown` or `fs.fchmod` can use a "read-only" file descriptor to change the owner and permissions of a file.

</details>

---
*Analysed by Claude on 2026-05-24*
