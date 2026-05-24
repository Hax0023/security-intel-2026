# Information disclosure (No rate limting in forgot password & other login)

## Metadata
- **Source:** HackerOne
- **Report:** 91343 | https://hackerone.com/reports/91343
- **Submitted:** 2015-09-30
- **Reporter:** protector47
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there,
I noticed a small information leak which allows an attacker to check whether an email address is associated with an account.If your account is not associated with website then an error will become raise that **"That username or email was not found."**
You should always return a status message like: **"If your email exists in our database, you'll receive a reset link"**. That way an attac

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

Hi there,
I noticed a small information leak which allows an attacker to check whether an email address is associated with an account.If your account is not associated with website then an error will become raise that **"That username or email was not found."**
You should always return a status message like: **"If your email exists in our database, you'll receive a reset link"**. That way an attacker cannot distinguish between the two cases.
Also you should add rate limiting :)

Thanks,

</details>

---
*Analysed by Claude on 2026-05-24*
