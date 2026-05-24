# Postgres Admin Credentials Exposed in GitLab Commit History

## Metadata
- **Source:** HackerOne
- **Report:** 1561448 | https://hackerone.com/reports/1561448
- **Submitted:** 2022-05-06
- **Reporter:** guusverbeek
- **Program:** Upchieve
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Sensitive Data Exposure, Hardcoded Credentials, Insecure Storage of Secrets
- **CVEs:** None
- **Category:** uncategorised

## Summary
Postgres admin username and password were committed in plain text to a public GitLab repository. An attacker with access to the repository commit history can extract valid database credentials and gain unauthorized administrative access to the PostgreSQL database.

## Attack scenario
1. Attacker discovers the public GitLab repository through repository enumeration or public source code searches
2. Attacker reviews commit history and identifies the exposed credentials in the specified commit
3. Attacker extracts the PostgreSQL admin username and password from the plaintext commit
4. Attacker uses credentials to connect to the PostgreSQL database with administrative privileges
5. Attacker gains full database access including data exfiltration, modification, or deletion capabilities

## Root cause
Developer inadvertently committed sensitive credentials directly into version control without using environment variables, secrets management systems, or .gitignore rules to prevent exposure.

## Attacker mindset
Opportunistic attacker performing reconnaissance on publicly available repositories, leveraging automated tools to search for common credential patterns in commit histories, aiming for quick database access for data theft or system compromise.

## Defensive takeaways
- Never commit secrets, passwords, or API keys directly into version control repositories
- Implement pre-commit hooks to scan for sensitive patterns before allowing commits
- Use environment variables and secrets management tools (HashiCorp Vault, AWS Secrets Manager, GitLab CI/CD secrets) for credential storage
- Configure .gitignore to exclude configuration files containing credentials
- Implement branch protection rules requiring code review before merging
- Regularly audit commit history for exposed credentials and rotate compromised credentials immediately
- Use GitLab's built-in secret detection features to prevent secrets from being pushed
- Implement least privilege database accounts for different application functions
- Enable database audit logging to detect unauthorized access attempts

## Variant hunting
Search commit history for other common database password patterns (mysql_password, db_password, PGPASSWORD)
Check environment configuration files (.env, config.yml, settings.py) in the repository for hardcoded credentials
Review pull request history for similar credential exposures across the organization
Search for API keys, SSH private keys, and authentication tokens in commit history
Examine backup or configuration branches for exposed credentials

## MITRE ATT&CK
- T1190
- T1555
- T1110
- T1021
- T1071

## Notes
Even though the repository or commit may no longer be publicly accessible, the credentials should be considered fully compromised. The commit history on GitLab may still be accessible to users with repository access. All Postgres administrative credentials should be immediately rotated. A comprehensive audit of database access logs is recommended to identify potential unauthorized access.

## Full report
<details><summary>Expand</summary>

## Summary:
Gitlab commit contains password in plain text

## Steps To Reproduce:
Navigate to 
https://gitlab.com/upchieve/subway/-/commit/e0e039496321c9d62a591504d387589224660a5c

## Supporting Material/References:


## Recommendations for Fixing/Mitigation
Do not disclose passwords in gitlab.
Implement a check that prevents developers from uploading passwords in plain text.
Use secure passwords.

## Impact

An attacker can login to the Postgres DB with admin privileges

</details>

---
*Analysed by Claude on 2026-05-24*
