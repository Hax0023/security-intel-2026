# Non-Production API Endpoints for CloudWatch Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 2972435 | https://hackerone.com/reports/2972435
- **Submitted:** 2025-02-03
- **Reporter:** nick_frichette_dd
- **Program:** AWS Bug Bounty
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Information Disclosure, Detection Evasion
- **CVEs:** None
- **Category:** uncategorised

## Summary
Two non-production CloudWatch API endpoints fail to log to CloudTrail while remaining accessible with standard IAM credentials, allowing attackers to silently enumerate permissions without generating audit logs. An adversary can determine what access compromised credentials have by observing API response codes without triggering CloudTrail detection.

## Attack scenario
1. Attacker obtains compromised AWS IAM credentials through phishing or credential theft
2. Instead of using production endpoints (which log to CloudTrail), attacker discovers non-production endpoint URLs containing employee names/aliases
3. Attacker calls CloudWatch API operations (e.g., describe-alarms) against non-production endpoints with --endpoint-url parameter
4. API responses indicate permission success/failure based on IAM policy evaluation, revealing which permissions the compromised identity has
5. No CloudTrail logs are generated for these API calls, avoiding detection by security monitoring tools
6. Attacker builds complete permission map of compromised credentials invisibly and escalates privileges or accesses sensitive resources

## Root cause
AWS deployed isolated non-production endpoints for CloudWatch service that accept standard IAM credentials and enforce IAM permission checks but lack CloudTrail logging integration. These endpoints appear to be internal test/development infrastructure that were inadvertently made callable from production accounts.

## Attacker mindset
Permission enumeration is a critical reconnaissance step after credential compromise. An attacker seeks to discover what they can access without alerting defenders. CloudTrail is the primary detection mechanism for this activity, so bypassing it enables silent post-exploitation reconnaissance. The presence of employee names in endpoints suggests these are internal testing resources not intended for customer access.

## Defensive takeaways
- Monitor for API calls to non-standard or internal-looking endpoint URLs in VPC flow logs and DNS query logs
- Implement network policies restricting access to non-production AWS endpoints from production accounts
- Use IAM permission boundaries to restrict endpoint-url parameter usage in CLI/SDK calls
- Establish baseline of expected CloudWatch endpoint usage and alert on anomalies
- Implement credential rotation policies and assume-role patterns to limit damage from compromised long-lived credentials
- Monitor CloudTrail logs for patterns of permission testing (high volume of failed API calls from single identity)
- Request AWS disable or properly instrument non-production endpoints, or restrict their accessibility to internal networks only

## Variant hunting
Search for similar non-production endpoints across other AWS services (bedrock, bedrock-agent, ssm already found). Look for: endpoints with employee names/aliases, endpoints that accept credentials but don't log to CloudTrail, internal-looking URLs that are publicly routable, API responses that leak permission information through status codes or error messages.

## MITRE ATT&CK
- T1087.004 (Account Discovery: Cloud Account)
- T1526 (Cloud Service Discovery)
- T1087.008 (Permission Groups Discovery: Cloud Account)
- T1562.008 (Impair Defenses: Disable CloudTrail Logging)
- T1078.001 (Valid Accounts: Default Accounts)

## Notes
This is part of a broader class of CloudTrail bypass vulnerabilities the reporter has documented extensively (Black Hat USA 2023, fwd:cloudsec 2023). AWS explicitly acknowledges this category as a security issue requiring disclosure. The CVSS 4.3 is relatively low because there's no access to actual customer data, but the impact is significant for post-compromise reconnaissance. Multiple AWS services affected indicates systematic issue with non-production endpoint instrumentation.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](██████) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](█████████). 

**We have found 2 non-production endpoints for the cloudwatch service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](██████) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

As an aside, these endpoints appear to include AWS employee names or aliases in them. Presumably these are for test environments or something similar.

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws cloudwatch describe-alarms
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws cloudwatch describe-alarms --endpoint-url █████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

cloudwatch

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](█████) and spoke about it at Black Hat USA 2023 (██████) and fwd:cloudsec 2023 (███████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [bedrock](██████)
* [bedrock-agent](███)
* [ssm](███)

The following is a list of endpoints we found that exhibited this behavior.

- ██████████
- █████

## Impact

## Summary: An adversary can enumerate permissions of compromised credentials for the bedrock-agent service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
