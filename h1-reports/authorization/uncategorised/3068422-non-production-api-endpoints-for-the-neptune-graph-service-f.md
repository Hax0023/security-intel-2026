# Non-Production API Endpoints for Neptune Graph Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3068422 | https://hackerone.com/reports/3068422
- **Submitted:** 2025-03-31
- **Reporter:** nick_frichette_dd
- **Program:** AWS Security (HackerOne Report #3068422)
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Information Disclosure, Credential Enumeration
- **CVEs:** None
- **Category:** uncategorised

## Summary
Seven non-production API endpoints for Amazon Neptune Graph service accept standard IAM credentials but fail to log API calls to CloudTrail. This allows attackers with compromised AWS credentials to enumerate permissions silently without generating detectable logs. While these endpoints lack access to customer data, they enable adversaries to map capabilities of stolen credentials undetected.

## Attack scenario
1. Attacker obtains AWS IAM credentials through phishing, supply chain compromise, or exposed secrets
2. Attacker discovers non-production Neptune Graph endpoints (either through documentation, scanning, or prior knowledge)
3. Attacker uses AWS CLI with custom endpoint URLs to probe Neptune Graph API permissions
4. Attacker observes API response codes (success vs. permission denied) to map compromised identity's capabilities
5. Attacker avoids CloudTrail detection since non-production endpoints do not log to CloudTrail
6. Attacker escalates to target higher-value services or data based on successfully enumerated permissions

## Root cause
Non-production/development endpoints for Neptune Graph service are configured to accept IAM authentication and authorization checks but lack CloudTrail logging instrumentation. AWS infrastructure fails to enforce unified logging requirements across all API endpoints, even development-isolated ones.

## Attacker mindset
Credential enumeration without logging is high-value for attackers after initial compromise. Being able to map permissions silently before lateral movement or privilege escalation attempts significantly reduces detection risk. This enables more targeted, stealthy post-exploitation reconnaissance.

## Defensive takeaways
- Implement CloudTrail logging universally across all API endpoints regardless of production status
- Monitor for API calls to non-production or development-aliased endpoints with standard credentials
- Implement real-time alerting on any API calls to unusual or development endpoints
- Regularly audit CloudTrail exclusions and endpoint logging configurations
- Use VPC endpoint policies to restrict access to development endpoints
- Implement canary credentials to detect unauthorized API enumeration attempts
- Apply least-privilege IAM policies limiting access to production endpoints only

## Variant hunting
Search for other AWS services with isolated non-production endpoints (dev stacks, staging environments, personal developer aliases) that accept standard IAM credentials but fail to log. The report identifies similar issues across 16+ services including Glue, Lake Formation, EventBridge, ElastiCache, Bedrock, CloudWatch, and others. Systematically audit all AWS services for endpoint-logging gaps.

## MITRE ATT&CK
- T1190
- T1526
- T1087
- T1078.001
- T1580

## Notes
This represents a systematic architectural issue affecting 20+ AWS services. The reporter has disclosed variants across multiple services per AWS guidance that stated such CloudTrail bypass vulnerabilities should be reported. The report follows 90-day disclosure policy. Non-production endpoints were developer personal stacks with aliases, creating a large attack surface of hidden endpoints.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](https://sysdig.com/blog/scarleteel-2-0/) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](███████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration). 

**We have found 7 non-production endpoints for the Amazon Neptune Graph service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#the-response-from-aws) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws neptune-graph list-graphs
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws neptune-graph list-graphs --endpoint-url ███████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

neptune-graph

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration) and spoke about it at Black Hat USA 2023 (█████) and fwd:cloudsec 2023 (████████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [lakeformation and m2](█████)
* [health](████)
* [glue](██████████)
* [globalaccelerator](█████)
* [forecast](█████)
* [events](████)
* [elasticache](████████)
* [datazone part 2](██████)
* [docdb-elastic](███████)
* [devicefarm](██████████)
* [datazone](███)
* [cloudwatch](███)
* [bedrock](██████████)
* [bedrock-agent](██████████one.com/bugs?subject=user&report_id=2800091)
* [ssm](███)

The following is the list of endpoints we found that exhibited this behavior. Note that these appear to be AWS developer personal stacks with their aliases in the domains. These should be redacted prior to disclosure

- ██████████
- ██████████
- █████
- ███████
- ██████
- █████

In addition to the above 6, we found another non-production endpoint which can only perform the `neptune-graph:ListGraphSnapshots` action. Presumably this endpoint is only configured for that specific API call.

- ███

Please note: We follow an industry standard 90-day vulnerability disclosure policy. You can read more about our policy [here](https://securitylabs.datadoghq.com/vulnerability-disclosure-policy/).

## Impact

## Summary: 
An adversary can enumerate permissions of compromised credentials for the lakeformation and m2 service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
