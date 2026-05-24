# Path traversal through Uint8Array in Node.js permission model

## Metadata
- **Source:** HackerOne
- **Report:** 2256167 | https://hackerone.com/reports/2256167
- **Submitted:** 2023-11-17
- **Reporter:** tniessen
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Path Traversal, Permission Bypass, Access Control Bypass
- **CVEs:** CVE-2023-39332
- **Category:** uncategorised

## Summary
Node.js filesystem functions accept paths as Uint8Array objects but fail to properly validate path traversal sequences in non-Buffer Uint8Array instances. An attacker can bypass the experimental permission model by encoding path traversal payloads (e.g., '/tmp/../etc/passwd') using TextEncoder to create Uint8Array objects, allowing unauthorized file access despite restrictive fs-read permissions.

## Attack scenario
1. Attacker identifies that Node.js with --experimental-permission flag restricts file access to specific directories (e.g., /tmp)
2. Attacker discovers that fs.readFileSync() accepts both string and Uint8Array path arguments
3. Attacker learns that path validation only checks string and Buffer types, missing plain Uint8Array instances
4. Attacker uses TextEncoder to convert malicious path '/tmp/../etc/passwd' into Uint8Array
5. Attacker calls fs.readFileSync() with the Uint8Array, bypassing permission checks
6. Attacker successfully reads /etc/passwd despite permission restriction, escalating to unauthorized file disclosure

## Root cause
Path traversal validation in Node.js fs module (commit 205f1e6 and 1f64147) only sanitizes string and Buffer object types. The code fails to recognize and validate Uint8Array instances that are not Buffer subclasses, allowing the '..' sequences to reach the underlying filesystem operations unsanitized.

## Attacker mindset
An attacker would recognize type-based security checks as incomplete and systematically test alternative input types (Uint8Array vs Buffer vs string) to find gaps in validation logic. The use of TextEncoder as a vector suggests probing for implicit type conversions or alternative APIs that produce similar but unchecked types.

## Defensive takeaways
- Validate all path inputs regardless of type; treat Uint8Array, Buffer, and string uniformly in security checks
- Use allowlists for path traversal validation rather than relying on type-specific handling
- Normalize paths before permission validation to resolve '..' and '.' sequences consistently
- Implement comprehensive type coverage in security-critical code paths, not just primary input types
- Apply path validation at the lowest common denominator (binary level) before filesystem operations
- Test permission models with all accepted input types during security review

## Variant hunting
Check if other Node.js APIs accepting path parameters have similar gaps (e.g., fs.stat, fs.open, fs.exists)
Test if other TypedArray subclasses (Int8Array, Uint16Array) bypass validation
Verify if permission validation gaps exist in other Node.js core modules using path parameters
Examine if child process spawning bypasses restrictions through similar Uint8Array usage
Test if custom Uint8Array-like objects with Symbol.toPrimitive bypass validation
Look for similar incomplete type-checking in other language runtimes with permission models

## MITRE ATT&CK
- T1190
- T1548
- T1083

## Notes
This vulnerability demonstrates how permission models can be undermined through incomplete type checking. The fix (commit fa5dae1944) likely normalizes all path input types before validation. The existence of CVE-2023-30584 and CVE-2023-32004 predecessors suggests a pattern of incremental discovery—each patch addressed specific types while missing edge cases. Node.js experimental permission feature itself is security-relevant, making path handling particularly critical.

## Full report
<details><summary>Expand</summary>

Various `node:fs` functions allow specifying paths as either strings or `Uint8Array` objects. In Node.js environments, the `Buffer` class extends the `Uint8Array` class. Node.js prevents path traversal through strings (see CVE-2023-30584) and `Buffer` objects (see CVE-2023-32004), but not through non-`Buffer` `Uint8Array` objects.

This is distinct from CVE-2023-32004 ([report 2038134](https://hackerone.com/reports/2038134)), which only referred to `Buffer` objects. However, the vulnerability follows the same pattern using `Uint8Array` instead of `Buffer`.

## Steps To Reproduce:

The following Node.js command prints the contents of `/etc/passwd` despite having been granted access to `/tmp` only. This relies on the fact that `TextDecoder` produces `Uint8Array` objects that are not `Buffer` objects.

```
$ node --experimental-permission \
        --allow-fs-read=/tmp/ \
        -p 'fs.readFileSync(new TextEncoder().encode("/tmp/../etc/passwd"))'
<Buffer 72 6f 6f 74 3a 78 3a 30 3a 30 3a 3a 2f 72 6f 6f 74 3a 2f 62 69 6e 2f 62 61 73 68 0a 6e 6f 62 6f 64 79 3a 78 3a 36 35 35 33 34 3a 36 35 35 33 34 3a 4e ... 2103 more bytes>
```

## Supporting Material/References:

* CVE-2023-30584 ([report 1952978](https://hackerone.com/reports/1952978))
* Commit [205f1e6](https://github.com/nodejs/node/commit/205f1e643e25648173239b2de885fec430268492) prevents CVE-2023-30584 but ignores non-string inputs.
* CVE-2023-32004 ([report 2038134](https://hackerone.com/reports/2038134))
* Commit [1f64147](https://github.com/nodejs/node/commit/1f64147eb607f82060e08884f993597774c69280) prevents CVE-2023-32004 but ignores non-`Buffer` objects.

## Patch

I provided a patch, which was merged into Node.js 20 as [commit fa5dae1944](https://github.com/nodejs/node/commit/fa5dae1944).

## Impact

Equivalent to CVE-2023-30584 ([report 1952978](https://hackerone.com/reports/1952978)) and CVE-2023-32004 ([report 2038134](https://hackerone.com/reports/2038134)).

</details>

---
*Analysed by Claude on 2026-05-24*
