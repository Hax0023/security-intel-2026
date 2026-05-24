# OAuth open redirect

## Metadata
- **Source:** HackerOne
- **Report:** 7900 | https://hackerone.com/reports/7900
- **Submitted:** 2014-04-17
- **Reporter:** melvin
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Open Redirect
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can use an open redirect vulnerability in the Twitter OAuth process to redirect someone to his/her webpage, while also obtaining the OAuth token and verifier of the victim. 

The vulnerability is right here: https://app.respond.ly/_oauth/twitter/?requestTokenAndRedirect=https://hackerone.com. When someone authorizes their Twitter account using that URL, the redirect will go to https:

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

An attacker can use an open redirect vulnerability in the Twitter OAuth process to redirect someone to his/her webpage, while also obtaining the OAuth token and verifier of the victim. 

The vulnerability is right here: https://app.respond.ly/_oauth/twitter/?requestTokenAndRedirect=https://hackerone.com. When someone authorizes their Twitter account using that URL, the redirect will go to https://hackerone.com.

Recommendation: make sure the `requestTokenAndRedirect` paramater only accepts hosts on whitelisted domains.

</details>

---
*Analysed by Claude on 2026-05-24*
