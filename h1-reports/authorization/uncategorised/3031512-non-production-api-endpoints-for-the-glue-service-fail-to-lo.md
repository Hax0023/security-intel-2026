# Non-Production API Endpoints for AWS Glue Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3031512 | https://hackerone.com/reports/3031512
- **Submitted:** 2025-03-11
- **Reporter:** nick_frichette_dd
- **Program:** AWS Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Permission Enumeration, Logging Evasion
- **CVEs:** None
- **Category:** uncategorised

## Summary
Twelve non-production endpoints for the AWS Glue service can be accessed with standard IAM credentials but fail to generate CloudTrail logs, enabling silent permission enumeration. An adversary with compromised credentials can test what permissions they have without triggering detectable logging, a critical gap in AWS security observability.

## Attack scenario
1. Adversary obtains or compromises AWS IAM credentials for a target environment
2. Instead of using standard production Glue endpoints (which log to CloudTrail), attacker targets non-production endpoints via custom endpoint URLs
3. Attacker calls various Glue API operations (e.g., list-jobs, create-job, etc.) against non-production endpoints to test permission levels
4. Each API call response reveals whether the compromised identity has specific permissions without generating CloudTrail logs
5. Attacker builds a complete permission map of the compromised identity through this silent enumeration
6. Security team has no audit trail to detect this reconnaissance activity, missing critical lateral movement indicators

## Root cause
Non-production endpoints for AWS Glue were implemented with IAM permission enforcement but were excluded from CloudTrail logging instrumentation. These endpoints are accessible with standard credentials yet bypass the centralized logging mechanism, creating an asymmetric security gap.

## Attacker mindset
A sophisticated adversary recognizes that permission enumeration is noisy on production endpoints due to CloudTrail logging. By discovering or targeting non-production endpoints, they eliminate the detection risk entirely while maintaining full functionality to map victim permissions. This enables stealthy post-compromise reconnaissance with zero observability.

## Defensive takeaways
- Enforce CloudTrail logging comprehensively across all API endpoints, including non-production and internal-facing endpoints that accept standard credentials
- Implement monitoring for permission enumeration patterns (multiple failed/denied API calls) across all sources, not just CloudTrail
- Regularly audit AWS service configurations to identify endpoint coverage gaps in logging infrastructure
- Use service control policies (SCPs) to restrict access to non-standard or non-production endpoints
- Monitor for unusual endpoint URL usage in application logs and network telemetry
- Establish principle of least privilege such that compromised credentials have minimal enumeration opportunities
- Implement anomaly detection for credential usage patterns that differ from normal baseline behavior

## Variant hunting
Search for similar patterns across all AWS services: identify endpoints that accept IAM credentials but are not configured to log to CloudTrail. Focus on services with internal/non-production endpoint variants (VPC endpoints, regional variants, deprecated endpoints). Review CloudTrail coverage gaps in lesser-used services like AWS Glue, Forecast, DataZone, Bedrock, and Systems Manager which the researcher identified as vulnerable.

## MITRE ATT&CK
- T1087
- T1526
- T1087.004
- T1033
- T1580

## Notes
Reporter has disclosed similar issues across 13+ AWS services, indicating a systemic pattern rather than isolated bugs. AWS has explicitly acknowledged this vulnerability class as reportable security issues per their policy. The 4.3 CVSS score reflects low confidentiality impact (no customer data exposure) but significant detection evasion capability for post-compromise reconnaissance. This vulnerability demonstrates that logging bypass attacks remain viable even within mature cloud platforms and highlights the importance of comprehensive observability.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](███) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](██████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](██████). 

**We have found 12 non-production endpoints for the AWS Glue service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](███████) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws glue list-jobs
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws glue list-jobs --endpoint-url ██████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

glue

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](███) and spoke about it at Black Hat USA 2023 (████████████YP2XNAbB_Nw) and fwd:cloudsec 2023 (█████████████61C_lEQ5qNM) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [globalaccelerator](████████)
* [forecast](█████████)
* [events](█████████)
* [elasticache](██████████)
* [datazone part 2](████████)
* [docdb-elastic](████)
* [devicefarm](██████)
* [datazone](█████)
* [cloudwatch](█████)
* [bedrock](█████████)
* [bedrock-agent](█████)
* [ssm](███)

The following is the list of endpoints we found that exhibited this behavior.

- ████
- ███████
- ██████████
- █████
- ████
- ██████████
- ██████████
- ████
- ███████
- ███
- ██████████
- ██████

Please note: We follow an industry standard 90-day vulnerability disclosure policy. You can read more about our policy [here](████).

## Impact

## Summary: 
An adversary can enumerate permissions of compromised credentials for the glue service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
