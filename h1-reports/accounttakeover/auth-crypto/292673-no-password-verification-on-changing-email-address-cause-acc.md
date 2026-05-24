# No Password Verification on  Changing Email Address Cause Account takeover   

## Metadata
- **Source:** HackerOne
- **Report:** 292673 | https://hackerone.com/reports/292673
- **Submitted:** 2017-11-23
- **Reporter:** nohack
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** auth-crypto

## Summary
In coursera.org website, there is no password verification on changing email id. 

Generally when user try to change the password , they were asked to verify the request by entering old password. For the same reason a verification should be there on changing email.

But the worst part is, when user change email address then coursera.org website send verification mail on new mail id without asking 

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

In coursera.org website, there is no password verification on changing email id. 

Generally when user try to change the password , they were asked to verify the request by entering old password. For the same reason a verification should be there on changing email.

But the worst part is, when user change email address then coursera.org website send verification mail on new mail id without asking current password or inform to old email id.

## Impact

if some one left his account open on public computer(say office or cafe), then attacker can change the email ,verify it himself. Then abuse forgot password field to take over whole account.

Suggested mitigation: 
a password field can be applied (just like Facebook do) or verification mail should be send on old email id registered.


If you required any POC then Let me know. 

Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
