# Non-Production API Endpoints for Global Accelerator Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3029552 | https://hackerone.com/reports/3029552
- **Submitted:** 2025-03-10
- **Reporter:** nick_frichette_dd
- **Program:** AWS Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Information Disclosure, Observability Gap
- **CVEs:** None
- **Category:** uncategorised

## Summary
Eight non-production API endpoints for AWS Global Accelerator service fail to log requests to CloudTrail while remaining callable with standard IAM credentials. An adversary with compromised AWS credentials can enumerate IAM permissions silently by invoking these endpoints and analyzing responses, bypassing detection mechanisms that typically rely on CloudTrail audit logs.

## Attack scenario
1. Attacker obtains AWS IAM credentials through credential theft, phishing, or supply chain compromise
2. Attacker identifies non-production Global Accelerator endpoints that accept standard IAM authentication
3. Attacker makes API calls to these endpoints (e.g., list-accelerators) using the compromised credentials
4. Attacker analyzes response codes (success/failure) to determine what permissions the compromised identity has
5. Attacker performs large-scale permission enumeration across multiple Global Accelerator operations without triggering CloudTrail alerts
6. Security team has no audit trail of permission enumeration activity, preventing detection of credential compromise

## Root cause
Non-production API endpoints for Global Accelerator service were implemented without CloudTrail logging integration, while still accepting and processing standard AWS IAM credentials and permission checks. These endpoints operate with the same IAM authorization model as production endpoints but lack corresponding audit logging, creating an asymmetric security boundary.

## Attacker mindset
Post-compromise reconnaissance and lateral movement optimization. Adversaries routinely enumerate permissions of compromised credentials to identify high-value targets and attack paths. CloudTrail logging bypasses allow this reconnaissance to occur undetected, giving attackers extended time before detection while reducing operational risk of exposure through security monitoring.

## Defensive takeaways
- Ensure all API endpoints accepting IAM credentials implement consistent CloudTrail logging regardless of production/non-production designation
- Monitor for unusual patterns in successful/failed API calls across compromised credential activity, not relying solely on CloudTrail for permission enumeration detection
- Implement endpoint inventory and classify all accessible AWS service endpoints by logging status and authentication requirements
- Use behavioral detection for credential compromise that identifies permission probing patterns across API calls
- Regularly audit AWS service configurations to identify non-production endpoints that accept standard credentials
- Implement deny policies on non-production endpoints if they serve no legitimate business purpose

## Variant hunting
Search for other AWS service non-production endpoints by: (1) Identifying service endpoints in AWS SDK configurations and documentation, (2) Testing standard service operations against non-standard endpoint URLs with CloudTrail visibility monitoring, (3) Checking for similar patterns across compute, database, analytics, and networking services, (4) Reviewing recently launched services for incomplete logging implementations, (5) Examining services with environmental variants (staging, preview, beta) that may lack logging integration

## MITRE ATT&CK
- T1526 - Gather Victim Identity Rule Information
- T1007 - System Service Discovery
- T1087 - Account Discovery
- T1580 - Cloud Infrastructure Discovery
- T1526.004 - Gather Victim Identity Rule Information: Cloud Infrastructure Discovery
- T1562.008 - Impair Defenses: Disable Cloud Logs

## Notes
This is part of a broader pattern across multiple AWS services. The researcher has identified similar issues in forecast, events, elasticache, datazone, docdb-elastic, devicefarm, cloudwatch, bedrock, bedrock-agent, and ssm services. AWS has explicitly acknowledged this category of vulnerability and encourages reporting. The 4.3 CVSS score reflects the requirement for prior compromise of credentials but acknowledges the complete bypass of audit logging for permission enumeration activity.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](https://sysdig.com/blog/scarleteel-2-0/) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](████████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration). 

**We have found 8 non-production endpoints for the Global Accelerator service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#the-response-from-aws) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws globalaccelerator list-accelerators --region us-west-2
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws globalaccelerator list-accelerators --region us-west-2 --endpoint-url █████████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

globalaccelerator

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration) and spoke about it at Black Hat USA 2023 (██████████) and fwd:cloudsec 2023 (█████████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [forecast](██████████)
* [events](████)
* [elasticache](██████)
* [datazone part 2](█████████)
* [docdb-elastic](█████████)
* [devicefarm](██████████)
* [datazone](█████████)
* [cloudwatch](████████)
* [bedrock](████████)
* [bedrock-agent](████)
* [ssm](██████████)

The following is the list of endpoints we found that exhibited this behavior.

- █████
- █████████
- █████████
- ███
- ███████
- █████████
- ████
- ████████

Please note: We follow an industry standard 90-day vulnerability disclosure policy. You can read more about our policy [here](https://securitylabs.datadoghq.com/vulnerability-disclosure-policy/). 

## Impact

## Summary: 
An adversary can enumerate permissions of compromised credentials for the globalaccelerator service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
