# RCE via Drag-and-Drop Shortcut Files to chrome://brave in Brave Browser

## Metadata
- **Source:** HackerOne
- **Report:** 415258 | https://hackerone.com/reports/415258
- **Submitted:** 2018-09-27
- **Reporter:** metnew
- **Program:** Brave Browser
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Remote Code Execution, Man-in-the-Middle Attack, Privilege Escalation, Arbitrary File Read, IPC Command Injection, URL Spoofing, UXSS (Universal XSS)
- **CVEs:** None
- **Category:** memory-binary

## Summary
Brave browser's handling of drag-and-drop shortcut files (.webloc on macOS, .desktop on Linux) allows navigation to the privileged chrome://brave origin, which can be exploited via MITM, local XSS, or known file paths to load malicious HTML. The loaded content gains access to private Electron APIs (ipcRenderer, ipcMain, chrome.remote.getBuiltin) enabling arbitrary IPC command execution, RCE through shell execution, and persistent device compromise.

## Attack scenario
1. Attacker performs MITM attack on victim's network or hosts malicious shortcut file with known path
2. Victim receives/downloads crafted shortcut file (.webloc/.desktop) pointing to attacker-controlled or chrome://brave URL
3. Victim drag-and-drops shortcut file into Brave browser tab
4. Browser navigates to chrome://brave origin with attacker's HTML content, bypassing navigation restrictions
5. Malicious HTML executes in chrome://brave context and accesses private APIs via ipcRenderer/getBuiltin
6. Attacker executes arbitrary IPC commands or downloads/executes malicious .terminal file, achieving RCE and persistence

## Root cause
Brave's patch blocking chrome://brave navigation only applied to direct navigation, not to Chromium's drag-and-drop handler which processes shortcut files at a lower level. The privileged chrome://brave origin was not properly isolated from Electron's private APIs (ipcRenderer, chrome.remote.getBuiltin), allowing loaded HTML to invoke dangerous IPC commands. HTTPS Everywhere was not enabled by default, and chrome:// origins lacked MITM protection.

## Attacker mindset
Sophisticated threat actor with network-level capabilities (MITM) or ability to place files locally. Exploits layering of security boundaries (navigation restrictions vs. drag-and-drop handling) and incomplete API sandboxing. Views shortcut files as social engineering vector and leverages Electron's powerful but dangerous IPC and remote module capabilities for maximum impact.

## Defensive takeaways
- Apply drag-and-drop restrictions at the same level as direct navigation - block navigation to privileged origins regardless of input vector
- Completely remove or deeply sandbox private Electron APIs (ipcRenderer, chrome.remote) in content processes, especially in privileged contexts
- Enable HTTPS Everywhere by default and extend MITM protections to chrome:// and file:// origins
- Implement origin-level isolation: privileged origins should not have access to any IPC mechanisms
- Validate and sanitize all file type handlers, especially shortcut files that trigger navigation
- Implement strict Content Security Policy for privileged origins preventing inline script execution
- Add user warnings for drag-and-drop actions from untrusted sources into browser tabs
- Regular security audits of Electron API surface exposed to renderer processes

## Variant hunting
Look for similar bypass vectors in drag-and-drop handling for other file types (.url on Windows, .ini files); check if other Electron-based browsers (Discord, Slack, VS Code) have similar layered protection bypasses; investigate whether file:// origin drag-and-drop has equivalent navigation bypass; search for other privileged origins (chrome://extensions, etc.) accessible via drag-and-drop; examine if IPC filtering existed but was incomplete; test whether SVG/object tag file:// loading can reach privileged origins; probe for other Electron API exposure paths beyond ipcRenderer.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1557.002 - Adversary-in-the-Middle: HTTPS Interception
- T1040 - Network Sniffing
- T1203 - Exploitation for Client Execution
- T1059.001 - Command and Scripting Interpreter: PowerShell/Bash
- T1053.005 - Scheduled Task/Job: Cron
- T1547.013 - Boot or Logon Autostart Execution: XDG Autostart Entries
- T1140 - Deobfuscation/Decoding

