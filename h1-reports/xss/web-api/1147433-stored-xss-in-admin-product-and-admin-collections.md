# Stored XSS in /admin/product and /admin/collections Rich Text Editor

## Metadata
- **Source:** HackerOne
- **Report:** 1147433 | https://hackerone.com/reports/1147433
- **Submitted:** 2021-04-03
- **Reporter:** ashketchum
- **Program:** Shopify
- **Bounty:** Unknown (not specified in report)
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
Stored XSS vulnerabilities were discovered in the Rich Text Editor HTML mode for both product and collection descriptions in Shopify admin panel. By injecting malicious image tags with onerror event handlers through the HTML editor, an attacker can execute arbitrary JavaScript in the context of admin users viewing these pages. This allows theft of session cookies and other sensitive data.

## Attack scenario
1. Attacker gains access to Shopify admin panel (as store owner or authorized user)
2. Attacker navigates to product creation or collection creation page
3. Attacker switches description field to HTML editor mode
4. Attacker injects payload: ">\]<img src=x onerror=alert(document.domain)>
5. Attacker saves the product/collection with malicious payload stored in database
6. When other admin users view the product/collection, XSS payload executes stealing cookies or performing actions on their behalf

## Root cause
The Rich Text Editor HTML mode does not properly sanitize or validate user input before storing it in the database. HTML tags and event handlers are accepted without filtering, allowing injection of executable JavaScript code that persists and runs when the content is rendered.

## Attacker mindset
An insider threat or compromised account holder would exploit this to establish persistence, escalate privileges, or harvest credentials from other admin users. The attack requires only basic XSS knowledge and access to admin functions.

## Defensive takeaways
- Implement server-side HTML sanitization using libraries like DOMPurify or similar for all rich text editor inputs
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Apply output encoding based on context (HTML entity encoding for HTML context)
- Validate and whitelist allowed HTML tags and attributes in rich text editors
- Implement strict input validation regardless of editor mode (visual or HTML)
- Conduct security reviews of all rich text editor implementations across the platform
- Add automated security testing for XSS in admin-facing features

## Variant hunting
Check other admin pages with rich text editors (email templates, email notifications, landing pages)
Test other HTML input fields across admin panel for similar bypass patterns
Investigate if other event handlers bypass filters (onload, oninput, onmouseover)
Test for DOM-based XSS in rich text editor preview functionality
Check if payload encoding/escaping differs between product and collection endpoints
Test if stored XSS persists across different admin user sessions and roles

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1003 - OS Credential Dumping
- T1055 - Process Injection
- T1539 - Steal Web Session Cookie
- T1566 - Phishing

## Notes
This report references a previously known XSS issue in rich text editors (report #978125) that Shopify had acknowledged but apparently not fully remediated. The vulnerability demonstrates that similar sanitization bypasses may exist in related endpoints. The report lacks specific severity rating and bounty amount but the impact is significant as it affects admin-level accounts with broad system access.

## Full report
<details><summary>Expand</summary>

### Hello Security Team,

I was going through previous reports of XSS and I have found this,
https://hackerone.com/reports/978125

As stated by team on this page even on https://hackerone.com/shopify?type=team under Known issues
 that we can now report XSS under Rich Text Editor on Product description and Collection description. 
I have found XSS on this endpoints /admin/product and /admin/collections

{F1252456}

### Steps to Reproduce:
#### /admin/product

Step1: Go to https://your-store.myshopify.com/admin/products?selectedView=all
Step2: Click on Add product 
Step3: Add anything in Title
Step4: Right side corner in description click on Show HTML
Step5: Add below Payloads and Click on Save

#### Payload: 
">\]<img src=x onerror=alert(document.domain)>  ">\]<img src=x onerror=alert(document.cookie)>
      
XSS will get triggered.

{F1252457}

#### /admin/collections

Step1: Go to https://your-store.myshopify.com/admin/collections
Step2: Click on Create collection
Step3: Add anything in Title
Step4: Right side corner in description click on Show HTML
Step5: Add below Payloads and Click on Save

#### Payload: 
">\]<img src=x onerror=alert(document.domain)>  ">\]<img src=x onerror=alert(document.cookie)>
      
XSS will get triggered.

{F1252455}

I have attached POC Video, Please take a look.

{F1252458}

#### Thank You
Ashish Dhone

## Impact

A malicious user can steal cookies and use them to gain further access even an attacker can use XSS to send requests that appear to be from the victim to the web server.

</details>

---
*Analysed by Claude on 2026-05-12*
