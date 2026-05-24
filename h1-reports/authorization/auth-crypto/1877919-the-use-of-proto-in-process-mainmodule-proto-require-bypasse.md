# Permission System Bypass via __proto__ Chain in Node.js process.mainModule

## Metadata
- **Source:** HackerOne
- **Report:** 1877919 | https://hackerone.com/reports/1877919
- **Submitted:** 2023-02-17
- **Reporter:** haxatron1
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Privilege Escalation, Permission Policy Bypass, Prototype Pollution, Access Control Bypass
- **CVEs:** CVE-2023-30581
- **Category:** auth-crypto

## Summary
The Node.js permission system can be bypassed by accessing the require() function through the prototype chain via process.mainModule.__proto__.require() instead of the standard process.mainModule.require(). This allows loading modules that should be restricted by policy without triggering permission checks.

## Attack scenario
1. Administrator deploys Node.js application with experimental-policy flag to restrict module loading and enforce security boundaries
2. Policy.json defines resource integrity rules that prohibit loading certain modules (e.g., 'os', 'fs', 'child_process')
3. Attacker crafts malicious JavaScript code that accesses require() through the prototype chain instead of direct API
4. Attacker uses process.mainModule.__proto__.require('restricted-module') to load forbidden modules
5. Permission validation layer fails to intercept the require call because it only hooks the direct method
6. Attacker successfully loads and executes code from restricted modules, achieving unauthorized access

## Root cause
The permission system's require() interception only validates calls to process.mainModule.require() directly, but fails to validate calls that traverse the prototype chain through __proto__. The permission check is not applied to the underlying require function accessible via prototype chain traversal.

## Attacker mindset
An attacker would recognize that security policies enforced through method interception can sometimes be bypassed by accessing the underlying implementation through alternative code paths, particularly via prototype chain manipulation which is a well-known JavaScript technique.

## Defensive takeaways
- Implement permission checks at the module resolution engine level rather than only at the public API surface
- Validate all require() calls regardless of how the function is accessed (direct vs. prototype chain)
- Apply Object.freeze() or Object.seal() to sensitive objects to prevent prototype manipulation
- Consider disabling or strictly validating __proto__ access in security-sensitive contexts
- Audit all entry points to module loading, not just the primary ones
- Use internal slots or symbols instead of prototype-accessible properties for permission validation state

## Variant hunting
Test other prototype chain paths: process.mainModule.constructor.prototype.require()
Attempt Object.getPrototypeOf(process.mainModule).require()
Check if similar bypasses exist for require.resolve() or require.cache()
Test if other global objects with require methods (e.g., Module instances) have the same vulnerability
Investigate whether indirect require access through other parent modules bypasses checks
Test if the vulnerability extends to import() statements or dynamic require patterns

## MITRE ATT&CK
- T1548.001 - Abuse Elevation Control Mechanism
- T1027 - Obfuscated Files or Information
- T1218 - System Binary Proxy Execution
- T1108 - Application Shimming
- T1195.002 - Supply Chain Compromise: Compromise Software Supply Chain

## Notes
This vulnerability demonstrates that security boundaries implemented at the API level must account for JavaScript's dynamic prototype chain. The experimental-policy feature is not yet stable, and this finding highlights the challenges in sandboxing Node.js applications. The issue affects Node v19.6.1 and likely other versions with permission system support.

## Full report
<details><summary>Expand</summary>

process.mainModule.require() correctly works with permission system in Node v19.6.1. 
But the use of \_\_proto\_\_  in process.mainModule.\_\_proto\_\_.require() can bypass the check.

# Description and STR
Consider the following policy.json:
`````
{
  "resources": {
    "./proc.js": {
      "integrity": true
    }
  }
}
`````
The policy only allows proc.js file to be loaded without any dependencies.

However with the following proc.js
`````
const os = process.mainModule.__proto__.require("os")

console.log(process.version)
console.log(os.version())
`````
We get the output:
`````
└─$ ../node-v19.6.1-linux-x64/bin/node --experimental-policy=policy.json proc.js
v19.6.1
#1 SMP PREEMPT Debian 5.16.18-1kali1 (2022-04-01)
(node:2720) ExperimentalWarning: Policies are experimental.
(Use `node --trace-warnings ...` to show where the warning was created)
`````
Therefore os dependency can be loaded and os.version executed even if unspecified in permission system.

## Impact

Bypass the permission system

</details>

---
*Analysed by Claude on 2026-05-24*
