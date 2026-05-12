# Account Takeover of Existing HackerOne Accounts Through SCIM Provisioning

## Metadata
- **Source:** HackerOne
- **Report:** 3178999 | https://hackerone.com/reports/3178999
- **Submitted:** 2025-06-05
- **Reporter:** boy_child_
- **Program:** HackerOne
- **Bounty:** Not disclosed in writeup
- **Severity:** critical
- **Vuln:** Account Takeover, Broken Access Control, Improper Input Validation, SCIM Provisioning Bypass, Identity Management Flaw, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker with a verified domain and SSO/SCIM provisioning access can take over existing HackerOne user accounts by manipulating the SCIM provisioning flow. By importing existing users, changing their email addresses to attacker-controlled addresses within the verified domain, and resetting passwords without notification, an attacker gains full account access. This is particularly critical because default demo accounts are present in all organizations and easily exploitable.

## Attack scenario
1. Attacker sets up a sandbox program with SSO and SCIM provisioning enabled and verifies a domain
2. Attacker creates a user account in Okta with an email they control (attacker@verified.com)
3. Attacker imports existing HackerOne users into Okta, including default demo accounts (demo-member@hackerone.com)
4. Attacker assigns the victim's HackerOne account to their Okta user, maintaining the original username but changing the email to attacker@verified.com
5. Attacker triggers a password reset through SCIM, which syncs without notifying the original account owner
6. Attacker logs in to the compromised account using the new credentials sent to their controlled email address

## Root cause
HackerOne's SCIM provisioning implementation fails to validate that email changes should only apply to newly created accounts, not existing accounts. Additionally, the system does not send notifications when SCIM changes critical account attributes (email, password), allowing silent account takeovers. The email matching logic prioritizes username over email validation, and there is insufficient verification that the person making changes has authorization to modify existing accounts.

## Attacker mindset
The attacker explored the SCIM provisioning workflow methodically, recognizing that existing user accounts could be reassigned and modified through the provisioning interface. They identified that the system trusted SCIM updates implicitly and that default demo accounts present in all organizations provided easy initial targets for account takeover, scaling the attack from individual compromise to organizational level.

## Defensive takeaways
- Implement strict separation between user creation and user modification in SCIM provisioning—existing accounts should never have email addresses changed through provisioning
- Require explicit out-of-band confirmation for critical attribute changes (email, password) made via SCIM, especially when targeting existing accounts
- Send email notifications to the original email address (not the new one) whenever account-critical attributes are modified
- Implement rate limiting and anomaly detection on SCIM operations that target existing high-privilege accounts
- Remove or disable default demo accounts in production environments, or require explicit consent to activate them
- Require domain verification re-confirmation when SCIM operations would affect accounts with different domain suffixes
- Log and audit all SCIM-based account modifications with clear traceability to the originating request
- Implement a grace period or confirmation step before SCIM email changes take effect on existing accounts

## Variant hunting
Test SCIM provisioning with other IdP providers (Okta, Ping, Azure AD) for similar email modification issues
Investigate if username changes can also bypass validation checks in SCIM workflows
Check if other critical user attributes (role, permissions, 2FA settings) can be silently modified via SCIM
Test if SCIM provisioning can be used to modify accounts across multiple organizations if the attacker has verified domains for each
Examine whether SCIM deprovisioning flows have similar notification bypass issues
Check if guest or external user accounts have different validation rules than internal accounts in SCIM
Test if SCIM operations on accounts with active SSO sessions cause forced logouts or session invalidation

## MITRE ATT&CK
- T1190
- T1199
- T1621
- T1098
- T1556
- T1078
- T1133
- T1021

## Notes
This is a critical vulnerability because it requires only domain verification (which an attacker might achieve legitimately) and default demo accounts present in all organizations. The lack of notifications for email/password changes is particularly dangerous as it enables silent compromise. The researcher methodically identified the flaw through systematic testing of the SCIM workflow and clearly documented the sequence required for exploitation. HackerOne should have enforced stricter validation on email modifications for existing accounts and mandatory notification to original email addresses.

## Full report
<details><summary>Expand</summary>

After numerous attempts and understanding, I was able to take over existing user accounts through SCIM provisioning.

When using SCIM provisioning, the following must be met:
* Verified domain.
* Working SSO configuration.

Initially, I thought this would automatically be a certain loophole. In my first attempt, this was the procedure used for testing:
1. Import organisation users into Okta.
2. Receive an error stating that existing users don't have matching email domains to the verified one on file.
3. Change the email.
4. Instead, a new user is created in the organisation's users page.

After many attempts, I figured out how to change the sequence to:
1. In Okta, create a user whose email I control, say `attacker@verifed.com`
2. Import organisation users into Okta.
3. Assign the victim account to the created user in step 1.
4. Change the email parameter field to `attacker@verified.com`
5. Change password.
6. Bingo!

I then thought this looked too easy, so I assigned the user access to Okta and tried to log in via SSO, but it failed and did not work. Why?

Two fields in Okta are of importance: `username` and `email`. 

{F4416609}

{F4416611}

* If the attacker with verified domain as `verified.com` adds a victim as `victim@ato.com` to Okta, you will get an error that `ato.com` does not match the H1 verified domain settings.
* If the attacker with a verified domain as `verified.com` adds a victim as `victim@ato.com` to Okta and then changes the username and email to `victim@verified.com`, it will instead create a new user in the H1 organisation.
* If the attacker with verified domain as `verified.com` adds a victim as `victim@ato.com` to Okta, with the username as `victim@ato.com`  and email field as `victim@verifed.com`, the victim's email will be changed, AND no notification will be sent to the victim (issue 2)
* Now the attacker wants to log in. If the attacker wants to do so via the SSO provider (Okta), they can't add the victim to the Okta directory since the username `victim@ato.com` has already been imported and is in use.

{F4416607}

* So the attacker sets a password reset, which also does not send a notification to the user! (issue 3) Rather, the new email is controlled by the attacker.


##Setup:
Before you proceed, have the following setup:
1. A sandbox program setup from [here](https://hackerone.com/teams/new/sandbox) and don't delete the demo members.
2. Contact HackerOne support to activate SSO and SCIM provisioning for your sandbox program.
3. [Set up SSO with Okta](https://docs.hackerone.com/en/articles/8490526-okta-sso-setup-via-saml)
4. [Set up SCIM in Okta](https://docs.hackerone.com/en/articles/9250705-scim-provisioning-for-okta)
5. Added users.

## Steps To Reproduce
1. Go to the Okta directory and add a user with an email you have access to.
2. Go to the Okta application configured for Hackerone SCIM provisioning and import users.
3. In your imported users, assign the user `demo-member@hackerone.com` ( or any other user if the demo member is deleted)
4. Under the Okta application configured for Hackerone SCIM provisioning, tap on the **Assignments** tab, then the pencil icon to edit.

{F4416681}

5. Look for the email field and change it to what you control and in line with your verified domain.

{F4416680}

6. Save.
7. It will automatically sync.
6. Reset the user password, and you should be in.

### Proof of concept:
███

## Impact

Why I think this is so critical is that apart from taking over user accounts, take note of EVERY new organisation,  sandbox alike, there are two users present by default:
 
* Demo Triager `demo-triager@hackerone.com`
* Demo Member `demo-member@hackerone.com`

The above are always present and already members of the sandbox, private, and public organisations unless removed. (I tested on an old sandbox I own, wish I didn't delete them.)

All the attacker has to do is import these default members, leave the username unchanged, change the email, password reset, and they are in!.

</details>

---
*Analysed by Claude on 2026-05-11*
