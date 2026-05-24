# Non-Production API Endpoints for AWS Health Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3042588 | https://hackerone.com/reports/3042588
- **Submitted:** 2025-03-17
- **Reporter:** nick_frichette_dd
- **Program:** AWS Security
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Information Disclosure, Detection Evasion
- **CVEs:** None
- **Category:** uncategorised

## Summary
Eleven non-production endpoints for the AWS Health service accept standard IAM credentials and perform normal permission checking but fail to log API calls to CloudTrail. This allows attackers with compromised credentials to enumerate IAM permissions invisibly, a critical advantage in post-exploitation reconnaissance that bypasses standard AWS security monitoring and detection mechanisms.

## Attack scenario
1. Attacker obtains AWS IAM credentials through phishing, data breach, or lateral movement
2. Attacker uses automated tools or manual testing to enumerate permissions on compromised credentials
3. Instead of using production Health service endpoints (which log to CloudTrail), attacker targets non-production endpoints with identical IAM permission checking
4. Attacker performs API calls to Health endpoints and observes responses to determine what actions are permitted
5. Attacker avoids detection as CloudTrail generates no audit logs for these non-production endpoint calls
6. Attacker escalates privileges or moves laterally based on discovered permissions without triggering security alerts

## Root cause
Non-production endpoints for the AWS Health service were not configured to emit logs to CloudTrail while still accepting standard IAM credentials and enforcing normal IAM permission policies. This creates a logging blind spot where legitimate API authentication and authorization still occurs but is not audited.

## Attacker mindset
Post-exploitation reconnaissance and privilege enumeration are critical phases after credential compromise. Attackers actively seek methods to map permissions without triggering alerts. Using non-production endpoints is an elegant technique because it maintains the same IAM behavior as production but eliminates the audit trail, allowing invisible permission discovery and informed lateral movement decisions.

## Defensive takeaways
- Ensure all AWS API endpoints that accept IAM credentials and perform permission checks log to CloudTrail, including non-production, staging, and isolated endpoints
- Implement comprehensive CloudTrail logging at the organization level rather than per-service to prevent endpoint-specific bypass techniques
- Monitor for unusual patterns of permission check failures across services, which may indicate credential compromise and enumeration attempts
- Maintain an inventory of all AWS API endpoints per service and regularly audit their CloudTrail logging status
- Use AWS Config rules to validate that CloudTrail logging is enabled for all service endpoints
- Implement behavioral detection for permission enumeration patterns regardless of logging completeness
- Review and restrict which non-production endpoints are accessible with standard IAM credentials

## Variant hunting
Search for non-production endpoints across all AWS services (especially newer services like Bedrock, DataZone, and forecast). Check for: (1) endpoints with non-standard domain names or paths, (2) services with staging/test/dev endpoints, (3) endpoints that accept IAM credentials but aren't documented in primary service APIs, (4) CloudTrail log gaps in service coverage. The reporter found similar issues in 13+ other AWS services (glue, globalaccelerator, forecast, events, elasticache, datazone, docdb-elastic, devicefarm, cloudwatch, bedrock, bedrock-agent, ssm, and others).

## MITRE ATT&CK
- T1087.004
- T1580
- T1526
- T1619
- T1087

## Notes
This is part of a broader class of CloudTrail bypass vulnerabilities exploiting non-production endpoints. The reporter has published extensive research and presented at major security conferences (Black Hat USA 2023, fwd:cloudsec 2023). AWS explicitly acknowledged this threat category and requested security researchers report similar findings. The CVSS 4.3 (Low-Medium) score underestimates impact because permission enumeration directly enables privilege escalation and lateral movement. The reporter followed AWS's 90-day disclosure policy. 11 specific endpoints affected but names redacted in the original report. This technique is particularly dangerous because it's invisible to standard CloudTrail-based detection systems.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](https://sysdig.com/blog/scarleteel-2-0/) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](██████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration). 

**We have found 11 non-production endpoints for the AWS Health service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#the-response-from-aws) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws health describe-entity-aggregates
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws health describe-entity-aggregates --endpoint-url █████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

health

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration) and spoke about it at Black Hat USA 2023 (██████████) and fwd:cloudsec 2023 (████████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [glue](████)
* [globalaccelerator](████████)
* [forecast](████████)
* [events](██████)
* [elasticache](██████)
* [datazone part 2](█████)
* [docdb-elastic](██████)
* [devicefarm](████████)
* [datazone](████)
* [cloudwatch](████)
* [bedrock](███)
* [bedrock-agent](████████)
* [ssm](███)

The following is the list of endpoints we found that exhibited this behavior.

- ████
- █████████
- ████████
- █████
- ██████
- ███████
- ██████
- ████████
- ███
- █████
- ███████

Please note: We follow an industry standard 90-day vulnerability disclosure policy. You can read more about our policy [here](https://securitylabs.datadoghq.com/vulnerability-disclosure-policy/).

## Impact

## Summary: 
An adversary can enumerate permissions of compromised credentials for the health service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
