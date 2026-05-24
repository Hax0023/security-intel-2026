# IP Address Leak via UNC Path in Windows File Picker

## Metadata
- **Source:** HackerOne
- **Report:** 376004 | https://hackerone.com/reports/376004
- **Submitted:** 2018-07-03
- **Reporter:** newfunction
- **Program:** Tor Browser
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Information Disclosure, IP Address Leak, Proxy Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can trick Tor Browser users into revealing their real IP address by using UNC paths in the Windows file picker dialog. When users browse to an attacker-controlled UNC path, the browser makes network requests outside the Tor proxy, exposing their actual IP. This bypasses Tor's privacy protections through the file picker input element and social engineering.

## Attack scenario
1. Attacker hosts a malicious website with an HTML file input element (<input type='file'>)
2. Attacker uses social engineering (fake file upload form) to convince Tor user to click 'Browse'
3. User clicks Browse button which opens Windows file picker dialog
4. Attacker instructs user to type UNC path (e.g., \\attacker-ip\share) into file picker
5. Windows file picker resolves UNC path and connects to attacker's server directly, bypassing Tor proxy
6. Attacker's server receives connection request containing user's real IP address in logs

## Root cause
Windows file picker dialog processes UNC paths outside the Tor proxy configuration. The browser fails to prevent or intercept UNC path resolution in the native file picker, allowing direct network connections that bypass Tor tunneling.

## Attacker mindset
Exploit native OS functionality that isn't constrained by the browser's security policies. Use social engineering combined with seemingly innocent UI elements to trick privacy-conscious users into revealing identifying information.

## Defensive takeaways
- Disable or block UNC path input in file picker dialogs for privacy-focused browsers
- Display warning messages when UNC paths are detected in file picker
- Consider hooking or intercepting Windows file picker API calls to enforce proxy routing
- Implement validation on file:// URIs to prevent UNC path resolution
- Add user awareness warnings about file picker social engineering techniques
- Test browser privacy features against native OS dialog interactions

## Variant hunting
Test other file dialog APIs (GetOpenFileName, GetSaveFileName) for similar bypasses
Check if SMB/CIFS protocol requests bypass proxy on macOS/Linux equivalents
Investigate if other protocols (ftp://, sftp://) in file pickers bypass proxy
Test if drag-and-drop of UNC paths into file inputs triggers same behavior
Check clipboard operations with UNC paths in file pickers
Verify if WebRTC or other APIs can similarly enumerate network shares

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing: Social Engineering
- T1040 - Traffic Sniffing
- T1557 - Man-in-the-Middle
- T1566 - Phishing

## Notes
This is a follow-up to bug #294364 where UNC paths were supposed to be disabled. The vulnerability persists because disabling happened at application level but native Windows dialogs still process UNC paths. Requires user interaction/social engineering to exploit, limiting impact but affecting privacy-critical Tor Browser users. The attack demonstrates the challenge of securing applications that interact with OS-level dialogs.

## Full report
<details><summary>Expand</summary>

This report is inspired by #294364. The release note says that after fixing [Bug 26424](https://trac.torproject.org/projects/tor/ticket/26424), UNC path is disabled in Tor. But I found that I can still type UNC path in Windows file picker dialog box, and that sends requests to remote servers without Tor proxy.

Some social engineering is required to exploit this trick though. Attackers can use <input type="file"> on their website, and trick users to click "Browse" and type an attacker-controlled IP address into file picker in UNC format.

Is it possible to disable UNC path in the Windows file picker? If not, how about showing a warning message?

## Impact

With some social engineering, attackers can know user's real IP address with <input type="file">.

</details>

---
*Analysed by Claude on 2026-05-24*
