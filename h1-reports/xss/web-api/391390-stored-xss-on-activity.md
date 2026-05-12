# Stored XSS on Activity Page via Member Name Field

## Metadata
- **Source:** HackerOne
- **Report:** 391390 | https://hackerone.com/reports/391390
- **Submitted:** 2018-08-07
- **Reporter:** shazadsadiq
- **Program:** Unknown (HackerOne Report #391390)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the activity log feature where member names are not properly sanitized or encoded before storage and display. An attacker with staff member privileges can inject malicious JavaScript payloads into a member's name field, which executes when administrators view the activity log, enabling admin account takeover through cookie theft.

## Attack scenario
1. Attacker creates or gains access to a store as a staff member
2. Attacker modifies their own or another member's name to include XSS payload: hunter"><svg/onload=alert(2)>
3. The payload is stored in the database without proper sanitization
4. Administrator logs in and views the activity log to monitor store changes
5. The malicious payload executes in the admin's browser context when the activity is rendered
6. Attacker's JavaScript steals admin session cookies or performs admin-level actions

## Root cause
The application fails to properly sanitize user input on the member name field and does not encode output when rendering activity logs. The vulnerable code path allows raw HTML/JavaScript to be stored and later executed in the admin's browser without Content Security Policy (CSP) or HTML encoding protections.

## Attacker mindset
Privilege escalation from staff member to administrator. The attacker recognizes that activity logs are viewed by admins and leverage this to inject persistent payloads that execute with elevated privileges, enabling account compromise and unauthorized access.

## Defensive takeaways
- Implement strict input validation and sanitization on all user-supplied fields, especially those displayed in logs or activity feeds
- Apply context-appropriate output encoding (HTML entity encoding) when rendering user-controlled data in HTML context
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Use templating engines with auto-escaping enabled by default
- Apply principle of least privilege: restrict staff member capabilities to modify sensitive fields like usernames
- Implement audit logging for sensitive field changes with additional approval workflows
- Perform security code review focusing on data flow from input to output in activity/log features
- Add automated security testing (SAST/DAST) to catch XSS vulnerabilities in CI/CD pipeline

## Variant hunting
Check other log/activity features for similar XSS vulnerabilities (audit logs, change history, user activity feeds)
Test other user-modifiable fields that appear in activity logs (descriptions, titles, comments)
Investigate if other user roles (customer, guest) can inject payloads into fields viewed by higher-privileged users
Check if member names are used in email notifications or exported reports without encoding
Test for mutation-based XSS bypasses using alternative payload encoding (Unicode, hex, mixed case tags)

## MITRE ATT&CK
- T1190
- T1539
- T1566
- T1598

## Notes
Report lacks specific bounty amount and affected company name. The vulnerability requires staff-level access but compromises admin accounts, making it a critical escalation vector. The POC image reference (F329469) suggests visual confirmation was provided. Timeframe and patch status unknown. Consider whether this affects multi-tenancy isolation.

## Full report
<details><summary>Expand</summary>

Hi security team members,

#Description
I found a store xss on the activity which allows an attacker to steal admin account cookies.

#Step to reproduce
1-Create store
2- Add a member in a store
3- Member can choose any name 
4- So change the any member name with hunter"><svg/onload=alert(2)>
5- Now on admain account make changes 
6- That will create activity with attacker malicious payload

#POC
Please see the below image
{F329469}
Let me know if more information is needed to my end.
Best Regards,
Shahzad

## Impact

An attacker(staff member) can takeover admin account.

</details>

---
*Analysed by Claude on 2026-05-12*
