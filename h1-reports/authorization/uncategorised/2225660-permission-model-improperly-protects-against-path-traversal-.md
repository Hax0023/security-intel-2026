# Permission Model Path Traversal via Dynamic Property Lookup in Node.js 20

## Metadata
- **Source:** HackerOne
- **Report:** 2225660 | https://hackerone.com/reports/2225660
- **Submitted:** 2023-10-25
- **Reporter:** tniessen
- **Program:** Node.js
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Path Traversal, Insufficient Input Validation, Improper Access Control, Dynamic Function Resolution Vulnerability
- **CVEs:** CVE-2023-39331
- **Category:** uncategorised

## Summary
A path traversal vulnerability exists in Node.js 20's permission model implementation due to dynamic property lookup of `pathModule.resolve()`. An attacker can override the built-in `path.resolve` function with a malicious implementation that bypasses path normalization, allowing unauthorized file system access despite permission restrictions.

## Attack scenario
1. Attacker identifies that the application uses Node.js 20 with the experimental permission model enabled (--experimental-permission flag)
2. Application is started with restricted fs-read permissions (e.g., --allow-fs-read=/tmp/)
3. Attacker injects code that overwrites the global `path.resolve` function with an identity function: `path.resolve = (s) => s`
4. Attacker calls `fs.readFileSync('/tmp/../etc/passwd')` to access files outside the allowed directory
5. The permission model's `possiblyTransformPath()` function dynamically retrieves the overridden `path.resolve` and fails to normalize the path
6. The traversal succeeds, exposing sensitive files like /etc/passwd to unauthorized access

## Root cause
The `possiblyTransformPath()` function in `lib/internal/fs/utils.js` dynamically retrieves `pathModule.resolve` via property lookup rather than maintaining a local reference to the original built-in function. This allows application code to replace the function with a malicious implementation that bypasses path normalization logic required by the permission model.

## Attacker mindset
An attacker seeks to bypass the experimental permission model in Node.js to access sensitive files outside the granted directory scope. By understanding that the permission model relies on dynamic property resolution, the attacker exploits this design flaw by injecting code that hijacks the path resolution mechanism, converting a restriction mechanism into a useless check.

## Defensive takeaways
- Capture references to critical built-in functions at module load time rather than performing dynamic property lookups at runtime
- In security-critical code paths, avoid relying on properties that can be modified by user code
- Implement immutable references to core functionality used in permission/security enforcement mechanisms
- Consider using Object.freeze() or other defensive techniques to prevent modification of security-critical built-ins
- Conduct thorough security review of refactored security patches, especially when addressing previously disclosed vulnerabilities
- Use static analysis to identify all dynamic function calls in security-critical code paths

## Variant hunting
Search for other dynamic property lookups of built-in functions (Math.*, Array.prototype.*, Object.*, etc.) in permission-model related code
Audit all uses of `pathModule` properties across the fs permission implementation for similar dynamic resolution patterns
Test whether other core modules used in permission checks (crypto, buffer, etc.) are similarly vulnerable to property injection
Check if the permission model validates paths using other methods (e.g., string manipulation) that could be similarly bypassed
Investigate whether URL parsing or encoding functions used in path validation are similarly vulnerable
Test permission model with other path traversal techniques (symlinks, URL encoding, Unicode normalization) combined with function hijacking

## MITRE ATT&CK
- T1190
- T1548
- T1556
- T1036

## Notes
This is a regression of CVE-2023-30584, indicating insufficient patch verification. The vulnerability demonstrates a common security anti-pattern: relying on dynamic property access for security-critical operations. The fix is minimal but effective: capturing a reference to the original `pathModule.resolve` at module initialization time (before user code can modify it). This case highlights the importance of threat modeling property injection attacks in security-sensitive contexts and the need for post-patch security testing that includes adversarial property manipulation scenarios.

## Full report
<details><summary>Expand</summary>

**Summary:** A previously disclosed vulnerability (CVE-2023-30584) was patched insufficiently in commit [205f1e6](https://github.com/nodejs/node/commit/205f1e643e25648173239b2de885fec430268492). The new path traversal vulnerability arises because the implementation does not protect itself against the application overwriting built-in utility functions with user-defined implementations.

**Description:** The function `possiblyTransformPath` calls `pathModule.resolve(path)`, where `pathModule` is the result of `require('path')`. Application code may replace the value of the `require('path').resolve`property with a user-defined function that does not resolve `/../` within any given path. Because `possiblyTransformPath` retrieves the value of the `pathModule.resolve` property dynamically, it will use the user-defined function instead of the built-in function and will thus fail to fully resolve the path given by the application. The vulnerability can be prevented by maintaining a reference to the original value of `pathModule.resolve` for use in `possiblyTransformPath`, assuming that the original implementation of the `resolve()` function is not subject to any such vulnerabilities itself.

## Steps To Reproduce:

Temporarily assigning `path.resolve = (s) => s` disables the resolution of `/../` within the permission model implementation.

```console
$ node --experimental-permission --allow-fs-read=/tmp/ -p "path.resolve = (s) => s; fs.readFileSync('/tmp/../etc/passwd')"
<Buffer 72 6f 6f 74 3a 78 3a 30 3a 30 3a 72 6f 6f 74 3a 2f 72 6f 6f 74 3a 2f 62 69 6e 2f 62 61 73 68 0a 64 61 65 6d 6f 6e 3a 78 3a 31 3a 31 3a 64 61 65 6d 6f ... 3174 more bytes>
```

## Supporting Material/References:

* [Original HackerOne report 2092852 of this vulnerability](https://hackerone.com/reports/2092852)
* [HackerOne report 1952978](https://hackerone.com/reports/1952978) for the previous path traversal vulnerability (CVE-2023-30584)
* [Vulnerable implementation of `possiblyTransformPath`](https://github.com/nodejs/node/blob/af4cdcde154be58fc47b389670efbe10da489923/lib/internal/fs/utils.js#L711-L718)

## Suggested patch

```patch
diff --git a/lib/internal/fs/utils.js b/lib/internal/fs/utils.js
index b7354e30e9..4971656d0a 100644
--- a/lib/internal/fs/utils.js
+++ b/lib/internal/fs/utils.js
@@ -710,2 +710,3 @@ const validatePath = hideStackFrames((path, propName = 'path') => {
 // The permission model needs the absolute path for the fs_permission
+const resolvePath = pathModule.resolve;
 function possiblyTransformPath(path) {
@@ -713,3 +714,3 @@ function possiblyTransformPath(path) {
     if (typeof path === 'string') {
-      return pathModule.resolve(path);
+      return resolvePath(path);
     }
```

This patch assumes that `pathModule.resolve()` itself is not susceptible to having its behavior altered in a security-critical way through user-defined properties.

This patch was merged into the main branch of Node.js as [commit 32bcf4ca](https://github.com/nodejs/node/commit/32bcf4ca27bba9d4e48418f12dc6d7c2252e71ec) and into the Node.js 20 release line as [commit cd352751](https://github.com/nodejs/node/commit/cd352751118eccab625573092bf47d9b0d84b792).

## Impact

The impact is almost identical with that of CVE-2023-30584. Applications may use this vulnerability to read and write files and directories that the user has not granted access to.

</details>

---
*Analysed by Claude on 2026-05-24*
