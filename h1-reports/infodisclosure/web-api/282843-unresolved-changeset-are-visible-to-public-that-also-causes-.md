# Unresolved ChangeSet Information Disclosure in Public Repository

## Metadata
- **Source:** HackerOne
- **Report:** 282843 | https://hackerone.com/reports/282843
- **Submitted:** 2017-10-25
- **Reporter:** hackerwahab
- **Program:** WordPress
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Sensitive Data Exposure, Improper Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
Public access to unresolved changesets in WordPress's public code repository (code.trac.wordpress.org) exposes sensitive information including unpatched security vulnerabilities and PHP source code. Attackers can enumerate changesets by ID to discover pending security issues before fixes are deployed, enabling targeted exploitation.

## Attack scenario
1. Attacker discovers WordPress uses public Trac repository at code.trac.wordpress.org
2. Attacker identifies changeset URL pattern and begins sequential enumeration (469, 470, 471, etc.)
3. Attacker accesses unresolved changesets containing security-related code modifications
4. Attacker analyzes exposed PHP code and identifies unpatched vulnerabilities
5. Attacker correlates unresolved bugs with publicly reported issues to understand attack surface
6. Attacker develops exploits targeting unpatched vulnerabilities before official fixes are released

## Root cause
Improper access controls on development repository changesets allowing public visibility of security-sensitive code changes and unresolved bug information without authentication or authorization checks

## Attacker mindset
Reconnaissance-focused adversary seeking to identify zero-day or pre-patch vulnerabilities through systematic enumeration of development artifacts, leveraging the information disclosure to gain advantage before official security patches are available

## Defensive takeaways
- Implement access controls restricting visibility of security-sensitive changesets to authenticated users only
- Implement rate limiting or CAPTCHA on changeset enumeration to prevent automated discovery
- Separate security-critical changesets into private/restricted repositories until patches are released
- Redact or anonymize security-related code in public changesets until public disclosure date
- Implement change classification system to mark security-related commits as restricted visibility
- Monitor for suspicious enumeration patterns of sequential changeset IDs
- Coordinate disclosure timeline to minimize window between unresolved changeset visibility and patch availability

## Variant hunting
Check for other public development repositories (GitHub, GitLab) with unresolved security commits
Enumerate Trac instances for other projects with similar access control issues
Search public Git history and mirrors for deleted/unresolved security changesets
Test for information disclosure in version control tags and branches
Investigate commit message contents for hardcoded secrets or vulnerability details
Check archived/cached versions of public repositories on Wayback Machine

## MITRE ATT&CK
- T1190
- T1526
- T1589
- T1595
- T1592
- T1598

## Notes
Report quality is poor with grammatical errors and unclear technical explanation, but the core vulnerability of information disclosure through public changeset enumeration is valid. The researcher demonstrates proof-of-concept via URL enumeration but lacks detailed technical analysis. WordPress Trac is development infrastructure; impact depends on actual sensitivity of exposed changesets. Bounty amount not disclosed in report.

## Full report
<details><summary>Expand</summary>

Hello,

While testing Your Security I Observed that the Security Report Reported to You After Validation arranged for fix  or you can say that a public  repository created for the code powering the site at https://code.trac.wordpress.org/changeset/[ID]
that Leaks Following Things

1.UnResolved Bugs
2.PHP Code of Website

Impact
=====
Let an Attacker Dont Know The Vulnerabilities in Your System he can search for different id's like 469,470,471 Like this:-
https://code.trac.wordpress.org/changeset/469
https://code.trac.wordpress.org/changeset/470
https://code.trac.wordpress.org/changeset/471

Which is Disclosing PHP Code and Unresolved Security Bugs To Public An Attacker can see Unresolved Vulnerabilities From Here can Use it to destroy Your Services.


Thanks,
Abdulwahab Khan,
Independent Cyber Security Researcher.

</details>

---
*Analysed by Claude on 2026-05-24*
