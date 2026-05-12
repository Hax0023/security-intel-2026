# GitHub Personal Access Token Exposure in Employee Application

## Metadata
- **Source:** HackerOne
- **Report:** 1087489 | https://hackerone.com/reports/1087489
- **Submitted:** 2021-01-26
- **Reporter:** augustozanellato
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Credential Exposure, Hardcoded Secrets, Information Disclosure, Inadequate Secret Management
- **CVEs:** None
- **Category:** uncategorised

## Summary
A GitHub Personal Access Token (PAT) with full organizational repository access was discovered embedded in an employee's application. The token grants an attacker read and write access to all private repositories within the organization, enabling code manipulation, data theft, and supply chain attacks.

## Attack scenario
1. Attacker discovers exposed GitHub PAT in employee's application code, configuration files, or debugging artifacts
2. Attacker uses the PAT to authenticate to GitHub API with full organizational privileges
3. Attacker gains read access to all private repositories, allowing reconnaissance and vulnerability discovery
4. Attacker modifies code in critical repositories by pushing malicious commits using the compromised token
5. Attacker exfiltrates proprietary code, secrets, or sensitive business logic from private repositories
6. Attacker potentially injects backdoors or supply chain attacks affecting downstream users of Shopify's products

## Root cause
The employee hardcoded or embedded a GitHub Personal Access Token with overly broad permissions in an application without proper secret management practices. Lack of environment-based configuration, secret scanning, and credential rotation policies allowed the token to remain exposed.

## Attacker mindset
An attacker recognizing that credentials provide direct access to organizational assets performs reconnaissance on employee applications to discover exposed tokens. With org-level access, they can execute lateral movement, exfiltrate proprietary code, and maintain persistence through code injection.

## Defensive takeaways
- Implement pre-commit hooks and CI/CD secret scanning (e.g., TruffleHog, GitGuardian) to detect hardcoded credentials
- Enforce environment-based configuration using .env files, secrets managers (Vault, AWS Secrets Manager), or CI/CD platform secret stores
- Reduce PAT scope to minimum required permissions (never use org-wide access for individual applications)
- Implement automatic token rotation policies and expiration windows (e.g., 90-day rotation)
- Use GitHub fine-grained PATs instead of classic tokens with narrowed repository and permission scopes
- Enforce branch protection rules, code review requirements, and audit logging for all repository modifications
- Conduct regular credential audits and revoke unused or suspicious tokens
- Educate developers on secure credential handling and provide secure development guidelines
- Monitor GitHub audit logs for suspicious API activity and unauthorized commits

## Variant hunting
Search employee applications and containers for other exposed GitHub tokens or related credentials
Audit GitHub audit logs for unusual API calls, commits, or pushes using the compromised token's timeline
Review git history for commits containing patterns matching PAT format (github_pat_, ghp_, gho_, ghu_, ghs_)
Check environment variable listings, configuration files, and documentation that may reference token storage
Scan Docker images, container registries, and build artifacts for embedded credentials
Investigate similar credential exposure in other platforms (GitLab, Bitbucket, Azure DevOps)
Analyze if the token was used to access or modify any repositories since creation

## MITRE ATT&CK
- T1187
- T1552.001
- T1550.001
- T1021.003
- T1190
- T1199
- T1556

## Notes
This report demonstrates a critical supply chain risk where a single compromised credential grants access to an entire organization's codebase. The proof-of-concept using SHA512 of a specific README commit confirms successful repository access. This is particularly severe for organizations like Shopify where code repositories contain intellectual property and may be used to inject malicious code affecting downstream users.

## Full report
<details><summary>Expand</summary>

While dissecting an application made by one of your employees I found his GitHub Personal Access Token (PAT), he's a member of the org with pull and push access to all of your repositories. 
As a proof I can tell you that on the repo github.com/Shopify/shopify at commit hash `cea9c273391d` the sha512 of the README.md is `69750574bec56c1f1052db3471252b1daacdc9dda9f6d5332a3400a847fa413ec1caf19ef0b5501f18a5a76c232e7210d5f3b91c24c9439f4e0f64c02d6db824`.

## Impact

Read and write access to all your private github repositories.

</details>

---
*Analysed by Claude on 2026-05-11*
