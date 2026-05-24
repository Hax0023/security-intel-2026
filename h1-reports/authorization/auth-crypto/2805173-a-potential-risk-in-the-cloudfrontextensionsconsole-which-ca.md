# Excessive IAM Permissions in CloudFront Extensions Console Lambda Functions Enable Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 2805173 | https://hackerone.com/reports/2805173
- **Submitted:** 2024-10-26
- **Reporter:** zolaer9527
- **Program:** AWS Labs (CloudFront Extensions Console)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Privilege Escalation, Excessive Permissions, IAM Misconfiguration, Overly Permissive Roles
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The CloudFront Extensions Console application created multiple Lambda functions sharing IAM roles with excessive permissions, including iam:CreateRole, iam:AttachRolePolicy, and iam:* on all resources. A malicious user with access to these Lambda functions could leverage these permissions to escalate privileges to full AWS account administrator.

## Attack scenario
1. Attacker gains access to invoke a Lambda function created by CloudFront Extensions Console (cf_config_version_exporter, cf_config_version_manager, etc.)
2. Attacker uses the Lambda's attached role which has iam:CreatePolicy and iam:CreateRole permissions on all resources
3. Attacker creates a new IAM role with full AdministratorAccess policy attached
4. Attacker creates or modifies an IAM user/role they can assume with the new powerful role
5. Attacker assumes the newly created role and gains full administrator access to the AWS account
6. Attacker can now perform any action including data exfiltration, resource deletion, or lateral movement

## Root cause
Infrastructure-as-Code (CloudFormation) templates defined overly permissive IAM roles without applying principle of least privilege. Multiple functions shared a single role, and wildcard resources were used instead of specific ARNs. No permission boundaries were implemented.

## Attacker mindset
An insider or attacker with legitimate access to invoke Lambda functions could exploit the excessive permissions to persistently escalate privileges and gain complete control over the AWS account without triggering obvious alerts.

## Defensive takeaways
- Apply principle of least privilege: grant only necessary permissions for specific resources
- Use separate IAM roles per Lambda function instead of shared roles
- Replace wildcard resources (*) with specific ARNs
- Implement IAM permission boundaries to restrict maximum permissions a role can have
- Regularly audit IAM policies attached to Lambda functions and other services
- Use AWS Access Analyzer to identify overly permissive policies
- Implement preventive controls like SCPs (Service Control Policies) to deny dangerous IAM operations
- Enable CloudTrail logging and monitor IAM API calls for anomalies
- Remove IAM permissions that don't directly support core functionality

## Variant hunting
Search for other Lambda-based applications in AWS Labs and open-source repositories with similar patterns: shared IAM roles, wildcard resources, iam:* permissions, iam:AttachRolePolicy without resource restrictions, missing permission boundaries on service roles

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1098 - Account Manipulation
- T1110 - Brute Force
- T1199 - Trusted Relationship
- T1578 - Modify Cloud Compute Infrastructure

## Notes
This vulnerability is particularly dangerous because it affects infrastructure-as-code templates that may be deployed across multiple organizations. The vulnerability exists at infrastructure deployment time, not runtime, making it a supply chain risk. CloudFormation templates should be reviewed by security teams before deployment.

## Full report
<details><summary>Expand</summary>

**Summary:**  I found a potential risk in the cloudFrontExtensionsConsole when I deployed it in the awslabs repository on GitHub. The application created functions and the roles of the functions had too many excessive permissions. A  malicious user could leverage these permissions to escalate his/her privilege in multiple ways.

**Description:** First, the cloudFrontExtensionsConsole application created four functions that are cf_config_version_exporter, cf_config_version_manager, cf_config_version_manager_graphql, and cloudFrontExtensionsConso-SingletonLambdaf7d4f7304-ZbLF9YFgQ4eq rLambdaFunction. These functions share the same role which is cloudFrontExtensionsConso-CloudFrontConfigVersionCo-rAgdktzDTPRh. The role has the "iam:CreateRole", "iam:GetRole", "iam:CreatePolicy", and "iam:AttachRolePolicy" for "*" resources.  A  malicious user could leverage these permissions to escalate his/her privilege in multiple ways. For example, he/she can leverage the AttachRolePolicy permission to attach the AWS-managed policy or the policy created by the CreatePolicy to the role that he/she can access. It could allow a user to gain full administrator access to the AWS account.

Second, the cloudFrontExtensionsConsole application also created two functions that are cloudFrontExtensionsConso-RepoConstructSyncExtensi-ydrYwNGQCoFr and cloudFrontExtensionsConso-RepoConstructExtDeployer-1uHGWxrjog9S. These two functions share the same role which is cloudFrontExtensionsConso-RepoConstructExtDeployerR-wBEukYirZfbr. The role has the "iam:*" for "*" resources. These permissions can be exploited in more ways, including but not limited to the attack methods mentioned above.

In a word, the functions created by the cloudFrontExtensionsConsole have too many excessive permissions, which could cause very serious consequences.


## Remediation Instructions
1. Use finer-grained authorization roles to replace the way that many functions share one role. And use the specific resource names to replace the "*".
2. The permissions for IAM resources should be removed if they do not affect normal functionality.
3. Add a permissions boundary to restrict the permission.

## Impact

## Summary:
A  malicious user could leverage these permissions to escalate his/her privilege.

</details>

---
*Analysed by Claude on 2026-05-24*
