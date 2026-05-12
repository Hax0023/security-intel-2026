# Stored XSS in Return Magic App Portal Content

## Metadata
- **Source:** HackerOne
- **Report:** 420459 | https://hackerone.com/reports/420459
- **Submitted:** 2018-10-07
- **Reporter:** zombiehelp54
- **Program:** Shopify Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Return Magic Shopify app's portal content settings that fails to sanitize user-supplied HTML content. Attackers can inject malicious JavaScript that executes in the context of other users' sessions when they access the portal settings page or search functionality.

## Attack scenario
1. Attacker installs the Return Magic app on a Shopify store they control or have access to
2. Attacker navigates to Settings > Portal > Content and switches to Code view
3. Attacker injects malicious payload such as `<img src=x onerror=alert(2)>` or more sophisticated XSS vectors
4. Attacker saves the malicious content, which is stored in the application database without sanitization
5. When any user (admin, staff, or customer) accesses the portal settings page or portal search page, the malicious script executes in their browser context
6. Attacker can steal session tokens, CSRF tokens, sensitive data, or perform unauthorized actions on behalf of the victim

## Root cause
The application accepts and stores user-supplied HTML content in the portal settings without proper input validation, sanitization, or output encoding. The rendered content is displayed directly in the DOM without escaping special characters or removing potentially dangerous HTML tags and event handlers.

## Attacker mindset
An attacker with access to the Return Magic app settings seeks to compromise other users' sessions and perform unauthorized actions. They recognize that portal content is likely displayed to multiple users without sanitization, making it an effective vector for persistent XSS attacks. The attacker exploits the WYSIWYG editor's code view to bypass frontend protections.

## Defensive takeaways
- Implement strict input validation on all user-supplied content, specifically whitelisting allowed HTML tags and attributes
- Use a robust HTML sanitization library (e.g., DOMPurify, sanitize-html) on both client and server side
- Apply proper output encoding/escaping when rendering user content in the DOM
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Use frameworks that auto-escape by default (e.g., React, Vue with proper configuration)
- Apply the principle of least privilege - restrict who can edit portal content
- Conduct security code reviews specifically for user-generated content handling
- Perform regular security testing including XSS payload testing across all content input fields

## Variant hunting
Search for similar stored XSS vulnerabilities in other Shopify apps that accept rich HTML content, such as custom page builders, email template editors, notification systems, and admin notification features. Check for similar patterns where WYSIWYG editors provide code views without sanitization. Test other portals, settings pages, and any administrative interfaces that accept user-supplied content.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1566 - Phishing
- T1539 - Steal Web Session Cookie

## Notes
The vulnerability affects both the admin dashboard at `/dashboard-shopify/settings/portal/content` and the customer-facing portal at `/portal/search`, suggesting widespread impact. The attacker demonstrated a simple payload, but more sophisticated attacks could steal authentication tokens or perform actions as the logged-in user. The use of `services.alveo.io` domain indicates the Return Magic app is hosted separately from Shopify's infrastructure, expanding the attack surface.

## Full report
<details><summary>Expand</summary>

**Summary:** 
Stored XSS vulnerability was found in return magic app portal content which executes in the application domain in `https://services.alveo.io/dashboard-shopify/settings/portal/content` 

**Description:** 
It's been found that Return Magic app allows users to add HTML content to their return portal without sanitizing the HTML which makes it possible to inject malicious tags that can be used to execute arbitrary JavaScript through other users' sessions.

## Steps To Reproduce:
1. Install Return Magic app
2. Navigate to `https://<shop>.myshopify.com/admin/apps/returnmagic`
3. Open **Settings** tab from the top menu and then open **Portal** --> **Content** from the left menu 
4. For the textarea where you enter your portal content, click the **Code** icon and enter `Test <img src=x onerror=alert(2)>` then click **Save** 
5. Now each time a user opens the portal settings page, `alert(2)` will be executed.
6. XSS also triggers in `https://services.alveo.io/portal/search?shop=<shop>.myshopify.com` 
{F356974}

## Impact

Through this vulnerability a malicious user will be able to execute JavaScript through other user's sessions' which allows him to do malicious actions such as stealing sensitive information, submitting requests that bypass csrf protection ..etc

</details>

---
*Analysed by Claude on 2026-05-12*
