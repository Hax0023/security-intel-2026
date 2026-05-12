# Universal XSS via Playlist Feature - Token Exposure and String Injection

## Metadata
- **Source:** HackerOne
- **Report:** 1436558 | https://hackerone.com/reports/1436558
- **Submitted:** 2021-12-27
- **Reporter:** nishimunea
- **Program:** Brave Software
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (XSS), Information Disclosure, Code Injection, Token Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
Brave iOS contains a critical Universal XSS vulnerability in the Playlist feature resulting from three chained weaknesses: exposure of security tokens through embedded values in user scripts, and string concatenation of unsanitized user-controlled input (nodeTag) in JavaScript code executed on the mainframe. An attacker can exploit this to achieve arbitrary code execution with mainframe privileges across any domain.

## Attack scenario
1. Attacker crafts a malicious webpage and hosts it on attacker-controlled domain
2. Attacker embeds the malicious page as an iframe within a legitimate Google Sites page to bypass CORS restrictions
3. Victim visits the Google Sites page, which loads the cross-origin iframe
4. Malicious iframe reads the exposed securityToken from HTMLVideoElement.prototype.setAttribute and messageHandlerToken from postMessage handler
5. Malicious iframe crafts a nodeTag parameter containing JavaScript payload (e.g., `');alert(document.location);//`) and invokes Playlist functionality
6. PlaylistHelper.swift concatenates the unsanitized nodeTag into JavaScript code and executes it on mainframe, achieving UXSS

## Root cause
Three cascading vulnerabilities: (1) Playlist.js embeds security tokens directly into template strings accessible to page scripts, (2) WindowRenderHelper.js similarly exposes messageHandlerToken in plaintext, (3) PlaylistHelper.swift performs unsafe string concatenation without sanitization when building JavaScript code for mainframe execution, treating user-supplied nodeTag as trusted code rather than data

## Attacker mindset
An attacker recognizes that embedded security tokens in user scripts are meant to prevent script injection but can be extracted if directly visible in DOM operations. They identify that combining token exfiltration with string concatenation vulnerabilities creates a complete exploit chain. The cross-origin iframe technique leverages timing and the Playlist feature interaction to bypass additional security layers.

## Defensive takeaways
- Never embed security tokens directly in template strings or as observable parameter values in DOM operations
- Use indirect token lookup mechanisms (arrays, objects with opaque references) instead of direct value embedding
- Implement strict input validation and sanitization for all user-controlled data before code generation
- Use parameterized/templated JavaScript execution APIs that separate code from data rather than string concatenation
- Apply Content Security Policy (CSP) to restrict cross-origin iframe interactions and limit postMessage attack surface
- Use security tokens as keying material for cryptographic operations rather than as directly readable values
- Sanitize all nodeTag and similar parameters through allowlisting or escaping before inclusion in generated code
- Implement mainframe execution sandboxing to isolate injected code privileges

## Variant hunting
Search for similar patterns: (1) other user scripts embedding tokens in observable locations, (2) additional string concatenation vulnerabilities in *Helper.swift files, (3) other WebView mainframe execution points accepting user input, (4) similar token exposure in postMessage handlers for different features, (5) other DOM manipulation operations that may leak embedded values

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1567 - Exfiltration Over Web Service
- T1048 - Exfiltration Over Alternative Protocol
- T1059 - Command and Scripting Interpreter
- T1563 - Exploitation for Credential Access

## Notes
This is a chain of three distinct vulnerabilities that only becomes UXSS when combined. The cross-origin iframe technique is critical for the exploit as it allows the attacker to interact with Playlist functionality while maintaining the ability to read exposed tokens. The vulnerability affects the iOS platform specifically. Affected versions: 1.32.3 and higher including Nightly builds at time of report.

## Full report
<details><summary>Expand</summary>

## Summary:

Brave iOS has three weaknesses described below. By combining them, Universal XSS can be achieved.

1. Exposure of UserScriptManager.securityToken
[Playlist.js](https://github.com/brave/brave-ios/blob/fdff99ca3997816322015fe5efcd63490193b88d/Client/Frontend/UserContent/UserScripts/Playlist.js#L353) embeds the exact value of the `$<notifyNode>` into `HTMLVideoElement.prototype.setAttribute`. By reading the value, an attacker can retrieve the hidden security token.

2. Exposure of UserScriptManager.messageHandlerToken
Also, [WindowRenderHelper.js](https://github.com/brave/brave-ios/blob/83eb41ac922d7bd18fd311e0a4279e02cdd8e190/Client/Frontend/UserContent/UserScripts/WindowRenderHelper.js#L12) embeds the exact value of the `$<handler>` into `W{securityToken}.postMessage`. By reading the value, an attacker can retrieve the hidden message handler token.

3. UXSS in PlaylistHelper through nodeTag
[PlaylistHelper.swift](https://github.com/brave/brave-ios/blob/83eb41ac922d7bd18fd311e0a4279e02cdd8e190/Client/Frontend/Browser/PlaylistHelper.swift#L228) concatenates strings to build a JavaScript code and executes it on the mainframe of a WebView. Then, `nodeTag` given from a webpage is directly included in the code. So, if the `nodeTag`, named as `tagId` in JS world, passed from the page contained `');alert(document.location);//`, unintended `alert()` is executed on the mainframe.

## Products affected: 

 * Brave iOS 1.32.3 and higher (include the latest Nightly)

## Steps To Reproduce:

 * Visit the Google page: https://sites.google.com/view/nishimunea-brave-uxss1/page
* This page contains a cross origin malicious page https://csrf.jp/brave/playlist.php in an iframe
* The iframe exploits the above three weaknesses to send a message to playlistHelper
* Push `Add to Brave Playlist` and `Open` button in the setting menu
* An alert dialog is appear on the sites.google.com

## Supporting Material/References:

  * Demonstration movie is attached

## Impact

* Universal XSS on the arbitrary domains

</details>

---
*Analysed by Claude on 2026-05-12*
