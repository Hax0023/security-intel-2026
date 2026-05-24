# CSRF token valid even after the session logout of a particular user

## Metadata
- **Source:** HackerOne
- **Report:** 2857 | https://hackerone.com/reports/2857
- **Submitted:** 2014-03-03
- **Reporter:** anandpingsafe
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

To reproduce the issue:

1) Login to your https://secure.phabricator.com account and copy your Anti CSRF token.

2) Now logout and again login after sometime.

3) Open up your burp suite to modify the request and now submit any form with your old CSRF token.

The request will be completed.

So let's suppose i am somehow able to get CSRF token of a particular user then i can use th

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

To reproduce the issue:

1) Login to your https://secure.phabricator.com account and copy your Anti CSRF token.

2) Now logout and again login after sometime.

3) Open up your burp suite to modify the request and now submit any form with your old CSRF token.

The request will be completed.

So let's suppose i am somehow able to get CSRF token of a particular user then i can use the same token again and again to perform the attack.

The token should be thrown from the db after the session logout.

Please have a look.

Best regards,
Anand


</details>

---
*Analysed by Claude on 2026-05-24*
