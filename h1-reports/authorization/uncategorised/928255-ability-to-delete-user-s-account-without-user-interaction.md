# Account Deletion Without User Interaction via Spoofed GDPR Requests

## Metadata
- **Source:** HackerOne
- **Report:** 928255 | https://hackerone.com/reports/928255
- **Submitted:** 2020-07-20
- **Reporter:** hx01
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Insufficient Authentication, Lack of Verification, Email Spoofing, GDPR Compliance Violation, Account Takeover
- **CVEs:** None
- **Category:** uncategorised

## Summary
GitLab's GDPR Right to Delete process lacks proper verification mechanisms, allowing attackers to spoof emails from victim addresses and trigger account deletion without authentication or identity verification. The system processes deletion requests based solely on email address without secondary confirmation like security questions, government ID, or date of birth validation.

## Attack scenario
1. Attacker identifies target GitLab user account to compromise
2. Attacker crafts a spoofed email appearing to originate from victim's registered email address
3. Attacker sends spoofed GDPR deletion request to gdpr-request@gitlab.com using third-party SMTP service (e.g., SendGrid) to bypass email authentication checks
4. GitLab system receives request and validates only the sender's email address without secondary verification
5. Victim receives confirmation email about account deletion request but cannot cancel or verify
6. Account is automatically deleted within days, permanently removing user access and associated data

## Root cause
GitLab implemented GDPR Right to Delete functionality without implementing proper identity verification controls. The system trusts email headers without validating sender identity through secondary authentication factors (security questions, government ID, OTP, or in-person verification). Email authentication mechanisms (SPF/DKIM/DMARC) were either not enforced or not properly implemented to prevent email spoofing.

## Attacker mindset
An attacker seeking to disrupt service availability, destroy user accounts, or cause denial of service would exploit this vulnerability as a low-effort, high-impact attack requiring only knowledge of target email addresses and access to an SMTP relay service. This demonstrates a 'spray and pray' mentality where minimal effort yields maximum damage.

## Defensive takeaways
- Implement multi-factor verification for account deletion requests: require security questions, government ID verification, or identity document upload
- Mandate user-initiated confirmation through secondary channel (SMS, authenticator app, or in-app notification) separate from email
- Enforce strict email authentication (SPF, DKIM, DMARC) and verify DMARC alignment for sensitive requests
- Implement rate limiting on GDPR requests per email address to detect abuse patterns
- Add account deletion request cooldown period (24-72 hours) requiring active user confirmation
- Log all deletion requests with detailed audit trail including IP address, timestamp, and verification status
- Require government-issued ID verification (passport, driver's license) for account deletion matching registration details
- Implement knowledge-based authentication (KBA) questions set during account creation
- Send deletion confirmation emails with clickable approval link that expires after short window
- Escalate requests to manual review team for high-value accounts or unusual patterns

## Variant hunting
Test other GDPR rights implementation (Right to Access, Right to Rectification) for similar verification gaps
Attempt email spoofing on password reset flows using similar SMTP relay techniques
Test if API endpoints for account management have similar email-only authentication
Investigate whether other platforms accepting legal requests (abuse reports, copyright claims) have identical verification bypasses
Check if organization deletion requests have similar vulnerabilities affecting multiple users
Test cross-tenant attacks if GitLab handles multiple organizations
Verify if impersonation is possible through other communication channels (support tickets, API keys)

## MITRE ATT&CK
- T1187
- T1566.002
- T1078.001
- T1531
- T1561
- T1485

## Notes
This vulnerability represents a critical compliance and security failure. The attack requires minimal resources (basic SMTP knowledge) and produces catastrophic results (permanent account deletion). GitLab's failure to implement GDPR-compliant verification procedures violates Article 12(2) of GDPR which requires controllers to authenticate data subject requests. The vulnerability affects account confidentiality, integrity, and availability. The report demonstrates the attacker successfully deleted a test account, proving practical exploitability.

## Full report
<details><summary>Expand</summary>

### Summary:
Gitlab allows its user to exercise their GDPR rights (Right to Access/Delete) user data by sending an email to gdpr-request@gitlab.com however gitlab team doesn't ask for security question(i.e Date Of Birth) before deleting the user account moreover doesn't authenticate the incoming emails from their  instance which allows an attacker to delete user accounts without user interaction :
██████

### Steps to reproduce
1. Send an spoofed email from victim's email address to gdpr-request@gitlab.com from a reputable SMTP (e.g: Sendgrid):
███████
2. Victim will receive the following  confirmation email:

{F914565}
3. In the next few days victim's account will be deleted :

██████

### Fix :
* Add second verification i.e ask for DOB,Government ID.

## Impact

Since Gitlab doesn't verify the request with an Valid ID before triggering Right to Access/Deletion this breaches the GDPR Law(Article 15) & moreover allows an attacker to delete User Accounts without user interaction.

</details>

---
*Analysed by Claude on 2026-05-24*
