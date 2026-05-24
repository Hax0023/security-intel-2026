# RCE of Burp Suite Scanner/Crawler via Clickjacking and Chrome Remote Debugging

## Metadata
- **Source:** HackerOne
- **Report:** 1274695 | https://hackerone.com/reports/1274695
- **Submitted:** 2021-07-23
- **Reporter:** mattaustin
- **Program:** Burp Suite (PortSwigger)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Clickjacking, Information Disclosure (Port Discovery), Insecure Remote Debugging Configuration, Privilege Escalation via JVM Options Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
Burp Suite's embedded Chrome browser is launched with remote debugging enabled via WebSocket (instead of named pipe), allowing attackers to discover the debugging port via JavaScript port scanning and exploit a known Chrome XSS vulnerability through clickjacking. By compromising the WebSocket GUID, attackers can leverage Chrome's remote debugging APIs to inject malicious JVM options that execute arbitrary OS commands when Burp Suite restarts.

## Attack scenario
1. Attacker hosts a malicious HTML page containing JavaScript port scanner and clickjacking payload
2. Victim visits the malicious page in Chrome while Burp Suite's embedded browser is scanning the attacker's web server
3. JavaScript port scanner brute-forces localhost ports to identify Chrome's remote debugging WebSocket port
4. Once identified, clickjacking payload leverages known Chrome XSS vulnerability to interact with remote debugging interface
5. Attacker uses Chrome DevTools Protocol to trigger file download of malicious user.vmoptions to Burp Suite application directory
6. Next Burp Suite launch executes injected JVM command via OnOutOfMemoryError handler, achieving RCE as the user running Burp

## Root cause
Burp Suite launches embedded Chrome with --remote-debugging flag using WebSocket protocol instead of named pipe. WebSocket port is randomized but discoverable via JavaScript port scanning. Combined with an exploitable Chrome XSS vulnerability (public since 2016), this allows unauthenticated port discovery and subsequent exploitation of Chrome DevTools Protocol to modify application configuration files.

## Attacker mindset
Opportunistic exploitation of a defense-in-depth failure: while individual components (Chrome XSS, port sniffing, clickjacking) are known issues, their combination in Burp Suite's architecture creates a critical RCE vector. The attacker identifies that WebSocket-based remote debugging is network-discoverable and exploitable, whereas named-pipe transport would isolate the debugging channel from network attacks.

## Defensive takeaways
- Use named-pipe transport (--remote-debugging-pipe) instead of WebSocket for embedded browser remote debugging to prevent network-based port discovery
- Implement Content-Security-Policy headers to prevent clickjacking and XSS exploitation on developer-facing pages
- Restrict file write permissions for application directories; use signed/validated configuration mechanisms instead of injectable options files
- Consider running embedded browsers in isolated sandboxes with minimal host system access
- Disable remote debugging in production/released builds; only enable in controlled development environments
- Implement JVM startup validation to reject suspicious memory/command options before execution

## Variant hunting
Search for similar patterns in other security tools: IDE plugins with embedded browsers (VS Code, JetBrains), web proxies (Fiddler, Telerik), and API testing tools (Postman) that may use embedded Chromium with network-exposed debugging. Also investigate other Java-based tools that accept user.vmoptions or similar configuration injection vectors.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1056 - Input Capture (Port Scanning via JavaScript)
- T1185 - Traffic Signaling
- T1611 - Escape to Host
- T1547.001 - Boot or Logon Initialization Scripts (JVM options injection)
- T1218 - Signed Binary Proxy Execution (JVM execution)
- T1021 - Remote Services (Chrome DevTools Protocol)
- T1005 - Data from Local System (WebSocket GUID extraction)

## Notes
Reporter appropriately attributes vulnerability to Burp Suite rather than Chrome, since Chrome's XSS is marked 'security impact: none' under official guidelines. The attack requires victim interaction (clickjacking click), but given the context of an active security scanner on a malicious website, user interaction is highly probable. Video PoC provided but not included in this analysis. Attack chain elegantly combines multiple weak points into a practical exploitation path.

## Full report
<details><summary>Expand</summary>

Burp Suite utilizes an embedded Chrome browser for crawling and scanning web applications. The Chrome instance is launched in headless mode, with remote debugging enabled via the remote-debugging websocket port instead of remote-debugging-pipe. As a result, a known XSS vulnerability in Chrome can be leveraged in combination with a JavaScript port sniffing and ClickJacking attack to compromise the WebSocket GUID for the remote debugging channel. Using the provided remote debugging APIs, it’s possible to trigger a file download to the `/Applications/Burp Suite Professional.app/Contents/` directory with a new `user.vmoptions` file. This will provide the `-Xmx5m` and `-XX:OnOutOfMemoryError=open -a Calculator` flags to JVM the next time that Burp Suite is launched. Accordingly, Burp Suite will quickly exhaust the available JVM memory and trigger the supplied OS command.

Based on Google’s security impact guidelines, this issue would typically be considered to have no security impact since Chrome requires additional flags to run (`--remote-debugging` and `--headless`) [1]. Additionally, the XSS vector used in this PoC has been public to Chrome since at least 2016 and reported in multiple tickets [2-6]. As a result, we are reporting this as a Burp Suite vulnerability since the named pipe transport could be utilized to mitigate this issue, which is supported by tools like puppeteer (e.g. `--remote-debugging-pipe`) [7]. 

### POC: 
See attached video. 

### Steps to reproduce:

To confirm this issue, perform the following steps:

1. Download the attached ‘burp.html’ exploit, and host it on a web server (e.g. `python -m http.server`)
2. Launch an instance of Burp Suite, and start a new scan of the web server.
3. Open a Chrome browser and navigate to the hosted exploit page (e.g. http://127.0.0.1:8000/burp.html)
4. Observe that a JavaScript port scanner is determining the randomized port listening for Chrome remote debugging. After the port is identified, a clickjacking payload will be rendered on the page. 
5. After clicking the ‘CLICK ME!!!’ button, restart Burp Suite and observe that the Calculator app has been launched. 

### References:
[1] https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/security-labels.md#TOC-Security_Impact-None
[2] https://bugs.chromium.org/p/chromium/issues/detail?id=607939
[3] https://bugs.chromium.org/p/chromium/issues/detail?id=618333
[4] https://bugs.chromium.org/p/chromium/issues/detail?id=619414
[5] https://bugs.chromium.org/p/chromium/issues/detail?id=775527
[6] https://bugs.chromium.org/p/chromium/issues/detail?id=798163
[7] https://github.com/puppeteer/puppeteer/blob/943477cc1eb4b129870142873b3554737d5ef252/src/node/PipeTransport.ts

## Impact

After successful exploitation an attacker can gain control over victim's computer with the same permissions as the user running the scanner.

</details>

---
*Analysed by Claude on 2026-05-24*
