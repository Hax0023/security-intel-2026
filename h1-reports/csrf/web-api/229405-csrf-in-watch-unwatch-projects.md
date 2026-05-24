# Csrf in watch-unwatch projects

## Metadata
- **Source:** HackerOne
- **Report:** 229405 | https://hackerone.com/reports/229405
- **Submitted:** 2017-05-17
- **Reporter:** ashish_r_padelkar
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

When you visit any projects from `https://hosted.weblate.org/` , there is a button provided on top-right called `Watch` / `Unwatch` for each projects. when you click on that button, a POST request is sent which contains csrf token.  But this request also works without that token.

Just hit the urls in your browser and you will be able to `Watch` or `Unwatch` the projects

`https://hosted.w

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

Hello,

When you visit any projects from `https://hosted.weblate.org/` , there is a button provided on top-right called `Watch` / `Unwatch` for each projects. when you click on that button, a POST request is sent which contains csrf token.  But this request also works without that token.

Just hit the urls in your browser and you will be able to `Watch` or `Unwatch` the projects

`https://hosted.weblate.org/accounts/watch/androbd/`
https://hosted.weblate.org/accounts/unwatch/androbd/

where androbd is a project name!

Regrads
Ashish



</details>

---
*Analysed by Claude on 2026-05-24*
