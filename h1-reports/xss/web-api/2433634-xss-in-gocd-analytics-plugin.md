# Stored/Reflected XSS in GOCD Analytics Plugin via msg Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2433634 | https://hackerone.com/reports/2433634
- **Submitted:** 2024-03-25
- **Reporter:** aviv_keller
- **Program:** GOCD Analytics Plugin
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Improper Input Validation, Unsafe DOM Manipulation
- **CVEs:** None
- **Category:** web-api

## Summary
The GOCD Analytics Plugin's info-message.js is vulnerable to reflected XSS through the unvalidated `msg` URL parameter. User-supplied input is decoded and directly injected into the DOM via jQuery's `.html()` method without sanitization. An attacker can craft malicious URLs to execute arbitrary JavaScript in the context of victims' browsers.

## Attack scenario
1. Attacker crafts a malicious URL: `https://gocd-server/plugin?msg=%3Csvg%2Fonload%3Dalert%28%22XSS%22%29%20%3E`
2. Attacker sends the URL to a GOCD user via phishing email, chat, or social engineering
3. Victim clicks the link while authenticated to the GOCD server
4. The malicious payload is decoded to `<svg/onload=alert("XSS") >` and passed to `Utils.infoMessage()`
5. The payload is wrapped in a `</p>` tag and injected directly into the DOM via `.html()`
6. Browser parses the SVG element and executes the `onload` handler, running arbitrary JavaScript in the victim's session context

## Root cause
The application directly uses user-controlled input from the URL query parameter without any sanitization or validation before inserting it into the DOM. The use of jQuery's `.html()` method treats the input as HTML rather than plain text, allowing embedded scripts and event handlers to execute.

## Attacker mindset
An attacker recognizes that the `msg` parameter is reflected directly into the page without sanitization. They understand that URL decoding converts encoded payloads back to executable HTML/JavaScript. By leveraging DOM-based injection through `.html()`, they can bypass basic filters and execute arbitrary code in authenticated user sessions, potentially stealing credentials, session tokens, or performing admin actions.

## Defensive takeaways
- Use `.text()` instead of `.html()` when displaying user-supplied content as plain text
- Implement input validation: whitelist allowed characters and reject anything containing HTML/script indicators
- Apply output encoding: encode special characters (`<`, `>`, `&`, `"`, `'`) before rendering
- Use Content Security Policy (CSP) headers to restrict inline script execution
- Sanitize user input with established libraries (DOMPurify, xss.js) if HTML formatting is required
- Avoid using `decodeURIComponent()` directly on user input without subsequent validation
- Implement security code reviews focusing on DOM manipulation patterns
- Use template engines with auto-escaping enabled

## Variant hunting
Search for other instances of `.html()` receiving unvalidated user input in the GOCD codebase
Check for other URL parameters passed through `window.location.search` without sanitization
Look for similar patterns in other GOCD plugins that accept user input
Test other URL-based parameter injection points (hash, pathname, query strings)
Check if `Utils.infoMessage()` is used elsewhere with untrusted data
Review any localStorage/sessionStorage operations that might accept user input
Search for other uses of `decodeURIComponent()` followed by DOM insertion

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1566 - Phishing
- T1204 - User Execution

## Notes
This is a classic reflected XSS vulnerability in a server-side application plugin. The attack vector is particularly dangerous because it targets authenticated users and can be delivered via phishing. The simplicity of the vulnerability suggests inadequate security testing of user input handling. The report demonstrates proper exploitation with both URL-encoded and decoded payload examples.

## Full report
<details><summary>Expand</summary>

[gocd/gocd-analytics-plugin (info-message.js#L28)](https://github.com/gocd/gocd-analytics-plugin/blob/c9b5f776539b3eb68dc3177c87b99b40319f8b22/assets/js/pages/info-message.js#L28) is vulnerable to XSS via the `?msg=` parameter. 
By supplying an attack payload such as `?msg=%3Csvg%2Fonload%3Dalert%28%22XSS%22%29%20%3E`, `<svg/onload=alert("XSS") >` will be injected into the webpage.

```js
$(document).ready(function () {
  const msg = window.location.search.match(/[&?]msg=([^&]+)/);
  const msgText = msg ? decodeURIComponent(msg[1]) : "No data collected for this metric, cannot generate analytics.";

  $(document.body).html(Utils.infoMessage(msgText));
});
```
> `Utils.infoMessage` basically just wraps `msgText` in a `</p>`

## Impact

An attacker can run malicious code on servers running this plugin, comprising the integrity and confidentiality of such servers.

</details>

---
*Analysed by Claude on 2026-05-12*
