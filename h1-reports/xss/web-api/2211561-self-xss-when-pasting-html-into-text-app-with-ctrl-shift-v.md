# Self XSS via Ctrl+Shift+V Plaintext Paste in Nextcloud Text App

## Metadata
- **Source:** HackerOne
- **Report:** 2211561 | https://hackerone.com/reports/2211561
- **Submitted:** 2023-10-16
- **Reporter:** max_nextcloud
- **Program:** Nextcloud
- **Bounty:** Unknown
- **Severity:** medium
- **Vuln:** Cross-Site Scripting (XSS), DOM-based XSS, Improper Input Handling
- **CVEs:** CVE-2023-48302
- **Category:** web-api

## Summary
The Nextcloud Text application's Ctrl+Shift+V plaintext paste function bypasses HTML sanitization by directly inserting user-controlled content into DOM element innerHtml. An attacker can craft malicious HTML content and socially engineer users into pasting it via Ctrl+Shift+V, resulting in arbitrary HTML/JavaScript execution in the application context.

## Attack scenario
1. Attacker identifies that Ctrl+Shift+V is intended for plaintext paste but doesn't properly sanitize HTML
2. Attacker crafts malicious HTML payload containing JavaScript (e.g., '<img src=x onerror=alert(1)>')
3. Attacker tricks a target user into copying the payload to clipboard
4. Target user pastes content into a markdown file using Ctrl+Shift+V within the Text app
5. Payload is inserted directly into a DOM element's innerHtml without sanitization
6. JavaScript executes in the user's browser within the Nextcloud application context, potentially stealing session tokens or performing actions as the user

## Root cause
The Markdown.js extension handles Ctrl+Shift+V paste by directly writing unsanitized clipboard content to a DOM element's innerHtml property rather than treating it as plaintext. The paste handler fails to sanitize HTML entities or escape the content before DOM insertion.

## Attacker mindset
An attacker recognizes that special keyboard shortcuts often bypass standard input validation. By exploiting user expectations that 'plaintext paste' is safe, the attacker can deliver XSS payloads through social engineering without visible indicators of malicious content.

## Defensive takeaways
- Always sanitize or escape user input before inserting into DOM, regardless of input method (paste, type, etc.)
- Use textContent instead of innerHtml when dealing with user-controlled text content
- Implement HTML entity encoding for all paste operations, even 'plaintext' ones
- Validate that plaintext paste functions only handle text by using appropriate DOM APIs (createTextNode, textContent)
- Apply Content Security Policy (CSP) headers to limit XSS impact even if sanitization fails
- Security test special input methods (Ctrl+Shift+V, drag-drop, etc.) with known XSS payloads

## Variant hunting
Check other paste handlers (Ctrl+V, right-click paste, drag-and-drop) for similar issues
Audit other editor extensions in Nextcloud for innerHtml usage with user input
Test if the vulnerability persists in different markdown editors or note-taking features
Investigate whether other keyboard shortcuts bypass sanitization functions
Check if file import features parse HTML without sanitization
Review clipboard handling in other Nextcloud apps (Deck, Notes, etc.)

## MITRE ATT&CK
- T1190
- T1566
- T1566.002

## Notes
This is a Self-XSS vulnerability requiring social engineering (convincing user to paste attacker-controlled content). Impact is limited to self-compromise unless combined with CSRF or stored XSS vectors. The vulnerability exists in plaintext paste feature - a feature specifically designed to avoid HTML interpretation - making this a logic flaw in security assumptions.

## Full report
<details><summary>Expand</summary>

## Summary:
ctrl-shift-v is meant to paste plaintext as is. However it will paste it into a dom elements `innerHtml` and can thus be used to inject malicious html.

## Steps To Reproduce:

  1. copy "<h1>html</h1>"
  1. use ctrl-shift-v to paste it into a .md file
  1. See the heading getting added.

## Supporting Material/References:
https://github.com/nextcloud/text/blob/main/src/extensions/Markdown.js#L97

  * [attachment / reference]

## Impact

If you can trick someone into using ctrl-shift-v to paste content you control you can insert html into the page leading to a possible xss attack.

The html will be inserted into the editors schema - but before that happens it's already pasted into the innerHtml of a dom element.

</details>

---
*Analysed by Claude on 2026-05-12*
