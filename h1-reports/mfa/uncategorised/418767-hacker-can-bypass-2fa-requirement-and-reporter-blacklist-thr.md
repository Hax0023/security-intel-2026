# 2FA Requirement Bypass via Embedded Submission Form

## Metadata
- **Source:** HackerOne
- **Report:** 418767 | https://hackerone.com/reports/418767
- **Submitted:** 2018-10-04
- **Reporter:** japz
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Authentication Bypass, Authorization Bypass, Security Control Circumvention
- **CVEs:** None
- **Category:** uncategorised

## Summary
Program owners can enforce two-factor authentication (2FA) as a requirement before hackers submit vulnerability reports. However, this security control can be bypassed by accessing the embedded submission form URL directly, which does not enforce the same 2FA requirements, allowing unauthenticated or non-2FA users to submit reports.

## Attack scenario
1. Program owner enables 2FA requirement in submission settings for their program
2. Attacker removes or does not configure 2FA on their HackerOne account
3. Attacker attempts normal report submission and is blocked due to 2FA requirement
4. Attacker obtains the embedded submission form URL (publicly available on policy page)
5. Attacker directly accesses the embedded submission URL, bypassing the 2FA check
6. Attacker successfully submits vulnerability report without 2FA enabled

## Root cause
The 2FA enforcement logic was implemented only in the primary submission form endpoint but not in the embedded submission form endpoint. The embedded form endpoint lacks validation of the same security requirements, creating a parallel path that circumvents the control.

## Attacker mindset
An attacker could exploit this to submit false or spam reports from accounts without 2FA, potentially harassing programs or flooding report queues. Bad actors could bypass intended security barriers meant to increase accountability and legitimacy of submissions.

## Defensive takeaways
- Enforce security requirements (2FA, blacklist checks) at a centralized validation layer applied to all submission endpoints
- Implement consistent authorization checks for both primary and embedded/alternative form submissions
- Audit all entry points to critical functionality to ensure security controls are uniformly applied
- Test security controls through alternative access paths and API endpoints
- Consider moving 2FA enforcement to pre-submission authentication rather than form-level validation
- Implement server-side session validation that carries security context through all submission methods

## Variant hunting
Test other embedded or iframe-based forms for similar authorization bypasses
Check API endpoints for report submission that may bypass web UI controls
Verify reporter blacklist enforcement is also applied to embedded form
Test if other submission-related security controls (email verification, account age) are bypassed
Look for other features with 'embedded' variants that may have inconsistent enforcement
Test if program-specific restrictions are enforced on embedded forms

## MITRE ATT&CK
- T1190
- T1566

## Notes
The vulnerability is a classic case of security control fragmentation where different code paths handle the same functionality. The embedded submission form was likely created as a feature for easy integration into program websites but inherited from or was inconsistently updated with new security requirements. The public availability of the embedded URL (visible on policy pages) makes this trivial to discover and exploit.

## Full report
<details><summary>Expand</summary>

Hi Team,

### Summary:

A program owner can enforce the hackers to setup the two-factor authentication before submitting new reports to their program here: https://hackerone.com/parrot_sec/submission_requirements (see below image)

{F355169}

The [Parrot Sec](https://hackerone.com/parrot_sec) program has this feature enabled to enforce the hackers to setup `2FA` before submitting reports. I removed my `2FA` to test and it is good that i was block from submitting new reports (see below image)

{F355168}

---

### BYPASS 2FA Requirements using Embedded Submission:

Now i was able to bypass this 2FA setup requirements by using the Parrot Sec program __Embedded Submission Form__.

## Steps to reproduce:

  1. Login to your account and __remove__ your 2FA on your account (if you already setup it)
  2. Now go to https://hackerone.com/parrot_sec and hit `Submit Report` button, observed that you cannot submit report unless you will enable your 2FA.
  3. __BYPASS:__ Get the `Embedded Submission` URL on their [policy page](https://hackerone.com/parrot_sec): i get this ->> https://hackerone.com/0a1e1f11-257e-4b46-b949-c7151212ffbb/embedded_submissions/new
  4. Now submit report using that embedded submission form and you can submit reports without setting-up your 2FA, despite the program __enforce__ the user to setup the 2FA before submitting new reports.
  5. 2FA requirements successfully bypassed!

## Impact

Bypassing the enabled protection/feature of the program.

Let me know if anything else is needed.

Regards
Japz

</details>

---
*Analysed by Claude on 2026-05-24*
