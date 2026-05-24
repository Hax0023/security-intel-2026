# Renderer Process Bluetooth Access Without Permission in Electron

## Metadata
- **Source:** HackerOne
- **Report:** 1519099 | https://hackerone.com/reports/1519099
- **Submitted:** 2022-03-22
- **Reporter:** palmeral
- **Program:** Electron
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Privilege Escalation, Permission Bypass, Insufficient Access Control, Sandbox Escape
- **CVEs:** CVE-2022-21718
- **Category:** uncategorised

## Summary
Renderer processes in vulnerable Electron versions can access nearby Bluetooth devices without user permission, despite being sandboxed. This allows untrusted content loaded in a renderer to interact with Bluetooth hardware, potentially compromising connected devices and user privacy.

## Attack scenario
1. Attacker identifies an Electron application that loads remote or user-supplied content in a renderer process
2. Attacker injects malicious JavaScript code into the renderer process (via compromised website, MITM, etc.)
3. Malicious script calls navigator.bluetooth.requestDevice() with permissive parameters
4. Vulnerable Electron version fails to enforce permission checks and returns a Bluetooth device object
5. Attacker gains read/write access to nearby Bluetooth devices without user consent
6. Attacker can interact with Bluetooth devices (read data, send commands, modify settings)

## Root cause
The Electron framework failed to properly validate and enforce Bluetooth permissions in renderer processes. The Web Bluetooth API permission check was either missing or incorrectly implemented, allowing sandboxed renderer processes to bypass the intended security boundary and access system Bluetooth resources.

## Attacker mindset
An attacker would target Electron applications that load untrusted content (web pages, user files, remote scripts). This is particularly dangerous because developers may assume renderer processes are safely sandboxed and allow loading of less-trusted content. The attacker leverages the Web Bluetooth API as a vector to escape the renderer sandbox and interact with physical hardware.

## Defensive takeaways
- Enforce strict permission checks for all Web APIs in renderer processes, even when they seem to have built-in safeguards
- Implement a whitelist-based approach for sensitive APIs rather than relying on default denial
- Ensure that all permission dialogs are mandatory and properly attributed to the requesting context
- Regularly audit the implementation of Web API permissions against the Chromium upstream
- Use preload scripts to selectively expose only necessary APIs rather than relying on sandbox defaults
- Keep Electron updated to the latest patch versions to receive security fixes
- Consider disabling Bluetooth access entirely if not needed by the application

## Variant hunting
Look for similar permission bypass vulnerabilities in other Web APIs accessible from renderer processes: USB API, NFC, Serial API, MIDI API, HID devices. Also investigate whether other Chromium-based applications (VS Code, Discord, Slack) have similar issues. Check for incomplete permission checks in preload script implementations that might expose other system resources.

## MITRE ATT&CK
- T1190
- T1548
- T1566

## Notes
This vulnerability is particularly concerning because it affects the core security model of Electron applications - the assumption that renderer processes are unprivileged. The vulnerability requires a default/vulnerable Electron configuration but doesn't require user interaction beyond the application loading untrusted content, which is a common use case. The impact depends on what Bluetooth devices are nearby but could include fitness trackers, smartwatches, hearing aids, medical devices, and smart home equipment.

## Full report
<details><summary>Expand</summary>

With the default configuration in Electron, renderer processes (which should not have access to system resources by default) can gain read/write access to a nearby bluetooth device. To reproduce:

* Run the electron-quick-start app with a vulnerable version of Electron: https://github.com/electron/electron-quick-start
* Using the developer tools, run `await navigator.bluetooth.requestDevice({acceptAllDevices: true})`
* You should get a permission error, but in vulnerable versions you will get a bluetooth device object instead.

## Impact

If an Electron app loads remote or untrusted content in a renderer process (which is normally fine, as the process should not have any privileges), the remote content would have read/write access to nearby bluetooth devices. The impact would then depend on what devices the user has nearby.

</details>

---
*Analysed by Claude on 2026-05-24*
