# Reflected XSS on https://███████/

## Metadata
- **Source:** HackerOne
- **Report:** 804364 | https://hackerone.com/reports/804364
- **Submitted:** 2020-02-25
- **Reporter:** the_unlucky_guy
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**

Hey Team,

There is reflected xss on https://█████/kinetic/ when certain action results in 404 error.

**Description:**

I am using some random strings paths after kinetic in https://███████/kinetic/ if that path is not exist then it says 404 not found. Strings is not sanitized after kinetic/ due to which any one can able to use Java Script code after kinetic/ and it executed success

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

**Summary:**

Hey Team,

There is reflected xss on https://█████/kinetic/ when certain action results in 404 error.

**Description:**

I am using some random strings paths after kinetic in https://███████/kinetic/ if that path is not exist then it says 404 not found. Strings is not sanitized after kinetic/ due to which any one can able to use Java Script code after kinetic/ and it executed successfully leads to reflected xss.

## Impact

The attacker can able to execute JS code.

## Step-by-step Reproduction Instructions

1. open this  https://████████/kinetic/1%3C!--%3E%3CSvg%20OnLoad=(confirm)(document.domain)--%3E/ in firefox
2. You will get alert pop up.

## Product, Version, and Configuration (If applicable)

## Suggested Mitigation/Remediation Actions

Sanitize string

## Impact

The attacker can able to execute JS code.

</details>

---
*Analysed by Claude on 2026-05-24*
