# Pre-generation of 2FA Secret/Backup Codes Exposed in DOM via XSS

## Metadata
- **Source:** HackerOne
- **Report:** 100509 | https://hackerone.com/reports/100509
- **Submitted:** 2015-11-19
- **Reporter:** danlec
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Information Disclosure, Improper Cryptographic Key Management, Cross-Site Scripting (XSS) - prerequisite, Sensitive Data Exposure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
HackerOne pre-generates 2FA secrets and backup codes on the authentication settings page, exposing them in the DOM before activation. An attacker with XSS access or session compromise can extract these codes before the user confirms 2FA enablement, allowing account takeover even if the user later enables 2FA. The vulnerability exists because credential confirmation is only required for activation, not for secret generation.

## Attack scenario
1. Attacker identifies XSS vulnerability in HackerOne or crafts malicious link leading to authentication settings page
2. Victim clicks malicious link or visits compromised page, executing attacker's JavaScript in HackerOne's domain context
3. JavaScript makes request to /settings/authentication/edit and parses DOM to extract pre-generated 2FA secret and backup codes
4. Attacker exfiltrates codes to their server; victim may notice unusual behavior and close/reopen browser window
5. Victim enables 2FA using the pre-generated secret/codes, unaware attacker already possesses them
6. Attacker gains access to victim's account using stolen 2FA codes and backup codes, bypassing 2FA protection

## Root cause
2FA secrets and backup codes are generated and embedded in the authentication settings form before user confirmation (password/TOTP verification). The application assumes that reading these values requires activation, but DOM access via XSS or session compromise bypasses this protection. No rate limiting or invalidation occurs when 2FA is not activated.

## Attacker mindset
An attacker recognizes that while 2FA is meant to protect accounts, pre-generation creates a window of opportunity where credentials exist in an unconfirmed state. By combining session compromise or XSS with social engineering (triggering suspicious behavior to prompt user action), the attacker can capture secrets before activation. The attack leverages the assumption that HTML form data is inherently protected by server-side logic.

## Defensive takeaways
- Generate cryptographic secrets only after successful password/TOTP verification, not during form rendering
- Implement server-side session state to track 2FA setup progress; invalidate pre-generated secrets if setup is not completed
- Never embed sensitive cryptographic material (secrets, backup codes) in HTML/DOM; transmit only to authenticated users via secure channels
- Implement Content Security Policy (CSP) to mitigate XSS impact and prevent exfiltration of sensitive data
- Consider one-time or time-limited backup codes that cannot be re-used if 2FA setup is abandoned
- Require TOTP verification before allowing backup code access or regeneration, not just for initial setup
- Audit authentication settings endpoints for XSS vulnerabilities regularly
- Log access to sensitive credential pages and alert users of unusual activity

## Variant hunting
Check if other authentication settings (password reset tokens, temporary credentials) are pre-generated and exposed in DOM
Test whether backup code regeneration leaks new codes before confirmation
Verify if disabled accounts or users without 2FA permission can still access pre-generated secrets via /settings/authentication/edit
Examine whether recovery codes for password reset are similarly pre-generated
Test if 2FA secrets persist across browser refreshes or session resets before activation
Check for similar patterns in other OAuth/SSO providers or identity platforms

## MITRE ATT&CK
- T1190
- T1005
- T1056
- T1539
- T1528
- T1550

## Notes
This report demonstrates a subtle but critical design flaw in 2FA implementation. While activation requires credential confirmation, the pre-generation of secrets creates a temporal vulnerability window. The reporter specifically notes the surprising discovery that disabled 2FA users could still access codes, suggesting insufficient access controls. The attack requires either XSS or session compromise as a prerequisite, but the impact is severe: complete 2FA bypass. This is a good example of defense-in-depth failure where cryptographic secrets should never be generated until the moment of commitment.

## Full report
<details><summary>Expand</summary>

If you manage to get a malicious script running in HackerOne, requesting `https://hackerone.com/settings/authentication/edit` and parsing out the two factor authentication form will yield either… 

- the 2FA secret key and backup codes that *will* be used if 2FA is enabled for the first time this session
- the backup codes that *will* be used if 2FA is already being used and the codes are regenerated during this session

While *activating* 2FA or *confirming* backup codes regeneration requires knowledge of the user's password/TOTP code, reading the values out from the DOM does not (again, provided that you've compromised the user's session and are running script in their domain)

A theoretical attack might play out like this:

- A victim clicks a link or something in HackerOne which triggers XSS (which seems unlikely, but …)
- The XSS makes a request to `https://hackerone.com/settings/authentication/edit` to obtain the victim's potential 2FA secret and backup codes.  Possibly the attacker is able to abuse a password manager's behavior to obtain the victim's username/password at this point.
- Because of the strange behavior that occurred when they clicked the link, the victim possibly closes and re-opens the window (in an attempt to stop whatever the script is doing) and then enables 2FA on their account
- The attacker would now know the 2FA secret and backup codes that are currently being used for the victim's account

While achieving this attack seems rather unlikely, it seems that it could be mitigated by not generating the 2FA values until the user is trying to enable 2FA or generate their codes and has provided their password (and then generating new codes each time, regardless of whether the process was cancelled previously)

(Also, I was somewhat surprised to see that the `https://hackerone.com/settings/authentication/edit` form contained a 2FA secret/backup codes for users that aren't allowed to set up two factor authentication.)

</details>

---
*Analysed by Claude on 2026-05-24*
