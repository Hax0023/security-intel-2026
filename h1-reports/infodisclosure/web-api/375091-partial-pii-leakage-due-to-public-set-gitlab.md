# Partial PII Leakage via Public GitLab Snippets Configuration

## Metadata
- **Source:** HackerOne
- **Report:** 375091 | https://hackerone.com/reports/375091
- **Submitted:** 2018-07-01
- **Reporter:** alyssa_herrera
- **Program:** GitLab
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, PII Leakage, Improper Access Control, Configuration Issue
- **CVEs:** None
- **Category:** web-api

## Summary
A GitLab instance was misconfigured to publicly expose code snippets that should have been private, revealing partial PII including usernames and profile pictures. This allows unauthenticated attackers to enumerate user information and discover code artifacts that could be leveraged for reconnaissance in subsequent attacks.

## Attack scenario
1. Attacker discovers the target's GitLab instance and navigates to the public snippets exploration interface
2. Attacker browses the /explore/snippets endpoint which lists all publicly accessible snippets
3. Attacker identifies snippets containing code and metadata, extracting usernames and profile picture URLs
4. Attacker correlates usernames with other public information to build a profile of the organization's users
5. Attacker uses discovered code snippets for reconnaissance (identifying technologies, patterns, potential hardcoded secrets)
6. Attacker leverages this intelligence for targeted phishing, social engineering, or exploitation of identified technologies

## Root cause
GitLab instance was configured with default or overly permissive visibility settings for snippets, allowing unauthenticated public access to what should have been private code and user metadata. The snippets feature did not enforce appropriate access controls by default.

## Attacker mindset
Reconnaissance-focused attacker seeking low-hanging fruit for initial information gathering. The attacker recognizes that partial PII combined with code leakage provides valuable reconnaissance data to inform more targeted attacks against the organization.

## Defensive takeaways
- Audit default visibility settings on all code repositories and snippets management features
- Enforce private-by-default policies for code snippets and user-generated content
- Implement regular reviews of access control configurations across development platforms
- Restrict /explore endpoints to authenticated users or disable public exploration features
- Minimize user profile information exposure in public APIs and listing pages
- Implement logging and alerting for bulk enumeration attempts against public endpoints
- Use infrastructure-as-code and configuration management to prevent security misconfigurations
- Educate development teams about the risks of public code repositories and PII exposure

## Variant hunting
Check for publicly accessible project wikis, project snippets, and gists in other platforms (GitHub, Bitbucket, Gitea)
Enumerate other metadata exposure vectors: issue trackers, CI/CD logs, wiki pages with user mentions
Test visibility settings on user profiles, groups, and organizational structures
Search for similar misconfigured instances using search engines (site:gitlab.com/explore/snippets, etc.)
Check for API endpoints that list users, projects, or snippets without proper authentication
Investigate search index exposure (Google cache, archive.org) for previously public content
Look for migration traces where private projects were accidentally exposed during transfers

## MITRE ATT&CK
- T1590.002 - Gather Victim Identity Information: Credentials
- T1598.003 - Phishing: Spearphishing Link
- T1592.004 - Gather Victim Host Information: Client Configurations
- T1589.001 - Gather Victim Identity Information: Credentials
- T1589.002 - Gather Victim Identity Information: Email Addresses
- T1598.001 - Phishing: Spearphishing Attachment

## Notes
Low severity classification appropriate due to partial nature of PII exposure (username and picture only, no authentication credentials). However, the combination with code disclosure elevates intelligence value for attackers. The writeup lacks specific impact metrics or evidence of actual misuse. Default-deny approach and regular configuration audits are recommended preventive measures.

## Full report
<details><summary>Expand</summary>

**Summary:**
 ████████ allows you to explore the repos, snippets,etc. On the snippets we find a name+icon and some code information. This shouldn't publicly exposed as an attacker may use it to perform further attacks
**Description:**
A configuration issue allows code and the name+icon of a user on the gitlab instance to leaked publicly.
## Impact
A tiny bit of PII leakage, mainly name+ personal picture. Along with a bit of code leakage
## Step-by-step Reproduction Instructions

https://█████/snippets/72
https://███/explore/snippets

## Product, Version, and Configuration (If applicable)
Gitlab
## Suggested Mitigation/Remediation Actions
Make private

## Impact

Recovery of  partial code and username+picture

</details>

---
*Analysed by Claude on 2026-05-24*
