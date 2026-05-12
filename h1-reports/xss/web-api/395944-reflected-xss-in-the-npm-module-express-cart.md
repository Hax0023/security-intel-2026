# Reflected XSS in express-cart Product Options Field

## Metadata
- **Source:** HackerOne
- **Report:** 395944 | https://hackerone.com/reports/395944
- **Submitted:** 2018-08-16
- **Reporter:** avi3719
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Input Validation Failure
- **CVEs:** None
- **Category:** web-api

## Summary
The express-cart npm module version 1.1.5 contains a reflected XSS vulnerability in the product options field that allows authenticated admin users to inject malicious JavaScript code. When creating a new product and inserting a payload in the 'Product options' field, the unescaped input is reflected directly in the browser, enabling arbitrary script execution.

## Attack scenario
1. Attacker authenticates as an admin user to the express-cart application
2. Attacker navigates to the product creation page via the left menu panel
3. Attacker enters a malicious JavaScript payload (e.g., <script>alert(1234)</script>) in the 'Product options' input field
4. Attacker submits the form with the malicious payload
5. The server reflects the unescaped payload back in the response HTML
6. The victim's browser executes the injected JavaScript code, potentially stealing session cookies, redirecting to phishing sites, or performing unauthorized actions

## Root cause
Insufficient input validation and output encoding on the product options field. The application fails to sanitize or properly escape user-supplied input before reflecting it back in the HTTP response, allowing direct injection of HTML/JavaScript code.

## Attacker mindset
An insider threat or compromised admin account could weaponize this to execute malicious scripts affecting other users. The attacker recognizes that admin-level access to product creation workflows is often less scrutinized than customer-facing inputs, making it an effective persistence or privilege escalation vector.

## Defensive takeaways
- Implement comprehensive input validation on all user-supplied fields, including product options
- Apply context-aware output encoding (HTML entity encoding) to all data reflected in responses
- Use templating engines with auto-escaping enabled by default
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Perform security code review of form handling and rendering logic
- Apply the principle of least privilege to admin functions
- Regularly update and audit npm dependencies for known vulnerabilities
- Implement security testing (SAST/DAST) in the CI/CD pipeline

## Variant hunting
Check other product-related input fields (name, description, price, SKU) for similar XSS vulnerabilities
Test category creation and editing pages for reflected/stored XSS
Examine customer review/comment functionality for XSS
Audit user profile and settings pages for input validation gaps
Check payment gateway configuration fields for injection flaws
Test search functionality for reflected XSS
Review order notes and admin messaging features

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a relatively straightforward reflected XSS affecting an e-commerce module with low adoption (27 weekly downloads). The vulnerability is limited to authenticated admin users, reducing the attack surface. However, it could still be exploited via compromised credentials or social engineering. The reporter did not contact the maintainer or open an issue, which may indicate the vulnerability remained unpatched at time of report.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

I would like to report Reflected XSS  in the npm module express-cart.
It allows a user to insert malicious payload in the user input field and the script gets reflected in the browser

# Module

**module name:** express-cart
**version:** 1.1.5
**npm page:** `https://www.npmjs.com/package/express-cart`

## Module Description

expressCart is a fully functional shopping cart built in Node.js (Express, MongoDB) with Stripe, PayPal, and Authorize.net payments.

## Module Stats

[27] downloads in the last week


# Vulnerability

## Vulnerability Description
when the admin user creates a request for a new product, then the field 'Product option' accepts any malicious user input. This lead me to identify the reflected XSS attack. 

## Steps To Reproduce:
1. Login with admin user credentials.
2. From Left Menu panel, select new under product tab
3. In 'product options' details, insert any javascript payload eg. <script>alert(1234)</script>
4. The reflected XSS in the form of an alert box will be pop up in a browser window.


## Supporting Material/References:
- https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)

>l technical information about the stack where the vulnerability was found

- OS used Windows 10 
- NODEJS VERSION - V8.11.3 
- NPM VERSION - 5.6.0
- Browser - Chrome 68.0.3440.106


# Wrap up

- I contacted the maintainer to let them know: [N] 
- I opened an issue in the related repository: [N]

## Impact

This vulnerability would allow a user to insert javascript payloads which can be reflected in a browser.

</details>

---
*Analysed by Claude on 2026-05-12*
