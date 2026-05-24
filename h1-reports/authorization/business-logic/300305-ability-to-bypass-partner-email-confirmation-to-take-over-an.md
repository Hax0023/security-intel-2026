# Partner Email Confirmation Bypass via Race Condition to Takeover Store Accounts

## Metadata
- **Source:** HackerOne
- **Report:** 300305 | https://hackerone.com/reports/300305
- **Submitted:** 2017-12-24
- **Reporter:** cache-money
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Race Condition, Email Verification Bypass, Account Takeover, Insufficient Transaction Isolation
- **CVEs:** None
- **Category:** business-logic

## Summary
A race condition in Shopify's partner email verification system allows an attacker to confirm ownership of arbitrary email addresses, enabling complete takeover of any store account. By simultaneously requesting email validation for an owned email while changing the partner account email to a victim's address, the attacker can bypass email confirmation controls through improper database transaction handling.

## Attack scenario
1. Attacker creates a partner account and obtains a valid email confirmation link for their own email address
2. Attacker initiates a request to change their partner account email to the target store employee's email address
3. While the email change request is processing (1,100-2,500ms window), attacker quickly validates their original email confirmation link in a parallel request
4. Due to missing or improper transaction isolation, the email validation completes against the victim's email address despite ownership never being verified
5. Attacker's partner account now shows the victim's email as confirmed and validated
6. Attacker adds the victim's store as a managed store through the compromised partner account, gaining full store access

## Root cause
The email verification system lacks proper database transaction isolation when processing concurrent requests. The application fails to atomically validate that the email being confirmed matches the email currently being changed, allowing a race condition where validation of one email address gets applied to a different address during the update window.

## Attacker mindset
An attacker with knowledge of store employee email addresses can systematically compromise any Shopify store by exploiting the timing window in email verification. The attacker needs only to know the target employee's email—no credentials or existing access required. The vulnerability is highly reproducible with basic timing manipulation.

## Defensive takeaways
- Implement database transactions that atomically validate and update email addresses—verification tokens must be bound to specific email addresses with transaction-level consistency checks
- Add email validation state tracking that prevents confirmation of emails that differ from the pending email change request
- Implement strict request-level locking or sequencing to prevent concurrent email modification and verification operations on the same account
- Add rate limiting and temporal constraints on email verification link usage relative to email change requests
- Include email ownership verification checks at the point of confirming validation, not just at token generation
- Add logging and alerting for email changes to different domains or bulk confirmation attempts
- Consider adding a confirmation step requiring the target email to explicitly approve the change (double opt-in)

## Variant hunting
Check for similar race conditions in password reset workflows where confirmation tokens are issued but account state is modified concurrently
Examine two-factor authentication enrollment for timing-based bypasses between device registration and confirmation
Test account recovery flows for race conditions between identity verification and credential reset
Review any workflow involving email validation tokens combined with concurrent account modification operations
Hunt for transaction isolation issues in account merging or conversion workflows (user to collaborator conversions referenced in the bug)

## MITRE ATT&CK
- T1190
- T1078.001
- T1199
- T1550.001

## Notes
The reporter explicitly references a previous security report (#270981) indicating this vulnerability exists in a system designed to automatically convert user accounts to collaborator accounts when partner invitations are accepted. The race condition window of 1,100-2,500ms is substantial enough to reliably exploit manually. The vulnerability chain is elegant: partner account email validation + account takeover + managed store access = complete store compromise. Shopify's partner ecosystem has significant trust implications, making this a high-impact vector.

## Full report
<details><summary>Expand</summary>

I told Pete I would take a look at Spotify, hi Pete.

**Summary**
It's possible to take over any store account through partners given an employee email address. This is possible because I found a way to confirm arbitrary emails. I don't know the Shopify ecosystem well enough to know the other ramifications of such a bug.

On #270981 you wrote:
> The intention was that, when a partner already had a valid user account on the store, their collaborator account request could be accepted automatically, with the user account converted into a collaborator account.

I tested that functionality and confirmed how it works. I realized that if you can somehow create a partner account with a business email that matched that of an employee, you would be able to take over their employee account, then convert it to a collaborator. The problem is that business accounts need emails to be validated, but this can be bypassed with a race condition.

The bug works by hitting the email validation endpoint for an email you own, at the same time as changing your email to a victim's. It might take a few tries, but eventually your email will be changed and be validated due to not (properly) using a DB transaction.

**Steps to reproduce**
1. Create a store account and invite an employee.
2. Accept the employee invite (maybe not necessary I didn't test).
3. Login to or create a partner account as the attacker.
4. Go to your partner settings page `https://partners.shopify.com/[ID]/settings` and change your email to something you own.
5. Check your email and grab the confirmation link, but don't visit it yet.
6. Go back to your partner account and change your email to that of the store employee from step 2, but intercept the request to not let it through yet.
7. Now the tricky part. The "change email" takes anywhere from 1,100 - 2,500 ms to load so you need to take that into account. But let the request go through, wait for some milliseconds, then in another tab visit that email confirmation link from step 5.
8. If done correctly you will now have confirmed an email you do not own.
9. Visit `https://partners.shopify.com/[ID]/managed_stores`, add the store, and you now have access.

As proof, look at the email for partner account `698396`. It will be confirmed `cache@hackerone.com`, which I obviously would never be able to validate otherwise.

Thanks,
-- Tanner

## Impact

Ability to take over stores, and possibly perform any other action that relies on a validated email as a security measure.

</details>

---
*Analysed by Claude on 2026-05-24*
