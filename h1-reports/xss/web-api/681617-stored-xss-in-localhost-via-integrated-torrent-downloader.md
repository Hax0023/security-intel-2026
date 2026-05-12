# Stored XSS in localhost:* via Integrated Torrent Downloader

## Metadata
- **Source:** HackerOne
- **Report:** 681617 | https://hackerone.com/reports/681617
- **Submitted:** 2019-08-25
- **Reporter:** ryotak
- **Program:** Brave Browser
- **Bounty:** Not specified in provided content
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Path Traversal via Filename
- **CVEs:** CVE-2019-15782
- **Category:** web-api

## Summary
Brave Browser's integrated torrent downloader fails to sanitize torrent filenames, allowing attackers to execute arbitrary JavaScript on localhost:* through crafted torrent files. The vulnerability persists via service workers, enabling theft of sensitive data from any future service running on the compromised port.

## Attack scenario
1. Attacker crafts a malicious .torrent file with a filename containing JavaScript payload (e.g., filename with XSS payload like '../../../localhost:8080/malicious.html')
2. Victim downloads the torrent file through Brave's integrated downloader (either directly or via iframe embedding)
3. Brave initiates torrent download and fails to sanitize the filename, storing the payload in a localhost:* accessible location
4. Service worker registered during torrent download caches the malicious JavaScript
5. Attacker can now access the stored XSS via iframe or by brute-forcing the port number used
6. Any future application running on that port has its data compromised as the malicious service worker intercepts requests

## Root cause
The torrent downloader module does not implement filename sanitization or validation before processing and storing torrent metadata. The combination of unsanitized filenames and service worker registration creates a persistent attack surface on localhost addresses.

## Attacker mindset
An attacker recognizes that localhost services are often less protected than internet-facing applications and that service workers provide persistent storage. By embedding the attack in a torrent file, they leverage user trust in file downloads and exploit the browser's built-in torrent handler. Port brute-forcing and iframe embedding allow passive, stealthy exploitation without user awareness.

## Defensive takeaways
- Implement strict filename validation and sanitization for all downloaded files, especially those processed by built-in handlers
- Sanitize filenames to remove path traversal sequences (../, .\) and special characters that could be interpreted as HTML/JavaScript
- Apply Content Security Policy (CSP) restrictions to localhost origins to prevent arbitrary script execution
- Isolate service worker registration scope to prevent cross-origin service worker interference
- Validate and sanitize all metadata extracted from torrent files before using it in file operations or web contexts
- Implement same-origin policy enforcement for localhost with port-based isolation
- Add warnings or require explicit user consent before registering service workers from downloaded content

## Variant hunting
Check other integrated file handlers (FTP, magnet links, HTTP streams) for similar filename sanitization issues
Test if other Chromium-based browsers (Chrome, Edge, Vivaldi) have similar torrent handling vulnerabilities
Investigate whether crafted filenames can exploit other localhost services beyond XSS (SSRF, file write attacks)
Examine if service worker scope can be abused to affect file:// protocol access
Test special characters in filenames that might bypass sanitization (Unicode, encoding bypasses)
Verify if the vulnerability affects other localhost:port combinations or if certain ports are protected

## MITRE ATT&CK
- T1190
- T1566.002
- T1059.007
- T1547.016
- T1102.003

## Notes
The vulnerability is particularly dangerous because: (1) Service workers persist across browser sessions, (2) Localhost services are increasingly common (dev tools, Docker, local DBs), (3) The attack surface can be expanded via iframe embedding without user interaction, (4) Port brute-forcing is feasible for common ports (3000, 5000, 8000, 8080, 8888, 9000, etc.). The fix requires defense-in-depth: filename sanitization, CSP headers, and service worker scope restrictions.

## Full report
<details><summary>Expand</summary>

## Summary:

Due to filename of downloading torrent file isn't sanitized, an attacker is able to execute arbitrary JavaScript on localhost:* by abusing crafted torrent file.

## Products affected: 

 * Brave 0.68.131 Chromium: 76.0.3809.100 (Official Build)

## Steps To Reproduce:

 1. Open https://exec.ga/browser/brave/xss.torrent in Brave Browser.
 1. Click "Start Torrent" button
 1. Copy link address of "Save File" button.
 1. Paste it to URL bar with only hostname and port (e.g. http://localhost:8080).
 1. Alert will be popped up.

**Note**: Since it can be embedded with iframe (and it's possible to brute force port number), Steps after 2 won't be needed in real attack.

## Video PoC
{F565161}

## Impact

Attacker will be able to store arbitrary JavaScript on localhost:* with service worker, so if victim run any software on same port after attack, any information in the website that on same port can be stolen.

</details>

---
*Analysed by Claude on 2026-05-12*
