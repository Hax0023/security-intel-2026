# Stored XSS via HTML File Upload in Shopify Services Marketplace

## Metadata
- **Source:** HackerOne
- **Report:** 591786 | https://hackerone.com/reports/591786
- **Submitted:** 2019-05-28
- **Reporter:** encryptsaan123
- **Program:** Shopify
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper File Upload Validation, Insufficient Input Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the services.shopify.com email template builder that allows authenticated users to upload HTML files containing malicious JavaScript code. When the uploaded file is accessed, the XSS payload executes in the browser context, potentially allowing session hijacking and cookie theft.

## Attack scenario
1. Attacker authenticates to Shopify Admin and navigates to the Services Marketplace
2. Attacker accesses the email template design feature under Marketing and Sales > Email Marketing
3. Attacker creates a new template and uses the 'attach file' functionality to upload a malicious HTML file containing XSS payload
4. Attacker stores the malicious template in the marketplace
5. When victim or attacker right-clicks and opens the attached file location, JavaScript executes in victim's browser
6. Attacker's JavaScript steals session cookies, authentication tokens, or sensitive user data

## Root cause
The application fails to properly sanitize or validate uploaded HTML files. The system treats uploaded HTML content as trustworthy and renders it without Content Security Policy (CSP) protections or HTML escaping. No server-side validation ensures uploaded files contain safe content.

## Attacker mindset
An authenticated attacker seeks to compromise other Shopify users by leveraging a feature designed for legitimate file attachments. The attacker exploits trust in the upload mechanism and assumes HTML files will be rendered without security controls. Goal is credential theft and account takeover.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) headers to prevent inline script execution
- Validate and sanitize all uploaded files, especially HTML - consider converting to PDFs or images
- Serve uploaded files with appropriate Content-Type headers (e.g., text/plain, application/octet-stream) instead of text/html
- Implement file type whitelist validation both client and server-side
- Use sandboxed iframes or separate domain to render user-uploaded content
- Apply HTML sanitization libraries (e.g., DOMPurify) to strip dangerous elements
- Implement proper authentication and authorization checks for file access
- Log and monitor file upload activities for suspicious patterns

## Variant hunting
Check other file upload functionality across Shopify Admin for similar XSS vectors
Test SVG file uploads which can contain embedded JavaScript
Investigate other marketplace features (Design, Sales channels) for file upload XSS
Look for stored XSS in email template preview/rendering features
Test XML/XXE payloads in document uploads
Check if other authenticated users can access/execute uploaded files
Test for DOM-based XSS in file processing/parsing logic

## MITRE ATT&CK
- T1190
- T1203
- T1105

## Notes
Report lacks detail on whether vulnerability requires victim interaction or affects other users. Unclear if XSS is strictly stored or requires specific conditions. The impact is potentially severe for multi-tenant Shopify ecosystem. Bounty amount not disclosed in provided content. File location context-dependent - clarification needed on persistence scope.

## Full report
<details><summary>Expand</summary>

Hy security,
 i Got a stored xss in one of your sub-domain "services.shopify.com"

steps:
1- Go to https://(your_store).myshopify.com/admin/apps/experts_marketplace/services_marketplace
2- Then Go to  All services>Marketing and sales>email marketing> Design custom email templates >click select
3- fill al the data, there will be an option for "attach file"
4: selcet a html file where the xss payloads are got stored.
5. write click on the attached file and go to that location, you will see the pop-up

## Impact

can steal cookies

</details>

---
*Analysed by Claude on 2026-05-12*
