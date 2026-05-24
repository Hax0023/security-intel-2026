# Path Traversal via Buffer.prototype.utf8Write Monkey-Patching in Node.js Permission Model

## Metadata
- **Source:** HackerOne
- **Report:** 2434811 | https://hackerone.com/reports/2434811
- **Submitted:** 2024-03-26
- **Reporter:** tniessen
- **Program:** Node.js
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Path Traversal, Privilege Escalation, Permission Model Bypass, Prototype Pollution
- **CVEs:** CVE-2024-21896
- **Category:** uncategorised

## Summary
Node.js 20 and 21 permission model vulnerability allowing attackers to bypass path traversal protections by monkey-patching Buffer.prototype.utf8Write. The vulnerability enables reading/writing files outside the process's allowed filesystem paths by intercepting Buffer encoding during internal path resolution.

## Attack scenario
1. Attacker identifies application running with Node.js experimental permission model with restricted filesystem access (e.g., --allow-fs-read=/tmp)
2. Attacker executes arbitrary JavaScript code within the process (or injects code through vulnerable dependencies)
3. Attacker monkey-patches Buffer.prototype.utf8Write with custom function that modifies path strings during encoding
4. Application calls fs.readFileSync() with attacker-controlled buffer path parameter
5. Internal possiblyTransformPath() calls path.resolve() which sanitizes to /tmp/etc/passwd
6. Buffer.from() internally calls utf8Write, which intercepts and replaces sanitized path with /tmp/../etc/passwd, bypassing permission checks

## Root cause
The permission model's possiblyTransformPath() function relies on path.resolve() for sanitization, then converts result to Buffer using Buffer.from(). An attacker can intercept the utf8Write() method called during Buffer creation to modify the resolved path string before it's encoded, bypassing the sanitization that occurred in path.resolve(). The implementation assumes the path cannot be modified after resolution, but fails to account for mutable Buffer encoding internals.

## Attacker mindset
Understanding that security controls are only effective when applied at the right layer; recognizing that path.resolve() output must be protected from modification during any subsequent processing; identifying that internal Buffer operations are part of the trusted code path and therefore not properly defended against prototype pollution attacks.

## Defensive takeaways
- Never rely on object method integrity for security-critical operations; use C++ bindings or frozen prototypes for sensitive code paths
- Apply security transformations at the lowest possible layer (e.g., C++ bindings) rather than JavaScript, which can be monkey-patched
- Freeze critical built-in prototypes or use Object.create(null) to prevent prototype pollution in sensitive contexts
- Validate and enforce security properties on both function inputs and outputs, not assuming intermediate steps cannot be bypassed
- Implement defense-in-depth: even if path.resolve() is called, additional integrity checks on the result should occur before use
- Review all prototype methods called during security-critical operations for monkey-patch vectors
- Consider using native bindings (encodeUtf8String) instead of JavaScript Buffer methods for security-sensitive encoding operations

## Variant hunting
Other Buffer methods used in security contexts (utf16leWrite, utf16beWrite, asciiWrite, latin1Write, hexWrite, ucs2Write)
Similar permission bypass vulnerabilities in other runtime permission models that use intermediate object methods
Monkey-patching of String.prototype methods if path is converted to string during security checks
Prototype pollution of path module internals or Object.prototype affecting path resolution
Buffer.allocUnsafe() or Buffer.alloc() calls in security-critical code paths
Check if similar patterns exist in other Node.js built-in modules that use Buffer for security-critical data
Explore if array/typed array prototype methods are called during filesystem permission checks

## MITRE ATT&CK
- T1036.004
- T1548.004
- T1548
- T1190
- T1027.010

## Notes
This is the fourth iteration of path traversal vulnerabilities in Node.js permission model (following CVE-2023-30584, CVE-2023-32004, CVE-2023-39331, CVE-2023-39332). The vulnerability exists despite previous patching attempts that hardened path.resolve() and Buffer.from() replacement. The core issue is incomplete hardening - while preventing direct replacement of critical functions, the implementation overlooked monkey-patching of methods called during internal execution. The proposed fix uses C++ binding encodeUtf8String() instead of JavaScript Buffer.from(), which cannot be monkey-patched from user code.

## Full report
<details><summary>Expand</summary>

**Summary:** In Node.js 20 and Node.js 21, the permission model protects itself against path traversal attacks by calling `path.resolve()` on any paths given by the user. If the path is to be treated as a `Buffer`, the implementation uses `Buffer.from()` to obtain a `Buffer` from the result of `path.resolve()`. By monkey-patching `Buffer` internals, namely, `Buffer.prototype.utf8Write`, the application can modify the result of `path.resolve()`, which leads to a path traversal vulnerability.

