# Github OSINT: Reconnaissance and Sensitive Data Exposure through Github Dorks

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** General Security Research / Bug Bounty Community
- **Bounty:** Not specified - Educational writeup
- **Severity:** High
- **Vuln types:** Information Disclosure, Credential Exposure, API Key Leakage, OSINT/Recon, Hardcoded Secrets
- **Category:** uncategorised
- **Writeup:** https://medium.com/@ghostlulzhacks/github-osint-1e8a96f9fdb8

## Summary
This writeup describes techniques for discovering sensitive information exposed through public Github repositories, including credentials, API keys, SSH passwords, and other secrets accidentally committed by developers. The author demonstrates how Github Dorks (similar to Google Dorks) can systematically identify exposed files and sensitive data across Github, and how directly monitoring company Github pages and employee accounts can reveal further vulnerabilities.

## Attack scenario (step by step)
1. Attacker identifies a target organization and locates their public Github organization page
2. Attacker enumerates all developers/employees associated with the company via the 'people' tab
3. Attacker crafts Github dorks using filenames (e.g., filename:.bash_history DOMAIN-NAME) to search for sensitive files
4. Attacker searches for common secret patterns (passwords, tokens, api_keys) combined with company domain or employee names
5. Attacker discovers exposed credentials, SSH keys, or API keys in public repositories or commit history
6. Attacker uses discovered credentials to gain unauthorized access to systems, applications, or infrastructure

## Root cause
Developers inadvertently commit sensitive files and credentials to public Github repositories without proper .gitignore configuration, pre-commit hooks, or secrets scanning tools; lack of developer security awareness regarding what should not be committed to version control.

## Attacker mindset
Patient, methodical reconnaissance operator viewing Github as a primary intelligence source during initial access phases; recognizes that repositories contain valuable metadata, credentials, and architectural information; understands that larger organizations with more developers statistically have higher likelihood of exposure; treats Github OSINT as scalable reconnaissance requiring minimal detection risk.

## Defensive takeaways
- Implement mandatory pre-commit hooks to scan for common credential patterns before code commits
- Use tools like git-secrets, detect-secrets, or TruffleHog to automatically detect hardcoded secrets in repositories
- Enforce strict .gitignore policies and security training for all developers on what should never be committed
- Rotate and revoke any credentials found in public repositories immediately
- Implement Github organization settings to enforce branch protection rules, code review requirements, and secret scanning
- Use Github's built-in secret scanning and push protection features
- Monitor public Github repositories owned by organization and employee accounts using automated tools
- Implement vault solutions (HashiCorp Vault, AWS Secrets Manager) to manage secrets externally from code
- Establish secure development lifecycle (SDLC) training emphasizing secrets management
- Regularly audit public repositories and git history for exposed credentials

## Variant hunting
Search for similar OSINT techniques including: GitLab dorks, Bitbucket repository exposure, Docker Hub registry scanning, npm/PyPI package analysis for embedded credentials, commit message analysis revealing infrastructure details, public cloud storage bucket enumeration (S3, Azure Blobs), Pastebin/GitHub gist monitoring, employee social media profiles linking to repositories, Github actions workflow files exposing secrets, and browser history/cached credentials in publicly archived repositories.

## MITRE ATT&CK
- T1592 - Gather Victim Org Information (Github reconnaissance)
- T1594 - Search Victim-Owned Websites (Github org/repo crawling)
- T1589 - Gather Victim Identity Information (Employee enumeration via Github)
- T1598 - Phishing for Information (reconnaissance to support phishing)
- T1200 - Hardware Additions (if SSH keys found)
- T1199 - Trusted Relationship (using discovered credentials)
- T1110 - Brute Force (use of discovered credentials)
- T1187 - Forced Authentication (discovered creds for lateral movement)

## Notes
This is a foundational OSINT writeup demonstrating reconnaissance techniques rather than a specific vulnerability disclosure. The techniques described are well-known and widely used in security research. Value lies in practical dork examples and systematic methodology. The bash_history example is particularly relevant as shell history files often contain unencrypted credentials. This represents a critical vulnerability class (CWE-798: Use of Hard-Coded Credentials) that should be addressed at the development process level rather than individually patched.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
