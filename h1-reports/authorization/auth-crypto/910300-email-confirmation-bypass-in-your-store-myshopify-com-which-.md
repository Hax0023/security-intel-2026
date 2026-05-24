# Email Confirmation Bypass Leading to Account Takeover on Shopify Partners

## Metadata
- **Source:** HackerOne
- **Report:** 910300 | https://hackerone.com/reports/910300
- **Submitted:** 2020-06-28
- **Reporter:** say_ch33se
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Email Verification Bypass, Privilege Escalation, Account Takeover, Insecure Direct Object Reference (IDOR), Session Manipulation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A critical vulnerability in Shopify's partner account management allows attackers to bypass email confirmation requirements and take over accounts without SSO protection. By manipulating HTTP requests through Burp Suite to replace email addresses in confirmation flows, an attacker can verify arbitrary email addresses and subsequently gain full access to victim accounts and associated stores.

## Attack scenario
1. Attacker creates a partner account and new store without verifying their email
2. Attacker navigates to account settings and changes their email to the victim's email address
3. Using Burp Suite match/replace rules, attacker intercepts requests and substitutes the victim's email throughout the session
4. Attacker performs actions requiring confirmation (profile photo upload) while email is set to victim's address via proxy interception
5. Attacker changes email back to their own address and receives confirmation link to their email, which they click while proxy is still replacing emails
6. Attacker completes the email verification process, then sets up Shopify ID and password recovery to gain persistent access to victim's account

## Root cause
The application fails to properly validate and bind email verification tokens to the actual email address being confirmed. The verification flow does not verify that confirmation requests originated from the email address being confirmed, allowing request manipulation via proxy to bypass this control. Additionally, session state management allows email changes without proper confirmation at critical points.

## Attacker mindset
Opportunistic account takeover targeting non-SSO protected accounts. The attacker discovered this through testing edge cases in the email verification flow and realized that HTTP-level email substitution was not properly validated server-side. The detailed step-by-step nature suggests deliberate exploration of the confirmation mechanism.

## Defensive takeaways
- Implement server-side validation that confirmation tokens are bound to specific email addresses and user IDs, not just generic verification codes
- Require out-of-band verification (confirmation link sent to NEW email must be clicked from that email or confirmed by the user at that address)
- Do not allow email changes to take effect until verification is complete; maintain previous email as primary until new email is confirmed
- Implement additional friction for sensitive operations: require password re-entry, security questions, or push notifications for email changes
- Add logging and alerting on email change attempts, especially when followed by account recovery or SSO setup
- Ensure that critical account modifications (Shopify ID setup, password changes) require additional authentication beyond session tokens
- Implement rate limiting on email change requests and account recovery flows
- Validate all user-supplied data on both client and server side; do not rely on proxy-level request manipulation being prevented

## Variant hunting
Test other account settings changes (phone number, security questions) for similar email substitution vulnerabilities
Check if password reset flows have the same email binding issue
Test whether the vulnerability works with encoded or alternative email formats (plus addressing, domain variations)
Verify if two-factor authentication setup is also bypassable through similar mechanisms
Check if the vulnerability affects other Shopify services beyond partner accounts
Test API endpoints for the same email verification bypass patterns
Investigate if organization/team member invitations have similar flaws
Check if the match/replace technique works on other confirmation-based flows (subscription changes, payment method verification)

## MITRE ATT&CK
- T1190
- T1566
- T1199
- T1021
- T1078
- T1556
- T1111

## Notes
This is a sophisticated attack requiring multiple steps and deep understanding of the authentication flow. The attacker's use of Burp Suite match/replace rules indicates this is a manual security testing technique. The vulnerability is particularly dangerous because it affects the Shopify Partners program, which manages both stores and developer accounts. The reliance on SSO as the 'protection' suggests Shopify may have been aware of this flow but considered SSO mandatory for high-value accounts. The attack demonstrates a fundamental flaw in how email verification tokens are validated—the server likely validates the token exists but not that it matches the email in the current session context.

## Full report
<details><summary>Expand</summary>

Hello Shopify, I have found a bug by which I can verify any email on .myshopify.com, the bug is very strange but it works. Also I can take over the accounts but only the ones which do not have SSO.

To reproduce please follow the steps exactly as I written otherwise you will not be able to reproduce it.

Steps to reproduce: 

1. Go to your partners account and make a store
{F886149}

2. Go to your new store and don't verify email, then go to admin/settings/account/youraccountnumber
{F886151}

3. Change your email to victims email(in my case say_ch33se+111@wearehackerone.com)
{F886138}

4. Go to burps match and replace and replace your email with the email you want to takeover(in my case say_ch33se+111@wearehackerone.com)
{F886137}
{F886139}
{F886140}

5. Refresh the account page so its updated with victims email
{F886141}

6. Still on accounts page click on Upload photo and upload any photo and save
{F886142}

7. After that uncheck match and replace, refresh and on accounts page change email to your email which you own so you can get a confirmation email
{F886143}

8. In burp check match and replace again to replace your email with the email you want to takeover(same as above)
9. Go to your email which you own where is the confirmation link and click on it(in the browser where you are already logged in)
10. On that page where you verified email, upload another image
{F886144}

11. Now click on Review accounts
12. Enter stores password and you'll be greeted with Shopify ID
13. Click on Set up Shopify ID
{F886145}

14. And there you got it
{F886146}

15. Click continue and set up password
{F886147}
{F886148}

16. Now you can access vitims store and partner account without any problems

## Impact

Ability to confirm any email on your-store.myshopify.com and leverage SSO to take over accounts.

</details>

---
*Analysed by Claude on 2026-05-24*
