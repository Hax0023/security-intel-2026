# XSS leads to RCE on the RocketChat desktop client

## Metadata
- **Source:** HackerOne
- **Report:** 899964 | https://hackerone.com/reports/899964
- **Submitted:** 2020-06-16
- **Reporter:** fabianfreyer
- **Program:** RocketChat
- **Bounty:** Not specified in provided content
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (XSS), Remote Code Execution (RCE), Improper Access Control, Unsafe Electron API Usage
- **CVEs:** None
- **Category:** web-api

## Summary
A critical vulnerability in RocketChat Desktop Client allows attackers to achieve Remote Code Execution by chaining XSS vulnerabilities with unsafe Electron API exposure. By exploiting the `onclick` handler and manipulating `RegExp.prototype.test`, attackers can trigger `electron.shell.openExternal` with arbitrary URLs, enabling command execution on the victim's machine.

## Attack scenario
1. Attacker identifies or leverages an existing XSS vulnerability in RocketChat (such as CVE references #894462 or #899954)
2. Attacker crafts a malicious XSS payload that creates a DOM element with an attacker-controlled href attribute
3. Payload overrides `RegExp.prototype.test` to manipulate validation logic and bypass security checks
4. Attacker dispatches a click event on the crafted element, triggering the vulnerable onclick handler
5. The handler calls `electron.shell.openExternal` with a file:// URI pointing to an executable or command
6. Operating system executes the specified application or command with the privileges of the RocketChat desktop client process

## Root cause
The RocketChat Desktop Client exposed Electron's `shell.openExternal` API to the renderer process without proper validation. The onclick handler did not adequately sanitize or validate URLs before passing them to the dangerous API. Additionally, the validation logic relied on `RegExp.prototype.test`, which could be manipulated by overriding the prototype method.

## Attacker mindset
An attacker would recognize that XSS in an Electron application is significantly more dangerous than browser-based XSS due to access to native APIs. By chaining with an existing XSS flaw, the attacker could escalate to arbitrary code execution. The prototype pollution technique demonstrates sophisticated understanding of JavaScript internals and Electron architecture.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) to prevent XSS and prototype pollution
- Never expose dangerous Electron APIs (shell.openExternal, child_process.exec, etc.) to renderer processes
- Use preload scripts with IPC channels for controlled communication between renderer and main processes
- Validate and sanitize all user input and URL schemes before processing
- Implement URL scheme whitelisting and disable file:// protocol access from web content
- Use Object.freeze() or Object.defineProperty() to prevent prototype pollution
- Apply principle of least privilege to Electron contexts
- Regularly audit Electron security advisories and update promptly
- Implement both server-side and client-side XSS protections

## Variant hunting
Search for other Electron applications exposing dangerous APIs to renderers; look for similar prototype override techniques bypassing validation; investigate other onclick/event handlers that may invoke dangerous functions; examine file:// URI handling in other desktop applications; test for XSS in messaging/collaboration platforms with Electron clients

## MITRE ATT&CK
- T1190
- T1203
- T1059
- T1547
- T1566

## Notes
This vulnerability requires chaining with a pre-existing XSS flaw, making it a high-impact secondary exploit. The use of prototype manipulation to bypass regex-based validation demonstrates advanced JavaScript exploitation. Affects RocketChat Desktop Client versions up to 2.17.9. The vulnerability is OS-agnostic but requires OS-specific payload adjustment (file paths differ between Windows, macOS, Linux).

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
