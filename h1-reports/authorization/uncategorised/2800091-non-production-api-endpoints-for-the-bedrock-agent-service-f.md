# Non-Production API Endpoints for bedrock-agent Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 2800091 | https://hackerone.com/reports/2800091
- **Submitted:** 2024-10-23
- **Reporter:** nick_frichette_dd
- **Program:** Amazon Web Services (AWS)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
26 non-production API endpoints for the AWS bedrock-agent service can be called with standard IAM credentials but fail to generate CloudTrail logs, enabling silent permission enumeration. An adversary with compromised AWS credentials can systematically test permissions without triggering detection mechanisms that typically alert on failed API calls.

## Attack scenario
1. Attacker obtains AWS IAM credentials through credential theft or compromise
2. Attacker discovers non-production bedrock-agent endpoints (likely through reconnaissance or public disclosure)
3. Attacker calls non-production endpoints with stolen credentials to enumerate permissions (list-agents, etc.)
4. Attacker analyzes API responses to determine which operations are permitted vs. denied
5. Unlike production endpoints, these non-production calls generate no CloudTrail logs
6. Security team has no visibility into this reconnaissance activity, allowing undetected permission mapping

## Root cause
AWS deployed non-production endpoints for the bedrock-agent service that accept standard IAM credentials and honor IAM permission policies but were not configured to log API calls to CloudTrail. These endpoints appear to be test/development infrastructure that was inadvertently exposed to callers with valid credentials.

## Attacker mindset
Credential enumeration is a standard post-exploitation technique. Attackers systematically probe APIs to understand compromised identity permissions before lateral movement or data exfiltration. CloudTrail bypass allows reconnaissance without triggering security alerts, making this an attractive attack vector for advanced persistent threats.

## Defensive takeaways
- Audit all AWS service endpoints to ensure non-production environments log to CloudTrail when accessible with standard credentials
- Implement behavioral detection for permission enumeration patterns (multiple failed API calls from single principal)
- Segregate non-production infrastructure from production credential paths; do not allow production IAM credentials on dev/test endpoints
- Monitor for API calls to non-standard endpoint URLs that may bypass logging
- Regularly scan AWS infrastructure for exposed non-production endpoints using public cloud reconnaissance techniques
- Establish CloudTrail logging as mandatory for any endpoint that accepts IAM authentication, regardless of intended environment tier

## Variant hunting
Search for similar patterns in other AWS services: Look for non-production endpoints in services like bedrock, sagemaker, lambda, s3, or any service with -dev, -test, -internal, -qa suffixes or employee name references in endpoint URLs. Test whether these endpoints log to CloudTrail. Also investigate whether other AWS services have undocumented endpoints accessible via custom endpoint-url parameters that skip logging.

## MITRE ATT&CK
- T1087.004 - Account Discovery: Domain Account
- T1526 - Enumerate Cloud Resources
- T1087 - Account Discovery
- T1580 - Cloud Infrastructure Discovery
- T1562.008 - Impair Defenses: Disable or Modify Cloud Logs

## Notes
AWS has explicitly stated that CloudTrail bypass on non-production endpoints accessible with normal IAM credentials should be reported as security issues. The researcher previously presented this attack category at Black Hat USA 2023 and fwd:cloudsec 2023. The endpoints contained employee names/aliases suggesting these are internal test infrastructure. The report does not indicate whether customer data is accessible, only that permission enumeration is possible undetected.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](https://sysdig.com/blog/scarleteel-2-0/) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](█████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration). 

**We have found 26 non-production endpoints for the bedrock-agent service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#the-response-from-aws) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

As an aside, these endpoints appear to include AWS employee names or aliases in them. Presumably these are for test environments or something similar.

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws bedrock-agent list-agents --region us-west-2
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws bedrock-agent list-agents --region us-west-2 --endpoint-url ████████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

bedrock-agent  

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration) and spoke about it at Black Hat USA 2023 (██████████) and fwd:cloudsec 2023 (█████████) [I have broken these links because HackerOne appeared to complain about them?] 

The following is a list of endpoints we found that exhibited this behavior.

* ████████
* ████
* █████
* ███████
* ████
* ██████████
* ███████
* ██████████
* ██████████
* ████
* ████
* ████████
* ████████
* █████████
* ██████████
* ████████
* ████████
* ████
* ██████████
* █████████
* ███████
* ████
* ████████
* ███████
* ████
* ██████

## Impact

## Summary: An adversary can enumerate permissions of compromised credentials for the bedrock-agent service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
