# Privilege Escalation via Overly Permissive sts:AssumeRole in experimental-programmatic-access-ccft Lambda Function

## Metadata
- **Source:** HackerOne
- **Report:** 2808412 | https://hackerone.com/reports/2808412
- **Submitted:** 2024-10-29
- **Reporter:** zolaer9527
- **Program:** AWS Serverless Application Repository
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Privilege Escalation, Overly Permissive IAM Permissions, Insufficient Access Control, Lateral Movement
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The experimental-programmatic-access-ccft AWS CloudFormation Template creates a Lambda function with an overly permissive IAM role that grants sts:AssumeRole permissions to all resources (*). An attacker can exploit this to assume roles across the AWS Organization and escalate their privileges. This vulnerability enables lateral movement and privilege escalation within the organization's AWS infrastructure.

## Attack scenario
1. Attacker deploys the experimental-programmatic-access-ccft application in their AWS account through the Serverless Application Repository
2. Attacker observes the ExtractCarbonEmissionsFunction Lambda function is assigned an IAM role with sts:AssumeRole on '*' resources
3. Attacker enumerates IAM roles available in the AWS Organization that they could assume
4. Attacker uses the Lambda execution role to call sts:AssumeRole against high-privilege roles in other accounts (e.g., admin roles)
5. Attacker successfully assumes the target role, gaining elevated permissions in other AWS accounts
6. Attacker performs unauthorized actions in the compromised accounts using the assumed role credentials

## Root cause
The CloudFormation template uses overly broad IAM permissions by granting sts:AssumeRole to all resources ('*') without resource-level restrictions, permission boundaries, or validation of which roles should be assumable. This violates the principle of least privilege.

## Attacker mindset
An attacker would target this vulnerability as a straightforward path to lateral movement within an AWS Organization. By identifying an application with overly permissive STS permissions, they can chain this access to assume higher-privileged roles and expand their foothold across multiple accounts.

## Defensive takeaways
- Implement principle of least privilege: restrict sts:AssumeRole to specific role ARNs rather than wildcard '*'
- Remove unnecessary STS permissions entirely if they are not required for normal application functionality
- Use IAM permissions boundaries to limit the maximum permissions an assumed role can have
- Conduct regular IAM permission audits to identify overly permissive policies in CloudFormation templates
- Use AWS tools like IAM Access Analyzer to detect overly permissive policies before deployment
- Implement conditions on AssumeRole (e.g., ExternalId, IP restrictions) to prevent unauthorized assumption
- Apply resource-based policies on sensitive roles to restrict who can assume them
- Enable CloudTrail logging to detect suspicious AssumeRole calls

## Variant hunting
Search for similar patterns in other AWS Serverless Application Repository templates, custom CloudFormation templates, and IaC code that grant sts:AssumeRole, sts:GetCallerIdentity, or other STS permissions with wildcard resources. Check for other AWS-managed policies that may be overly permissive when applied to Lambda execution roles.

## MITRE ATT&CK
- T1078
- T1136
- T1548
- T1550

## Notes
This vulnerability is particularly dangerous in organizational AWS environments where multiple accounts exist. The Serverless Application Repository makes it easy for users to deploy templates without thoroughly reviewing IAM permissions. The remediation should be applied to the template before it's re-published to prevent future deployments from inheriting the same vulnerability.

## Full report
<details><summary>Expand</summary>

**Summary:**  I found a potential risk in the experimental-programmatic-access-ccft when I deployed it in the AWS Serverless Application Repository. A malicious can leverage the "sts:AssumeRole" permissions for "*" resources to escalate permission.

**Description:**  The experimental-programmatic-access-ccft application creates a function named ExtractCarbonEmissionsFunction, and the associated role is assigned policies with permissions such as "sts:AssumeRole " for  "*"  resources. A malicious user can leverage the "sts:AssumeRole" permissions to assume into any AWS Account in the AWS Organization, resulting in privilege escalation. This poses a significant security risk to the account used to deploy the application.



## Remediation Instructions
1. Use finer-grained authorization policies to replace the AWS-managed policies. And use the specific resource names to replace the "*".
2. The permissions for STS resources should be removed if they do not affect normal functionality.
3. Add a permissions boundary to restrict the permission.

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on: (AWS S3, Amazon Lambda, etc): Amazon Lambda

## Impact

## Summary:
A malicious user could leverage these permissions to escalate his/her privilege.

</details>

---
*Analysed by Claude on 2026-05-24*
