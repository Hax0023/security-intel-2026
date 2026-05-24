# Non-Production API Endpoint for EventBridge Service Fails to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3021618 | https://hackerone.com/reports/3021618
- **Submitted:** 2025-03-03
- **Reporter:** nick_frichette_dd
- **Program:** AWS Security
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Information Disclosure, Lack of Audit Trail
- **CVEs:** None
- **Category:** uncategorised

## Summary
A non-production API endpoint for AWS EventBridge service accepts standard IAM credentials but fails to generate CloudTrail logs, enabling attackers to silently enumerate permissions of compromised credentials. This allows adversaries to test API access without triggering detection mechanisms that normally alert on repeated failed authentication attempts.

## Attack scenario
1. Attacker obtains compromised AWS IAM credentials through credential theft or social engineering
2. Attacker uses automated permission enumeration tools against non-production EventBridge endpoints instead of production endpoints
3. Each API call to the non-production endpoint succeeds or fails based on IAM permissions but generates no CloudTrail audit logs
4. Attacker systematically tests permissions across EventBridge operations (e.g., list-event-buses, put-events) to map credential capabilities
5. Security team monitoring CloudTrail for suspicious activity sees no indication of permission probing activity
6. Attacker gains comprehensive understanding of compromised account's permissions undetected and proceeds with lateral movement or data exfiltration

## Root cause
AWS EventBridge service maintains a non-production API endpoint that accepts valid IAM credentials and enforces IAM permission policies but lacks integration with CloudTrail logging mechanisms. The endpoint operates in isolation from standard logging infrastructure despite maintaining production-grade access controls.

## Attacker mindset
Sophisticated adversary seeking to enumerate compromised credential permissions while evading detection. Recognizes that standard production API calls generate CloudTrail logs that trigger alerts on repeated failures. Leverages non-production endpoints as a blind spot in security monitoring to methodically test permissions without leaving audit trails, enabling quiet reconnaissance before exploitation.

## Defensive takeaways
- Implement CloudTrail logging for all API endpoints regardless of production status if they accept standard IAM credentials
- Monitor for API calls to non-standard or non-production endpoints in addition to standard endpoints
- Implement permission-based monitoring that alerts on patterns consistent with credential enumeration across any accessible endpoint
- Maintain inventory of all API endpoints (production and non-production) and verify CloudTrail logging coverage for each
- Implement endpoint discovery and enumeration prevention controls to limit attacker ability to discover non-logged endpoints
- Use service control policies (SCPs) to restrict access to non-production endpoints if they serve no business purpose

## Variant hunting
Search for other AWS services with non-production endpoints that accept IAM credentials but lack CloudTrail integration. Previous similar findings identified across ElastiCache, DataZone, DocumentDB Elastic, Device Farm, CloudWatch, Bedrock, Bedrock Agents, and SSM services. Examine any service with separate staging, testing, or development API endpoints.

## MITRE ATT&CK
- T1087
- T1526
- T1087.004
- T1136

## Notes
Reporter is security researcher from Datadog who has extensively documented this vulnerability class publicly through conference presentations (Black Hat USA 2023, fwd:cloudsec 2023) and blog articles. AWS explicitly stated this type of finding warrants security team notification. This represents systemic issue across multiple AWS services rather than isolated incident. CVSS 4.3 indicates low impact but concerning from detection evasion perspective.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](https://sysdig.com/blog/scarleteel-2-0/) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](████████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration). 

**We have found 1 non-production endpoint for the EventBridge service which can be used with standard IAM credentials, and does not log to CloudTrail.** While it is good that it doesn’t appear to have access to customer partition data, it can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#the-response-from-aws) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws events list-event-buses
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws events list-event-buses --endpoint-url █████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

events

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration) and spoke about it at Black Hat USA 2023 (█████) and fwd:cloudsec 2023 (█████████?v█████████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [elasticache](███)
* [datazone part 2](███)
* [docdb-elastic](████████)
* [devicefarm](██████)
* [datazone](███████)
* [cloudwatch](██████████)
* [bedrock](██████████)
* [bedrock-agent](███████)
* [ssm](██████)

The following is the endpoint we found that exhibited this behavior.

- ██████████

## Impact

## Summary: 
An adversary can enumerate permissions of compromised credentials for the elasticache service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
