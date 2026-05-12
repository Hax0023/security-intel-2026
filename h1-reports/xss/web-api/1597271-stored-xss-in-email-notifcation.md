# Stored XSS in Email Notification Subject

## Metadata
- **Source:** HackerOne
- **Report:** 1597271 | https://hackerone.com/reports/1597271
- **Submitted:** 2022-06-10
- **Reporter:** khaledx
- **Program:** Insightly CRM
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the email notification feature of Insightly CRM where user-supplied input in the email subject line is not properly sanitized or encoded. When any group member views the notification, the malicious JavaScript payload executes in their browser context, allowing attackers to steal session cookies and compromise user accounts.

## Attack scenario
1. Attacker creates or gains access to an Insightly CRM account and joins a shared group
2. Attacker enables email service integration on the platform
3. Attacker crafts a malicious email with XSS payload in the subject field: ><img src="X" onerror=top[8680439..toString(30)](1337+document.cookie)>
4. Victim group member logs in and navigates to the email notification section at crm.na1.insightly.com/list/Email/
5. The email notification message renders and the JavaScript payload executes in victim's browser with their privileges
6. Attacker's payload steals the victim's session cookies and other sensitive data, enabling account takeover

## Root cause
The application fails to properly decode and sanitize user input in the email subject field before storing it in the database. Upon rendering the notification, the stored payload is executed as JavaScript rather than being treated as plain text or properly HTML-encoded.

## Attacker mindset
An insider threat or group member seeks to compromise other users in the organization by injecting malicious code into shared notification channels. The attacker recognizes that notifications are viewed by multiple users, maximizing the impact of a single payload.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-supplied fields, especially those displayed in notifications
- Apply proper HTML entity encoding/escaping to all output, particularly in dynamically rendered content
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Implement a robust HTML sanitization library (e.g., DOMPurify) for any rich text fields
- Validate and filter dangerous HTML tags and event handlers on both client and server side
- Apply the principle of least privilege to group member access controls
- Implement regular security testing including XSS fuzzing of notification systems
- Use parameterized/template rendering to separate data from executable code

## Variant hunting
Search for similar stored XSS in: other notification channels (SMS, push notifications), message subjects in discussion forums, user profile fields displayed in group contexts, email templates, report titles, attachment names, and any other user-controlled fields that are persisted and displayed to multiple users

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1539 - Steal Web Session Cookie
- T1204 - User Execution

## Notes
The writeup contains formatting issues and unclear sections (marked with ==), suggesting English may not be the reporter's first language. However, the core vulnerability is clearly a stored XSS with group-based amplification. The payload uses obfuscation (toString(30)) to bypass basic filters. The impact is significant as it affects all group members viewing notifications, not just the initial recipient.

## Full report
<details><summary>Expand</summary>

##Summary:
Hi team user input most be Decoded this is wired Stored XSS as the XSS been fired  in https://crm.na1.insightly.com/list/Email/ when  ever user open the ==Notifcation == message been send or even refresh his mail service as the site https://crm.na1.insightly.com/list/Email/  ==Notifcation== execute the ==Subject Emaill name Code== as Code and when ever any user in the Group login and try to see the ==Notifcation== XSS fired

##Steps To Reproduce:
1-Create Two account and invite user to join  to your Group
2-add  email service to enable send email in the platform
3-as ==any user in the Group= able to see sended message ==Create email== and enter this payload as Subject name
><img src="X" onerror=top[8680439..toString(30)](1337+document.cookie)>

4-as The Emaill ==Subject name been executed== when ever user login and try to see the missing ==Notifcation== The XSS been Fired


Video POC: ███████

## Impact

as any user in the Group able to see the ==Notifcation== attacker able to still users Cookie

</details>

---
*Analysed by Claude on 2026-05-12*
