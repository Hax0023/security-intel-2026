# RCE of Burp Suite Scanner/Crawler via Clickjacking and Chrome Remote Debugging

## Metadata
- **Source:** HackerOne
- **Report:** 1274695 | https://hackerone.com/reports/1274695
- **Submitted:** 2021-07-23
- **Reporter:** mattaustin
- **Program:** Burp Suite Professional
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Clickjacking, Insecure WebSocket Configuration, Port Enumeration, Arbitrary File Write
- **CVEs:** None
- **Category:** memory-binary

## Summary
Burp Suite's embedded Chrome browser runs with remote debugging enabled via WebSocket instead of named pipes, allowing attackers to discover the debug port through JavaScript port scanning. Combined with a Chrome XSS vulnerability and clickjacking, attackers can leverage Chrome remote debugging APIs to write malicious JVM configuration files, achieving RCE with user privileges.

## Attack scenario
1. Attacker hosts malicious HTML page containing JavaScript port scanner and clickjacking payload
2. Victim visits malicious page while Burp Suite is running with active crawler/scanner
3. JavaScript port scanner probes common port ranges to identify the Chrome remote debugging WebSocket port
4. Once port is identified, attacker crafts clickjacking overlay to trick victim into clicking button that triggers XSS
5. XSS vulnerability in Chrome executes attacker-controlled JavaScript with access to remote debugging APIs
6. Attacker uses debugging APIs to trigger file download of malicious user.vmoptions to Burp Suite installation directory with JVM exploit flags

## Root cause
Burp Suite launches embedded Chrome with --remote-debugging-port (WebSocket) instead of --remote-debugging-pipe (named pipe transport). WebSocket port is network-accessible and can be discovered via port scanning, whereas named pipes are protected by OS-level file permissions. Combined with known Chrome XSS vulnerability (unpatched since 2016) and lack of clickjacking protections, this creates exploitable attack chain.

## Attacker mindset
Sophisticated supply-chain or targeted attacker seeking to compromise security researchers/penetration testers using Burp Suite. Attack leverages public Chrome XSS vulnerabilities and social engineering (clickjacking) rather than zero-days, demonstrating awareness of tool deployment in security workflows and ability to chain multiple weaknesses into critical RCE.

## Defensive takeaways
- Use --remote-debugging-pipe instead of --remote-debugging-port for embedded browser instances to prevent network-level port discovery
- Implement clickjacking defenses (X-Frame-Options headers, frame-busting JavaScript) even for local/development tools
- Regularly patch or update embedded browser engines; do not rely on public knowledge of age as security through obscurity
- Apply principle of least privilege to embedded browser capabilities and remote debugging APIs
- Validate and sanitize any file operations triggered through remote debugging channels
- Consider disabling remote debugging by default in production tool builds unless explicitly required
- Implement strong authentication/authorization for remote debugging APIs rather than relying on port obscurity

## Variant hunting
Similar patterns exist in other tools embedding Chromium (VS Code, Electron apps, web automation frameworks). Investigate: (1) other JetBrains products with embedded browsers, (2) other security tools using Chrome headless mode for scanning, (3) Electron-based applications with remote debugging enabled, (4) custom built browsers in Java-based tools, (5) any tool allowing file writes via debugging APIs without proper validation.

## MITRE ATT&CK
- T1190
- T1200
- T1566.002
- T1218
- T1195.002
- T1021.001
- T1547.001

## Notes
Researcher correctly attributes this to Burp Suite rather than Chrome since the mitigation (named pipes) is available but not implemented. Attack requires victim interaction (clickjacking) but provides full system compromise. The chaining of port enumeration + known XSS + clickjacking + file write is creative exploitation of configuration weakness. No patch details provided in writeup but should use named pipe transport as remediation.

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
*Analysed by Claude on 2026-05-11*
