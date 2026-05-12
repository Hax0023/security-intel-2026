# Cross-site Scripting in Contact Customer Form

## Metadata
- **Source:** HackerOne
- **Report:** 294505 | https://hackerone.com/reports/294505
- **Submitted:** 2017-12-02
- **Reporter:** protector47
- **Program:** HackerOne (Unspecified Platform/Program)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), HTML Injection, Stored XSS
- **CVEs:** None
- **Category:** web-api

## Summary
An HTML injection vulnerability exists in the 'Contact Customer' admin form where unsanitized input in the Customer Message field is executed when the 'Review Email' button is clicked. An authenticated admin can inject arbitrary HTML/JavaScript to compromise customers, though this requires admin-level access.

## Attack scenario
1. Attacker with admin credentials accesses the Customers section
2. Attacker navigates to a customer's email and clicks to open the contact form popup
3. Attacker enters malicious HTML/JavaScript payload in the Customer Message field (e.g., <script>window.location='http://malicious-site.com'</script>)
4. Attacker clicks 'Review Email' button to trigger payload execution
5. The payload executes in the customer's browser when they receive/view the email or when admin previews it
6. Customer is redirected to malicious site or experiences credential theft, malware delivery, or session hijacking

## Root cause
User input from the Customer Message field is not properly sanitized or HTML-encoded before being rendered in the email preview or sent to customers. The application fails to implement output encoding or Content Security Policy to prevent script execution.

## Attacker mindset
A malicious admin leveraging their trusted position to compromise customer data and trust. This represents an insider threat scenario where the attacker abuses administrative privileges. The attacker recognizes that admins are trusted by customers and misuses this to deliver targeted phishing or malware attacks.

## Defensive takeaways
- Implement strict output encoding/HTML escaping for all user inputs before rendering in HTML context
- Apply input validation to reject or sanitize HTML tags in message fields
- Deploy Content Security Policy (CSP) headers to restrict script execution
- Use templating engines with auto-escaping enabled
- Implement email sanitization libraries before sending to users
- Add audit logging for admin message creation to detect suspicious activity
- Consider splitting the preview functionality from actual message delivery with additional controls
- Educate admins about XSS risks and secure coding practices

## Variant hunting
Check other admin-to-user communication features (notifications, alerts, reports)
Test message fields in support tickets, feedback forms, and comment sections
Review customer-to-customer messaging or review systems for similar XSS
Examine order confirmation messages and notification customization panels
Test event/promotion message creation features for HTML injection
Check admin dashboard widgets or custom message templates

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1566.002

## Notes
While severity is elevated due to potential customer compromise, the requirement for admin-level access limits exposure compared to unauthenticated XSS. The actual impact depends on whether the payload executes in the customer's browser (when viewing received email) or only in the admin's preview. Clarification needed on whether this is stored XSS (persisted and sent to customers) or reflected XSS (preview only). POC video referenced but not detailed in writeup. This appears to be a legitimate finding as stored XSS from admin context can still compromise customers through email-based attack vectors.

## Full report
<details><summary>Expand</summary>

Hi,
I found HTML Injection Vulnerability while admin contact with customer.
In this vulnerability admin is attacker whereas customer is victim.

#Steps to Reproduce:

1. Go to **Customers** and Click on **Customer Email Address**.
2. New Pop-Up window will become open, In **Customer Message** field type this html code

><h1>HTML INJECTION</h1>

3 . Click on **Review Email** Button.

HTML will become execute.

Checkout the POC Video.
  
Thanks,

## Impact

Admin of store can redirect any user to any malicious website, and can perform all possible attacks through this vulnerability.

</details>

---
*Analysed by Claude on 2026-05-12*
