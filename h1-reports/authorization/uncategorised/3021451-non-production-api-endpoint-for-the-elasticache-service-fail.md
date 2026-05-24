# Non-Production API Endpoint for ElastiCache Service Fails to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3021451 | https://hackerone.com/reports/3021451
- **Submitted:** 2025-03-03
- **Reporter:** nick_frichette_dd
- **Program:** AWS Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Privilege Escalation/Information Disclosure, Non-Production Endpoint Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
An adversary with compromised AWS IAM credentials can enumerate permissions for the ElastiCache service using a non-production endpoint that fails to log API calls to CloudTrail. This enables silent reconnaissance without triggering detection mechanisms that normally identify permission probing attempts. While the endpoint lacks access to customer data, it allows attackers to determine which IAM permissions are available without audit trail evidence.

## Attack scenario
1. Attacker obtains AWS IAM credentials through phishing, credential exposure, or supply chain compromise
2. Attacker uses automated permission enumeration tools (e.g., Enumerate-IAM) against ElastiCache endpoints
3. Attacker discovers non-production endpoint URL and targets it with elasticache API calls
4. Attacker receives success/failure responses from API calls, revealing permission grants without CloudTrail logging
5. Attacker maps out available permissions and access levels in the compromised identity
6. Defender's detection systems fail to alert on this activity since CloudTrail logging is bypassed

## Root cause
AWS provisioned a non-production ElastiCache endpoint that accepts standard IAM credentials and enforces normal IAM permission checks but was not configured to log to CloudTrail. This creates an asymmetry where the endpoint is functional and callable but invisible to audit systems.

## Attacker mindset
Post-credential compromise reconnaissance. After stealing credentials, attackers immediately test permissions to understand access scope and plan lateral movement. Detection during this phase typically relies on CloudTrail visibility of failed API attempts. Bypassing CloudTrail logging eliminates this detection opportunity, allowing silent enumeration before exploitation.

## Defensive takeaways
- Audit all AWS service endpoints (production and non-production) to ensure CloudTrail logging is enabled
- Implement centralized IAM permission change alerts independent of CloudTrail, detecting unexpected permission grants
- Deploy IAM credential exposure detection to identify compromised credentials early
- Use AWS Config to track service endpoint configurations and audit logging status
- Implement VPC endpoint policies to restrict API calls to known-good endpoints only
- Monitor for unusual permission enumeration patterns even in non-production environments
- Establish inventory of all AWS endpoints including non-production variants

## Variant hunting
Search for other AWS service endpoints (both production and non-production variants) that may not be logging to CloudTrail. Previous similar findings identified: DataZone, DocDB-elastic, DeviceFarm, CloudWatch, Bedrock, Bedrock-Agent, and Systems Manager endpoints with identical characteristics. Systematically review each AWS service for split-endpoint architectures.

## MITRE ATT&CK
- T1526
- T1087
- T1526.001
- T1578

## Notes
AWS explicitly acknowledged this class of vulnerability as reportable per their security guidance. Reporter is a security researcher who has extensively published on CloudTrail bypass techniques at Black Hat USA 2023 and fwd:cloudsec 2023. This represents a systemic issue across multiple AWS services rather than isolated incident. CVSS 4.3 (Low-Medium) reflects information disclosure risk without direct data access. CWE-778 (Insufficient Logging) is primary classification.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](█████) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](███████). 

**We have found 1 non-production endpoint for the ElastiCache service which can be used with standard IAM credentials, and does not log to CloudTrail.** While it is good that it doesn’t appear to have access to customer partition data, it can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](███████) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws elasticache describe-users
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws elasticache describe-users --endpoint-url ███████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

elasticache

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](███████) and spoke about it at Black Hat USA 2023 (████████) and fwd:cloudsec 2023 (██████████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [datazone part 2](███)
* [docdb-elastic](█████)
* [devicefarm](█████████)
* [datazone](█████)
* [cloudwatch](█████)
* [bedrock](█████████)
* [bedrock-agent](████████)
* [ssm](████████)

The following is the endpoint we found that exhibited this behavior.

- ████: 
An adversary can enumerate permissions of compromised credentials for the elasticache service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
