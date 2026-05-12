# Cross-site scripting on algorithm collaborator via unencoded WebSocket messages

## Metadata
- **Source:** HackerOne
- **Report:** 615672 | https://hackerone.com/reports/615672
- **Submitted:** 2019-06-15
- **Reporter:** irisrumtub
- **Program:** Undisclosed (Algorithm/Debugger Platform)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can execute arbitrary JavaScript in a collaborator's browser by intercepting and modifying WebSocket messages sent during algorithm collaboration sessions. The vulnerability exists because the application fails to properly encode HTML entities in WebSocket payloads before rendering them to other users.

## Attack scenario
1. Attacker and victim establish a collaboration session in the algorithm debugger/collaborator tool
2. Attacker intercepts WebSocket traffic between their client and the server using a proxy tool
3. Attacker modifies a debugger input update message, replacing the encoded value with raw HTML/JavaScript payload (e.g., <img src=x onerror=alert(1)>)
4. Attacker sends the modified WebSocket message with the unencoded payload
5. Server reflects or broadcasts the unencoded payload to the victim's collaborator session
6. Victim's browser renders the payload as HTML/JavaScript, executing the attacker's code in their session context

## Root cause
The application encodes payloads at the HTTP level (likely due to Cloudflare restrictions) but fails to enforce the same encoding on WebSocket messages. WebSocket message values are transmitted and rendered without proper HTML entity encoding, allowing injection of arbitrary HTML and JavaScript that executes in recipients' browsers.

## Attacker mindset
An experienced security researcher systematically probing multiple attack vectors (HTTP requests, HTML injection, WebSocket interception). Noticed pattern of requests to specific endpoints when submitting payloads, then pivoted to examine WebSocket-layer encoding gaps after HTTP-level protections blocked inline scripts. Recognized that debugger behavior (payload stripping) indicated server-side processing and tested lower-layer protocol for bypass.

## Defensive takeaways
- Apply consistent output encoding across all data transmission channels (HTTP, WebSocket, APIs)
- Implement server-side HTML entity encoding for all user-controllable content before broadcasting to other users
- Do not rely solely on transport-layer protections (Cloudflare WAF); enforce encoding at application layer
- Audit third-party libraries (TogetherJS mentioned) for security implications when handling collaborative features
- Use Content Security Policy (CSP) headers to mitigate XSS impact even if encoding fails
- Validate and sanitize all data received via WebSocket, not just HTTP endpoints
- Test security controls across all communication protocols, not just primary request paths

## Variant hunting
Look for similar XSS vulnerabilities in other real-time collaboration features (shared editors, debugging tools, live chat). Test WebSocket endpoints for proper encoding of: user inputs, code snippets, comments, and any content synchronized between multiple clients. Check for discrepancies between HTTP and WebSocket payload handling.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059.007 - Command and Scripting Interpreter: JavaScript
- T1566.002 - Phishing: Spearphishing Link (if used to deliver payload)
- T1185 - Traffic Signaling

## Notes
Researcher demonstrated good methodological approach: noticed patterns across multiple tests, pivoted investigation to lower-layer protocols when HTTP defenses blocked payloads, and identified the TogetherJS library as potential source. The researcher provided test accounts and noted willingness to assist with fix validation. This is a classic case of security controls being implemented at one layer without comprehensive coverage of all input/output channels.

## Full report
<details><summary>Expand</summary>

Hi again my favorite VDP team. I bring you 8th bug and 4th cross-site scripting. Currently trying to upload python code via self-serve data, not looking for XSS'es only, but they're a thing still, right?

**Summary:**
By sending specially crafted websockets request attacker can run javascript in algorithm collaborator's web browser

**Description:**
This is actually quite a funny bug. Some time ago when I was testing algo debugger, i noticed that there is a request to */algorithms/algoid/x* which usually happens when i try to insert html's <img src=x>. But since some time your cloudflare became more strict and adding inline scripts in request might result in 403 Forbidden, so i remove them and try without them. But at that time i couldn't find the image that caused that request. I sent that to Chris.
Today i was trying to test against debugger again. The purpose wasn't to find XSS, but i spammed XSS payloads alongside with some different stuff. And again that request to page *X*. And i noticed that debugger removed part of my payload which contained image. That's it! That should be the vulnerable place. 
However typing html entity in it didn't produce anything. And html was injected only on my side, not the other collaborator's. So i decided to take a look at the websocket request that sends it
It turned out that HTML's <> and other entities were encoded. So i tried intercepting the websockets request and enter <img src=x onerror=alert(1)> and it worked not only on me, but on collaborator as well.
So is it TogetherJS library that is in charge of websockets? I think you might need to encode payloads server-side to avoid this kind of things. I would be glad to help you test the fix for this.


## Steps To Reproduce:


  1. Intercept websockets message like this (debugger input update)
{F509648}
  2. Replace value with raw html/javascript
  3. Send the message. Payload will work in collaborator's browser


## Test account information

irisrumtub+hackerone@mail.ru
tvburis+hackerone@gmail.com

## Impact

Run javascript in victim's browser

</details>

---
*Analysed by Claude on 2026-05-12*
