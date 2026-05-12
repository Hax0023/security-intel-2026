# CSS Injection in Message Avatar

## Metadata
- **Source:** HackerOne
- **Report:** 1031613 | https://hackerone.com/reports/1031613
- **Submitted:** 2020-11-11
- **Reporter:** gronke
- **Program:** Rocket.Chat
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** CSS Injection, DOM-based XSS, UI Redressing, Phishing
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Meteor.method `sendMessage` allows custom avatars containing inline CSS that can be injected to manipulate HTML element rendering. Attackers can inject CSS rules via the avatar parameter that overlay UI elements and create fake login/2FA dialogs to phish for user credentials. The vulnerability exploits inadequate input validation and CSS sanitization.

## Attack scenario
1. Attacker authenticates to Rocket.Chat and identifies target room or DM ID
2. Attacker crafts malicious Meteor.call with avatar parameter containing CSS injection payload (e.g., 'none);position:fixed;top:0;...')
3. Attacker sends message with CSS that creates fixed-position overlay matching 2FA or login dialog appearance
4. Victim views the message in chat and sees what appears to be a legitimate 2FA challenge dialog
5. Victim enters their 2FA token or credentials into the overlaid fake form
6. Attacker captures credentials through the chat message or by monitoring user behavior

## Root cause
The avatar parameter is concatenated directly into inline CSS without proper sanitization. Input validation only blocks certain characters (whitespace) but fails to prevent CSS injection syntax like semicolons and CSS property values. The application constructs CSS inline styles from user-controlled input without escaping or validation of CSS syntax.

## Attacker mindset
An attacker would recognize that avatar parameters accept string values that get rendered as CSS properties. By understanding CSS parsing, they could break out of intended property values using semicolons to inject arbitrary CSS rules. The attacker would leverage CSS capabilities (position, z-index, background-image) to create convincing UI overlays that trick users into revealing sensitive information through social engineering combined with technical manipulation.

## Defensive takeaways
- Implement strict allowlist validation for avatar URLs - only permit URLs from trusted domains or base64-encoded data URIs with validation
- Use Content Security Policy (CSP) to restrict inline styles and prevent style injection attacks
- Escape and validate all user input before inserting into style attributes; use parameterized style setters instead of string concatenation
- Implement HTML/CSS sanitization libraries (DOMPurify, sanitize-html) for any user-controlled content affecting styling
- Apply style attribute allowlist - only permit safe, pre-defined CSS properties and values
- Use CSS-in-JS solutions with type safety or CSS modules to prevent dynamic style injection
- Add input length limits and character restrictions more comprehensively (not just whitespace)
- Implement security headers like X-Content-Type-Options, X-Frame-Options to mitigate secondary attack surfaces
- Conduct security review of all Meteor.methods that accept user input affecting DOM rendering

## Variant hunting
Look for similar injection points in: user profile settings (background images, custom themes), room/channel descriptions with styling, user status messages, custom emoji data, notification templates, and any other Meteor.methods accepting user input that gets rendered as HTML or CSS. Check for similar issues in aliasing, username, or room name fields that might support styling.

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1059

## Notes
The report demonstrates practical impact through 2FA phishing scenario. The vulnerability requires authentication but can target any user in shared channels. The 'none);' bypass technique indicates incomplete blacklist validation. While the bounty amount is not specified in the provided content, this would typically be medium severity (not critical due to auth requirement, not low due to practical phishing impact). The develop branch status suggests this may have been pre-release or not yet deployed to production.

## Full report
<details><summary>Expand</summary>

## Summary

Custom message avatars can contain inline CSS that influences the resulting HTML element rendering.

## Description

The Meteor.method `sendMessage` allows setting custom avatars. When escaping the input with `none);` further CSS is applied to the elements inline styles. The injected CSS may not contain certain characters, including whitespace.

```
Meteor.call("sendMessage", {
    rid: "<ROOM OR DM ID>",
    avatar: "none);position:fixed;top:0;right:0;bottom:0;left:0;z-index:999;background-color:black;opacity:0.5;pointer-events:none;",
    msg: "Enjoy the Dark Theme!",
    alias: "hacker"
});
```

When the background image is a screenshot of the 2FA message dialog, users could be confused to enter their 2FA token to the chat message field and accidentallty sent it into the currently open channel. A more sophisticated attack would use a second CSS injection overlaying the text input. Although only one CSS element at a time can be influenced, the combination many can lead to the UI being in attacker control.

## Releases Affected:

  * develop

## Steps To Reproduce (from initial installation to vulnerability):

  1. Login to Rocket.Chat
  2. Figure out channel or direct message ID
  3. Open Web Inspector
  4. Send malicious message with Meteor.call `sendMessage`

## Suggested mitigation

  * Verify avatar URLs
  * Sanitize user input

## Impact

Attackers can overlay UI elements and phish for users credentials that are accidentally entered in chat messages.

</details>

---
*Analysed by Claude on 2026-05-12*
