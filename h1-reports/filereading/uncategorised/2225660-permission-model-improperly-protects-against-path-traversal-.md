# Permission Model Path Traversal via Built-in Function Override in Node.js 20

## Metadata
- **Source:** HackerOne
- **Report:** 2225660 | https://hackerone.com/reports/2225660
- **Submitted:** 2023-10-25
- **Reporter:** tniessen
- **Program:** Node.js
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Path Traversal, Permission Bypass, Insufficient Input Validation
- **CVEs:** CVE-2023-39331
- **Category:** uncategorised

## Summary
Node.js 20's experimental permission model fails to protect against path traversal when application code overrides the built-in `path.resolve()` function. An attacker can bypass filesystem permission restrictions by replacing `path.resolve` with a function that does not normalize paths containing `/../` sequences, allowing unauthorized file access.

## Attack scenario
1. Attacker identifies application running Node.js with `--experimental-permission --allow-fs-read=/tmp/` flag
2. Attacker injects or crafts code that overwrites the global `path.resolve` property with a no-op function: `path.resolve = (s) => s`
3. When permission model calls `possiblyTransformPath()`, it dynamically retrieves `pathModule.resolve` which now points to the attacker's function
4. Attacker constructs a path like `/tmp/../etc/passwd` which the compromised resolve function returns unchanged
5. Permission model validates the unresolved path against ACL `/tmp/` rule, which matches the prefix
6. Attacker successfully reads `/etc/passwd` despite only having `/tmp/` permission

## Root cause
The `possiblyTransformPath()` function in `lib/internal/fs/utils.js` dynamically accesses `pathModule.resolve()` at runtime rather than capturing a reference to the original built-in function at module load time. This allows user code to intercept and replace the function with a malicious implementation that bypasses path normalization, defeating the permission model's path validation logic.

## Attacker mindset
An attacker recognizes that security boundaries depending on dynamic property lookups can be circumvented by overwriting those properties. By replacing the path resolution function with an identity function, the attacker causes the permission validation to operate on non-canonical paths, allowing traversal attacks despite restrictive permission ACLs. This demonstrates understanding of prototype pollution and dynamic dispatch vulnerabilities.

## Defensive takeaways
- Capture references to critical built-in functions at module initialization rather than performing dynamic lookups at runtime
- When implementing security-sensitive code paths, use static references to known-good implementations to prevent runtime interception
- Avoid relying on properties of required modules that can be modified by user code; cache immutable references early
- Apply defense-in-depth: validate paths both before and after normalization, and use multiple independent checks
- Recognize that CVE patches must close all attack vectors, including indirect ones through function overriding
- For permission models, consider using Object.freeze() or Object.seal() on critical utility objects to prevent modification

## Variant hunting
Check for other dynamic function calls in security-critical paths that could be overridden (e.g., `Buffer.isBuffer()`, `Array.isArray()`)
Search for other instances where `pathModule.resolve`, `pathModule.join`, or path normalization functions are called dynamically
Audit all permission-gating code for similar patterns where built-in functions are retrieved via property access rather than captured references
Test whether overriding other path functions like `path.join()`, `path.normalize()`, or `path.relative()` can bypass permissions
Examine whether similar vulnerabilities exist in other Node.js security features (e.g., VM module, worker threads isolation)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1059 - Command and Scripting Interpreter
- T1083 - File and Directory Discovery
- T1005 - Data from Local System

## Notes
This is a regression/insufficient patch of CVE-2023-30584. The fix captures `pathModule.resolve` as a constant `resolvePath` at module load time, preventing runtime interception. The vulnerability demonstrates that security-critical code must be defensive against both direct attacks and indirect attacks through function/property manipulation. The patch assumes `pathModule.resolve()` itself cannot be vulnerable to similar tampering, which requires analyzing its implementation.

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
