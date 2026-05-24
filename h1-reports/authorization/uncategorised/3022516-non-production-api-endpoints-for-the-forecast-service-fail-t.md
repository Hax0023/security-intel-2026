# Non-Production API Endpoints for Forecast Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3022516 | https://hackerone.com/reports/3022516
- **Submitted:** 2025-03-04
- **Reporter:** nick_frichette_dd
- **Program:** AWS
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Permission Enumeration, Detection Evasion
- **CVEs:** None
- **Category:** uncategorised

## Summary
Four non-production endpoints for the AWS Forecast service can be accessed with standard IAM credentials but do not log API calls to CloudTrail, enabling adversaries to enumerate permissions silently. While these endpoints don't provide access to customer data, they allow attackers to test compromised credentials and determine what permissions exist without generating detectable audit logs that would trigger security alerts.

## Attack scenario
1. Attacker obtains AWS IAM credentials through phishing, credential stuffing, or infrastructure compromise
2. Attacker uses automated tools or manual testing to enumerate available permissions on compromised credentials
3. Attacker targets non-production Forecast service endpoints via custom endpoint-url parameter in AWS CLI
4. Attacker observes API responses (success/failure/permission denied) to determine accessible operations
5. Enumeration activity completes without generating CloudTrail logs, avoiding detection by security monitoring systems
6. Attacker uses gathered permission information to plan targeted exploitation or lateral movement within the AWS environment

## Root cause
AWS Forecast service maintains isolated non-production endpoints that accept standard IAM credentials and enforce IAM permission checks, but are not configured to log API activity to CloudTrail. This creates an intentional or oversight configuration gap where normal API behavior (authentication, authorization, execution) occurs without audit logging.

## Attacker mindset
Credential enumeration and reconnaissance without detection is a critical early-stage attack activity. By finding logging-blind endpoints, attackers can map out compromised account capabilities risk-free, enabling more targeted and efficient exploitation. This is particularly valuable for persistence and privilege escalation planning.

## Defensive takeaways
- Ensure all AWS service endpoints that accept credentials and enforce IAM permissions also log to CloudTrail without exception
- Implement CloudTrail monitoring rules to detect permission enumeration patterns (high volumes of failed API calls to related operations)
- Regularly audit AWS service configurations to identify non-production or staging endpoints that may bypass logging
- Use preventive policies to restrict or monitor access to non-production endpoints if they must exist
- Monitor for unusual --endpoint-url parameters in CloudTrail logs for AWS CLI activity
- Implement detection rules for suspicious IAM activity even if direct CloudTrail logs are absent (via VPC Flow Logs, DNS logs, network monitoring)

## Variant hunting
Search for other AWS services with non-production, staging, or sandbox endpoints that accept IAM credentials. This includes: development endpoints, preview service endpoints, regional testing endpoints, and beta service versions. Previously vulnerable services: EventBridge, ElastiCache, DataZone, DocDB-Elastic, Device Farm, CloudWatch, Bedrock, Systems Manager. Check newly launched services and regional rollouts.

## MITRE ATT&CK
- T1087
- T1526
- T1580
- T1562.008

## Notes
Reporter has extensive prior work on CloudTrail bypass variants across multiple AWS services and presented research at Black Hat USA 2023 and fwd:cloudsec 2023. AWS has explicitly acknowledged this class of vulnerability as reportable. The 4.3 CVSS score reflects low impact (no customer data exposure) but notable information disclosure risk (permission inference). This demonstrates systematic configuration issues across AWS services where non-production endpoints are not integrated into logging infrastructure.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](█████████) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](███████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](████████). 

**We have found 4 non-production endpoints for the Forecast service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](█████████) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws forecast list-datasets --region us-west-2
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws forecast list-datasets --region us-west-2 --endpoint-url ███████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

forecast

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](████████) and spoke about it at Black Hat USA 2023 (████████) and fwd:cloudsec 2023 (████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [events](███████)
* [elasticache](███)
* [datazone part 2](██████████)
* [docdb-elastic](██████████)
* [devicefarm](███████)
* [datazone](██████)
* [cloudwatch](████)
* [bedrock](████)
* [bedrock-agent](███████)
* [ssm](█████████)

The following is the list of endpoints we found that exhibited this behavior.

- ██████████
- ██████████
- ██████████
- ███████

## Impact

## Summary: 
An adversary can enumerate permissions of compromised credentials for the forcast service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
