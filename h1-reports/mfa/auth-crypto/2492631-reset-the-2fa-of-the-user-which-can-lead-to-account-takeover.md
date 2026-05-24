# 2FA Reset Without Confirmation Enables Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 2492631 | https://hackerone.com/reports/2492631
- **Submitted:** 2024-05-07
- **Reporter:** 5zdob13
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Insufficient Access Controls, Weak Account Recovery Mechanism, Missing Email Confirmation for Sensitive Actions, Insecure Direct Object References, Account Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
HackerOne's 2FA reset mechanism allows any attacker to initiate a 2FA disable request for a victim's account, which auto-completes after 24 hours if the victim fails to cancel via email. This bypass of multi-factor authentication enables complete account takeover without requiring the attacker to possess the victim's TOTP secret or have access to their authenticated session.

## Attack scenario
1. Attacker identifies target HackerOne user and navigates to the login page
2. During login, attacker enters victim's known credentials but omits the TOTP code
3. Attacker clicks 'Reset two-factor authentication' button without any additional verification
4. System sends cancellation email to victim's inbox requesting action within 24 hours
5. If victim does not interact with the cancellation email within 24-hour window, 2FA is automatically disabled
6. Attacker returns to login with victim's credentials and gains full account access without 2FA protection

## Root cause
The application implements a opt-out model for sensitive security operations rather than opt-in. The 2FA reset request defaults to approval after timeout instead of requiring explicit confirmation from the account owner before proceeding. No additional verification (security questions, password re-entry, backup codes) is required to initiate the reset.

## Attacker mindset
Low-skill attacker leveraging social engineering or credential stuffing to identify target accounts, then exploiting a forgiving security control default that prioritizes convenience over security. The attacker can perform this attack entirely passively without technical sophistication.

## Defensive takeaways
- Implement opt-in confirmation model: require explicit approval from authenticated session or secondary channel before 2FA modifications take effect
- Require password re-entry or additional authentication factor before initiating 2FA reset
- Shorten the default acceptance window from 24 hours to 4-6 hours maximum
- Send confirmation email to primary email requiring immediate action rather than cancellation email allowing inaction
- Implement rate limiting on 2FA reset requests per account
- Log all 2FA modification attempts and alert users of suspicious activity
- Consider requiring backup codes or secondary verification method to confirm identity before processing 2FA changes
- Implement geographic or device anomaly detection when 2FA reset is requested from unusual locations/devices

## Variant hunting
Check for similar insecure defaults on password reset flows
Audit other account recovery mechanisms that may use timeout-based approval
Test for race conditions between cancellation email delivery and timeout expiration
Verify if reset requests can be repeated to create multiple active reset windows
Check if attacker can modify reset request delivery email address
Test whether authenticated users can request 2FA reset for other users via IDOR
Examine if API endpoints for 2FA management have same flaws as web interface

## MITRE ATT&CK
- T1190
- T1566
- T1621
- T1078
- T1098

## Notes
This is a fundamental flaw in account security architecture. The researcher's suggested improvement (confirmation vs cancellation model) is sound and represents industry best practice. The vulnerability is easily exploitable with no special tools, making it a high-impact finding. HackerOne's exposure on this platform makes it particularly significant as it affects security researchers and organizations.

## Full report
<details><summary>Expand</summary>

**Summary:**

  Dear H1 Security Team,
   This report details a vulnerability that allows attacker to reset the 2FA of the victim and takeover their account within a day.

**Description:**

 The 2FA is extra layer of protection from getting your account compromised and that means even if the attacker knows your email and password still they can't access to your account but when you sign-in to "https:hackerone.com" with 2FA enable there's a  **Reset option** :
F3250375
   And then you'll got an email to **cancel the request** :
██████████
  If you don't Interact with this email within a day your 2FA will be disabled.
So Attacker can request to disabled the 2FA of the victim and If the victim don't cancel this request after a one day  attacker can takeover the victim's account and have a full access to it.
  On my opinion, Requesting something like this is a too serious so even If the attacker can request to disable the 2FA the email should be to **Confirm this action** not to stop it. "I mean after user request to reset their 2FA,  they have to check their email and confirm that they want to reset the 2FA and then the process can start and  maybe after that HackerOne email them If they want to cancel the request like this one:
 ████

I hope I was helpful and sorry If there anything not clear enough.
Kind regards,
5zdob13
 
### Steps To Reproduce

1. Enable the 2FA one your account and sign-out.
2. Sign-in and don't enter your Time-based One-Time Password (TOTP) and click on "Reset two-factor authentication" and press ok like this below:
█████
3. don't Interact with the email that you received.
4. After one day, try to sign-in and you’ll be able to sign in successfully.

### Optional: Supporting Material/References (Screenshots)
  
On my PoC I just showed you what happened after one day from requesting to reset the 2FA

████████

## Impact

Attacker can request to reset victim's 2FA and takeover victim's HackerOne account and also exploiting this vulnerability requires minimal technical skill too.

</details>

---
*Analysed by Claude on 2026-05-24*
