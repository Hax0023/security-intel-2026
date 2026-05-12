# Post-Auth Stored XSS with User Interaction leads to Remote Code Execution in Rocket.Chat

## Metadata
- **Source:** HackerOne
- **Report:** 1132202 | https://hackerone.com/reports/1132202
- **Submitted:** 2021-03-22
- **Reporter:** sonarsource
- **Program:** Rocket.Chat (HackerOne)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Unsafe Library Usage, Privilege Escalation, Remote Code Execution
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Rocket.Chat's handling of room names due to unsafe usage of the toastr notification library combined with input validation bypass in the createRoom function. When an admin interacts with a malicious room name, the XSS payload executes with admin privileges, allowing attackers to create webhooks with arbitrary scripts and achieve Remote Code Execution on the server.

## Attack scenario
1. Attacker creates a normal user account and authenticates to Rocket.Chat instance
2. Attacker exploits validation bypass in createRoom function's extraData parameter to override room properties with XSS payload in room name (e.g., '<img src onerror=alert(origin)>')
3. Attacker invites an administrator to the maliciously created channel
4. Administrator logs in and attempts to edit the channel title/settings through the UI
5. API endpoint rooms.saveRoomSettings calls getValidRoomName which reflects the malicious room name back in error message
6. Frontend handleError function passes unsanitized error message to toastr library, executing XSS payload in admin's browser context; attacker then uses admin session to create incoming webhook with malicious script for RCE

## Root cause
Multiple security failures: (1) extraData parameter in createRoom function lacks proper validation and allows property overrides, (2) toastr library is used without escapeHtml option enabled, (3) handleError function fails to sanitize message and title properties before passing to toastr, (4) getValidRoomName reflects user input in error responses, (5) absence of Content-Security-Policy prevents XSS execution mitigation

## Attacker mindset
Opportunistic privilege escalation through low-effort chaining of multiple vulnerabilities. Attacker recognizes that XSS in admin context provides pathway to RCE via webhook mechanism, making this a high-value attack chain. The requirement for admin interaction is seen as acceptable friction given the critical endpoint result (RCE).

## Defensive takeaways
- Implement strict whitelist validation for all user-controllable parameters, especially those that override existing properties (extraData)
- Always enable HTML escaping in third-party notification/UI libraries or perform manual sanitization before use
- Sanitize all data returned from APIs before rendering in DOM, regardless of source
- Implement nonce-based Content-Security-Policy headers to prevent inline script execution even if XSS bypasses occur
- Audit all API endpoints that reflect user input and ensure validation/sanitization is applied consistently
- Restrict scripting capabilities in webhooks or isolate them with sandboxing mechanisms
- Require explicit re-authentication for sensitive operations like channel editing in admin accounts
- Implement input validation at both client and server layers
- Use security headers (CSP, X-XSS-Protection) as defense-in-depth measure

## Variant hunting
Search for other endpoints that reflect user input in API responses (similar to getValidRoomName). Investigate other uses of toastr library throughout codebase for missing escapeHtml options. Check for other parameters passed to utility functions without validation (similar to extraData abuse). Review webhook implementation for other RCE vectors. Examine error handling paths for sensitive operations. Test file upload functionality mentioned in CSP notes for alternative XSS vectors.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1133
- T1078
- T1199
- T1059

## Notes
Vulnerability requires post-authentication access but attacker doesn't need admin privileges initially, only ability to create rooms and invite admins. Writeup author notes ambiguity between stored vs reflected XSS classification (payload stored in DB but reflected by API then unsafely rendered). Version 3.12.1 confirmed vulnerable but author notes difficulty in determining exact affected versions due to codebase complexity. The progression from post-auth XSS to RCE demonstrates critical importance of treating admin session compromise as equivalent to server compromise in chat applications. Webhook script execution without security boundary appears intentional design flaw.

## Full report
<details><summary>Expand</summary>

**Summary:**
Unsafe usage of the `toastr` library leads to Stored XSS when combined with a validation bypass in the `createRoom` function. Targeting an admin account leads to Remote Code Execution.

**Description:**
The frontend uses the `toastr` library to display error messages to the user. However, it is used in an unsafe way which allows XSS when user input is reflected in an API error message. This happens for example when channel info is edited and the channel's name contains invalid characters.

