# Stored XSS on Demo App Link (apps.shopify.com)

## Metadata
- **Source:** HackerOne
- **Report:** 439912 | https://hackerone.com/reports/439912
- **Submitted:** 2018-11-13
- **Reporter:** flashdisk
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the demo URL field of Shopify's app submission form at apps.shopify.com. An attacker can inject malicious JavaScript into the demo link field that persists and executes when other users preview or view the example store, potentially compromising account credentials or performing unauthorized actions.

## Attack scenario
1. Attacker creates a new Shopify Partner app or obtains access to an existing app
2. Attacker navigates to the app settings page and locates the DEMO URL field
3. Attacker injects XSS payload (e.g., <script>alert('XSS')</script>) into the DEMO URL field
4. Attacker clicks 'Preview Changes' to confirm payload is stored
5. When the attacker or any other user clicks 'View Example Store' button, the payload executes in their browser
6. Attacker's JavaScript can steal session tokens, redirect users to phishing pages, or modify page content

## Root cause
The application fails to properly sanitize and encode user input in the DEMO URL field before storing it in the database. Upon retrieval and rendering, the unsanitized data is rendered directly in HTML without proper escaping or Content Security Policy protections.

## Attacker mindset
An app developer with partner account access recognizes that the demo URL field accepts arbitrary input without validation. They inject JavaScript to test XSS, discovering the vulnerability can persist and execute for all users who interact with the demo link, enabling credential theft or account compromise.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, especially URLs and demo links
- Apply proper output encoding (HTML entity encoding) when rendering stored data
- Use a URL validation library to whitelist only valid URL schemes (http, https)
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Apply HTMLSanitizer or similar library to strip malicious tags from stored content
- Use parameterized templates to prevent injection of unescaped data
- Implement server-side validation in addition to client-side checks
- Regularly perform security testing including stored XSS scenarios

## Variant hunting
Test other URL/link input fields in app submission forms (support URL, privacy policy URL, etc.)
Check if demo URL field allows JavaScript protocol handlers (javascript:alert(1))
Test Data URI encoding (data:text/html,<script>alert(1)</script>)
Verify if stored XSS persists across different user sessions or roles
Test if admin/moderator views of app submissions are also vulnerable
Check for DOM-based XSS variants when demo URL is processed client-side
Investigate if encoded payloads bypass validation (URL encoding, double encoding)

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a classic stored XSS vulnerability in a user-controlled field that lacks proper input sanitization and output encoding. The fact that the payload executes when previewing the demo store suggests the vulnerable code path is in the example store rendering logic. The vulnerability affects not just the attacker but any user interacting with the app's demo link, making it a high-severity issue affecting platform integrity and user trust.

## Full report
<details><summary>Expand</summary>

Hi,

I found stored XSS in apps.shopify.com in the `DEMO` URL of the apps you create.

#POC

1. go to your partner account and create a new app
2. go to DEMO link in https://apps.shopify.com/services/app_submissions/edit# of your app 

put the payload you see below:

{F374863}

and when pressing on `preview changes` button and then pressing on `view example store` xss will fire as follows:

{F374865}


thanks!

## Impact

Stored XSS on apps.shopify.com

</details>

---
*Analysed by Claude on 2026-05-12*
