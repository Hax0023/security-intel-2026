# Non-Production API Endpoints for AI Ops Service Fails to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3418966 | https://hackerone.com/reports/3418966
- **Submitted:** 2025-11-10
- **Reporter:** nick_frichette_dd
- **Program:** Amazon Web Services (AWS) Bug Bounty
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Permission Enumeration, Detection Evasion
- **CVEs:** None
- **Category:** uncategorised

## Summary
Five non-production endpoints for the AWS AI Ops service accept standard IAM credentials but fail to log API calls to CloudTrail, enabling attackers to enumerate permissions without detection. This represents a CloudTrail logging bypass vulnerability that allows adversaries with compromised credentials to test access levels invisibly, contrary to normal production endpoint behavior which generates audit logs.

## Attack scenario
1. Attacker obtains AWS IAM credentials through credential theft or phishing
2. Attacker uses automated tools to enumerate IAM permissions via standard production endpoints, generating detectable CloudTrail logs
3. Attacker discovers non-production endpoints for AI Ops service that accept same credentials
4. Attacker performs permission enumeration queries against non-production endpoints, observing success/failure responses
5. API calls to non-production endpoints return authorization results but generate no CloudTrail logs
6. Attacker maps compromised identity's permissions silently and without triggering security alerts or detection

## Root cause
Non-production API endpoints for the AI Ops service are configured to accept standard IAM credentials and enforce normal IAM permission checks, but the infrastructure fails to send audit logs to CloudTrail. This creates an asymmetry where endpoint behavior matches production (permission enforcement) but logging does not (no audit trail).

## Attacker mindset
Once credentials are compromised, the attacker's primary goal is reconnaissance without detection. The ability to enumerate permissions silently enables them to identify which services and operations are available before conducting actual exploitation, all while avoiding security monitoring and alerts that would trigger on production endpoint probing.

## Defensive takeaways
- Ensure all API endpoints, including non-production and development endpoints, are configured to log to CloudTrail consistently
- Implement endpoint discovery and inventory controls to prevent undocumented or non-production endpoints from accepting production credentials
- Monitor for successful API calls from unexpected or non-production endpoints as a detection signal
- Enforce mandatory CloudTrail logging at the infrastructure level rather than relying on per-endpoint configuration
- Regularly audit AWS service configurations for missing CloudTrail integrations across all endpoint variants
- Use service control policies (SCPs) to restrict API calls to known production endpoints only

## Variant hunting
The researcher has identified this pattern across 20+ AWS services including Neptune Graph, Transcribe, Storage Gateway, SSO Admin, SSM Quick Setup, Security Hub, Route53, Redshift Data, Lake Formation, Health, Glue, Global Accelerator, Forecast, Events, ElastiCache, DataZone, DocumentDB Elastic, Device Farm, CloudWatch, Bedrock, and Bedrock Agent. This suggests a systemic issue across AWS where non-production endpoints lack CloudTrail logging, indicating a platform-wide architectural problem rather than isolated service misconfigurations.

## MITRE ATT&CK
- T1526 - Gather Victim Identity and Access Information
- T1087 - Account Discovery
- T1526.004 - Cloud Accounts
- T1580 - Cloud Infrastructure Discovery
- T1562.008 - Impair Defenses: Disable or Modify Cloud Logs

## Notes
AWS explicitly acknowledged this class of vulnerability as a security issue and requested reporting of any isolated non-production endpoints that accept normal credentials, enforce IAM permissions, but do not log to CloudTrail. The researcher's extensive history of discovering variants across multiple services suggests this may represent a systematic design flaw in how AWS manages non-production infrastructure and logging configurations. CVSS score 4.3 reflects low confidentiality impact (no customer data exposure) but integrity impact through undetected enumeration.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](██████) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](██████████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](█████). 

**We have found 5 non-production endpoints for the AI Ops service which could be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don't appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](███-surface-in-aws/#the-response-from-aws) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws aiops list-investigation-groups
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws aiops list-investigation-groups --endpoint-url ██████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

aiops

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/CR:H/IR:H/AR:H

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](███████) and spoke about it at Black Hat USA 2023 (███████) and fwd:cloudsec 2023 (█████████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [neptune-graph](https://hackerone.com/bugs?subject=user&report_id=3203781)
* [transcribe](https://hackerone.com/bugs?subject=user&report_id=3184866)
* [storagegateway](https://hackerone.com/bugs?subject=user&report_id=3184044)
* [sso-admin](https://hackerone.com/bugs?subject=user&report_id=3174521)
* [ssm-quicksetup](https://hackerone.com/reports/3164098)
* [securityhub](https://hackerone.com/reports/3127982)
* [route53](https://hackerone.com/bugs?subject=user&report_id=3092085)
* [redshift-data](https://hackerone.com/bugs?subject=user&report_id=3081305)
* [neptune-graph](https://hackerone.com/bugs?subject=user&report_id=3068422)
* [lakeformation and m2](https://hackerone.com/bugs?subject=user&report_id=3055683)
* [health](https://hackerone.com/bugs?subject=user&report_id=3042588)
* [glue](https://hackerone.com/bugs?subject=user&report_id=3031512)
* [globalaccelerator](https://hackerone.com/bugs?subject=user&report_id=3029552)
* [forecast](https://hackerone.com/reports/3022516)
* [events](https://hackerone.com/bugs?subject=user&report_id=3021618)
* [elasticache](https://hackerone.com/bugs?subject=user&report_id=3021451)
* [datazone part 2](https://hackerone.com/bugs?subject=user&report_id=3014785)
* [docdb-elastic](https://hackerone.com/bugs?subject=user&report_id=3009411)
* [devicefarm](https://hackerone.com/bugs?subject=user&report_id=2999116)
* [datazone](https://hackerone.com/bugs?subject=user&report_id=2981210)
* [cloudwatch](https://hackerone.com/bugs?subject=user&report_id=2972435)
* [bedrock](https://hackerone.com/bugs?subject=user&report_id=2951803)
* [bedrock-agent](https://hackerone.com/bugs?subject=user&report_id=2800091)
* [ssm](https://hackerone.com/bugs?subject=user&report_id=2926361)

The following is a list of endpoints we found that exhibited this behavior:

- █████████
- ██████
- ████████
- █████
- █████████

These appear to be personal stacks for a few developers. It would be good practice to allowlist specific AWS accounts which are permitted to call them as this would close off this attack. 

Please note: We follow an industry standard 90-day vulnerability disclosure policy. You can read more about our policy [here](██████████).

## Impact

## Summary: 
An adversary can enumerate permissions of compromised credentials for the aiops service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
