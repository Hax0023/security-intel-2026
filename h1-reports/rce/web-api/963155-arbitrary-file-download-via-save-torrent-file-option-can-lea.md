# Arbitrary File Download via 'Save .torrent File' Option Leading to Client RCE and XSS

## Metadata
- **Source:** HackerOne
- **Report:** 963155 | https://hackerone.com/reports/963155
- **Submitted:** 2020-08-20
- **Reporter:** d3f4u17
- **Program:** Brave Browser
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Arbitrary File Download, Remote Code Execution, Cross-Site Scripting (XSS), Content-Type Validation Bypass, File Type Confusion
- **CVEs:** None
- **Category:** web-api

## Summary
WebTorrent's file validation in Brave Browser relies solely on HTTP headers (Content-Disposition and Content-Type) to determine if a file is a legitimate torrent, allowing attackers to bypass validation by setting appropriate headers while serving malicious files. An attacker can exploit this to deliver executable files (.bat, .exe, .js) or HTML/JavaScript payloads that execute with the user's privileges, achieving RCE or XSS.

## Attack scenario
1. Attacker creates a malicious server that responds with torrent-like headers (Content-Disposition with .torrent filename and Content-Type: application/octet-stream) when Referer header is present
2. Attacker sends victim a link to the malicious server where clicking 'Save .torrent file' is presented
3. WebTorrent validates the response based only on headers and permits download without proper file content verification
4. User's browser saves the file with attacker-controlled extension (.bat, .exe, .js, .html) instead of legitimate .torrent
5. User executes the downloaded file, triggering RCE (for .bat/.exe), XSS (for HTML/JS), or malware installation
6. Attacker gains code execution with the user's privileges or steals sensitive browser data through XSS

## Root cause
WebTorrent implements insufficient file validation by trusting HTTP response headers (Content-Disposition and Content-Type) without verifying actual file content or magic bytes. The validation logic does not inspect the file body to confirm it is a valid torrent file, and the dual-filename technique in Content-Disposition allows filename smuggling.

## Attacker mindset
An attacker recognizes that client applications often trust HTTP headers as a security boundary and that users are conditioned to trust 'Save' dialogs. By crafting headers that appear legitimate to automated parsers while serving different file content, they can disguise malicious executables as harmless torrent files, exploiting the gap between what the browser shows the user and what is actually written to disk.

## Defensive takeaways
- Never rely solely on HTTP headers (Content-Type, Content-Disposition) for file type validation; always verify file content (magic bytes/file signatures)
- Implement strict content validation: parse the downloaded content as a torrent and reject if parsing fails, before allowing the download to complete
- Use a whitelist of allowed file extensions and MIME types for torrent downloads; reject mismatches between declared and actual file types
- Sanitize filename from Content-Disposition header; remove or reject dual-filename encoding attempts and suspicious characters
- Warn users when downloaded file extension differs from the expected type or when content-type mismatches file signature
- Consider sandboxing torrent file processing or executing downloaded files in restricted environments
- Implement sub-resource integrity checks or cryptographic verification for critical file downloads

## Variant hunting
Test other Chromium-based browsers (Edge, Chrome, Opera) for the same WebTorrent integration vulnerability
Probe file download handlers in other applications for header-only validation without content verification
Investigate if other content types accepted by browsers (.zip, .pdf, .exe) are similarly vulnerable to header spoofing
Research RFC 6266 Content-Disposition parsing inconsistencies across different browsers (filename vs filename* parameter handling)
Test polyglot file techniques where a single file is both a valid torrent and executable to bypass extension-based filtering
Examine if temporary file paths or download directories have predictable locations that could be exploited
Investigate if the Referer-based conditional logic can be bypassed using referrer-policy headers or other header manipulations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204.001 - User Execution: Malicious Link
- T1204.002 - User Execution: Malicious File
- T1566.002 - Phishing: Spearphishing Link
- T1105 - Ingress Tool Transfer
- T1059.001 - Command and Scripting Interpreter: PowerShell
- T1609 - Container Administration Command

## Notes
This vulnerability demonstrates a classic security mistake: trusting client-controlled data (HTTP headers) as a security boundary. The attack leverages the Referer header as a simple condition to determine which file to serve, showing how attackers can weaponize legitimate user workflows. The PoC using Notepad is relatively benign, but the technique scales to full RCE via .bat, .exe, or .vbs files, or XSS via JavaScript/HTML files. The vulnerability affects all users who interact with WebTorrent downloads, making it broadly exploitable.

## Full report
<details><summary>Expand</summary>

## Summary:

An attacker can use the "Save .torrent file" option in WebTorrent to smuggle malicious files onto the client's machine.

## Description

Brave allows users to download the ".torrent"  via WebTorrent. WebTorrent decides whether a file is torrent or not based on the following headers `Content-Disposition` and `Content-Type` an attacker can craft a clever looking server side file to bypass the WebTorrent validation which in turn allows the users to download the malicious file instead of an actual torrent file, this behavior can easily lead to localhost* xss and client side RCE.

I used the following PHP code to bypass the WebTorrent validation.

```php
<?php

if(isset($_SERVER['HTTP_REFERER'])){
    header("Content-Disposition: attachment; filename='PoC.torrent'; filename*=UTF-8''PoC.torrent");
    header("Content-Type: application/octet-stream");
}
else{
    header("Content-Disposition: attachment; filename='PoC.bat'; filename*=UTF-8''PoC.bat");
    header("Content-Type: application/x-bat");
    echo "@echo off\n";
    echo "START C:\Windows\NOTEPAD.EXE";
}
?>

```
In the above code when the `Referer` header is passed along with the request then only the server returns a torrent file response otherwise the server will return a `.bat` file which when executed will open notepad on a Windows Machine.

## Tested on 

 * Brave Version 1.12.114 Chromium: 84.0.4147.135 (Windows)

## Steps To Reproduce:

* Visit https://php-demo-app-shibli.cfapps.io/test-driver.php on your brave webbrowser on Windows OS.
* Click on "click me" link
* Click on "Save .torrent file" option
* Save the file and open it.
* When you will execute the file Notepad will open on our windows machine.

Below is a video POC for the above attack scenario

{F956579}

## Impact

* Remote Code Execution
* Remote JavaScript execution
* Installing malware on client's machine

</details>

---
*Analysed by Claude on 2026-05-12*
