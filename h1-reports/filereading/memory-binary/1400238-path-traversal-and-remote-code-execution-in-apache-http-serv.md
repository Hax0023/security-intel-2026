# Path Traversal and Remote Code Execution in Apache HTTP Server 2.4.49/2.4.50 (CVE-2021-42013)

## Metadata
- **Source:** HackerOne
- **Report:** 1400238 | https://hackerone.com/reports/1400238
- **Submitted:** 2021-11-14
- **Reporter:** fms
- **Program:** Apache HTTP Server
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Path Traversal, Directory Traversal, Incomplete Patch, Remote Code Execution
- **CVEs:** CVE-2021-41773, CVE-2021-42013
- **Category:** memory-binary

## Summary
The fix for CVE-2021-41773 in Apache HTTP Server 2.4.50 was incomplete, allowing attackers to bypass path traversal protections using encoded path manipulation. An attacker could map URLs to files outside configured Alias directories and execute arbitrary code if CGI scripts are enabled on aliased paths.

## Attack scenario
1. Attacker identifies Apache HTTP Server 2.4.49 or 2.4.50 installation with Alias-like directives configured
2. Attacker crafts malicious URL with path traversal sequences (likely using encoding bypasses like double encoding or alternative encoding schemes)
3. Attacker sends crafted request to bypass the incomplete CVE-2021-41773 patch validation
4. Server maps the traversal request to files outside the intended Alias directories
5. If CGI is enabled on the aliased path, attacker gains ability to execute arbitrary scripts
6. Attacker achieves remote code execution with web server privileges

## Root cause
The patch for CVE-2021-41773 failed to comprehensively address all path normalization edge cases. Likely causes include: incomplete validation of path traversal sequences, insufficient handling of encoded traversal patterns, or flawed regex/string matching logic that allows bypass through encoding variations or alternative representations.

## Attacker mindset
Attackers analyze incomplete security patches by testing variations of the original vulnerability technique. They recognize that first-pass fixes often miss edge cases and attempt alternative encoding/representation methods. The combination with CGI execution capabilities escalates from information disclosure to critical RCE.

## Defensive takeaways
- Implement comprehensive path canonicalization before any access control checks, resolving all encodings and symbolic representations
- Use allowlist-based validation rather than blacklist/blocklist approaches for path traversal protection
- Test security patches thoroughly against variant attack vectors, not just the original PoC
- Apply defense-in-depth: combine multiple validation layers and ensure default-deny configurations on sensitive paths
- Disable unnecessary features like CGI execution on user-accessible directories
- Implement strict input validation that handles multiple encoding layers (double encoding, unicode normalization, etc.)
- Prioritize path traversal fixes at the lowest layers before business logic processing

## Variant hunting
Test for similar incomplete fixes in: URL normalization routines, symlink resolution logic, case-sensitivity handling on case-insensitive filesystems, Unicode/UTF-8 normalization bypasses, alternate path separators on different OS, null byte injection, and mixed encoding schemes across path components.

## MITRE ATT&CK
- T1190
- T1083
- T1047
- T1059

## Notes
This is a critical example of incomplete patch development. The original CVE-2021-41773 affected versions 2.4.49 and 2.4.50, and this variant (CVE-2021-42013) demonstrated the patch was insufficient. Researchers coordinated disclosure with Apache HTTPd project before public release. The vulnerability demonstrates why security patches require comprehensive threat modeling and edge case analysis rather than simple targeted fixes.

## Full report
<details><summary>Expand</summary>

It was found that the fix for CVE-2021-41773 in Apache HTTP Server 2.4.50 was insufficient. An attacker could use a path traversal attack to map URLs to files outside the directories configured by Alias-like directives.

This issue only affects Apache 2.4.49 and Apache 2.4.50 and not earlier versions.

-
My friend Juan Escobar @itsecurityco and me (Fernando Munoz) reported this internally to Apache HTTPd project and worked with them to test the new patch before the new version was released.

## Impact

If files outside of these directories are not protected by the usual default configuration "require all denied", these requests can succeed. If CGI scripts are also enabled for these aliased pathes, this could allow for remote code execution.

</details>

---
*Analysed by Claude on 2026-05-24*
