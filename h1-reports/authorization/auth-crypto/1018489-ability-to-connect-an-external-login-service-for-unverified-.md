# Ability to connect external login service for unverified emails/accounts at accounts.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 1018489 | https://hackerone.com/reports/1018489
- **Submitted:** 2020-10-25
- **Reporter:** saltymermaid
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Missing Email Verification Validation, Account Takeover, Authentication Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can connect external login services (e.g., Google) to any Shopify account without email verification by directly accessing the external-login endpoint via injected HTML/DOM manipulation. This enables account takeover by creating backdoor authentication methods on accounts the attacker doesn't own, particularly targeting unverified accounts created with victim email addresses.

## Attack scenario
1. Attacker creates a Shopify account at partners.myshopify.com using victim's email address
2. Attacker obtains the newly created account ID from the profile page URL
3. Attacker injects HTML link to external-login endpoint via browser console without triggering email verification
4. Attacker clicks injected link and authenticates with their own Google account
5. External login service gets connected to victim's unverified account despite UI restriction
6. Attacker can now login as victim at partners.shopify.com using 'Log in with Google' on subsequent login attempts

## Root cause
Server-side validation of email verification status is missing or not enforced before processing external login service connection requests. The application relies on client-side UI restrictions ('Please verify your email address to connect a login service') without backend validation, allowing direct endpoint access to bypass this check.

## Attacker mindset
Account takeover and persistence mechanism - attacker seeks to gain unauthorized access to merchant accounts and establish backup authentication methods that circumvent email verification controls. Targeting unverified accounts to exploit the account creation window before legitimate users verify ownership.

## Defensive takeaways
- Implement server-side validation to enforce email verification requirement before accepting external login service connections
- Validate user intent and authorization on all sensitive state-changing operations, not just UI-level restrictions
- Add rate limiting and anomaly detection on account modification endpoints, especially around authentication method changes
- Implement CSRF tokens on external login connection endpoints to prevent unauthorized requests
- Log all external login service connection attempts with IP, timestamp, and user agent for audit trails
- Send verification emails to users when external login services are connected to accounts
- Consider implementing step-up authentication for sensitive operations like adding login methods

## Variant hunting
Check other account modification endpoints that may have similar email verification bypasses
Test password reset functionality on unverified accounts - may allow takeover without external services
Examine 2FA/MFA setup endpoints for email verification enforcement
Test recovery code generation and modification without email verification
Check if other external login providers (GitHub, Microsoft, etc.) have similar vulnerabilities
Test cross-tenant account linking or shop access permissions without email verification
Examine API endpoints for external-login functionality - may lack same protections as web UI

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1598
- T1187
- T1111

## Notes
The vulnerability relies on direct endpoint access bypass rather than complex exploitation. The attacker demonstrates good understanding of account enumeration (obtaining victim account ID). The report mentions a POC video was planned. This is a classic example of security-by-obscurity (hiding endpoint behind UI) rather than true security controls. The attack specifically targets the account creation to verified account window, which is a realistic attack window in practice.

## Full report
<details><summary>Expand</summary>

Hi,

## Description
I have found that it is possible to add external login service even if the email address is not verified. This allows someone to create an account with an email he does not own and create some kind of backdoor accounts that would allow him to get access to shops and more.

In the external login services of the profil, it is said that **You do not have an external login service connected to your Shopify ID. Please verify your email address to connect a login service.**. So one should not be able to connect and external login account if the email was not verified.

{F1051426}

## Steps de reproduce
1. Create a new account at `partners.myshopify.com` with the victim email (saltymermaid+victim@wearehackerone.com)

2.  The account is created, now go to your profile at  https://accounts.shopify.com/accounts/{account_id}`

3. In the external login service section or anywhere else in the page, with your browser developper console, add the following HTML snippet `<a href="/accounts/{victim_account_id}/external-login/1" data-method="post">Connect to Google</a>` and replace the **{victim_account_id}** with the victim's account id from the url.

4. Now click on the link you injected in the page and it will bring you too the google account authentication page

5. Connect to your google account or create a new one. You will be redirected to the victims account uppon success.

6. Notice that the external login account was added even if the email was not verified.

7. Now, on another browser, go to https://partners.shopify.com/organizations, enter the victims email address and notice that **Log in with Google** button is shown. You should be able to connect that the "backdoor" account.

## Impact

Ability to create backdoors login accounts via external login services for an account that was not verified could lead to important information disclosures. I think the chances of this happening  are low since a victim would be carreful after receiving the shopify confirmation email but in somes cases, this could lead to important leak of informations.

If you need extra details, just le me know. I will make a POC video soon.

Thank you.

</details>

---
*Analysed by Claude on 2026-05-24*
