# Unauthorized Command Execution in Kaspersky Web Protection Component via Script Injection Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 470544 | https://hackerone.com/reports/470544
- **Submitted:** 2018-12-21
- **Reporter:** palant
- **Program:** Kaspersky
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Command Injection, Security Bypass, Privilege Escalation, Code Injection, Sandbox Escape
- **CVEs:** CVE-2019-15685
- **Category:** memory-binary

## Summary
Kaspersky Internet Security falls back to direct script injection into webpages when browser extensions are unavailable, allowing arbitrary websites to manipulate the injected scripts and gain full access to Kaspersky's command interface. Attackers can disable security features, manipulate blocklists, and potentially trigger RCE vulnerabilities in the avp.exe process running with SYSTEM privileges.

## Attack scenario
1. Attacker identifies that Kaspersky injects protection scripts directly into webpages matching pattern www.google.* when no browser extension is installed
2. Attacker crafts malicious HTML page that downloads and analyzes the injected Kaspersky script to locate the command interface address
3. Attacker manipulates JavaScript objects and re-executes Kaspersky's initialization code to gain unprotected references to the command interface
4. Attacker calls Kaspersky API methods through the command interface to disable Anti-Banner and Private Browsing features
5. Attacker adds malicious URLs to Kaspersky's blocklist or explores RCE attack vectors against avp.exe
6. User experiences degraded security posture with features disabled and potential system compromise via elevated process exploitation

## Root cause
Kaspersky's fallback protection mechanism relies on script injection combined with weak obfuscation and timing-based security assumptions. The script injection occurs before webpage scripts execute, but attackers can manipulate the JavaScript environment and re-trigger initialization to obtain unprotected API access. Domain-pattern whitelisting (www.google.*) is insufficient to prevent abuse.

## Attacker mindset
Exploit the gap in security coverage when browser extensions fail to load by leveraging the antivirus vendor's own fallback protection mechanism against them. Recognize that script injection without strong isolation creates a privilege escalation vector to system-level processes. View this as entry point to RCE exploitation of the underlying avp.exe process.

## Defensive takeaways
- Never rely on script injection as primary security mechanism without strong sandbox isolation and content security policy enforcement
- Implement cryptographic verification and integrity checks for injected scripts rather than relying on obfuscation or domain patterns
- Use separate isolated contexts (Web Workers, sandboxed iframes) for security-critical functionality to prevent DOM manipulation attacks
- Establish robust fallback mechanisms that degrade gracefully to read-only telemetry rather than exposing command interfaces when extensions unavailable
- Implement strict API access controls with origin verification and capability-based security model
- Conduct threat modeling specifically for scenarios where security overlays fail or are bypassed
- Add Content Security Policy headers and X-Frame-Options to prevent script context manipulation
- Perform regular security audits of privileged process exposure to web-accessible APIs

## Variant hunting
Search for similar patterns in other antivirus products: Norton, McAfee, Avast, AVG, Trend Micro. Look for fallback mechanisms in browser-based security features. Investigate whether other products using domain-pattern whitelisting (*.google.com, *.microsoft.com) have comparable bypass techniques. Check for privilege escalation vectors via exposed command interfaces in any security software with SYSTEM-level processes.

## MITRE ATT&CK
- T1190
- T1203
- T1548
- T1562
- T1562.001
- T1036
- T1036.004
- T1547

## Notes
Report demonstrates sophisticated understanding of Kaspersky's architecture and protection mechanisms. The vulnerability chains multiple weaknesses: insufficient script isolation, weak domain whitelisting, and exposure of privileged APIs. The mention of potential RCE via avp.exe process bugs is particularly concerning and suggests defense-in-depth failures. Requires no user interaction beyond visiting a webpage and no elevated privileges, making it trivial to exploit at scale.

## Full report
<details><summary>Expand</summary>

**Summary**
When no browser extension is installed, arbitrary webpages can take control of the Kaspersky command interface and disable parts of the functionality for example.

**Description**
Without a browser extension (e.g. because extension installation not confirmed by user, unsupported like in MS Edge or uninstalled via https://hackerone.com/reports/470519), Kaspersky fall back to injecting its script directly into the webpage. There are provisions to prevent the webpage from discovering the address of these script, which are trivially circumvented by the webpage downloading itself. There are also provisions to inject the script before any webpage scripts can run, so that unmanipulated references to various JavaScript objects can be stored. These provisions can also be circumvented by manipulating the objects and rerunning Kaspersky's script then. As a result, webpages can get full access to Kaspersky's command interface which allows disabling Anti-Banner and Private Browsing functionality for example (either completely or on specific sites), adding URLs to the blocklist and much more. Worse yet: by exposing Kaspersky's internal processing to the web, bugs in this processing code will turn into Remote Code Execution vulnerabilities allowing websites to execute code with the privileges of the SYSTEM user (I haven't explored this possibility further).

**Environment**
- Scope: Application
- Product name: Kaspersky Internet Security
- Product version: 19.0.0.1088
- OS name and version (incl SP): Windows 10.0.17134
- Attack type: Command Injection
- Maximum user privileges needed to reproduce your issue: no privileges

**Steps to reproduce**
I tested this with Chrome 71, it should work with any other browser as well however.

1. Go to Kaspersky settings and make sure that Anti-Banner and Private Browsing features are turned on.
2. Download attached `server.py` and `disable_features1.html` to some directory on your computer and run `server.py` (Python 3 required). This is a very rudimentary HTTP server running on http://localhost:5000/, you could use some other web server as well.
3. Edit the file %WINDIR%\sysnative\drivers\etc\hosts as administrator and add the following line: `127.0.0.1 www.google.example.com`. Normally, you would just use a subdomain of a domain you own - the host name has to start with "www.google." for Kaspersky's script to be injected there.
4. Make sure that no Kaspersky browser extension is installed in your browser. If it is, disable the extension and restart the browser.
5. Go to http://www.google.example.com:5000/disable_features1.html with your browser.
6. Check Kaspersky settings and note that Anti-Banner and Private Browsing features are now disabled.

## Impact

Websites gain full control of Kaspersky's command interface and can disable or manipulate its functionality. They can also attack potential vulnerabilities of the avp.exe process running with elevated privileges.

</details>

---
*Analysed by Claude on 2026-05-24*
