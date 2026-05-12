# Path Traversal and Remote Code Execution in Apache HTTP Server 2.4.49 and 2.4.50 (CVE-2021-42013)

## Metadata
- **Source:** HackerOne
- **Report:** 1400238 | https://hackerone.com/reports/1400238
- **Submitted:** 2021-11-14
- **Reporter:** fms
- **Program:** Apache HTTP Server
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Path Traversal, Directory Traversal, Remote Code Execution, Incomplete Security Patch
- **CVEs:** CVE-2021-41773, CVE-2021-42013
- **Category:** memory-binary

## Summary
Apache HTTP Server 2.4.50's patch for CVE-2021-41773 was incomplete, allowing attackers to bypass path traversal protections through specially crafted URLs. By combining directory traversal with CGI script execution, an unauthenticated attacker could achieve remote code execution on affected servers.

## Attack scenario
1. Attacker identifies Apache 2.4.49 or 2.4.50 server with Alias-like directives configured
2. Attacker crafts malicious URL using path traversal sequences (e.g., encoded traversal patterns) to bypass the incomplete CVE-2021-41773 fix
3. URL is mapped to files outside the intended aliased directories, bypassing 'require all denied' restrictions
4. Attacker locates CGI scripts enabled on the aliased paths that are now accessible
5. Attacker executes arbitrary commands through the accessible CGI scripts
6. Remote code execution achieved with web server privileges

## Root cause
The initial patch for CVE-2021-41773 did not comprehensively address all path traversal bypass techniques. The validation logic could still be circumvented using alternative encoding or traversal patterns, particularly when Alias directives were configured and CGI execution was enabled.

## Attacker mindset
Exploit incomplete security patches that prioritize speed over thorough validation. Target common server configurations (Alias directives + CGI) to achieve maximum impact. Focus on bypass techniques that evade simplistic path checks without addressing the root validation flaw.

## Defensive takeaways
- Ensure comprehensive testing of security patches before release, including edge cases and alternative bypass techniques
- Implement defense-in-depth with multiple validation layers rather than relying on single filter mechanisms
- Apply strict whitelist-based path validation instead of blacklist approaches to directory traversal
- Disable CGI script execution in aliased directories unless absolutely necessary
- Use security headers and restrict file access permissions at OS level to limit impact of path traversal vulnerabilities
- Prioritize updating to patched versions (2.4.51+) immediately when critical patches are released
- Monitor and test for regression of previously patched vulnerabilities

## Variant hunting
Search for similar incomplete patches in Apache HTTPd history and other web servers. Look for path traversal issues in Alias/AliasMatch directive handling, particularly with URL encoding/decoding edge cases. Test if other directive types (ScriptAlias, ProxyPass) have similar bypass potential. Examine how other web servers implement path normalization.

## MITRE ATT&CK
- T1190
- T1083
- T1021

## Notes
This vulnerability demonstrates the danger of incomplete patches for security issues. Reported responsibly to Apache HTTPd team by Fernando Munoz and Juan Escobar, who collaborated on testing before official release. The fact that only 2.4.49 and 2.4.50 were affected (not earlier versions) indicates the initial patch introduction created the vulnerability window.

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
*Analysed by Claude on 2026-05-12*
