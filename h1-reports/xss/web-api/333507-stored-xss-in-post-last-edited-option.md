# Stored XSS in Post Last Edited Option

## Metadata
- **Source:** HackerOne
- **Report:** 333507 | https://hackerone.com/reports/333507
- **Submitted:** 2018-04-04
- **Reporter:** luigigubello
- **Program:** Discourse
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored, Input Validation Failure, Output Encoding Failure
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Discourse's post edit history feature, where malicious JavaScript injected during post creation or editing is executed when users view the edit history via the pencil icon. The vulnerability affects both private messages and public topics, allowing attackers to compromise multiple victims simultaneously through a single malicious post.

## Attack scenario
1. Attacker initiates a private message conversation with a victim user
2. Attacker sends a message containing malicious XSS payload (e.g., <script> tags or event handlers)
3. Attacker edits or deletes the message to trigger the edit history feature
4. Victim receives notification and sees the yellow pencil icon indicating the message was edited
5. Victim clicks the pencil icon to view edit history, triggering execution of stored XSS payload
6. Malicious script executes in victim's browser context, stealing cookies, session tokens, or performing unauthorized actions

## Root cause
The application fails to properly sanitize and encode user-supplied content when storing and rendering post edit history. The edit history feature does not sanitize HTML/JavaScript before storage or apply proper output encoding when displaying the edited content to users.

## Attacker mindset
An attacker would recognize that edit history is a commonly-viewed feature with high user interaction, making it an effective vector for widespread XSS exploitation. The ability to affect multiple users through a single post in public topics provides significant reach with minimal effort.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-generated content at the point of entry
- Apply context-appropriate output encoding (HTML entity encoding) when rendering post content and edit history
- Use a whitelist-based HTML sanitization library to strip potentially dangerous tags and attributes
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize content both at storage time and render time as defense in depth
- Apply the same security controls to edit history as to initial post content
- Conduct security review of all user-facing content rendering paths, especially historical/metadata features
- Implement automated security testing for XSS vulnerabilities in all content display features

## Variant hunting
Test other history/metadata features (post revisions, user activity logs, edit timestamps) for similar XSS vulnerabilities
Check comment replies and nested discussions for XSS in edit history
Test direct messages, group messages, and forum posts separately as they may have different sanitization logic
Examine other user-editable fields (titles, descriptions, profiles) for stored XSS via edit history
Test attribute-based XSS vectors (onerror, onload, onclick) in edit history rendering
Check for DOM-based XSS in client-side edit history visualization

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
The vulnerability was verified on Discourse's public instance (try.discourse.org). The widespread impact across multiple users viewing the same edited post makes this particularly dangerous. The pencil icon interaction pattern suggests this feature is widely used, increasing exploitation likelihood.

## Full report
<details><summary>Expand</summary>

1. There are two users: **Attacker** and **Victim**.
2. **Attacker** starts a private talk via private message with the **Victim**.
3. **Attacker** send a message to **Victim**, then he edits it or deletes it.
4. **Victim** sees the *yellow pencil*, symbol of the edit.
5. **Victim** clicks on *yellow pencil* to see the edit and the XSS runs.

Other info: the XSS also runs on topic (video PoC #2). You can find my XSS message on this URL:
https://try.discourse.org/t/recommended-reading-for-community-and-foss-enthusiasts/278
It is very dangerous because it can hit many users at the same time.

## Impact

XSS can use to steal cookies, password or to run arbitrary code on victim's browser

The hacker selected the **Cross-site Scripting (XSS) - Stored** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
https://try.discourse.org/t/recommended-reading-for-community-and-foss-enthusiasts/278

**Verified**
Yes



</details>

---
*Analysed by Claude on 2026-05-12*
