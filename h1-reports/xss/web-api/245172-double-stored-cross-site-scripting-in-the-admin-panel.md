# Double Stored Cross-Site scripting in the admin panel

## Metadata
- **Source:** HackerOne
- **Report:** 245172 | https://hackerone.com/reports/245172
- **Submitted:** 2017-07-01
- **Reporter:** sp1d3rs
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
##Description
Hello. I discovered a Stored XSS attack vector in the `Custom Domain` field

##POC & Reproduction steps
1. Login to the federalist and go to the some instance `http://localhost:1337/sites/<siteid>/settings`
2. Fill the `Custom Domain` field by the
```
javascript:alert(document.domain)
```
and `Demo domain`
```
javascript:alert(document.domain);
```
(it cannot be the same so we bypass

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

##Description
Hello. I discovered a Stored XSS attack vector in the `Custom Domain` field

##POC & Reproduction steps
1. Login to the federalist and go to the some instance `http://localhost:1337/sites/<siteid>/settings`
2. Fill the `Custom Domain` field by the
```
javascript:alert(document.domain)
```
and `Demo domain`
```
javascript:alert(document.domain);
```
(it cannot be the same so we bypass the check by adding `;`)

3. Save and press `View Website` button. You will be XSSed.
{F199337}
{F199336}
4) Go to the `http://localhost:1337/sites/<siteid>/published` - and press view on the demo site to test second Stored XSS
{F199338}

##The impact
The XSS requires user interaction (e.g. clicking the button). But still, it is a bad thing. Anyone who gain access here, can conduct stored XSS attack against other admins.

##The root cause & suggested fix
The input fields not sanitized properly - it should allow only alphanumeric characters, and dots.


</details>

---
*Analysed by Claude on 2026-05-24*
