# Stored XSS in Address Field - Billing Activity at shop.aaf.com

## Metadata
- **Source:** HackerOne
- **Report:** 411690 | https://hackerone.com/reports/411690
- **Submitted:** 2018-09-20
- **Reporter:** gujjuboy10x00
- **Program:** AAF (hackerone.com/reports/411690)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The billing address field in the checkout process at shop.aaf.com/Order/step1/index.cfm is vulnerable to stored XSS attacks. An attacker can inject malicious JavaScript payloads (e.g., a"><svg/onload=prompt(1)>) into address fields, which are stored and executed in the browsers of users viewing the order details. This vulnerability can lead to session hijacking, cookie theft, and complete account takeover.

## Attack scenario
1. Attacker navigates to shop.aaf.com and selects a product to add to cart
2. Attacker proceeds to checkout and reaches the billing information step (step1/index.cfm)
3. Attacker injects XSS payload a"><svg/onload=prompt(1)> into one or more address fields (street address, city, etc.)
4. Attacker completes the purchase or order submission, causing the malicious payload to be stored in the application database
5. When legitimate users or administrators view the order details, the stored XSS payload executes in their browser context
6. Attacker's JavaScript can steal session cookies, perform actions on behalf of the user, or redirect to phishing pages

## Root cause
The application fails to properly sanitize and validate user input in address fields before storage and fails to encode output when displaying stored data. The address field accepts arbitrary HTML/JavaScript without filtering, and the application renders it as HTML rather than plain text.

## Attacker mindset
An attacker with basic XSS knowledge recognizes that billing addresses are often viewed by multiple parties (users, admins, support staff) and that stored XSS has wider impact than reflected XSS. The attacker tests simple SVG-based payloads to bypass basic filters and leverages the checkout flow where defenses may be weaker.

## Defensive takeaways
- Implement strict input validation for all address fields, allowing only alphanumeric characters, spaces, hyphens, commas, and periods
- Apply HTML entity encoding to all user-supplied data before rendering in HTML context (e.g., &lt;, &gt;, &quot;, &amp;)
- Use a Content Security Policy (CSP) header to restrict inline script execution and limit script sources
- Implement parameterized queries and ORM frameworks to prevent injection attacks at the database layer
- Apply output escaping context-appropriately (HTML escaping for HTML context, JavaScript escaping for JS context, etc.)
- Conduct security code review of all user input handling in checkout and payment flows
- Implement WAF rules to block common XSS payloads and SVG/event handler patterns
- Perform regular security testing including automated SAST/DAST and manual penetration testing
- Sanitize data server-side using libraries like OWASP ESAPI or similar before storage

## Variant hunting
Test other form fields in checkout (shipping address, billing name, phone, email) for similar XSS vulnerabilities
Attempt stored XSS in user profile/account settings pages
Test for DOM-based XSS variations in JavaScript event handlers
Check if order history/previous orders also display the vulnerable data
Test file upload fields in checkout for stored XSS via filename
Verify if admin panels viewing orders are also vulnerable to the stored XSS
Check for bypass techniques: encoding variations, case sensitivity, nested payloads
Test other e-commerce flows (returns, refunds, shipping info updates)

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The report is relatively basic and lacks detailed information about impact assessment, testing environment, and remediation timeline. The payload a"><svg/onload=prompt(1)> is a standard XSS test vector but the attacker could have used more dangerous payloads like cookie stealing or keylogging. The vulnerability affects the entire checkout process flow and potentially impacts all users who place orders. AAF should prioritize this as high-severity due to e-commerce context and potential for account takeover.

## Full report
<details><summary>Expand</summary>

Dear Team,

**Summary:** [add summary of the vulnerability]
After looking into https://shop.aaf.com/Order/step1/index.cfm i get to know that there is address field is vulnerable to stored xss which can lead to steal any user's cookie and can lead to complete account takeover

**Description:** [add more details about this vulnerability]

## Steps To Reproduce:

  1. go to https://shop.aaf.com and click on any products , tshirt
  2. add that in cart and click on proceed
  3. enter xss payload (a"><svg/onload=prompt(1)> ) in every address field and click on OK proceed
  4. xss will popup 

## Supporting Material/References:

XSS OWASP

Thanks,
Vishal

## Impact

Stored xss in address field in billing activity at https://shop.aaf.com/Order/step1/index.cfm

</details>

---
*Analysed by Claude on 2026-05-12*
