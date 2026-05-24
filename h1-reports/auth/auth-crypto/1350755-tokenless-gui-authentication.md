# Tokenless GUI Authentication

## Metadata
- **Source:** HackerOne
- **Report:** 1350755 | https://hackerone.com/reports/1350755
- **Submitted:** 2021-09-24
- **Reporter:** seanland
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Report Submission Form

## Summary:
A person has the ability to bypass the login screen using the 401 error code produced from a failed token login.  The user is given the privileges of an system:anonymous user. 

## Kubernetes Version:
kubectl, kubeadm, kubelet 1.22.2
Ubuntu 20.04.3 - 64bit

## Component Version:
Dashboard v2.3.1+0.g8d9f8e76c

## Steps To Reproduce:

  1. Attempt to log in with a

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
A person has the ability to bypass the login screen using the 401 error code produced from a failed token login.  The user is given the privileges of an system:anonymous user. 

## Kubernetes Version:
kubectl, kubeadm, kubelet 1.22.2
Ubuntu 20.04.3 - 64bit

## Component Version:
Dashboard v2.3.1+0.g8d9f8e76c

## Steps To Reproduce:

  1. Attempt to log in with a token (just put in gibberish)
  2. Cut and paste the entire 401 authentication error starting from the back, forwards.
  3. Paste the 401 error into the token password field 
  4. Hit enter to Submit

## Supporting Material/References:
Please refer to the demonstration.

## Impact

The user is given the privileges of an system:anonymous user and access to the GUI.

</details>

---
*Analysed by Claude on 2026-05-24*
