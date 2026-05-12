# XSS via /api/v1/chat.postMessage Attachment Fields

## Metadata
- **Source:** HackerOne
- **Report:** 219957 | https://hackerone.com/reports/219957
- **Submitted:** 2017-04-10
- **Reporter:** gronke
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can inject arbitrary HTML/JavaScript code via the chat.postMessage REST API by crafting malicious attachment field values. When a message with an image_url attachment is viewed, the unencoded field content executes in the victim's browser context, allowing arbitrary code execution.

## Attack scenario
1. Attacker obtains valid API credentials through phishing, credential stuffing, or other means
2. Attacker identifies a target channel or private conversation room ID
3. Attacker crafts a POST request to /api/v1/chat.postMessage with a malicious attachment containing an img tag with onload event handler in the field value
4. Attacker sends the crafted message to the target room
5. Victim views the message in their Rocket.Chat client (desktop or browser)
6. The unencoded HTML in the attachment field renders and executes the onload JavaScript payload in victim's browser

## Root cause
The chat.postMessage API endpoint fails to properly encode/sanitize user-supplied content in attachment field values before storing or rendering them. The application renders these fields as HTML without escaping special characters, allowing script injection.

## Attacker mindset
An authenticated attacker with API access seeks to compromise other users in the chat system. By exploiting the attachment field rendering mechanism, they can execute arbitrary code in victims' browsers to steal sessions, credentials, or perform actions on their behalf without detection.

## Defensive takeaways
- Implement strict output encoding - HTML-encode all user-controlled data before rendering in any context
- Apply Content Security Policy (CSP) headers to restrict script execution sources
- Use templating engines with auto-escaping enabled by default
- Implement input validation to reject or sanitize potentially dangerous HTML tags
- Validate attachment structure and field content server-side before storage
- Use DOM APIs safely - prefer textContent over innerHTML for user data
- Apply defense-in-depth: validate on server, encode on server, encode again on client rendering
- Regular security testing including both automated XSS scanning and manual testing of all API endpoints

## Variant hunting
Similar vulnerabilities likely exist in other message/content endpoints: /api/v1/chat.sendMessage, attachment rendering in different message types (files, videos), user profile fields, channel descriptions, custom fields. Test all parameters that accept user input and are later displayed. Check for DOM-based XSS in client-side rendering of attachment data. Examine how other attachment types (video, audio, file) handle metadata fields.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
The vulnerability requires valid API authentication, reducing immediate blast radius but not severity given API key exposure risks. The PoC uses image_url to force rendering context, but similar injection may work in other attachment properties. Rocket.Chat is widely deployed in enterprise environments, making this a high-impact issue. The fix is straightforward (HTML entity encoding) but indicates systemic input handling issues that should trigger broader security review.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to verify and then potentially issue a bounty, so be sure to take your time filling out the report!

**Summary:** An attacker can craft a custom message using the REST API that, once seen by the observer, executes arbitrary code in the context of the client user.

**Description:** According to the API documentation chat messages can have attachments. These attachments then can have fields which contain a title and subtitle for the attachment. When the attachment has an `image_url` assigned, the first field's value can be used to inject HTML tags. For example <img onload=""> can be used to execute arbitrary code. `<` must be the leading character of the field's value property.

## Releases Affected:

  * Client App (OSX)
  * Firefox 48 (Debian)
  * Firefox 52 (OSX)
  * Chrome 58 (OSX)

## Steps To Reproduce (from initial installation to vulnerability):

  1. Create a Channel or get obtain a RoomId of a private conversation
  2. Login to the Rest API
  3. Send crafted message

## Supporting Material/References:

```bash
# Login to get Auth Token and User Id
curl http://127.0.0.1:3000/api/v1/login -d "username=<USER_NAME>&password=<PASSWORD>"

# Send crafted message
curl -H "X-Auth-Token: <USER_TOKEN>" -H "X-User-Id: <USER_ID>" http://127.0.0.1:3000/api/v1/chat.postMessage -d "channel=<CHANNEL_NAME>&attachments[0][image_url]=/assets/logo&attachments[0][fields][0][title]=&attachments[0][fields][0][value]=<img src=/assets/logo width=1 height=1 onload=alert('XSS4') />You're Pwned!"
```

## Suggested mitigation

  * Encode all user inputs to HTML entities


</details>

---
*Analysed by Claude on 2026-05-12*
