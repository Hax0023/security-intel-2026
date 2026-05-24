# Filesystem Experimental Permissions Policy Path Traversal Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1952978 | https://hackerone.com/reports/1952978
- **Submitted:** 2023-04-18
- **Reporter:** haxatron1
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Authorization Bypass, Insufficient Input Validation
- **CVEs:** CVE-2023-30584
- **Category:** uncategorised

## Summary
Node.js experimental permission policy fails to normalize filesystem paths before validation, allowing attackers to bypass write restrictions using relative path traversal sequences (../) to escape allowlisted directories. An attacker can write to arbitrary locations outside the permitted directory by including path traversal components in the file path.

## Attack scenario
1. Attacker discovers Node.js application running with --experimental-permission flag and restricted write permissions (e.g., --allow-fs-write=/home/kali/restricted/)
2. Attacker crafts a file path containing traversal sequences: /home/kali/restricted/../secret.txt
3. Application passes this path to fs.writeFileSync() or similar write operation
4. Permission policy checks if path starts with /home/kali/restricted/ (basic string prefix matching)
5. Check passes because literal string contains the allowlisted directory prefix
6. Operating system resolves the actual target path to /home/kali/secret.txt and writes file
7. Attacker achieves unauthorized write access outside the intended restricted directory

## Root cause
The permission policy implementation performs string-based prefix matching on file paths without normalizing or canonicalizing paths first. It fails to resolve relative path components (../, ., symlinks) before conducting the authorization check, allowing crafted paths to pass validation while actually targeting different locations.

## Attacker mindset
An attacker operating under experimental permission restrictions would recognize that path normalization failures are common in security controls. By injecting directory traversal sequences, they exploit the gap between the policy check (string matching) and the actual filesystem operation (path resolution), achieving privilege escalation from restricted to unrestricted access.

## Defensive takeaways
- Always normalize and canonicalize filesystem paths before authorization checks (realpath, Path.resolve)
- Implement whitelist checks against the normalized/canonical form, not raw user-supplied paths
- Validate that the resolved path stays within intended boundaries after normalization
- Use absolute paths internally and reject relative path components in permission policies
- Resolve symlinks when applicable to prevent symlink-based bypasses
- Implement comprehensive unit tests covering path traversal patterns (../, ./, symlinks)
- Consider allowlisting as prefix matching only for directories with trailing slashes

## Variant hunting
Search for similar path handling issues in other Node.js permission checks (--allow-child-process-management, --allow-worker-threads-management, etc). Review any custom file access controls in npm packages. Test symbolic link handling in permission policies. Examine network path handling in similar permission systems.

## MITRE ATT&CK
- T1548.004 - Abuse Elevation Control Mechanism: Elevated Execution with Prompt
- T1083 - File and Directory Discovery
- T1006 - Direct Volume Access

## Notes
This affects Node.js v20.0.0+ with experimental permission policies. The vulnerability is in the core permission validation logic rather than user application code. Demonstrates the importance of path canonicalization in security-critical code paths. Similar issues may exist in other permission enforcement mechanisms within Node.js.

## Full report
<details><summary>Expand</summary>

Consider the following command on Node v20.0.0:
```
node --experimental-permission --allow-fs-read=* --allow-fs-write=/home/kali/restricted/ poc.js
```
This command is intended to restrict write access to only files present in the directory /home/kali/restricted

However if we have the following poc.js:
```
const fs = module.require('fs')
fs.writeFileSync("/home/kali/restricted/../secret.txt", "Target Overwritten!")
```
This apparently matches the directory /home/kali/restricted/ directory check and then writes to /home/kali/secret.txt (by using ../), which is not intended, bypassing the experimental permission policy for files.

## Impact

Path traversal when checking experimental file permission policy

</details>

---
*Analysed by Claude on 2026-05-24*
