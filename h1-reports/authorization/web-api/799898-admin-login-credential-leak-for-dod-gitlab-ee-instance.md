# Admin Login Credential Leak for DoD Gitlab EE instance

## Metadata
- **Source:** HackerOne
- **Report:** 799898 | https://hackerone.com/reports/799898
- **Submitted:** 2020-02-19
- **Reporter:** daehee
- **Program:** DoD/DISA
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Credential Exposure, Hardcoded Credentials, Secret Management Failure, Insufficient Access Controls
- **CVEs:** None
- **Category:** web-api

## Summary
A DoD employee/contractor exposed administrative credentials for a private Gitlab Enterprise Edition instance in a public GitHub repository, allowing full administrative access to the system. The default Gitlab username and password were committed to source control, enabling any attacker to gain complete control of the platform and access sensitive DoD source code and secrets.

## Attack scenario
1. Attacker performs GitHub repository search for the exposed subdomain/hostname from TLS certificate
2. Attacker discovers GitHub commit containing hardcoded Jenkins credentials and Gitlab admin password
3. Attacker identifies the default Gitlab EE admin username from public documentation or reconnaissance
4. Attacker navigates to the Gitlab EE instance (identified via IP/hostname enumeration) and attempts login with discovered credentials
5. Attacker successfully authenticates as administrator and gains full access to private repositories, configuration, and user management
6. Attacker exfiltrates sensitive source code, API keys, tokens, and other secrets from private repositories

## Root cause
Security misconfigurations and practices: (1) Default credentials not changed from Gitlab deployment, (2) Credentials committed to version control without sanitization, (3) Public GitHub repository containing sensitive DoD infrastructure credentials, (4) Lack of credential scanning/pre-commit hooks, (5) Insufficient secrets management policy enforcement

## Attacker mindset
External reconnaissance attacker performing targeted search of public repositories for exposed DoD infrastructure. Leverages common security misconfigurations (default credentials, exposed secrets in source control) to gain rapid administrative access without requiring exploitation. Opportunistic approach focusing on low-effort, high-impact credential discovery.

## Defensive takeaways
- Implement mandatory pre-commit hooks to detect and prevent credentials from being committed to repositories
- Use secrets management solutions (Vault, AWS Secrets Manager) instead of hardcoding credentials in source code or configuration
- Change all default credentials immediately after deployment and enforce complex passwords
- Implement GitHub secret scanning and enable branch protection rules requiring security scanning
- Conduct regular credential rotation policies for all administrative and service accounts
- Monitor public repositories for exposed infrastructure hostnames and credentials using automated tools
- Implement network segmentation to restrict administrative access to Gitlab instances to specific IP ranges
- Enable multi-factor authentication for all administrative accounts
- Audit all existing repositories and commits for exposed credentials and rotate any discovered secrets
- Implement audit logging and alerting for administrative access to track unauthorized login attempts

## Variant hunting
Search for similar patterns: (1) Default Gitlab credentials in public repos (gitlab-runner, omnibus installations), (2) Other DoD/DISA contractor repositories with exposed AWS/Azure credentials, (3) Jenkins credentials exposed alongside Gitlab access (pipeline integrations), (4) TLS certificate enumeration of other DoD subdomains in public certificate logs (CT logs), (5) GitHub commits from DoD contractor email domains with JENKINS_, GITLAB_, or other environment variable patterns

## MITRE ATT&CK
- T1190
- T1200
- T1589
- T1590
- T1591
- T1592
- T1593
- T1598
- T1621
- T1040
- T1087
- T1110
- T1555
- T1187
- T1056
- T1557
- T1111
- T1021
- T1078
- T1199
- T1036
- T1556
- T1564
- T1480
- T1552

## Notes
Report demonstrates critical impact of credential exposure in government/military contexts. Redactions indicate classified/sensitive information. Researcher demonstrated responsible disclosure by confirming access without further exploitation. The multi-stage discovery (TLS cert -> GitHub search -> credential extraction) represents practical attack chain. High risk due to interconnected DoD systems potentially sharing same credentials. Lack of bounty amount in report suggests potential classification restrictions or government bounty program handling.

## Full report
<details><summary>Expand</summary>

## Summary

A DoD employee/contractor exposed the ███ password in a GitHub repository ([█████████](https://█████)) leading to full ███ access in a DoD DISA-associated private Gitlab EE instance (`███`).

## Description

The IP address `████` recently hosted the subdomain `█████████` (as of 2019-09-23). 

██████

Now `port 80` points to a private Gitlab Enterprise Edition instance. The current hostname is `██████` and the TLS certificate points to `████`.

```
HTTP/1.1 301 Moved Permanently
Server: nginx
Date: Tue, 18 Feb 2020 12:30:01 GMT
Content-Type: text/html
Content-Length: 162
Connection: keep-alive
Location: https://████:443/
```

Going to `https://██████████/explore` shows no projects, groups, or snippets exposed publicly.

However, a Github search for `█████████` as displayed in the TLS certificate leads to a few interesting code commits. This commit  ([████████](https://██████████)) for a project titled "██████ (█████)" contains █████ credentials for a particular Jenkins instance.

```
- name: JENKINS_OC_USER
value: ███████
- name: JENKINS_OC_PASSWD
value: ████████
```

The default Gitlab EE username `████████`  with the password `██████`, as shown in GitHub commit, gains full █████████istrative access.

After confirming valid login, I made no further attempts to escalate privileges on the machine, nor attempted deeper access into the private contents of this Gitlab EE instance. 

## Suggested Mitigation/Remediation Actions

In addition to updating security credentials to this Github commit, you might want to review any other DoD applications that are possibly using the same password.

### Other

In addition to updating ██████ credentials for this Gitlab EE application, you might want to review any other DoD applications that are possibly using the same password.

## Impact

Exploited by a malicious actor, the security impact of this leak could include:

* Leverage valid credential to gain access to other DoD applications
* View sensitive source code in private repositories
* Access potential secret tokens, API keys, passwords contained in source code
* Change user information
* Access other user accounts
* Create new unauthorized repositories
* Host malicious content

</details>

---
*Analysed by Claude on 2026-05-24*
