# Stored XSS in User Profile Signature Field

## Metadata
- **Source:** HackerOne
- **Report:** 1084183 | https://hackerone.com/reports/1084183
- **Submitted:** 2021-01-22
- **Reporter:** darkdream
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the user profile signature field on forum.acronis.com that allows authenticated attackers to inject malicious JavaScript code. When other users view the attacker's profile, the injected script executes in their browser context, enabling session hijacking, credential theft, or further exploitation.

## Attack scenario
1. Attacker creates an account on forum.acronis.com and logs in
2. Attacker navigates to their profile edit page and locates the Signature field
3. Attacker injects malicious JavaScript payload such as <xss onmouseover="alert(1)">test</xss> or more sophisticated payloads
4. Attacker shares their profile URL via email, forum posts, or direct messages to potential victims
5. When victims visit the attacker's profile page, the JavaScript executes in their browser with their privileges
6. Attacker can steal session cookies, capture keystrokes, redirect to phishing pages, or perform actions on behalf of victims

## Root cause
The application fails to properly sanitize and validate user input in the profile signature field before storage. On retrieval, the application does not adequately encode output, allowing stored HTML/JavaScript to be rendered as executable code rather than displayed as plain text.

## Attacker mindset
Low-effort, high-impact attack requiring only account creation and basic XSS payload knowledge. Attractive for mass phishing, credential harvesting, or spreading malware to forum users. The social engineering aspect (profile sharing via email) increases success rate.

## Defensive takeaways
- Implement strict input validation on all user-editable fields, particularly those displayed to other users
- Apply context-appropriate output encoding (HTML entity encoding minimum) when rendering user-supplied content
- Use a whitelist-based HTML sanitization library (e.g., DOMPurify, Bleach) if rich text is required
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Apply the principle of least privilege to user-generated content fields
- Conduct security testing for XSS across all input vectors during development
- Consider using automatic security scanning tools in the CI/CD pipeline

## Variant hunting
Check other profile fields (bio, about me, custom fields) for identical vulnerability
Test comment sections, forum posts, and user-to-user messaging for stored XSS
Examine signature functionality in private messages or email notifications
Look for stored XSS in avatar/profile picture metadata or EXIF data handling
Test rich text editors that may have bypass techniques for filtering
Check if signature field is reflected in email notifications sent to other users

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1005
- T1539
- T1056

## Notes
This is a classic stored XSS on a user-facing profile page. The vulnerability is straightforward to exploit but has significant impact due to trust relationships between forum users. The attack chain leverages social engineering (email/links) to increase victim engagement. The writeup demonstrates proper steps to reproduce but lacks technical depth regarding payload variations or impact demonstration. Simple fix via output encoding should resolve this issue completely.

## Full report
<details><summary>Expand</summary>

Summary
There is a stored XSS vulnerability in the users profile page.

Steps:

1-Go to https://forum.acronis.com , create an user and login
2-Go to profile and edit it
3- enter javascript code in Signature field for exampe  use this code in Signature : <xss onmouseover="alert(1)">test</xss>
4-send this profile to other users ,or send this profile link via email to victims.

## Impact

if someone views attacker profile the script will execute

</details>

---
*Analysed by Claude on 2026-05-12*