## Notes
Report demonstrates sophisticated understanding of Electron architecture, IPC mechanisms, and browser security boundaries. Attack leverages multiple bypass techniques (shortcut files, MITM, protocol registration). PoC for file reading provided; RCE PoC withheld but feasible. Brave's original patch (#395737) only blocked direct navigation, creating false sense of security. The core issue is Electron's powerful remote module exposure combined with privileged origin access. macOS .terminal file execution vulnerability (#374106) was used as RCE vector. Protocol module access (registerBufferProtocol, etc.) enables persistence through custom protocol handlers. Issue marked critical due to trivial user interaction requirement and complete system compromise potential.

## Full report
<details><summary>Expand</summary>

## Summary:

> \#395737 has shown that Brave supports `chrome://brave/<local_file>` URLs.
> The Brave team introduced a patch which blocks navigation to `chrome://brave` and removed `chrome.remote.require` to prevent command execution on the machine.

### Navigation to `chrome://brave` via shortcut files

> ~~From my understanding:~~

1. Brave allows DnDing files
2. DnD of shortcut files is handled on Chromium-level (shortcut files : e.g., `.webloc` on macOS or `.desktop` on Linux) 
3. DnDing a shortcut => navigation to URL the file points to.

This approach allows navigating to `chrome://brave/` origin.

#### Attack requirements

- The victim has to dnd a shortcut file to a tab
- Attacker needs **MITM** OR **local reflected XSS** OR an attacker-supplied **HTML file which absolute path** is known.

> MITM is the easiest way so far.

### Local files reading

Yeah, reading local files from `chrome://brave` is possible.
The same PoC as in #390362, but the origin is `chrome://brave`:

``` html
<head>
    <!-- Local files reading -->
    <script>
        function show() {
            var file = link.import.querySelector('body')
            alert(file.innerHTML)
        }
    </script>
    <link id="link" onload="show()" rel="import" as="document" href="chrome://brave/etc/passwd">
</head>
```

### `ipcRender` and `ipcMain`

HTML file loaded in `chrome://brave/` context has access to private APIs, like `ipcRenderer` and `ipcMain`:

``` js
let ipcMain = chrome.remote.getBuiltin('ipcMain')
let ipcRenderer = chrome.ipcRenderer
```

Sending arbitrary IPC commands -> full control over the browser.
**RCE through arbitrary IPC commands:** #188086 (includes PoC)

Impact: UXSS, URL spoofing, changing browser settings, etc.

### `chrome.remote.getBuiltin(module)`

Sending arbitrary IPC commands is a serious problem, but the impact isn't limited to it.

`chrome.remote.getBuiltin(module)` returns `electron[module]`.
``` js
// Alias to remote.require('electron').xxx.
binding.getBuiltin = function (module) {
  return metaToValue(ipcRenderer.sendSync('ELECTRON_BROWSER_GET_BUILTIN', module))
}
```

It's possible to leverage this func to obtain some "hidden" modules like `autoUpdater`, `Tray`, `protocol` and other.

#### Running attacker's executables on machine (download `.terminal` via IPC + <lack-of-quarantine> + `chrome.shell.openExternal`)

IPC allows doing many damaging things and possibly running shell commands too.

But there is an alternative way for an RCE:
1. IPC downloads a `.terminal` file from the web
2. #374106 - `.terminal` files could execute shell commands without `-x` permission
3. `chrome.remote.shell.openExternal` opens downloaded `.terminal` file
4. Commands from `.terminal` get executed

> No PoC provided, since the impact is already apparent, but could make it if required

#### Persistence

I'm sure, it's clear for the Brave team that it allows an attacker to persist on the device via changing browser settings.
However, I want to highlight that `chrome.remote.getBuiltin(module)` allows accessing `protocol` module, which allows:

```js
registerBufferProtocol: (...)
registerHttpProtocol: (...)
registerNavigatorHandler: (...)
registerServiceWorkerSchemes: ƒ ()
registerStandardSchemes: (...)
registerStringProtocol: ƒ ()
```

### MITM in Brave

- `chrome://brave` is always vulnerable to MITM even when HTTPSE is active
- `file://` is vulnerable to MITM, when HTTPSE is inactive

> Not sure whether HTTPSE is turned on by default.
> As far as I know, HTTPS Everywhere isn't enabled by default.

## Products affected: 

Brave: 0.24.0 
V8: 6.9.427.23 
rev: f657f15bf7e0e0c50a2b854c6b05edb59bfc556c 
Muon: 8.1.6 
OS Release: 17.7.0 
Update Channel: Release 
OS Architecture: x64 
OS Platform: macOS 
Node.js: 7.9.0 
Brave Sync: v1.4.2 
libchromiumcontent: 69.0.3497.100

## Steps To Reproduce:

### PoC for shortcut navigation

1. Open any page in Brave
2. DnD `etc-passwd.webloc` file to Brave
3. Brave opens `chrome://brave/etc/passwd` showing `/etc/passwd` file in `chrome://brave` origin's context

### Exploit (macOS)

-1. Make sure to stop `httpd` on macOS
0. Insert next line into your `/etc/hosts`: `127.0.0.1 maps.googleapis.com`
1. `sudo node server.js` - starts MITM server
2. Open any page in Brave
3. DnD `exploit.webloc` file
4. Opened page shows an alert with `/etc/passwd` contents + working `<webview>` tag  + starts `Calculator.app`

## Supporting Material/References:

Screencast attached.

## Impact

A remote attacker with a MITM access (or specific conditions like reflected XSS on `file:///` origin) could send arbitrary IPC commands(trigger RCE) when a user drag-n-drops 
crafted shortcut file into Brave.

</details>

---
*Analysed by Claude on 2026-05-12*
