# Permission model improperly processes UNC paths in Node.js

## Metadata
- **Source:** HackerOne
- **Report:** 2079103 | https://hackerone.com/reports/2079103
- **Submitted:** 2023-07-21
- **Reporter:** tniessen
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** Low
- **Vuln:** Improper Input Validation, Path Traversal, Authorization Bypass
- **CVEs:** CVE-2024-37372
- **Category:** auth-crypto

## Summary
The `is_tree_granted` function in Node.js's fs_permission.cc incorrectly assumes UNC paths always have a four-character prefix that can be safely ignored, failing to properly validate paths starting with `\\`. This allows attackers to bypass file system permission restrictions and access unintended UNC resources on Windows systems.

## Attack scenario
1. Attacker configures Node.js with experimental permissions using `--allow-fs-read=C:\*` to restrict access to local C: drive only
2. Attacker constructs a specially-crafted UNC path like `\\A\C:\Users` that exploits the prefix stripping logic
3. The `is_tree_granted` function incorrectly strips the first four characters (`\\A\`), leaving `C:\Users`
4. The permission check incorrectly matches this against the allowed `C:\*` pattern
5. The function returns true, granting access when it should deny
6. Attacker successfully reads files from the UNC path `\\A\C:\Users` despite only local C: drive access being intended

## Root cause
The `is_tree_granted` function contains a hardcoded assumption that paths beginning with `\\` always have a four-character prefix that represents UNC path overhead. This assumption fails for certain UNC path formats where the server/share component differs in length. The function does not properly validate or parse the actual structure of UNC paths before stripping characters.

## Attacker mindset
An attacker would recognize that Windows file path handling is complex and that permission validation logic may make simplifying assumptions. By studying the source code of the permission module, they identify the naive prefix-stripping logic and craft edge-case paths that exploit this assumption to bypass intended access controls.

## Defensive takeaways
- Never make assumptions about fixed-length prefixes in path parsing; use proper path parsing libraries designed for the target OS
- Implement comprehensive unit tests covering edge cases for Windows UNC path formats (various server/share name lengths)
- Use platform-specific path normalization and validation functions before permission checks
- For security-critical path validation, consult official documentation on file path formats and consider using OS-level path APIs
- Validate that the entire path structure is correctly understood before applying any transformations or prefix stripping
- Consider security implications of experimental features and ensure permission models are thoroughly tested before release

## Variant hunting
Search for other path parsing logic in permission modules that make assumptions about path structure. Investigate whether similar issues exist in: (1) relative path handling, (2) symlink resolution, (3) case sensitivity handling on different platforms, (4) other path prefixes like `\?\` for long paths on Windows, (5) drive letter vs. UNC path distinction logic.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1087 - Account Discovery

## Notes
The reporter appropriately notes the subtlety and complexity of Windows file path formats, which likely contributed to this bug going undetected. The use of Buffer.from() to pass the path is noteworthy as it may bypass certain string-based validation. This vulnerability demonstrates why security-critical path handling should use well-tested, battle-hardened libraries rather than custom implementations.

## Full report
<details><summary>Expand</summary>

The `is_tree_granted` function in `fs_permission.cc` assumes that any path starting with two backslashes `\\` has a four-character prefix that can be ignored, which is not always true. This subtle bug leads to vulnerable edge cases.

## Steps To Reproduce:

With a recent version of Node.js 20, run a command such as:

```
node --experimental-permission --allow-fs-read=C:\* -p "fs.readdirSync(Buffer.from('\\\\A\\C:\\Users'))"
```

The expected behavior is an `ERR_ACCESS_DENIED` error, but it does not occur. Instead, Node.js calls `scandir` on `\\A\C:\Users`.

## Supporting Material/References:

* [Implementation of `is_tree_granted`](https://github.com/nodejs/node/blob/b68fa599607f69f2ce3b1a3104e0d5984f6bc0d8/src/permission/fs_permission.cc#L53-L68)
* [File path formats on Windows systems: UNC paths](https://learn.microsoft.com/en-us/dotnet/standard/io/file-path-formats#unc-paths)

## Impact

An attacker can potentially gain unintended access to UNC resources. In the above example, an attacker gains file system access to the UNC path `\\A\C:\`, even though no access beyond the local `C:\` drive has been granted.

It is difficult to fully and accurately comprehend the impact. The bug is subtle, and Windows uses notoriously complex file path formats. Overall, I consider the severity of the issue to be low.

</details>

---
*Analysed by Claude on 2026-05-24*
