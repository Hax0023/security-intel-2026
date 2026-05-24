# Removed Staff Members Can Still Create Development Stores via Non-Expiring Affiliate Signature

## Metadata
- **Source:** HackerOne
- **Report:** 254588 | https://hackerone.com/reports/254588
- **Submitted:** 2017-07-29
- **Reporter:** zombiehelp54
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Authorization/Access Control Bypass, Privilege Escalation, Insecure Direct Object References (IDOR), Lack of Token/Session Invalidation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A non-expiring affiliate shop signature token remains valid even after a staff member is removed from an organization, allowing revoked users to create development stores that appear under the organization's account. The signature is static per organization and never invalidated when staff access is revoked, creating a persistent unauthorized access vector.

## Attack scenario
1. Attacker is added as a staff member to a target organization with 'Manage Shops' permission
2. Attacker captures the `extra[affiliate_shop]` signature parameter from the development store creation page source
3. Attacker is removed from the organization by the organization owner
4. Attacker crafts a POST request to `https://app.shopify.com/services/signup/setup` using the previously captured static signature
5. Attacker submits the form with a new shop name and email address, creating a development store
6. The new store appears in the organization's development stores list despite the attacker no longer having staff access

## Root cause
The affiliate shop signature used to link development stores to an organization is static, organization-wide, and never invalidated upon staff member removal. The backend lacks proper authorization checks to verify current staff membership and permissions before accepting store creation requests with the affiliate signature.

## Attacker mindset
Insider threat scenario: A disgruntled former employee or contractor with prior 'Manage Shops' access can maintain unauthorized control over partner organization resources indefinitely. The ability to create stores under a competitor or target organization could be used for fraud, brand impersonation, or competitive sabotage.

## Defensive takeaways
- Implement time-limited, per-user tokens for sensitive operations instead of static organization-wide signatures
- Invalidate or rotate all affiliate signatures when staff members are removed from an organization
- Add backend authorization checks to verify current staff membership and permissions before processing store creation requests
- Log all store creation attempts and cross-reference against current staff roster in real-time
- Require re-authentication or session refresh for sensitive partner operations like store creation
- Implement audit trails linking store creation to specific user sessions with timestamps
- Consider requiring explicit owner approval for development store creation by any staff member

## Variant hunting
Check if other affiliate/partner operations (shop deletion, modification, linking) use similar non-expiring static signatures
Test if removed staff can perform other privileged organization actions using cached credentials or tokens
Investigate if other Shopify partner endpoints accept organization-level tokens without validating current user permissions
Search for similar patterns in other SaaS platforms where organization-wide tokens are used instead of user-specific credentials
Test if the signature can be reused across different organizations or user accounts
Check if team role changes (permission downgrades) similarly fail to invalidate cached signatures

## MITRE ATT&CK
- T1078.001 - Valid Accounts: Default Accounts (captured affiliate signature acts as persistent valid account)
- T1098.001 - Account Manipulation: Additional Cloud Credentials (signature persists after removal)
- T1190 - Exploit Public-Facing Application (signup endpoint exploitation)
- T1550 - Use Alternate Authentication Material (static signature used as authentication bypass)
- T1556 - Modify Authentication Process (signature validation missing current authorization checks)

## Notes
This is a critical privilege persistence vulnerability in a multi-tenant SaaS environment. The static nature of the signature and lack of expiration creates a particularly dangerous scenario where insider knowledge combined with timing (removal lag or intentional disassociation) can grant indefinite unauthorized access. The vulnerability would be exploitable at scale if attackers could enumerate or predict affiliate shop signatures.

## Full report
<details><summary>Expand</summary>

## Details: 
It's been found that staff members of an organization in partners.shopify.com can have a permission to manage shops and those with that permission can create development stores that will be associated with the organization.

When a staff member tries to create a development store, a POST request is sent to `https://app.shopify.com/services/signup/setup` with the parameter `extra[affiliate_shop]` as the signature used to link the shop with the partners account.

It's been found that this signature is the same for all staff members of the same organization and it doesn't expire which means that if a staff member had "Manage Shops" permission for only one time, then he was removed from the organization he will still be able to create development stores associated with the organization and they will appear in `https://partners.shopify.com/[id]/development_stores` for organization members. 

## Steps to reproduce: 
1. Add a new staff member to your organization with "Manage Shops" permission. 
2. Login with the staff member you just added then navigate to `https://partners.shopify.com/641767/development_stores/new` and grab the value of `extra[affiliate_shop]` parameter from the source of the page.
3. Through the owner account remove the user's access to the organization. 
4. Through the new staff member who no longer has access submit the following HTML form: 

```
<form action="https://app.shopify.com/services/signup/setup" method=post>
<input name="utf8" value="Γ£ô">
<input name="authenticity_token" value="67uDHcA5IBtc1CRcl3teDJND+2w8ahtpbNo4aux93TfHq0MkadWVOPG0h/8Z+jjcWpXw96fX1BbnYTLiG9aqDw==">
<input name="signup[shop_name]" value="NewStoreTestTest1234">
<input name="signup[email]" value="testmahmoud16+2@gmail.com">
<input name="signup[password]" value="P@ssw0rd">
<input name="signup[confirm_password]" value="P@ssw0rd">
<input name="signup_types" value="affiliate_shop">
<input name="signup_source" value="development+shop">
<input name="signup_source_details" value="">
<input name="extra[affiliate_shop]" value="[SIGNATURE]">
<input name="signup[address1]" value="testxx">
<input name="signup[city]" value="test'ad">
<input name="signup[zip]" value="">
<input name="signup[province]" value="DK">
<input name="signup[country]" value="EG">
<input type=submit>
</form>
```
*Replace the value of `extra[affiliate_shop]` with the one you got through the staff member*

5. Navigate to `https://partners.shopify.com/[id]/development_stores` through the owner account and you'll see the new store added to the organization even though the staff member no longer has access.

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
