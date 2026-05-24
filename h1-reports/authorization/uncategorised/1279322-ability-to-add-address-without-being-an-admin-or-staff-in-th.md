# Unauthorized Address Addition to Customer Accounts via Wholesale Store Registration

## Metadata
- **Source:** HackerOne
- **Report:** 1279322 | https://hackerone.com/reports/1279322
- **Submitted:** 2021-07-27
- **Reporter:** urfavenemy01
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Insecure Direct Object Reference (IDOR), Authorization Bypass, Privilege Escalation, Account Takeover
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated attacker can add or modify customer addresses in a Shopify store by exploiting the wholesale store registration functionality when the 'Customers must provide an address' setting is enabled. By registering with an existing customer's email address and providing a different address during wholesale signup, the attacker can associate fraudulent addresses with legitimate customer accounts without requiring admin or staff privileges.

## Attack scenario
1. Attacker identifies target Shopify store with wholesale functionality enabled and 'Customers must provide an address' feature activated
2. Attacker obtains or enumerates valid customer email addresses from the target store
3. Attacker initiates wholesale store registration using a victim customer's email address
4. Attacker provides a malicious or fraudulent address during the wholesale registration process
5. Attacker completes registration by clicking 'Continue to shipping' without completing full checkout
6. System automatically associates the fraudulent address with the existing customer account, replacing or adding to customer profile

## Root cause
The wholesale store registration endpoint fails to validate that the email address being registered belongs to the current user or has authorization to modify the associated customer account. The system trusts user-supplied email input and directly associates provided addresses with existing customer records without proper authentication or authorization checks.

## Attacker mindset
An attacker could exploit this to conduct account takeover by changing default shipping addresses, commit payment fraud by redirecting shipments to attacker-controlled locations, perform identity theft by replacing legitimate customer addresses, or execute phishing/scam campaigns by modifying customer contact information.

## Defensive takeaways
- Implement strict authorization checks to ensure users can only modify their own customer records and associated data
- Require email verification before associating addresses with customer accounts, especially in wholesale flows
- Add multi-step confirmation when modifying existing customer addresses, particularly default addresses
- Implement role-based access control (RBAC) to ensure only authenticated account owners or admin staff can add/modify customer addresses
- Log all address modifications with user identity and timestamp for audit trail
- Validate that wholesale registration requests originate from the actual email account owner
- Separate wholesale customer account creation from address modification workflows
- Implement rate limiting on registration endpoints to prevent enumeration attacks

## Variant hunting
Check if other customer profile fields (phone, name, etc.) can be modified via wholesale registration
Test if the vulnerability exists in other checkout flows or registration endpoints
Verify if customer data from wholesale accounts can be used to manipulate B2B accounts
Test account recovery/password reset mechanisms using modified addresses
Check if addresses added via this method bypass address validation rules
Investigate if invoice/billing addresses are affected separately from shipping addresses
Test if API endpoints for customer address management have the same authorization bypass

## MITRE ATT&CK
- T1190
- T1556
- T1098
- T1021
- T1111

## Notes
This is a critical business logic vulnerability in a multi-tenant e-commerce platform. The impact could extend to fraud, supply chain compromise, and customer data manipulation at scale. The vulnerability appears to stem from inadequate separation of concerns between wholesale and retail customer flows, and insufficient input validation on email-based customer lookups. The attacker requires no prior authentication, making this a high-risk vulnerability. The reporter's mention of IDOR classification is accurate—the system allows modification of resources (customer addresses) belonging to other users (different email owners) without proper authorization.

## Full report
<details><summary>Expand</summary>

Customers in the shopify store can be added manually or automatically, an example is added automatically when you want to checkout (here we don't need to checkout) just by proceeding to "Continue to shipping" information will be sent directly to the customer such as email address and other things but when we do this again by filling in the same email with a different address then the address on the customer overview admin will not change or be added maybe this is the behavior expected by shopify because to avoid someone without access to change and add an address on existing customer but I found a vulnerability here that causes attackers to add addresses to customers even though they do not have admin rights or staff 

Step to reproduce :

1. Setting your shopify wholesale store and activate "Customers must provide an address" then save
2. Register and add business address at wholesale store and using another customers email then click sign up
3. Now on the shopify store, check on the customer whose email we used to register at wholesale, there will be an address that we just added via wholesale registration.

It will be dangerous if the shopify wholesale store activates the "Customers must provide an address" feature because attackers can add default addresses to customers without having any admin acces or staff and this maybe idor because we can add other customer addresses without having access but you can decide for yourself

## Impact

Vulnerabilities that cause attackers to add customer default addresses without having admin/staff rights should be only admins and staff can change and add customer default addresses, but here attackers who have no access admin/staff can add default addresses to customers, this can have an impact takeover default addresses that attackers can use to replace the default addresses of other customers

</details>

---
*Analysed by Claude on 2026-05-24*
