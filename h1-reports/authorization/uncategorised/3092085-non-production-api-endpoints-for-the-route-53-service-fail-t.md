# Non-Production API Endpoints for Route 53 Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3092085 | https://hackerone.com/reports/3092085
- **Submitted:** 2025-04-14
- **Reporter:** nick_frichette_dd
- **Program:** AWS Bug Bounty
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Information Disclosure, Detection Evasion
- **CVEs:** None
- **Category:** uncategorised

## Summary
Two non-production endpoints for the Amazon Route 53 Domains service accept standard IAM credentials but fail to log API calls to CloudTrail, enabling silent permission enumeration. An attacker with compromised AWS credentials can probe which permissions they have without generating detectable CloudTrail logs, creating a blind spot in security monitoring and threat detection.

## Attack scenario
1. Attacker obtains AWS IAM credentials through credential theft, insider access, or leaked credentials
2. Attacker discovers non-production endpoints for route53domains service that accept standard credentials
3. Attacker calls API operations (e.g., list-domains) against the non-production endpoint with a specific endpoint URL parameter
4. API responds with success or permission denial messages, revealing whether the compromised identity has specific permissions
5. Attacker repeats probe attempts across different API operations to build a complete picture of available permissions
6. Defender monitoring CloudTrail sees no evidence of reconnaissance activity since non-production endpoints bypass logging entirely

## Root cause
AWS deployed non-production/staging endpoints for the Route 53 Domains service that are routable with standard IAM credentials but were not configured to emit audit logs to CloudTrail. This creates a logging gap where API activity and permission decisions are invisible to CloudTrail-based security monitoring and alerting.

## Attacker mindset
An attacker who has compromised credentials wants to stealthily determine what actions they can perform without triggering security alerts. CloudTrail is a primary detection mechanism for credential abuse and lateral movement. By finding endpoints that accept valid credentials but don't log, the attacker can perform reconnaissance activity completely invisibly, directly undermining the detective controls that defenders rely on.

## Defensive takeaways
- Audit all AWS service endpoints (production and non-production) to ensure they all emit to CloudTrail when called with valid credentials
- Implement CloudTrail with S3 bucket policies to prevent tampering and ensure all API calls are logged regardless of endpoint used
- Monitor for API calls to unusual or non-standard endpoints that may bypass standard logging mechanisms
- Use AWS Config rules to detect and alert on calls to non-standard service endpoints
- Implement network-level controls to restrict access to non-production endpoints unless explicitly required
- Deploy behavioral analytics to detect permission enumeration patterns even when individual calls log correctly
- Regularly review AWS security advisories and non-production endpoint documentation for similar bypasses

## Variant hunting
Search for other AWS services with non-production endpoints (staging, testing, dev environments) that accept production credentials. Focus on services with multiple regional or endpoint variants. Verify that ALL endpoints, including those with non-standard domain names or URLs, emit CloudTrail logs. Test lesser-used AWS services where endpoint coverage may be incomplete. Check if deprecated service endpoints have similar logging gaps.

## MITRE ATT&CK
- T1526 - Gather Victim Identity and Access Infrastructure
- T1526.004 - Gather Victim Identity and Access Infrastructure: Cloud Instances and Services
- T1087.004 - Account Discovery: Cloud Account
- T1580 - Cloud Infrastructure Discovery
- T1562.008 - Impair Defenses: Disable or Modify Cloud Logs

## Notes
This vulnerability was part of a broader pattern across multiple AWS services (redshift-data, neptune-graph, lakeformation, glue, etc.). The researcher has extensive experience in this domain and published research at Black Hat USA 2023 and fwd:cloudsec 2023. AWS has explicitly stated that non-production endpoint CloudTrail bypass is a security issue. The 4.3 CVSS score reflects that while this enables information disclosure and reconnaissance, it requires already-compromised credentials. The real impact is the detection gap it creates—making credential compromise exploitation significantly harder to detect.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](https://sysdig.com/blog/scarleteel-2-0/) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](https://github.com/andresriancho/enumerate-iam) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration). 

**We have found 2 non-production endpoints for the Amazon Route 53 service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#the-response-from-aws) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws route53domains list-domains
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws route53domains list-domains --endpoint-url ███████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

route53domains

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration) and spoke about it at Black Hat USA 2023 (███) and fwd:cloudsec 2023 (█████████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [redshift-data](████)
* [neptune-graph](█████)
* [lakeformation and m2](███)
* [health](███████)
* [glue](██████████)
* [globalaccelerator](████)
* [forecast](██████████)
* [events](██████)
* [elasticache](██████████)
* [datazone part 2](████████)
* [docdb-elastic](████████)
* [devicefarm](█████)
* [datazone](██████)
* [cloudwatch](██████████bugs?subject=user&report_id=2972435)
* [bedrock](████)
* [bedrock-agent](███)
* [ssm](████)

The following is the list of endpoints we found that exhibited this behavior.:

- ███
- ████████

Please note: We follow an industry standard 90-day vulnerability disclosure policy. You can read more about our policy [here](https://securitylabs.datadoghq.com/vulnerability-disclosure-policy/).

## Impact

## Summary: 
An adversary can enumerate permissions of compromised credentials for the redshift-data service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
