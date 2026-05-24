# Unauthorized User Can Delete Any User Account via Email-Based Support Ticket System

## Metadata
- **Source:** HackerOne
- **Report:** 803141 | https://hackerone.com/reports/803141
- **Submitted:** 2020-02-24
- **Reporter:** d4rk_g1rl
- **Program:** NordVPN
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Broken Authentication, Broken Authorization, Insufficient Verification of User Identity, Account Takeover, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
NordVPN's help desk system allowed unauthorized users to create support tickets using any victim's email address, which could then be used to perform account deletion actions without proper verification. An attacker could send an email to the support system using a victim's email address to create a ticket, subsequently using that ticket to delete the victim's account entirely from the database.

## Attack scenario
1. Attacker identifies target victim email address registered with NordVPN
2. Attacker navigates to NordVPN login page and locates email-based ticket creation form
3. Attacker submits support ticket form using victim's email address without authentication
4. System creates support ticket associated with victim's account due to email matching
5. Attacker uses created ticket to request account deletion action
6. NordVPN processes account deletion request without secondary verification, permanently removing victim's account from database

## Root cause
Lack of proper authentication and authorization controls on the help desk ticket creation and processing system. The system trusted email addresses as sufficient proof of account ownership without implementing secondary verification mechanisms (PIN codes, confirmation emails, verification links) before performing critical actions like account deletion.

## Attacker mindset
Opportunistic attacker seeking to cause disruption or harm to targeted users by discovering that email alone could impersonate account owners in support systems. Attacker likely performed reconnaissance to identify the email-based ticket creation feature and tested it against known target email addresses.

## Defensive takeaways
- Implement multi-factor verification for critical account actions (deletion, email changes, password resets)
- Require PIN codes or one-time verification codes sent to registered email for sensitive operations
- Implement email confirmation with time-limited verification links for destructive account actions
- Add authentication requirements to support ticket creation systems; disallow unauthenticated ticket submission
- Implement account deletion confirmation workflows with mandatory user interaction
- Log and audit all critical account modifications with clear user identity verification
- Separate ticket creation from account actions; require explicit user authentication within their account panel for account modifications
- Implement rate limiting and anomaly detection on account deletion requests

## Variant hunting
Check if other critical actions (password reset, payment method changes, subscription modifications) can be triggered via unauthenticated support tickets
Test whether authenticated users can delete other accounts by submitting support tickets with different email addresses
Verify if ticket system validates sender email domain or allows spoofed email creation
Check if account recovery options suffer from similar email-only verification weaknesses
Test if API endpoints for account management have similar authorization bypasses
Examine two-factor authentication bypass vectors in the ticket-to-action workflow

## MITRE ATT&CK
- T1190
- T1078
- T1566
- T1589
- T1598
- T1021

## Notes
This vulnerability represents a critical account takeover vector affecting all NordVPN users. The attacker required no authentication, made requests from external systems, and could cause permanent data loss. The writeup demonstrates actual proof-of-concept with victim screenshots showing deleted accounts. This is a chained vulnerability combining weak identity verification with insufficient authorization controls on destructive operations. The root cause stems from design flaw rather than implementation bug - the entire ticket-to-action pipeline lacked proper security controls.

## Full report
<details><summary>Expand</summary>

###DESCRIPTION:

Your help desk allows creating tickets by email. Which means the user can send an email to the NordVPN support email to a add a new ticket to his activities. So when you send an email to `support@nordvpn.com` from your email address, this ticket will be created on the account that you have registered with the email.

###Steps To Reproduce:

1. Navigate this page:

        https://ucp.nordvpn.com/login/ 

2. Try to click the Email button below.
3. Try to fill up the form. See my attached photo.
{F726511}
4. As you notice I am not Authorized User and has no account in NordVPN.
5. Try to use the victim Email when deleting an account.
6. Few hours later.
7. The account of the victim was deleted successfully.

######Victim 1 :
{F726515}
######Victim 2 :
{F726516}

#####Note: The account was remove from the database

###Recommendation fix

* Critical actions like changing email or close account should be verify by sending PIN code to user email and asks him to reply back the code again.
* The second fix and I don’t like is disable creating tickets via your support email for more security
* Sending a confirmation link when deleting an account


Regards,

## Impact

The Unauthorized User Can Delete Any User Account

</details>

---
*Analysed by Claude on 2026-05-24*
