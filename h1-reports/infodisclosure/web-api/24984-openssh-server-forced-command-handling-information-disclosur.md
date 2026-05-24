# OpenSSH Forced Command Handling Information Disclosure (CVE-2012-0814)

## Metadata
- **Source:** HackerOne
- **Report:** 24984 | https://hackerone.com/reports/24984
- **Submitted:** 2014-08-18
- **Reporter:** simon90
- **Program:** blog.greenhouse.io
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Information Disclosure, Debug Information Exposure, Privilege Boundary Crossing
- **CVEs:** CVE-2012-0814
- **Category:** web-api

## Summary
OpenSSH versions before 5.7 leak sensitive information through debug messages in the auth_parse_options function, exposing authorized_keys command options to remote authenticated users. This vulnerability crosses privilege boundaries, allowing users with restricted accounts (no shell/filesystem access) to discover commands and configurations they should not have access to, particularly affecting shared accounts like those used by Gitolite.

## Attack scenario
1. Attacker authenticates to SSH server using valid credentials for a restricted account (e.g., Gitolite shared account with no shell access)
2. Attacker enables verbose/debug logging or monitors SSH connection output to capture debug messages
3. SSH daemon's auth_parse_options function processes authorized_keys entries and outputs debug messages containing command options
4. Attacker reads leaked debug output revealing sensitive command configurations, restrictions, and other account metadata
5. Attacker uses discovered information to understand system architecture, bypass restrictions, or chain with other vulnerabilities
6. Information disclosure crosses privilege boundaries since restricted accounts normally have no filesystem access to read authorized_keys files

## Root cause
The auth_parse_options function in auth-options.c outputs debugging information containing the full content of command options from authorized_keys entries. This debug output is accessible to authenticated users regardless of their intended privilege level, creating an unintended information leak across privilege boundaries.

## Attacker mindset
A privileged attacker or insider with valid credentials to a restricted account seeks to gather system intelligence. By leveraging debug output, they can discover what commands they're allowed to execute, what restrictions exist, and potentially exploit this information in multi-stage attacks. For shared accounts like Gitolite, this breaks isolation assumptions.

## Defensive takeaways
- Upgrade OpenSSH to version 5.7 or later immediately
- Disable SSH debug logging in production environments or restrict debug output visibility
- Never place sensitive command configurations in authorized_keys - use separate policy files with restricted permissions
- Implement principle of least privilege for shared accounts used by automation tools
- Monitor SSH debug output and restrict access to logs containing authentication details
- Audit all accounts with command restrictions to ensure information leakage didn't occur
- Use separate service accounts with distinct authorized_keys instead of shared accounts where possible

## Variant hunting
Check for similar debug output leaks in other authentication mechanisms (PAM, sudo, su)
Hunt for unintended information disclosure in other OpenSSH subsystems (config parsing, key validation)
Investigate whether verbose logging flags (ssh -vvv) in client-side retain similar issues
Search for comparable privilege boundary crossing issues in SSH key management tools and wrappers
Test if other restricted-account scenarios (e.g., rsync-only, git-only accounts) leak sensitive configuration

## MITRE ATT&CK
- T1552.007 - Unsecured Credentials: Container Environment Variables (information in environment/debug)
- T1526 - Active Scanning (reconnaissance through debug output)
- T1087.003 - Account Discovery: Email Account (discovery of account configurations)
- T1040 - Traffic Capture or Redirection (capturing debug output)
- T1518 - Software Discovery (discovering allowed commands and policies)

## Notes
CVE-2012-0814 assigned. Report targets OpenSSH 5.5p1 on Debian. The vulnerability is particularly impactful for Gitolite and similar tools using shared SSH accounts with forced commands, as it violates the privilege isolation model. The crossing of privilege boundaries makes this more severe than typical information disclosure - users with intentionally no shell access gain knowledge they should never have access to.

## Full report
<details><summary>Expand</summary>

Summary of the issue:


The auth_parse_options function in auth-options.c in sshd in OpenSSH before 5.7 provides debug messages containing

authorized_keys command options, which allows remote authenticated users to obtain potentially sensitive information

by reading these messages, as demonstrated by the shared user account required by Gitolite. NOTE: this can cross

privilege boundaries because a user account may intentionally have no shell or filesystem access, and therefore may

have no supported way to read an authorized_keys file in its own home directory.

OpenSSH before 5.7 is affected.

Attack details..:

According to its banner, the version of OpenSSH installed on the remote

host is older than 5.7:

ssh-2.0-openssh_5.5p1 debian-6+squeeze5

Summary:

The auth_parse_options function in auth-options.c in sshd in OpenSSH before 5.7

provides debug messages containing authorized_keys command options, which allows

remote authenticated users to obtain potentially sensitive information by

reading these messages, as demonstrated by the shared user account required by

Gitolite. NOTE: this can cross privilege boundaries because a user account may

intentionally have no shell or filesystem access, and therefore may have no

supported way to read an authorized_keys file in its own home directory.

OpenSSH before 5.7 is affected;

Solution/Fix: Updates are available.

References: CVE: CVE-2012-0814 (http://www.securityfocus.com/bid/51702, etc..)

Br,

Simone

</details>

---
*Analysed by Claude on 2026-05-24*
