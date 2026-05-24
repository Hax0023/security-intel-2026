# JetPack SSO Authentication Bypass via Email Invitation Verification Chain

## Metadata
- **Source:** HackerOne
- **Report:** 2037902 | https://hackerone.com/reports/2037902
- **Submitted:** 2023-06-25
- **Reporter:** hundredpercent
- **Program:** Jetpack by Automattic
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Authentication Bypass, Email Verification Bypass, Privilege Escalation, Account Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The JetPack SSO plugin contains an authentication bypass vulnerability that allows attackers to gain unauthorized admin access to WordPress instances without user interaction. By exploiting a flaw in the email verification process through WordPress.com user invitations combined with the 'Match accounts using email addresses' feature, an attacker can impersonate any user whose email exists in the target WordPress instance.

## Attack scenario
1. Attacker identifies a WordPress instance using JetPack SSO with 'Match accounts using email addresses' enabled and discovers existing user email addresses (e.g., through OSINT, directory enumeration, or error messages)
2. Attacker creates two WordPress.com accounts: one with their own confirmed email address, and a second with the target user's email address from the WordPress instance
3. Attacker uses their confirmed WordPress.com account to invite the second account (matching target email) to their user list through WordPress.com settings
4. Attacker accepts the invitation from the second account, which automatically marks that email as verified in WordPress.com without actual email confirmation
5. Attacker navigates to the target WordPress instance login page and selects 'Sign in with WordPress.com' using the second account with the spoofed email
6. The JetPack SSO plugin matches the verified WordPress.com email with the existing WordPress user email and grants admin-level access to the attacker

## Root cause
The vulnerability stems from two compounding issues: (1) JetPack's email verification process trusts user invitations as a valid confirmation method without requiring actual email ownership verification, and (2) when 'Match accounts using email addresses' is enabled, the plugin performs matching based solely on email address without proper validation of WordPress.com account ownership or linking it to the original WordPress user who registered that email.

## Attacker mindset
An attacker would recognize that invitation-based verification is weaker than direct email confirmation and that email matching without ownership validation creates an account linking vulnerability. They would systematically enumerate WordPress instances using JetPack, gather user email addresses through reconnaissance, and exploit the feature combination to gain administrative access for data theft, malware injection, or further network compromise.

## Defensive takeaways
- Require explicit user interaction or secondary verification (such as admin approval) when linking external SSO accounts to existing WordPress users, especially when matching by email
- Implement WordPress instance owner verification before allowing external SSO accounts to assume admin privileges
- Make 'Match accounts using email addresses' an opt-in feature with prominent security warnings and require email ownership re-verification during the SSO flow
- Add additional checks to validate that the WordPress.com account email was verified through primary channel (direct confirmation link) rather than accepting invitation-based verification as sufficient
- Implement rate limiting and anomaly detection on SSO authentication attempts to identify bulk account takeover attempts
- Require admin confirmation for any SSO login attempt that grants elevated privileges on first-time access
- Audit all existing SSO links created through this method and notify administrators of potentially compromised accounts

## Variant hunting
Test other Automattic products with SSO and email matching features for similar invitation bypass chains
Investigate whether other WordPress SSO providers implement similar insecure email matching patterns
Check if other user invitation flows in Jetpack/WordPress.com can bypass email verification for different account types
Test whether the vulnerability applies to non-admin user accounts or only administrators
Verify if this affects other JetPack features that may rely on email verification state
Examine whether direct WordPress.com API calls can be used to verify emails without the UI invitation flow

## MITRE ATT&CK
- T1190
- T1078.001
- T1199
- T1535
- T1556.001

## Notes
The writeup indicates real WordPress instances were tested ('As example I bypass [redacted]'), suggesting active exploitation was demonstrated. The vulnerability is particularly dangerous because it requires no user interaction on the target's side and succeeds regardless of whether the target user account was previously linked to WordPress.com. The 'Match accounts using email addresses' setting appears to be the critical enabler, suggesting organizations may have thought this was an optional advanced feature rather than a security-critical configuration. The attacker's ability to create accounts with arbitrary email addresses on WordPress.com and have them verified without ownership confirmation is a fundamental flaw in WordPress.com's account creation or invitation system.

## Full report
<details><summary>Expand</summary>

Hello team,

## Summary:
The JetPack SSO manager is plugin that allows any user to log into their wordpress using the same log-in credentials you use for WordPress.com, then they’ll now be able to register for and sign in to self-hosted WordPress.org sites quickly, example :

User creates their wordpress instance at host.com, they install and enable  JetPack SSO
They later can login into their wordpress instance at host.com using wordpress.com, users are also can make other users register/login with the same company email (@host.com) and access the administration panel of the host


## Description :
The user anyways when he tries to authenticate into his wordpress instance via wordpress.com he gotta have his email confirmed, otherwise it won't work, interstingly there is a way that bypasses the email confirmation when a user invites you to his account and you accept his invite your account will be confirmed, chaining those issues the following scenario can result for the authentication bypass of any wordpress  instance when these circumestances are met :

* wordpress installed on host.com have jetpack installed and "Match accounts using email addresses" enabled (IDK if this is necessary anyways) 
* wordpress instance have a user with specific email, that email does not exist on wordpress.com

You can access this host.com wordpress panel via

## Steps To Reproduce:
**Setup**

  1. Install Jetpack latest version, once installed go to plugins>Jetpack>settings>"Match accounts using email addresses">enable (I'm not sure if this is intended or not)
  2. Add user into your wordpress (host.com) with their email (says something@company.com)


* **As attacker (email confirmation bypass)** :
  1. Create two accounts at Wordpress.com 
        A/. One with your personal email and confirm it 
        B/.  Second with the victim's existed user at host.com email (something@company.com)

  2. At your confirmed wordpress.com account go to settings >users invite your second account (something@company.com)
  3. At your second account go to notifications at the top right, see the invitation and accept it 
  4. See that your Wordpress.com account’s email has been verified (email confirmation bypass )

* **access the wordpress admin panel**
  1. Now at the same browser where the (something@company.com) Wordpress.com account 
  2. go to host.com wordpress panel 
  3. Click on sign in with wordpress.com
  4. Forward 
  5. See yourself logged in as admin on host.com wordpress

## Platform(s) Affected:
JetPack latest version




## Supporting Material/References:
As example I bypass ███████ 

██████

## Impact

* Bypass authentication of websites that runs wordpress with JetPack plugin without any user inteaction


Regards,

Adam

</details>

---
*Analysed by Claude on 2026-05-24*
