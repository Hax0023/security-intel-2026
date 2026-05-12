# Authenticated Stored Cross-site Scripting (XSS) in bbPress Forum Admin Panel

## Metadata
- **Source:** HackerOne
- **Report:** 881918 | https://hackerone.com/reports/881918
- **Submitted:** 2020-05-24
- **Reporter:** whoisbinit
- **Program:** bbPress
- **Bounty:** Unknown
- **Severity:** medium
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Sanitization, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in bbPress that allows authenticated users to inject malicious JavaScript payloads into forum content via the Text editor. The payload is executed when administrators view the forum posts list in wp-admin/edit.php?post_type=forum, potentially compromising other users and site administrators.

## Attack scenario
1. Attacker authenticates to WordPress site with contributor or author privileges
2. Attacker navigates to Add New Forum post in wp-admin/edit.php?post_type=forum
3. Attacker enters malicious JavaScript payload (e.g., <script>alert('XSS')</script>) in Text editor mode instead of Visual editor
4. Attacker publishes the forum post containing the XSS payload
5. When administrators or other users view the forum posts list, the stored JavaScript executes in their browser session
6. Attacker can steal admin session cookies, perform unauthorized actions, or inject malware via the executed script

## Root cause
bbPress fails to properly sanitize and encode user input from the Text editor before storing and displaying forum content in the WordPress admin dashboard. The vulnerability exists because the content filter/sanitization functions are either missing or ineffective for the Text editor pathway.

## Attacker mindset
An authenticated user with malicious intent exploits a blind spot in bbPress security where the Text editor bypasses sanitization checks that may exist for the Visual editor. The attacker leverages admin dashboard access to target site administrators and high-privilege users.

## Defensive takeaways
- Implement consistent input sanitization across all content entry methods (Visual and Text editors) using WordPress sanitization functions like sanitize_text_field() or wp_kses_post()
- Apply proper output encoding when displaying user-generated content in admin contexts using esc_html(), esc_js(), or wp_kses_post()
- Use WordPress nonces to validate admin actions and prevent CSRF-based XSS exploitation chains
- Implement Content Security Policy (CSP) headers to mitigate XSS impact even if payload reaches DOM
- Conduct security code review of all content handling functions in bbPress, particularly those handling rich text input
- Apply principle of least privilege - limit contributor/author roles that can create forum posts if not necessary

## Variant hunting
Search for similar XSS vulnerabilities in other bbPress post types (topics, replies), check if the Visual editor has different sanitization logic than Text editor, examine whether the vulnerability affects other custom post types in bbPress, test if the payload persists across different user roles and permissions.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is an authenticated vulnerability requiring valid WordPress credentials, which reduces immediate risk but increases insider threat potential. The use of Text editor as attack vector suggests sanitization functions may be editor-mode aware. The vulnerability particularly threatens administrators viewing the posts list, making it suitable for privilege escalation or admin account compromise.

## Full report
<details><summary>Expand</summary>

## Description:
There exists a stored XSS vulnerability in bbPress, due to which the XSS payload which I enter in my content, gets executed at **/wp-admin/edit.php?post_type=forum**. This vulnerability requires you to be an authenticated user.

## Steps To Reproduce:
Step 1. Visit /wp-admin/edit.php?post_type=forum
Step 2. Click on **Add New**
Step 3. Write any title, and in content, write your XSS payload through the "Text" editor, rather than the "Visual" one, and publish the content.
Step 4. Now, visit /wp-admin/edit.php?post_type=forum, and you will be able to see the payload getting executed.

## Recommendations
Making use of proper functions in PHP or WordPress core in the bbPress source code regarding the filtering or sanitization of user input is a recommended way to fix this vulnerability.

## Impact

By taking an advantage of this vulnerability, an owner of a WordPress-based website would be able to execute their malicious JavaScript codes in context to the WordPress dashboard, which could result in bad issues to other users.

</details>

---
*Analysed by Claude on 2026-05-12*
