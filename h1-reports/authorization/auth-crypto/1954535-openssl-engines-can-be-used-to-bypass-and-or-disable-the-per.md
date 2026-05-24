# OpenSSL Engines Bypass Node.js Permission Model

## Metadata
- **Source:** HackerOne
- **Report:** 1954535 | https://hackerone.com/reports/1954535
- **Submitted:** 2023-04-19
- **Reporter:** tniessen
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Privilege Escalation, Security Policy Bypass, Arbitrary Code Execution, Native Code Injection
- **CVEs:** CVE-2023-30586
- **Category:** auth-crypto

## Summary
Node.js 20's permission model can be bypassed by loading arbitrary OpenSSL engines via crypto.setEngine(), which executes native code outside the permission system. An attacker can use this to disable the permission model entirely, allowing JavaScript to escalate its own privileges and execute unrestricted code.

## Attack scenario
1. Attacker obtains access to Node.js application running with permission model enabled to restrict capabilities
2. Attacker injects or supplies malicious JavaScript code that calls crypto.setEngine() with a crafted OpenSSL engine
3. Permission model fails to block native engine loading despite blocking native addons by default
4. Malicious OpenSSL engine code executes with native privileges, outside permission model constraints
5. Engine code patches or disables the permission model in the host process
6. Subsequent JavaScript execution runs unrestricted, gaining full access to previously forbidden resources

## Root cause
The permission model implementation did not enforce restrictions on OpenSSL engine loading through crypto.setEngine(), creating a gap between intended security boundaries and actual enforcement. Native code loading through the crypto module was not properly gated by the permission system.

## Attacker mindset
Identify security boundaries and permission enforcement gaps. Recognize that crypto operations often require native code integration and exploit this as a backdoor to bypass intended restrictions. Escalate from constrained execution context to full system access through legitimate API calls.

## Defensive takeaways
- Apply permission model restrictions uniformly across all code loading mechanisms, including native engines and crypto operations
- Audit and gate all native code execution paths, not just explicit addon loading mechanisms
- Implement deny-by-default for engine/module loading when permission model is active
- Validate that security policies cannot be disabled or circumvented from within restricted code contexts
- Test permission model enforcement end-to-end against attack vectors using legitimate APIs
- Document which APIs can load native code and ensure consistent security treatment

## Variant hunting
Search for other crypto or system APIs that load native code (e.g., native modules, FIPS engines, custom providers). Check for similar gaps in permission enforcement for: certificate loaders, OpenSSL provider modules, FFI mechanisms, and platform-specific native integrations.

## MITRE ATT&CK
- T1190
- T1548
- T1199
- T1574

## Notes
This is a critical sandbox escape in Node.js permission model (introduced in v20). The vulnerability demonstrates that security models must account for all execution paths, not just obvious ones. OpenSSL engine loading is a legitimate feature but became an unintended privilege escalation vector when permission enforcement was incomplete.

## Full report
<details><summary>Expand</summary>

**Summary:** Node.js 20 allows loading arbitrary OpenSSL engines even when the permission model is enabled, which can bypass and/or disable the permission model.

**Description:** The permission model implementation permits loading arbitrary native code, e.g., through `crypto.setEngine()`, even when native addons are disallowed, which is the default configuration. Not only can this code bypass the permission system, it can also disable the permission system entirely, effectively allowing JavaScript code to escalate its own privileges.

## Steps To Reproduce:

  1. Enable the permission model.
  2. Call, for example, `crypto.setEngine()` with a compatible OpenSSL engine.
  3. Arbitrary code execution occurs, unaffected by the permission model.

## Impact

The permission model is supposed to restrict the capabilities of running code. However, exploiting this vulnerability allows an attacker to easily bypass the permission model entirely. The OpenSSL engine can, for example, disable the permission model in the host process, and subsequently executed JavaScript code will be unaffected by the previously enabled permission model. This allows running JavaScript code to effectively elevate its own permissions.

</details>

---
*Analysed by Claude on 2026-05-24*
