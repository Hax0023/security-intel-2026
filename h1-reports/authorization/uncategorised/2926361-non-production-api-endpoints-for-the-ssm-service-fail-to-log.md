# Non-Production API Endpoints for SSM Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 2926361 | https://hackerone.com/reports/2926361
- **Submitted:** 2025-01-07
- **Reporter:** nick_frichette_dd
- **Program:** AWS Bug Bounty
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Information Disclosure, Permission Enumeration
- **CVEs:** None
- **Category:** uncategorised

## Summary
18 non-production API endpoints for the AWS Systems Manager (SSM) service fail to log specific actions (DescribeInstanceInformation and DescribeInstanceProperties) to CloudTrail, allowing attackers with compromised AWS credentials to enumerate permissions silently. While these endpoints lack access to customer partition data, they enable invisible permission discovery that could facilitate lateral movement and privilege escalation.

## Attack scenario
1. Attacker obtains stolen AWS IAM credentials through breach or phishing
2. Attacker discovers non-production SSM endpoints by reverse engineering or public documentation
3. Attacker calls DescribeInstanceProperties against non-production endpoint URL instead of production endpoint
4. API succeeds or fails based on IAM permissions, revealing access level without CloudTrail logging
5. Attacker iteratively tests permissions across multiple actions and services using non-production endpoints
6. Security team remains unaware of enumeration activity due to complete absence of CloudTrail logs

## Root cause
Non-production endpoints for SSM service are accessible with standard IAM credentials but lack proper CloudTrail instrumentation for specific API actions. The logging implementation appears inconsistent between production and non-production endpoints, and potentially between dependent API calls (DescribeInstanceProperties calls ec2:DescribeInstances which logs, but the parent SSM call does not).

## Attacker mindset
Post-exploitation reconnaissance: After gaining initial AWS credentials, attacker seeks to map permissions without triggering detection. Non-production endpoints represent an ideal attack surface as they maintain IAM permission enforcement but eliminate forensic visibility, enabling systematic permission enumeration at scale with minimal risk of detection.

## Defensive takeaways
- Implement consistent CloudTrail logging across all accessible API endpoints, including non-production variants
- Monitor for API calls to non-standard or non-production endpoint URLs using network-based detection
- Implement rate-limiting and alerting on permission denial patterns that may indicate enumeration attempts
- Audit IAM credential exposure response procedures to assume credentials are always tested for access
- Establish endpoint whitelisting policies to restrict API calls to known production endpoints only
- Implement additional logging layers at service mesh or proxy level to capture traffic that bypasses CloudTrail
- Regularly audit and document all service endpoints and their logging configurations

## Variant hunting
Search for similar CloudTrail bypass patterns in other AWS services by testing non-production, staging, or internal endpoints (identified via DNS enumeration or documentation) for: 1) Accessibility with standard credentials, 2) Absence of CloudTrail logging for specific actions, 3) Normal IAM permission behavior. Services with read-only operations (Describe*, Get*, List*) are prime candidates. Test endpoints with patterns like: internal-*, staging-*, us-gov-*, cn-*, regional variants, and alternate FQDNs. Focus on services that may have dependencies on other services' API calls.

## MITRE ATT&CK
- T1526 (Gather Victim AWS Account Information)
- T1087 (Account Discovery)
- T1526.004 (AWS Account Discovery)
- T1578 (Modify Cloud Compute Infrastructure)
- T1562.008 (Disable Cloud Logs)
- T1046 (Network Service Discovery)

## Notes
AWS has formally acknowledged this class of vulnerability as reportable security issues. The reporter has significant expertise in this attack surface, having published research and presented at Black Hat USA 2023 and fwd:cloudsec 2023. Two categories of impact exist: Category 1 affects only DescribeInstanceInformation/DescribeInstanceProperties on 14 endpoints; Category 2 affects broader action sets on additional endpoints. The inconsistency in logging behavior (some dependent API calls log while parent calls do not) suggests this may be a configuration issue rather than intentional design. Similar vulnerability reported in bedrock-agent service.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](███) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](█████████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](█████). 

**We have found 18 non-production endpoints for the ssm service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](█████) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws ssm describe-instance-properties --region us-west-2
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws ssm describe-instance-properties --region us-west-2 --endpoint-url ██████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

ssm

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

5.0 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/CR:H/IR:H/AR:H
(Note: That is the score I received on my previous submission for the same issue [here](█████████))

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](█████) and spoke about it at Black Hat USA 2023 (██████████) and fwd:cloudsec 2023 (██████████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we reported a similar finding for a different service:
- [bedrock-agent](███)

It is important to note that there are two categories at play here. 

**Category 1**: 
These endpoints do not log to CloudTrail **only** for the [ssm:DescribeInstanceInformation](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/describe-instance-information.html) and the [ssm:DescribeInstanceProperties](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/describe-instance-properties.html) actions. Other actions sent to those endpoints **will** log to CloudTrail. It is not clear why this behavior occurs. We hypothesize that it has to do with the fact that `ssm:DescribeInstanceProperties` has a dependency on [ec2:DescribeInstances](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-instances.html) (calls to production endpoints will generate a CloudTrail log for each of these). However, the same is not the case for `ssm:DescribeInstanceInformation`, so it's not clear if something else is going on.

The following is a list of endpoints we found that exhibited this behavior.

- ████
- ████
- ██████████
- ███
- █████
- ██████
- ███████
- ██████
- ██████
- ██████████
- █████████
- █████
- █████████
- ████

**Category 2**:
These endpoints are not nearly as limited as Category 1. While they still can't access the customer partition, they have a wider variety of actions they can perform without logging to CloudTrail. You will find the list below alongside an example action you can test.

- ████ - [ssm:DescribeParameters](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/describe-parameters.html)
- ██████ - [ssm:GetOpsSummary](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/get-ops-summary.html)
- ███ - [ssm:ListCommandInvocations](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/list-command-invocations.html)
- ██████████ - [ssm:GetOpsSummary](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/get-ops-summary.html)

## Impact

An adversary can enumerate permissions of compromised credentials for the ssm service without logging to CloudTrail. We have found 18 non-production endpoints which exhibit this behavior.

</details>

---
*Analysed by Claude on 2026-05-24*