To abuse this, an attacker can use a validation bypass in [the `createRoom` function](https://github.com/RocketChat/Rocket.Chat/blob/9bbf11ad53d43dc3a5d870d6df4a3022b6de3440/app/lib/server/functions/createRoom.js#L62): the `extraData` parameter is merged with the room object without proper validation, which allows an attacker to override all previous properties such as the name or the owner. The attacker can use this to create a room that contains their XSS payload in the room's name.

Triggering the XSS requires multiple steps of user interaction, because there are few API endpoints that reflect user input back. One of them is [the `rooms.saveRoomSettings` endpoint](https://github.com/RocketChat/Rocket.Chat/blob/9bbf11ad53d43dc3a5d870d6df4a3022b6de3440/app/api/server/v1/rooms.js#L340-L348) which calls [the `saveRoomSettings` method](https://github.com/RocketChat/Rocket.Chat/blob/9bbf11ad53d43dc3a5d870d6df4a3022b6de3440/app/channel-settings/server/methods/saveRoomSettings.js#L223-L322) which in turn uses [the `getValidRoomName` function](https://github.com/RocketChat/Rocket.Chat/blob/9bbf11ad53d43dc3a5d870d6df4a3022b6de3440/app/utils/lib/getValidRoomName.js#L7-L62). This function checks the room's name and reflects the user-provided value back if it is not a valid name.

The error returned by the API is unsafely handled by passing it to the `toastr` library without escaping it or using the library's `escapeHtml` option. [The `handleError` function](https://github.com/RocketChat/Rocket.Chat/blob/9bbf11ad53d43dc3a5d870d6df4a3022b6de3440/app/utils/client/lib/handleError.js#L7-L33) passes the value to the `toastr` library, it escapes the `details` property but not the `message` and `title` property.

To gain Remote Code Execution capabilities on the server, an attacker can follow these steps to take over an admin account. The attacker can then use the newly gained admin privileges to create an incoming web hook that has a script. This allows them to execute commands or get a shell on the server, because the script is executed on the server without a security boundary in place (which seems to be intended).

**Note:** This issue is classified as Stored XSS because the payload is stored permanently in the database, but it could be argued that it is Reflected XSS because the payload is reflected by the API which then leads to the unsafe handling and execution of the payload.

## Releases Affected:
We tested on 3.12.1, but it is hard to confirm since when Rocket.Chat is vulnerable because there are many parts of the code base involved.

## Steps To Reproduce (from initial installation to vulnerability):
1. Set up an instance of RocketChat 3.12.1, e.g. by cloning the repo and using Docker Compose:
  1. `git clone git@github.com:RocketChat/Rocket.Chat.git`
  1. `cd Rocket.Chat`
  1. `git checkout tags/3.12.1`
  1. `docker-compose up -d`
1. Configure the instance with default settings
1. Create a normal (non-admin) user with username `attacker` and password `attacker`
1. Log in as the `attacker` user
1. Open the browser's developer tools and execute the following line of code: `Meteor.call('createChannel', 'valid-name', [], false, {}, { name: 'edit me <img src onerror=alert(origin)>' })`
1. Invite the admin to the newly created channel
1. Log out and log in as an admin
1. Edit the title of the newly created channel (e.g. change `me` to `you`)
1. Click the save button
1. A dialog should pop up that shows the site's origin (e.g. http://localhost:3000), confirming that the XSS payload has been executed (this is only for the demo, the payload can be arbitrary JavaScript code)
1. (The demo ends here but it is trivial to get RCE capabilities when having access to an admin account, as explained before)

## Supporting Material/References:
The attached video shows the exploitation of the vulnerability with the attacker's view on the right and the victim's view (admin) on the left.

## Suggested mitigation
- Restrict and validate the `extraData` parameter when creating a room
- Use the `toastr` library with the `escapeHtml` option or sanitize the message and title manually
- Set a [`Content-Security-Policy` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) that prevents payload execution
  - preventing inline scripts might not be enough here because users can upload files
  - a [nonce-based CSP](https://content-security-policy.com/nonce/) would fit best

## Disclosure Policy
All reported issues are subject to a 90 day disclosure deadline.
After 90 days elapse, parts of the bug report will become visible to the public.

Don't hesitate to ask if you have any questions or need further help with this issue.

## Impact

An attacker can use this vulnerability to target an admin user and take over their account, which is already a high impact. The attacker can then use certain features that are available to admins in order to gain Remote Code Execution capabilities.

This gives them complete control over the Rocket.Chat instance and exposes all attached components, e.g. the database or any external system whose credentials are stored within Rocket.Chat settings. An attacker can read, change, or delete all items in the database, impacting confidentiality, integrity, and availability.

</details>

---
*Analysed by Claude on 2026-05-12*
