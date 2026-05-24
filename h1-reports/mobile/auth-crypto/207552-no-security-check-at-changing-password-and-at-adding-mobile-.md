# Missing Security Checks on Password Change and Mobile Number Addition Leading to Account Takeover and Spam

## Metadata
- **Source:** HackerOne
- **Report:** 207552 | https://hackerone.com/reports/207552
- **Submitted:** 2017-02-19
- **Reporter:** mohith_kalyan
- **Program:** Khan Academy
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Insufficient Access Controls, Missing CSRF Protection, Missing Email/SMS Verification, Broken Authentication, Account Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Khan Academy's settings page lacks security controls when changing passwords and adding/modifying mobile numbers. An attacker with brief physical access to a logged-in account can change the password without verification, leading to permanent account takeover. Additionally, mobile numbers can be added without SMS verification, enabling attackers to spam arbitrary phone numbers using Khan Academy as the source.

## Attack scenario
1. Attacker gains temporary physical access to victim's logged-in account (5+ seconds)
2. Attacker navigates to Settings via profile dropdown menu
3. Attacker enters new password and saves without any verification challenge
4. Victim is locked out; attacker now has full account control
5. Attacker can alternatively add attacker-controlled mobile number without SMS verification
6. Victim receives spam messages from Khan Academy, or attacker uses platform to harass third parties

## Root cause
Application fails to implement standard security controls on sensitive account operations: (1) No post-authentication verification (re-entering current password) before password change, (2) No CSRF token validation, (3) No out-of-band verification (email/SMS confirmation) for new password or mobile number changes, (4) No rate limiting on account modification endpoints.

## Attacker mindset
Opportunistic attacker exploiting unattended sessions. Primary motivation is account takeover through low-friction password change. Secondary motivation is harassment capability by changing contact information or using the platform to spam arbitrary phone numbers.

## Defensive takeaways
- Require current password verification before allowing password changes
- Implement CSRF tokens on all state-changing operations
- Send confirmation emails for password changes with rollback capability
- Require SMS/email verification codes before accepting new phone numbers
- Add security questions or multi-factor authentication before sensitive account changes
- Implement rate limiting and anomaly detection on account modification endpoints
- Add login alerts when account settings are modified
- Implement session invalidation across devices after password change
- Log all account modifications with IP address and timestamp

## Variant hunting
Check email change functionality for similar verification gaps
Test if security questions can be changed without verification
Verify two-factor authentication settings can be modified without challenge
Check if linked accounts/social logins can be disconnected without verification
Test if recovery email/phone can be changed without confirmation
Verify if API endpoints for account changes have same protections as UI
Check for similar issues on other user profile modification endpoints

## MITRE ATT&CK
- T1190
- T1133
- T1556
- T1098
- T1078

## Notes
This is a classic broken authentication vulnerability compounded by missing access controls. The dual impact (account takeover + spam capability) increases severity. The low friction required for exploitation (5 seconds of physical access) makes this a practical risk. Similar vulnerabilities are common in applications that overlook security controls on settings pages, treating them as lower-risk than login endpoints.

## Full report
<details><summary>Expand</summary>

#Description

I have noticed that there is no security check at changing password. If someone gets a logged in account for 5 seconds, they are extremely likely to change the password of the account with the knowledge of the victim. also, while adding a mobile number / changing a mobile number, there is no sms / call verification which leads to spamming of any user using Khan Academy as source.

Since there is no sms verification, I could spam anyone (not necessarily khan academy user) with khan Academy notifications.


#Steps to reproduce

1. Click on the name of the profile on top right.
2. Select settings in the drop down menu.
3.  Change the password by just entering the new password, without knowing anything.
4.  Add the mobile number (if already entered, change ) of your choice, since there is no security check, they will be spammed by khan academy messages.


#Impact

Lack of security check at password change leaves a vulnerability open to attackers to change the password without knowing anything about the user.
Lack of verification of mobile while adding / changing mobile number leaves every mobile user open for spamming via Khan Academy.


#Screen shots/ References

███
F162091


</details>

---
*Analysed by Claude on 2026-05-24*
