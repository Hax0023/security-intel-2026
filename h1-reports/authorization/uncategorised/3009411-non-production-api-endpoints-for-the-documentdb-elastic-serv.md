# Non-Production API Endpoints for DocumentDB Elastic Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3009411 | https://hackerone.com/reports/3009411
- **Submitted:** 2025-02-24
- **Reporter:** nick_frichette_dd
- **Program:** AWS/Amazon
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Three non-production API endpoints for AWS DocumentDB Elastic service can be called with standard IAM credentials but fail to generate CloudTrail logs, enabling adversaries to enumerate permissions of compromised credentials silently. This bypasses the typical detection mechanism of failed API calls that defenders rely on to identify credential compromise and unauthorized access attempts.

## Attack scenario
1. Attacker obtains compromised AWS IAM credentials through phishing, insider threat, or credential exposure
2. Attacker uses automated tools or manual testing to enumerate permissions by calling various AWS API endpoints
3. Instead of using standard production endpoints which log to CloudTrail, attacker targets non-production DocumentDB Elastic endpoints
4. Each API call to non-production endpoints succeeds or fails based on permissions, revealing the access level of compromised credentials
5. No CloudTrail logs are generated for these non-production endpoint calls, leaving no audit trail of the enumeration activity
6. Attacker gains complete visibility into compromised account permissions without triggering security alerts or logs

## Root cause
AWS DocumentDB Elastic service has isolated non-production API endpoints that accept standard IAM credentials and properly enforce IAM permissions, but are not configured to log API calls to CloudTrail. The service behaves identically to production endpoints in terms of authentication and authorization, but lacks the logging controls.

## Attacker mindset
An attacker who has compromised AWS credentials wants to quickly and silently determine what permissions they have to prioritize further exploitation. They specifically seek API endpoints that accept their stolen credentials but don't generate detectable logs, allowing them to perform reconnaissance without triggering security alerts or creating audit trails that could expose the compromise.

## Defensive takeaways
- Implement CloudTrail logging for all API endpoints including non-production and development endpoints that accept production credentials
- Monitor for successful API calls with unusual patterns even if they appear to be low-risk endpoints
- Implement detective controls that identify permission enumeration patterns (rapid sequential API calls with varying authorization failures)
- Regularly audit which API endpoints are callable with production IAM credentials and ensure all are properly logged
- Use cross-service correlation to detect suspicious activity across production and non-production endpoints
- Apply principle of least privilege to limit which credentials can access non-production endpoints
- Implement AWS Config rules to ensure CloudTrail is enabled for all applicable API endpoints and services

## Variant hunting
Search for other AWS services with isolated non-production endpoints by examining AWS documentation for development, testing, or staging endpoints that accept production IAM credentials. Prior similar findings identified in devicefarm, datazone, cloudwatch, bedrock, bedrock-agent, and ssm services suggest this is a systemic issue across AWS. Look for any service documentation mentioning alternate endpoints or URLs that bypass standard logging mechanisms.

## MITRE ATT&CK
- T1526: Gather Victim Identity and Access Infrastructure
- T1087: Account Discovery
- T1580: Cloud Infrastructure Enumeration
- T1526.004: Cloud Infrastructure Discovery
- T1562.008: Impair Defenses: Disable or Modify Cloud Logs

## Notes
This represents a class of CloudTrail bypass vulnerabilities specific to AWS. The researcher has previously disclosed this vulnerability type publicly through blog posts and conference presentations. AWS Security explicitly stated that non-production endpoints accepting normal credentials without CloudTrail logging should be reported as security issues. The CVSS score of 4.3 reflects low severity because there is no direct access to customer data, but the impact is significant for detection evasion. Multiple other AWS services have similar vulnerabilities, indicating this may be an architectural pattern rather than isolated bugs.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](https://sysdig.com/blog/scarleteel-2-0/) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](█████████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration). 

**We have found 3 non-production endpoints for the DocumentDB Elastic service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#the-response-from-aws) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at aws-security@amazon.com”. 

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws docdb-elastic list-cluster-snapshots
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws docdb-elastic list-cluster-snapshots --endpoint-url ██████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

docdb-elastic

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](https://securitylabs.datadoghq.com/articles/non-production-endpoints-as-an-attack-surface-in-aws/#silent-permission-enumeration) and spoke about it at Black Hat USA 2023 (███) and fwd:cloudsec 2023 (████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [devicefarm](█████████)
* [datazone](██████████)
* [cloudwatch](████)
* [bedrock](████)
* [bedrock-agent](██████)
* [ssm](████████)

The following is a list of endpoints we found that exhibited this behavior.

- ██████
- ██████
- ███

## Impact

## Summary: 
An adversary can enumerate permissions of compromised credentials for the docdb-elastic service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
