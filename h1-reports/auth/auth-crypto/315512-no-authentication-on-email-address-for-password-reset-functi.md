# No authentication on email address for password reset functionality/ https://platform.thecoalition.com/forgot-password

## Metadata
- **Source:** HackerOne
- **Report:** 315512 | https://hackerone.com/reports/315512
- **Submitted:** 2018-02-13
- **Reporter:** startedfromthebottom
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

**Summary:** It was observed that the forgot password functionality on https://platform.thecoalition.com/forgot-password did not verify

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

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

**Summary:** It was observed that the forgot password functionality on https://platform.thecoalition.com/forgot-password did not verify the email addresses of user accounts before sending an email to them. An attacker can use this functionality and send faulty password reset links to legitimate users.

**Description:** It was also observed that the website did not verify the authenticity of the email and accepted any arbitrary test mail. It also allowed multiple requests for the same email id without any limit. This vulnerability can be leveraged to spam genuine users of platform.thecoalition.com.

## Steps To Reproduce:

(Add details for how we can reproduce the issue)

  1.Visit the site https://platform.thecoalition.com/login
  2.Go to the forgot password functionality on https://platform.thecoalition.com/forgot-password
  3.Write an arbitrary email of attackers choice and click email me reset functions.

## Impact

An attacker could leverage this vulnerability by sending faulty password reset links 'n' number of times to legitimate users of platform.thecoalition.com  . This can also be done to add unnecessary load to the server by sending illegitimate mails repeatedly via using this functionality

</details>

---
*Analysed by Claude on 2026-05-24*
