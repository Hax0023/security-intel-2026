# fs.openAsBlob() bypasses Node.js permission system

## Metadata
- **Source:** HackerOne
- **Report:** 1966492 | https://hackerone.com/reports/1966492
- **Submitted:** 2023-04-29
- **Reporter:** cjihrig
- **Program:** Node.js
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Authorization Bypass, Permission Model Circumvention, Information Disclosure
- **CVEs:** CVE-2023-30583
- **Category:** uncategorised

## Summary
The fs.openAsBlob() API in Node.js does not respect the experimental permission system (--experimental-permission flag), allowing attackers to read files they should not have access to. This completely bypasses the intended permission restrictions for blob file operations.

## Attack scenario
1. Attacker obtains code execution within a Node.js process started with --experimental-permission
2. Permission system is configured to deny read access to sensitive files (e.g., file.txt)
3. Attacker calls fs.openAsBlob() with path to restricted file
4. Permission check is not enforced for openAsBlob() operation
5. Attacker successfully obtains file blob object without permission denial
6. Attacker extracts file contents via blob.text() or blob.stream()

## Root cause
The fs.openAsBlob() function was implemented without integrating permission checks from the experimental permission system. While other fs methods validate permissions, this newer API method skips the permission validation layer entirely.

## Attacker mindset
An attacker with code execution in a permission-restricted Node.js environment would systematically test new/modern APIs (like openAsBlob) to find permission bypass vectors, as developers may overlook newer methods when implementing security controls.

## Defensive takeaways
- Ensure all file access APIs consistently enforce permission checks at a central validation point
- Test new APIs and language features against security boundaries when releasing experimental features
- Implement permission checks at the lowest I/O abstraction layer rather than per-API
- Include experimental APIs in security feature compliance testing before stable release
- Use code auditing to identify permission validation gaps across API surface
- Consider unified permission decorator/middleware approach for all file operations

## Variant hunting
Similar permission bypasses likely exist in other newer Node.js APIs (fs.createReadStream with certain options, fs.promises variants, or Blob-related methods). Test all fs.* methods added after permission system implementation. Check buffer/stream APIs that may not have permission wrappers.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate Local System
- T1566 - Phishing
- T1059 - Command and Scripting Interpreter

## Notes
This is a permission model design flaw in Node.js. The experimental permission system was intended as a sandboxing mechanism, but incomplete coverage undermines its security guarantees. The bug demonstrates the difficulty of retrofitting security controls to existing APIs without comprehensive coverage.

## Full report
<details><summary>Expand</summary>

**Summary:** [add summary of the vulnerability]
`fs.openAsBlob()` does not appear to be limited by the permission system.

**Description:** [add more details about this vulnerability]
Starting Node with `--experimental-permission` does not appear to restrict `fs.openAsBlob()`.

## Steps To Reproduce:

Run the following code with `--experimental-permission` and do not grant is read access to `file.txt`:

```js
'use strict';
const fs = require('node:fs');

async function main() {
	const blob = await fs.openAsBlob(__dirname + '/file.txt');

	console.log(await blob.text());
}

main();
```

## Impact: [add why this issue matters]

The permission system is bypassed when it should not be.

## Supporting Material/References:

None

## Impact

An attacker can read files they should not be able to.

</details>

---
*Analysed by Claude on 2026-05-24*
