# Privilege Escalation via Excessive IAM Permissions in aws-lambda-ecs-run-task

## Metadata
- **Source:** HackerOne
- **Report:** 2894222 | https://hackerone.com/reports/2894222
- **Submitted:** 2024-12-11
- **Reporter:** zolaer9527
- **Program:** AWS Labs
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Excessive Permissions, Privilege Escalation, Insecure IAM Configuration, Over-Privileged Service Role
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The aws-lambda-ecs-run-task application creates a Lambda function with an IAM role attached to the AdministratorAccess policy, granting unrestricted permissions on all AWS resources. An attacker who gains control of this Lambda function could escalate privileges and perform arbitrary actions on the entire AWS account with administrative access.

## Attack scenario
1. Attacker identifies the aws-lambda-ecs-run-task Lambda function deployed in the target AWS account
2. Attacker gains access to invoke the Lambda function through misconfigured resource-based policies or public endpoint exposure
3. Attacker crafts a malicious payload or modifies the function code to execute arbitrary AWS API calls
4. Using the attached rLambdaFunctionRole with AdministratorAccess, attacker calls AWS APIs to create new IAM users, roles, or assume additional roles
5. Attacker exfiltrates sensitive data, modifies infrastructure, or establishes persistence mechanisms across the entire AWS account
6. Attacker achieves full account takeover with root-level privileges

## Root cause
The application follows an anti-pattern of attaching the AWS managed AdministratorAccess policy directly to a service-level IAM role rather than implementing the principle of least privilege by granting only specific, necessary permissions for the Lambda function's intended operations.

## Attacker mindset
An attacker would recognize that compromising a single Lambda function with administrative permissions provides a high-value pivot point for lateral movement and account-wide compromise, making this an attractive target for initial access exploitation or post-compromise privilege escalation.

## Defensive takeaways
- Never use AdministratorAccess or other AWS managed policies with wildcard permissions for service roles; instead, create custom IAM policies granting only required permissions
- Implement the principle of least privilege by explicitly defining allowed actions, resources, and conditions in IAM policies
- Regularly audit and validate IAM role permissions using tools like IAM Access Analyzer to detect over-privileged roles
- Use resource-based policies to restrict Lambda function invocation to trusted principals only
- Enable CloudTrail logging and monitor for suspicious API calls from Lambda execution roles
- Implement code review processes to catch insecure IAM configurations before deployment
- Use Infrastructure-as-Code scanning tools to detect overly permissive IAM policies in CloudFormation or Terraform templates

## Variant hunting
Search for other Lambda functions in the repository with AdministratorAccess or similar broad permissions
Check for ECS task definitions, EC2 instances, or other services using overly permissive IAM roles
Review all AWS managed policy attachments to custom roles in CloudFormation/Terraform templates
Look for inline policies within roles that lack resource restrictions or condition statements
Identify service roles used in examples or templates that could be copy-pasted into production environments
Examine other awslabs repositories for similar IAM configuration anti-patterns

## MITRE ATT&CK
- T1190
- T1078
- T1136
- T1098
- T1087
- T1580

## Notes
This vulnerability represents a configuration weakness rather than a code defect. The risk is amplified in shared repositories and examples because developers may deploy these templates directly to production without understanding the security implications. The use of AdministratorAccess in lab/example code sets a poor security precedent and normalizes dangerous IAM practices.

## Full report
<details><summary>Expand</summary>

**Summary:** I found a potential risk in the aws-lambda-ecs-run-task when I deployed it in the awslabs repository on GitHub. The application created a function with a role that has too many excessive permissions. A  malicious user could leverage these permissions to escalate his/her privilege in multiple ways.


**Description:** The aws-lambda-ecs-run-task application creates a function named rLambdaFunction, which has a role named rLambdaFunctionRole with the arn:aws:iam::aws:policy/AdministratorAccess policy. The policy allows for any action on all resources. That means the attacker can leverage these permissions to escalate privileges. If a malicious controlled this function, he/she can directly do what he/she wants to do as a root.

## Impact

## Summary:
A malicious user could leverage these permissions to escalate his/her privilege.

</details>

---
*Analysed by Claude on 2026-05-24*
