# Reflected XSS vector

## Metadata
- **Source:** HackerOne
- **Report:** 190247 | https://hackerone.com/reports/190247
- **Submitted:** 2016-12-11
- **Reporter:** creased
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello GoCD team,

I noticed a reflected / stored XSS vulnerability vector that could potentially be used to impact security of GoCD users.

- https://www.go.cd/user/upoad/..%2F..%2F
- https://docs.go.cd/current/user/upoad/..%2F..%2F

As you should see, this link is considered as valid by the HTTP service and thus does not cause redirect to root of *.go.cd nor return of an HTTP error code (e.g., 40

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

Hello GoCD team,

I noticed a reflected / stored XSS vulnerability vector that could potentially be used to impact security of GoCD users.

- https://www.go.cd/user/upoad/..%2F..%2F
- https://docs.go.cd/current/user/upoad/..%2F..%2F

As you should see, this link is considered as valid by the HTTP service and thus does not cause redirect to root of *.go.cd nor return of an HTTP error code (e.g., 404 not found) as it should be...

Such a link can be used to load an unexpected script located on the HTTP server of *.go.cd, eventually uploaded by user (see screenshot)

Please let me know if you need more information!

Looking forward!

</details>

---
*Analysed by Claude on 2026-05-24*
