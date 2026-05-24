# User Information leak allows user to bypass email verification.

## Metadata
- **Source:** HackerOne
- **Report:** 163467 | https://hackerone.com/reports/163467
- **Submitted:** 2016-08-26
- **Reporter:** cablej
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** uncategorised

## Summary
When a user is logged on, the following is sent:

```
██████
```

This contains some sensitive information, most notably the email token. A user can use this to bypass email verification and verify any email.

In addition, the hashed password is leaked, which could present a vulnerability if a user's account is compromised without compromising the password.

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

When a user is logged on, the following is sent:

```
██████
```

This contains some sensitive information, most notably the email token. A user can use this to bypass email verification and verify any email.

In addition, the hashed password is leaked, which could present a vulnerability if a user's account is compromised without compromising the password.

</details>

---
*Analysed by Claude on 2026-05-24*
