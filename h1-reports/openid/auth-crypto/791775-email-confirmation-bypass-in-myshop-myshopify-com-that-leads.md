# Email Confirmation Bypass Leading to Full Account Takeover via Shopify SSO

## Metadata
- **Source:** HackerOne
- **Report:** 791775 | https://hackerone.com/reports/791775
- **Submitted:** 2020-02-09
- **Reporter:** ngalog
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Email Verification Bypass, Privilege Escalation, Account Takeover, Logic Error, Insufficient Input Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A critical vulnerability in Shopify's email confirmation system allows attackers to confirm arbitrary email addresses by exploiting a logic flaw where confirmation links are sent to the original email instead of the new email being verified. By combining this with Shopify's SSO integration feature, attackers can takeover any store by knowing only the owner's email address and setting a master password across all integrated accounts.

## Attack scenario
1. Attacker signs up for a free Shopify trial using attacker@gmail.com (an email they control)
2. Attacker navigates to account profile and changes the email address to target@example.com (victim's email)
3. Shopify's email system sends the confirmation link for target@example.com to attacker@gmail.com instead of the new email
4. Attacker receives the confirmation email and clicks the link, successfully confirming target@example.com as their account email
5. Attacker logs into their test store and accesses SSO integration feature which detects other Shopify accounts under target@example.com
6. Attacker sets a master password for all integrated accounts, gaining full control of victim's Shopify stores

## Root cause
The email confirmation system failed to validate that confirmation links should be sent to the new email address being confirmed rather than the currently registered email address. The system maintained the original email as the recipient while updating the confirmation token for the new email, creating a mismatch between intent and implementation.

## Attacker mindset
An attacker with knowledge of a Shopify store owner's email address can systematically takeover their entire Shopify infrastructure without needing access to the owner's email inbox or original credentials. The attacker simply needs to control any email account to initiate the attack, making this a low-friction, high-impact attack requiring minimal reconnaissance.

## Defensive takeaways
- Always send email verification links to the NEW email address being verified, not the current email on file
- Implement verification token validation that confirms the token matches both the user context and the email being confirmed
- Require verification of the old email address before allowing email changes (confirmation of old email + confirmation of new email)
- Add rate limiting and anomaly detection to account changes, especially email modifications followed by immediate SSO integrations
- Implement additional authentication factors for account integration features or password changes
- Log and alert on email change attempts, particularly those followed by SSO account integrations
- Add a delay period between email confirmation and SSO integration features to allow account owners to detect unauthorized changes

## Variant hunting
Check if other user-modifiable account attributes (phone, backup email) have similar confirmation bypass issues
Test if password reset flows are vulnerable to the same email misdirection logic error
Investigate whether other Shopify subdomains or services share the vulnerable email confirmation code
Examine if the SSO integration feature can be exploited through other account modification vectors
Test if similar logic errors exist in other Shopify business products or partner integrations
Check if two-factor authentication setup uses the same vulnerable email confirmation mechanism

## MITRE ATT&CK
- T1190
- T1566
- T1187
- T1598
- T1621
- T1111
- T1556

## Notes
This vulnerability demonstrates a critical design flaw in email verification logic that has severe consequences due to Shopify's SSO integration feature. The attack requires no sophisticated technical skills, only knowledge of a target email address. The reporter demonstrated the vulnerability against h31ngalog.myshopify.com showing it was actively exploitable. The casual greeting ('I told Pete I would take a look at Spotify, hi Pete') suggests the reporter may have been triaging or investigating related reports. The vulnerability exemplifies how seemingly minor logic errors in email verification can cascade into complete account takeover when combined with other legitimate platform features.

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
