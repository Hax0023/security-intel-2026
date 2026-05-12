# XSS in Steam React Chat Client via javascript: URI in BBCode [url] Tag

## Metadata
- **Source:** HackerOne
- **Report:** 409850 | https://hackerone.com/reports/409850
- **Submitted:** 2018-09-14
- **Reporter:** zemnmez
- **Program:** Steam (Valve)
- **Bounty:** Not specified in provided content
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, URI Scheme Injection
- **CVEs:** None
- **Category:** web-api

## Summary
The Steam chat client supports BBCode formatting including [url] tags that can be abused to inject javascript: URIs, bypassing React's XSS mitigations. An attacker can craft malicious chat messages containing javascript: protocols that execute arbitrary code in the context of the Steam client, potentially leading to remote code execution if the client uses Electron or similar webview technologies.

## Attack scenario
1. Attacker identifies that Steam chat supports [url] BBCode tags that render as clickable links
2. Attacker crafts a malicious chat message containing [url=javascript:alert('xss')]click me[/url]
3. Message is transmitted to victim through Steam's chat interface
4. Victim receives the message which renders as a clickable link in the React chat client
5. Victim clicks the link or link is auto-triggered by JavaScript
6. javascript: URI executes in the context of the Steam client, potentially accessing Electron APIs or system functions

## Root cause
React's built-in XSS protection sanitizes HTML tags and event handlers but does not filter dangerous URI schemes like javascript:. The Steam chat application converts BBCode [url] tags directly to HTML anchor elements without validating or sanitizing the href attribute for dangerous protocols.

## Attacker mindset
An attacker would recognize that modern frameworks have shifted XSS protection focus to HTML attributes/events while overlooking URI scheme validation. By leveraging a supported feature (URL BBCode tags) combined with a dangerous URI scheme, they can bypass framework-level protections. Knowledge that Steam uses Electron-based clients exposes potential for escalation to RCE through exposed system APIs.

## Defensive takeaways
- Implement strict URI scheme whitelisting (http, https only) before rendering href attributes
- Do not rely solely on framework-level XSS protection; apply defense-in-depth at the application layer
- Sanitize or validate all user-controlled data used in HTML attributes, especially href, src, and event handlers
- Treat data coming from untrusted sources (chat messages) as potentially malicious regardless of framework assumptions
- Use Content Security Policy (CSP) headers to restrict script execution and prevent javascript: URI evaluation
- Implement message validation on both client and server side for BBCode parsing
- Minimize Electron/webview API exposure to chat rendering contexts using context isolation

## Variant hunting
Test other BBCode tags for similar URI injection (img src=javascript:, embed src, etc.)
Examine if other protocol schemes are blocked (data:, vbscript:, file:)
Check if event handler attributes are properly stripped from BBCode (onclick, onerror, etc.)
Test nested or encoded BBCode tags to bypass sanitization regex
Investigate if SVG-based XSS vectors work through BBCode image tags
Check if server-side message sanitization can be bypassed through binary WebSocket protocol manipulation

## MITRE ATT&CK
- T1190
- T1203
- T1566

## Notes
The vulnerability is particularly dangerous due to Steam's Electron-based architecture which exposes privileged APIs to the webview context. The attacker demonstrated persistent XSS via video proof-of-concept. The binary WebSocket protocol and client-side sanitization added complexity but did not prevent the attack. Distinction between client transmission sanitization and server reception validation is critical - attackers may manipulate the binary protocol directly.

## Full report
<details><summary>Expand</summary>

The Steam chat client both sends and receives bbcode format chat messages. These map to HTML elements, and notably the [url] bbcode tag is supported for arbitrary URLs. React has strong XSS mitigations but does not mitigate `javascript:` URI based XSS.

This is rather difficult to exploit as the client transmits sanitised messages and receives over a binary WebSocket. I've attached a video of executing this XSS, which is persistent.

## Impact

I strongly believe an attacker could get remote code execution in Steam via this method. The Steam chat client uses the same codebase as the steam web chat client, and, I imagine does so using electron or some other webview system. These systems all expose functions which allow arbitrary calls to system to allow them to be competitive with e.g. windows forms.

</details>

---
*Analysed by Claude on 2026-05-12*
