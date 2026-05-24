# State parameter missing on google OAuth

## Metadata
- **Source:** HackerOne
- **Report:** 2688 | https://hackerone.com/reports/2688
- **Submitted:** 2014-03-02
- **Reporter:** anandpingsafe
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary

Hi,

State parameter i.e anti-csrf token to prevent session hijacking attacks is missing on Google OAuth

i.e. https://accounts.google.com/o/oauth2/auth?response_type=code&redirect_uri=https%3A%2F%2Fslack.com%2Fservices%2Fauth%2Fgdrive&client_id=19570130570-tfuuvh6hutjd09bq64is5sao643q67jg.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&access_type=offline&ap

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


Hi,

State parameter i.e anti-csrf token to prevent session hijacking attacks is missing on Google OAuth

i.e. https://accounts.google.com/o/oauth2/auth?response_type=code&redirect_uri=https%3A%2F%2Fslack.com%2Fservices%2Fauth%2Fgdrive&client_id=19570130570-tfuuvh6hutjd09bq64is5sao643q67jg.apps.googleusercontent.com&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&access_type=offline&approval_prompt=force&state=sehacure

As we can see in above URL there is no state parameter to maintain session identity.

Best regards,
Anand

</details>

---
*Analysed by Claude on 2026-05-24*
