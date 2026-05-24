# Email Confirmation Bypass Leading to Full Account Takeover via Shopify SSO

## Metadata
- **Source:** HackerOne
- **Report:** 791775 | https://hackerone.com/reports/791775
- **Submitted:** 2020-02-09
- **Reporter:** ngalog
- **Program:** Shopify (HackerOne #791775)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Email Confirmation Bypass, Privilege Escalation, Account Takeover, Authentication Flaw, SSO Abuse
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can bypass email confirmation in Shopify by changing their email address before confirming the original signup email, causing the system to send the confirmation link for the new email to the original email address. This allows confirming arbitrary email addresses, which when combined with Shopify's SSO account integration feature, enables complete takeover of any Shopify store by knowing only the owner's email address.

## Attack scenario
1. Attacker signs up for a Shopify free trial using attacker@gmail.com (an email they control)
2. Attacker navigates to profile settings and changes the email to a target victim's email (e.g., victim@company.com) before confirming the original email
3. Shopify's email system sends the confirmation link for victim@company.com to attacker@gmail.com (the original email on file)
4. Attacker clicks the confirmation link in their own inbox, confirming the victim's email address in their Shopify account
5. Attacker navigates to account integration settings which detect other Shopify stores registered under victim@company.com
6. Attacker confirms integration of all detected stores and sets a master password, gaining full control of all victim's Shopify stores

## Root cause
The email confirmation system maintains a mismatch between the email address being changed (new email) and the email address where confirmation links are sent (original email on file). The system failed to invalidate pending confirmations when the email address was modified, and did not verify that the user initiating the confirmation actually controls the new email address before granting access.

## Attacker mindset
This attacker demonstrates sophisticated understanding of account lifecycle vulnerabilities and SSO weaknesses. By chaining two vulnerabilities (email confirmation bypass + SSO integration), they identified a complete account takeover path requiring minimal attacker effort. The disclosure methodology shows responsible security research with clear reproduction steps and impact demonstration.

## Defensive takeaways
- Implement email verification at the time of change request, not after - require confirmation from BOTH old and new email addresses
- Invalidate any pending email confirmations when an email change is initiated
- Add friction to email change operations (delay, additional authentication factors)
- Implement SSO account linking only after verifying control of all involved email addresses
- Audit account integration flows for privilege escalation opportunities
- Monitor for unusual account integration patterns (multiple accounts integrated in short timeframe)
- Require re-authentication or additional verification before accessing integration/SSO features
- Log all email change attempts and integrations with detailed audit trails
- Consider rate limiting on email change operations per account

## Variant hunting
Test password reset flows with similar email change-before-confirmation patterns
Check if other identity-linked services (API keys, OAuth tokens) have similar confirmation issues
Examine secondary email addresses or alternative contact methods for same bypass
Test SSO integration with partially-confirmed email states
Check if other Shopify properties (Partner accounts, Developer accounts) have similar vulnerabilities
Test email change during account creation flows vs. established accounts
Investigate if confirmed email change triggers re-verification in linked services

## MITRE ATT&CK
- T1190
- T1078
- T1586
- T1621
- T1556
- T1530

## Notes
This is a critical vulnerability affecting Shopify's core authentication infrastructure. The attacker demonstrated the vulnerability by successfully changing h31ngalog.myshopify.com owner email to ngalog@hackerone.com without legitimate access. The vulnerability is particularly severe because it requires minimal attacker resources (only knowing the victim's email address) and results in complete compromise of all Shopify stores under that email. The report references 'Pete' and 'Spotify' humorously, suggesting a casual disclosure tone. The vulnerability likely affected thousands of stores before patching.

## Full report
<details><summary>Expand</summary>

I told Pete I would take a look at Spotify, hi Pete.

## Summary
It's possible to take over any store account through bypassing the email confirmation step in *.myshopify.com. I found a way to confirm arbitrary emails, and after confirming arbitrary email in *.myshopify.com, user is able to **integrate** with other Shopify store that shares the same email address by setting a master password for all of the stores(if the owner hasn't integrated before), effectively taking over every Shopify stores by knowing just the owner's email address.

After signing up a new Shopify instance in https://www.shopify.com/pricing and start the free trial, user can change their email address to a new email address before confirming the one they used to sign up.

The bug is that Shopify email system mistakenly send the confirmation link of the new email address, to the one that is used to signed up.

And the result is user can confirm arbitrary email address. And the next step is taking over other user's Shopify instance by taking advantage of the SSO.

## Quick check
If you check https://h31ngalog.myshopify.com/ and see the email address of the owner, it is ngalog@hackerone.com, which I obviously would never be able to validate otherwise
{F711349}

## steps to reproduce
- Visit https://www.shopify.com/pricing and signup a free trial with an email address, say attacker@gmail.com that you can receive emails
- after entering the fields to enter the store, on top right corner, click your name and go to **Your Profile**
- change your email to someone that you want to takeover, for example yaworsk@hackerone.com and click save
- All done now, grab a coffee, sit back and relax, watch some YouTube videos and wait for an email to go to your email attacker@gmail.com
- The email that you are waiting for is from mailer@shopify.com, and the format should look like this {F711348}
- Click the link and you should see your email has been updated to yaworsk@hackerone.com

## Reason?
Email system mistakenly send the confirmation link of yaworsk@hackerone.com to attacker@gmail.com because attacker@gmail.com is the one that is saved on system, and the email system didn't notice the confirmation link has been updated to yaworsk@gmail.com, and should not be sent to attacker@gmail.com

## SSO account takeover
- now we have the ability to confirm arbitrary email, then we can takeover other stores
- On top right corner of you-shop.myshopify.com click your name then click profile, you should see a box that says, you have other two accounts in Shopify, want to integrate them together
- click yes, then just follow the instructions then you will be able to takeover all other stores by changing the master password for all of the stores under that email address.

## Impact

Ability to confirm arbitrary email on *.myshopify.com and leverage SSO to set master password for all other stores under the same password

</details>

---
*Analysed by Claude on 2026-05-24*