**Description:** This vulnerability was introduced in [commit 1f64147e](https://github.com/nodejs/node/commit/1f64147eb607f82060e08884f993597774c69280), which itself was a patch of a path traversal vulnerability (see CVE-2023-32004, [report 2038134](https://hackerone.com/reports/2038134)). Subsequent commits made the implementation more resilient against monkey-patching, for example, by not allowing users to replace `path.resolve()` ([commit 32bcf4ca](https://github.com/nodejs/node/commit/32bcf4ca27bba9d4e48418f12dc6d7c2252e71ec)) or `Buffer.from()` ([commit f447a461](https://github.com/nodejs/node/commit/f447a4611a49d1843c17bf9ffbc86a835f1f1b9c)) with user-defined functions. Nevertheless, the internals of `Buffer.from` can be monkey-patched in multiple ways. Most importantly, overwriting `Buffer.prototype.utf8Write` with a user-defined function enables a straightforward path traversal vulnerability because virtually any sanitization performed by `path.resolve()` can be overridden by the user.

## Steps to reproduce:

This can be exploited simply by overwriting `Buffer.prototype.utf8Write` with a user-defined function. The code is supposed to only have access to `/tmp`, yet it successfully reads `/etc/passwd`.

```
$ node --experimental-permission --allow-fs-read=/tmp 
Welcome to Node.js v20.8.1.
Type ".help" for more information.
> Buffer.prototype.utf8Write = ((w) => function (str, ...args) {
...   return w.apply(this, [str.replace(/^\/exploit/, '/tmp/..'), ...args]);
... })(Buffer.prototype.utf8Write);
[Function (anonymous)]
> fs.readFileSync(new TextEncoder().encode('/exploit/etc/passwd'))
<Buffer 72 6f 6f 74 3a 78 3a 30 3a 30 3a 72 6f 6f 74 3a 2f 72 6f 6f 74 3a 2f 62 69 6e 2f 62 61 73 68 0a 64 61 65 6d 6f 6e 3a 78 3a 31 3a 31 3a 64 61 65 6d 6f ... 3174 more bytes>
```

This example pretends to attempt to read `/exploit/etc/passwd`, which would ultimately be denied. However, after the permission model implementation has called `path.resolve()`, the exploit intercepts the internal call to `utf8Write()` within `Buffer.from()` and replaces the sanitized path with `/tmp/../etc/passwd`, thus bypassing the path traversal protection logic. Because Node.js assumes that the path has been resolved at this point, it allows access because the path begins with `/tmp/`.

## Suggested minimal patch:

```patch
diff --git a/lib/internal/fs/utils.js b/lib/internal/fs/utils.js
index 611b6c2420..d7e6ec3aa2 100644
--- a/lib/internal/fs/utils.js
+++ b/lib/internal/fs/utils.js
@@ -66,4 +66,6 @@ const kStats = Symbol('stats');
 const assert = require('internal/assert');
 
+const { encodeUtf8String } = internalBinding('encoding_binding');
+
 const {
   fs: {
@@ -720,5 +722,8 @@ function possiblyTransformPath(path) {
     assert(isUint8Array(path));
     if (!BufferIsBuffer(path)) path = BufferFrom(path);
-    return BufferFrom(resolvePath(BufferToString(path)));
+    // Avoid Buffer.from() and use a C++ binding instead to encode the result
+    // of path.resolve() in order to prevent path traversal attacks that
+    // monkey-patch Buffer internals.
+    return encodeUtf8String(resolvePath(BufferToString(path)));
   }
   return path;
```

## Supporting Material/References:

* The [vulnerable implementation of `possiblyTransformPath()`](https://github.com/nodejs/node/blob/9f46adf5bc14a7af8ec55be1d02fa46ed80720f2/lib/internal/fs/utils.js#L712-L725).
* [Commit 1f64147e](https://github.com/nodejs/node/commit/1f64147eb607f82060e08884f993597774c69280), which introduced the vulnerability.
* Previous path traversal vulnerabilities: CVE-2023-30584, CVE-2023-32004, CVE-2023-39331, and CVE-2023-39332.

## Impact

The impact is virtually the same as that of previous path traversal vulnerabilities: CVE-2023-30584, CVE-2023-32004, CVE-2023-39331, and CVE-2023-39332. Applications can access file system paths that access should be denied to based on the configured process permissions, and may be able to perform write operations on read-only resources.

This affects the most recent versions of Node.js on both the Node.js 20 and Node.js 21 release lines.

</details>

---
*Analysed by Claude on 2026-05-24*
