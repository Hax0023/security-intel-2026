# 2FA Requirement Bypass via Report Transfer Function

## Metadata
- **Source:** HackerOne
- **Report:** 2569993 | https://hackerone.com/reports/2569993
- **Submitted:** 2024-06-22
- **Reporter:** aloneh1
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Authorization Bypass, Business Logic Flaw, Insufficient Input Validation, Security Policy Circumvention
- **CVEs:** None
- **Category:** uncategorised

## Summary
A program can enforce 2FA requirement for new report submissions, but this security control can be bypassed by transferring reports from non-2FA users between programs. An attacker with non-2FA enabled account can submit reports to a lenient program and have them transferred to a strict 2FA-required program, completely circumventing the intended security requirement.

## Attack scenario
1. Attacker creates or uses an account without 2FA setup
2. Attacker identifies two programs: one without 2FA requirements (target A) and one with mandatory 2FA (target B)
3. Attacker submits a vulnerability report to program A using their non-2FA account
4. Program manager or attacker (if managing both programs) transfers the report from program A to program B
5. Report successfully appears in program B despite reporter not meeting 2FA requirement
6. Attacker can now engage with program B's security process without ever enabling 2FA

## Root cause
The report transfer endpoint lacks validation to check whether the reporter meets the destination program's submission requirements. The transfer function only verifies authorization to transfer reports but does not validate compliance with the destination program's security policies (specifically 2FA requirements).

## Attacker mindset
An attacker might exploit this to: (1) avoid enabling 2FA on their account while still participating in strict programs, (2) maintain anonymity by avoiding account security hardening, (3) transfer reports from accounts with history to programs with stricter verification, or (4) bypass security policies that programs intentionally enforce.

## Defensive takeaways
- Validate destination program security requirements before allowing report transfers
- Enforce submission requirements checks on all report submission paths, not just direct submissions
- Require reporter to explicitly acknowledge and comply with destination program policies before transfer completion
- Audit all report modification operations (transfer, reassign, etc.) against current program policies
- Consider requiring reporter action/confirmation when transferring to a program with stricter requirements than their origin
- Log and monitor report transfers that bypass standard submission requirements

## Variant hunting
Check if other submission requirements can be bypassed via transfer: IP whitelisting, email domain restrictions, hacker level/reputation thresholds, country-based restrictions, or account age requirements. Also verify if reverse transfers (from strict to lenient programs) are logged appropriately.

## MITRE ATT&CK
- T1190
- T1535
- T1566

## Notes
This is a business logic vulnerability where a security control is implemented on one code path (direct submission) but not enforced on an alternate code path (report transfer). The vulnerability is particularly concerning because program managers intentionally set 2FA requirements to ensure reporter accountability and identity verification. The transfer mechanism essentially provides an unintended backdoor that undermines this policy.

## Full report
<details><summary>Expand</summary>

Hello team,

While testing the report submission function i found that when setting up the 2fa require to submit new reports to the program even the program staff can not  able to submit report to the program but using transfer report method the reporter who doesn't setuped the 2fa has submitted the report to other program and that report can be transferred to this 2fa require submission program .

Step to reproduce:-

1:- create two programs for testing like `h1R` and  `h1B`
2: Now got `h1B` program settings and select submission requirements settings and choose 2fa requirements to submit new reports.
3: from a no 2fa setuped hackerone account submit a report to `h1R`
4: Now as a program manager of the two program above mentioned in 1st step transfer the  report from step 3  to `h1B` it successfully transferred the report even the reporter who doesn't have setupped the 2fa. 

POC VIDEO:-

█████████

## Impact

No proper validation while transfferring the report to a 2fa require submission program weather the reporter have settuped the 2fa to his/her account.

Thanks,
aloneh1

</details>

---
*Analysed by Claude on 2026-05-24*
