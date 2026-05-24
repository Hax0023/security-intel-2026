# Non-Production API Endpoints for Bedrock Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 2951803 | https://hackerone.com/reports/2951803
- **Submitted:** 2025-01-21
- **Reporter:** nick_frichette_dd
- **Program:** AWS Bug Bounty
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Insufficient Logging, Detection Evasion, CloudTrail Bypass, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Five non-production endpoints in the AWS Bedrock service fail to log API calls to CloudTrail while still accepting standard IAM credentials, allowing adversaries to silently enumerate permissions without detection. Attackers can invoke bedrock:ListImportedModels and bedrock:ListModelImportJobs operations on these endpoints without generating audit trails, enabling invisible credential validation and permission discovery.

## Attack scenario
1. Attacker obtains compromised AWS IAM credentials through credential theft or supply chain compromise
2. Attacker uses automated tools or manual CLI commands to systematically test permissions by calling various AWS API operations
3. Attacker calls bedrock operations (ListImportedModels, ListModelImportJobs) against non-production endpoints instead of standard endpoints
4. API calls succeed or fail based on actual IAM permissions but do NOT generate CloudTrail logs
5. Attacker maps out compromised account's permissions invisibly, building a privilege enumeration profile
6. Attacker uses permission enumeration results to plan further attacks with confidence, without triggering CloudTrail-based detection systems

## Root cause
Non-production Bedrock API endpoints are configured to accept standard IAM credentials and execute legitimate API operations (bedrock:ListImportedModels, bedrock:ListModelImportJobs) but are isolated from CloudTrail logging infrastructure. These endpoints maintain normal IAM permission behavior while bypassing audit logging mechanisms.

## Attacker mindset
An attacker with stolen credentials seeks to silently profile account permissions and capabilities before launching targeted attacks. By discovering that certain API endpoints don't log to CloudTrail, they can perform reconnaissance invisibly, gaining confidence in which operations are available without triggering security alerts that typically activate on failed permission attempts.

## Defensive takeaways
- Ensure all API endpoints (production and non-production) that accept IAM credentials are consistently logged to CloudTrail
- Implement comprehensive CloudTrail logging for all AWS service endpoints, including development and testing endpoints
- Monitor for credential validation patterns and permission enumeration behavior using alternative detection methods (VPC Flow Logs, DNS logs, API call patterns)
- Regularly audit and catalog all service endpoints to identify logging gaps
- Apply principle of least privilege to non-production endpoints and consider restricting access to specific identities
- Implement alerting on failed API calls across all endpoints, not just production ones

## Variant hunting
Hunt for other AWS services with non-production endpoints that accept standard IAM credentials without CloudTrail logging. Previous findings include bedrock-agent and ssm services with similar characteristics. Check any service with staging, testing, or development endpoints that maintain separate infrastructure from production CloudTrail logging. Prioritize services that handle sensitive operations or data access patterns.

## MITRE ATT&CK
- T1590.4 - Gather Victim Identity Information (Cloud Accounts)
- T1526 - Enumerate Cloud Resources
- T1087.004 - Account Discovery (Cloud Account)
- T1087.001 - Account Discovery (Local Account)
- T1552.007 - Unsecured Credentials (Cloud Instance Metadata)
- T1204.001 - User Execution (Malicious Link)

## Notes
This vulnerability was previously disclosed publicly by the researcher through blog posts, Black Hat USA 2023, and fwd:cloudsec 2023 presentations. AWS Security has officially stated that non-production endpoints lacking CloudTrail logging while accepting normal credentials constitute a security issue warranting disclosure to aws-security@amazon.com. The CVSS score of 5.0 (Medium) reflects the Integrity impact (I:L) from undetectable unauthorized activity and high confidence/integrity/availability requirements. The lack of customer partition data access limits the severity, but the detection evasion capability remains significant for post-compromise credential abuse scenarios.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](https://sysdig.com/blog/scarleteel-2-0/) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](█████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration). 

**We have found 5 non-production endpoints for the bedrock service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail.  More specifically, they can invoke [bedrock:ListImportedModels](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/bedrock/list-imported-models.html) and [bedrock:ListModelImportJobs](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/bedrock/list-model-import-jobs.html). 

AWS has previously [stated](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#the-response-from-aws) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws bedrock list-imported-models
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws bedrock list-imported-models --endpoint-url ██████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

bedrock

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

5.0 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/CR:H/IR:H/AR:H
(Note: That is the score I received on my previous submission for the same issue [here](███████))

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration) and spoke about it at Black Hat USA 2023 (██████) and fwd:cloudsec 2023 (█████████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
- [bedrock-agent](██████)
- [ssm](█████████)

It is important to note that there are two categories at play here. 

The following is a list of endpoints we found that have exhibited this behavior:

	* ██████
	* ██████
	* ████████
	* █████████
	* ███████

## Impact

An adversary can enumerate permissions of compromised credentials for two actions from the bedrock service without logging to CloudTrail. We have found 5 non-production endpoints which exhibit this behavior.

</details>

---
*Analysed by Claude on 2026-05-24*
