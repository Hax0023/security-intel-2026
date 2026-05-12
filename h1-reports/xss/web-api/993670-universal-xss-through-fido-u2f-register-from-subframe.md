# Universal XSS through FIDO U2F Register from Subframe in Brave iOS

## Metadata
- **Source:** HackerOne
- **Report:** 993670 | https://hackerone.com/reports/993670
- **Submitted:** 2020-09-28
- **Reporter:** nishimunea
- **Program:** Brave Software
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Cross-Site Scripting (XSS), Universal XSS (UXSS), Code Injection, Origin Confusion, Insecure Deserialization
- **CVEs:** None
- **Category:** web-api

## Summary
Brave iOS's FIDO U2F implementation contains three critical weaknesses that combine to enable Universal XSS. A cross-origin subframe can invoke U2F.register() via postMessage, and the unescaped version parameter is directly embedded into evaluateJavaScript, allowing arbitrary JavaScript execution on the top-level frame.

## Attack scenario
1. Attacker hosts a victim website (e.g., alice.csrf.jp) containing a legitimate FIDO registration flow
2. Victim visits attacker's site which contains a hidden cross-origin iframe pointing to attacker-controlled domain (evil.csrf.jp)
3. The malicious iframe calls U2F.postMessage directly to trigger u2f.register() with a crafted version parameter containing JavaScript payload
4. Brave's FIDO modal displays the legitimate top-frame origin name, deceiving the user into trusting the operation
5. User inserts FIDO device (e.g., YubiKey) and completes authentication on the attacker's malicious iframe
6. The unescaped version parameter is executed via evaluateJavaScript, resulting in arbitrary code execution in the context of the top-level origin

## Root cause
Three compounding implementation flaws: (1) U2F.postMessage handler lacks origin validation, allowing cross-origin subframe invocation, (2) FIDO modal displays top-frame origin instead of actual caller origin, creating user confusion, (3) the version parameter from postMessage is directly embedded into evaluateJavaScript without proper escaping or sanitization.

## Attacker mindset
Exploit weak cross-origin isolation in FIDO implementation. Abuse the trust displayed in security modals by showing legitimate origin names. Leverage the assumption that developers would escape JavaScript strings in code generators. Combine multiple weak controls to bypass individual security measures.

## Defensive takeaways
- Always validate the origin of postMessage callers and enforce strict same-origin policy for security-sensitive operations like FIDO registration
- Display the actual caller's origin in security-critical modals, not the top-level frame origin, to prevent origin confusion attacks
- Properly escape and sanitize all user-controlled and message-controlled parameters before passing them to code evaluation functions like evaluateJavaScript
- Implement Content Security Policy (CSP) to restrict script execution contexts and mitigate XSS impact
- Use parameterized or safer APIs instead of string concatenation for dynamic code execution
- Conduct security reviews of cross-origin communication handlers, particularly those handling cryptographic operations
- Implement frame ancestor checks and X-Frame-Options headers to limit framing capabilities

## Variant hunting
Search for similar patterns in other U2F/WebAuthn implementations where: (1) message handlers lack origin validation, (2) parameters are interpolated into evaluateJavaScript/eval-like functions, (3) security modals display incorrect origin information. Check other Brave platforms (Android, Desktop) for identical code patterns. Investigate other cryptographic UI operations that may have similar weaknesses.

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1539
- T1040

## Notes
This is a critical UXSS vulnerability combining multiple weak controls. The attack requires user interaction with a FIDO device but succeeds in breaking origin isolation completely. The vulnerability demonstrates why security-critical operations must validate both the caller and display accurate security context information. The fix requires changes across multiple code layers (message validation, UI display, and string escaping).

## Full report
<details><summary>Expand</summary>

## Summary:

There are three weaknesses in Brave's FIDO U2F implementation.

* `u2f.register()` can be executed from cross-origin subframe by invoking [U2F.postMessage](https://github.com/brave/brave-ios/blob/e52c52495aa654584abe8172d689977756e6549d/Client/Frontend/UserContent/UserScripts/U2F.js#L264) directly
* Then, FIDO related modals show the name of top frame origin (but not caller subframe)
* The `version` parameter sent from the above `postMessage` is embedded in an [evaluateJavaScript](https://github.com/brave/brave-ios/blob/d01b8c07b8a6244af48798efe4afeccd266707e2/Client/WebAuthN/U2FExtensions.swift#L1003) without escape

The combination of these weaknesses allows cross-domain subframe to inject any JavaScript code to the top frame through fake U2F registration process.
## Products affected: 

 * Brave iOS Version 1.20 (20.09.11.20), also current Nightly

## Steps To Reproduce:

* Open [UXSS Victim](https://alice.csrf.jp/brave/uxss_victim.php) hosted on alice.csrf.jp.
  This site has a cross-origin iframe that opens evil.csrf.jp.
* Ready to Scan dialog is shown with the name of top frame
* Insert your FIDO device such as YubiKey 5Ci and touch
* Injected JavaScript `alert()` is executed on the top frame

## Supporting Material/References:

  * See attached movie file for the demonstration

## Impact

As written in summary, malicious web content in subframe can UXSS on the top frame origin.

</details>

---
*Analysed by Claude on 2026-05-12*
