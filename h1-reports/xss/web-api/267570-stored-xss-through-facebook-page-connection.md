# Stored XSS through Facebook Page Connection

## Metadata
- **Source:** HackerOne
- **Report:** 267570 | https://hackerone.com/reports/267570
- **Submitted:** 2017-09-11
- **Reporter:** boredengineer21
- **Program:** KitCRM
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Client-Side Template Injection
- **CVEs:** None
- **Category:** web-api

## Summary
KitCRM fails to properly sanitize or encode Facebook page names when displaying them in the connections dropdown menu. An attacker with a Facebook page containing malicious JavaScript in its name can achieve stored XSS by selecting that page in the connections UI, causing the payload to execute for any user viewing the connections page.

## Attack scenario
1. Attacker creates a Facebook page with a malicious name containing JavaScript payload: "><img src=x onerror=alert(9)>
2. Attacker connects this Facebook page to their KitCRM account via the social connections feature
3. The malicious page name is stored in KitCRM's database without sanitization
4. When attacker (or any admin/user with access) visits /users/[id]/connections, the page name is rendered in the dropdown without encoding
5. The browser parses the unsanitized HTML/JavaScript and executes the onerror handler
6. Payload could be upgraded to steal session cookies, perform account takeover, or redirect to phishing site

## Root cause
KitCRM retrieves Facebook page metadata (including page names) from the Facebook API and stores it directly without sanitization. When rendering the dropdown options, the application fails to HTML-encode the page names before inserting them into the DOM, allowing arbitrary HTML/JavaScript to be executed.

## Attacker mindset
An attacker would recognize that user-controlled data from third-party APIs (Facebook) is inherently untrusted. By crafting a malicious page name, they can inject code that executes in the context of KitCRM users who view their connections, potentially escalating to session hijacking or credential theft.

## Defensive takeaways
- Always HTML-encode output when rendering user-controlled or external data in HTML context
- Implement Content Security Policy (CSP) to restrict inline script execution
- Sanitize and validate all data from third-party APIs before storage
- Use templating engines with automatic escaping enabled by default
- Apply input validation to reject or sanitize page names with suspicious patterns
- Implement a Web Application Firewall (WAF) to detect and block XSS patterns
- Regular security testing including XSS payload injection in external data sources

## Variant hunting
Check other social platform integrations (Instagram, Twitter, LinkedIn) for similar issues with profile names, bio fields, or descriptions
Test other user-editable fields that might be populated from external APIs
Look for similar encoding issues in business/organization name fields from third-party integrations
Check if the vulnerability exists in email templates or exported reports containing Facebook page data
Test whether the XSS persists across user sessions or affects other users with access to the connections page
Verify if admin panels displaying all user connections are also vulnerable to reflected/stored XSS

## MITRE ATT&CK
- T1190
- T1059
- T1566
- T1563

## Notes
This is a classic stored XSS vulnerability exacerbated by trust in external data sources. The fact that Facebook page names can be arbitrary strings (especially for test/attacker-controlled accounts) makes this a reliable exploitation vector. The vulnerability affects any user who can access the connections page, making it potentially high-impact in multi-user or admin scenarios. The use of Facebook's API data without encoding demonstrates insufficient security controls for third-party integrations.

## Full report
<details><summary>Expand</summary>

The following URL
https://kitcrm.com/users/122686/connections
displays us options to connect our several social networking accounts to kitcrm.
Once i connect my facebook account, the facebook section in above link will list out all my facebook page and will give me an option to select a business page. 
One of my facebook page name is "><img src=x onerror=alert(9)>
F220032: Screenshot from 2017-09-11 22-23-23.png 54.6KB 

Now when i click on that drop-down option an alert will pop-up.
F220033: Screenshot from 2017-09-11 22-25-20.png





</details>

---
*Analysed by Claude on 2026-05-12*
