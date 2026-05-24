# Github Account Takeover from Docs page of `kubernetes-csi.github.io`

## Metadata
- **Source:** HackerOne
- **Report:** 1434967 | https://hackerone.com/reports/1434967
- **Submitted:** 2021-12-23
- **Reporter:** codermak
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Report Submission Form

## Summary:
Kubernetes in its docs https://kubernetes-csi.github.io have a drivers list.
One of the driver was pointing to an external github account. That github account was not registered on github.com
So I was able to takeover the account and host PoC

## Kubernetes Version:
NA

## Component Version:
NA

## Steps To Reproduce:

  1. Go to https://kubernetes-csi.github.io

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

Report Submission Form

## Summary:
Kubernetes in its docs https://kubernetes-csi.github.io have a drivers list.
One of the driver was pointing to an external github account. That github account was not registered on github.com
So I was able to takeover the account and host PoC

## Kubernetes Version:
NA

## Component Version:
NA

## Steps To Reproduce:

  1. Go to https://kubernetes-csi.github.io/docs/drivers.html
  2. Search for `MacroSAN`
  3. Click on  `MacroSAN`
  4. You will be taken to this repository https://github.com/macrosan-csi/macrosan-csi-driver
  5. You will see takeover message there

## Supporting Material/References:

- https://github.com/macrosan-csi/macrosan-csi-driver
- https://kubernetes-csi.github.io/docs/drivers.html

{F1556768}

## Reference

- https://hackerone.com/reports/1212853

## Impact

An attacker can takeover the repository and host malicious code on it, when any user or employee will refer the docs and tries to download the dirver, they will end up using malicious code which could lead to RCE.

</details>

---
*Analysed by Claude on 2026-05-24*
