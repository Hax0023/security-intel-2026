# Permanent DoS at Happy Tools via Unverified Email Change During User Invitation

## Metadata
- **Source:** HackerOne
- **Report:** 1041173 | https://hackerone.com/reports/1041173
- **Submitted:** 2020-11-23
- **Reporter:** boy_child_
- **Program:** Happy Tools
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service, Email Verification Bypass, Business Logic Flaw, User Enumeration
- **CVEs:** None
- **Category:** memory-binary

## Summary
Happy Tools allows users to change their email address without verification, enabling attackers to claim email addresses of other users. When an admin attempts to invite a user with a claimed email, the invitation fails permanently, denying team member additions. This represents an exception to typical DoS exclusions as it involves legitimate business functionality being abused through a verification bypass.

## Attack scenario
1. Attacker creates two accounts on Happy Tools (one with admin privileges if possible, or uses enumeration)
2. Attacker identifies target email addresses of legitimate users or generates probable email addresses through enumeration
3. Attacker navigates to preferences and changes their account email to a target user's email without email verification
4. Admin attempts to invite the target email address to their team via the invite functionality
5. Invitation fails because the email is associated with an unauthorized account and verification cannot be completed
6. Attacker repeats process with multiple emails, preventing admins from expanding their teams and causing operational disruption

## Root cause
The application implements email change functionality in user preferences without requiring email verification (confirmation link or OTP). The invitation system fails when the email belongs to an account without proper authorization context, and no validation exists to prevent email address conflicts or unauthorized claims.

## Attacker mindset
A malicious actor performing competitive sabotage, user disruption, or testing exception-to-policy DoS vectors. The attacker recognizes that many platforms exclude DoS from scope, but this variant exploits legitimate features without requiring network/resource exhaustion, potentially qualifying as a valid security issue.

## Defensive takeaways
- Implement mandatory email verification (confirmation email with token) before email changes take effect
- Enforce email uniqueness constraints at the database level to prevent multiple accounts from claiming the same email
- Add a grace period where old email remains active until new email is verified
- Implement rate limiting on email change requests per user account
- Log all email change attempts and provide admin audit trails
- Validate email ownership before accepting invitations (send verification to new email)
- Implement CAPTCHA or additional verification steps for account changes
- Consider account lockdown/review period after email changes from unusual locations/IPs

## Variant hunting
Check if phone number changes have similar verification gaps
Test if password reset flows properly validate ownership of changed email
Examine if API endpoints for email change bypass UI-level protections
Test batch user operations (bulk invites) with unverified emails
Check if email change affects existing authentication sessions
Verify if similar issues exist in connected services (WordPress, Gmail integration)
Test if subdomain email addresses or plus-addressing bypass uniqueness checks
Examine email change in context of SSO/federated identity systems

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1087
- T1499

## Notes
This report cleverly frames a business logic/verification bypass as a DoS exception. The key insight is that the vulnerability doesn't require network flooding or resource exhaustion—it abuses legitimate functionality. The impact is permission-based (requires knowing/enumerating emails) but scalable. The program's acceptance suggests they recognized this as a valid exception to their DoS exclusion policy. The unverified email change combined with no uniqueness enforcement creates a compound vulnerability worse than either alone.

## Full report
<details><summary>Expand</summary>

Hi Team,

At [Happy Tools](https://happy.tools/), I found an exception to the exclusion of denial of service. The web app allows creating an account/login into an account either using Gmail or WordPress. The vulnerability lies in the fact that after registration, a user can change their email without verification.

## Steps To Reproduce:
1. Using separate browsers or browser containers, login to two different accounts. At least one account should have admin privileges in order to invite users.
2. In the other account under the [preferences tab](https://schedule.happy.tools/preferences), notice the user email, change the email to ``boy_child@wearehackerone.com`` and save changes.
3. In the admin account under the [users tab](https://schedule.happy.tools/admin/users), click on ``Invite team members`` and input the email ``boy_child@wearehackerone.com``.
4. Scroll down and click on ``Send invite``.
5. The request will fail.
6. Repeat steps 2 to 4, but changing the email to that of other users (test accounts) and the request to send an invite link will continuously fail.

## Impact

Through user enumeration of emails and mass exploitation, there is a permanent denial of service denying a Happy Tools admin from adding team members to their organization.

</details>

---
*Analysed by Claude on 2026-05-24*
