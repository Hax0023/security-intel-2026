# Non-Production API Endpoints for DataZone Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 2981210 | https://hackerone.com/reports/2981210
- **Submitted:** 2025-02-07
- **Reporter:** nick_frichette_dd
- **Program:** AWS Bug Bounty Program
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insufficient Logging, CloudTrail Bypass, Credential Enumeration, Security Monitoring Evasion
- **CVEs:** None
- **Category:** uncategorised

## Summary
44 non-production API endpoints for the AWS DataZone service fail to log to CloudTrail while remaining callable with standard IAM credentials and enforcing normal IAM permission checks. An adversary with compromised credentials can enumerate permissions silently by observing API responses without generating detectable CloudTrail logs, enabling reconnaissance without triggering security alerts.

## Attack scenario
1. Attacker obtains compromised AWS IAM credentials through credential theft or social engineering
2. Attacker discovers DataZone non-production endpoints (possibly through documentation, error messages, or reconnaissance)
3. Attacker systematically calls non-production endpoints with the compromised credentials to test permissions
4. API responses reveal which permissions are available (success/failure patterns) without generating CloudTrail logs
5. Attacker maps the permission landscape of the compromised identity silently, avoiding detection mechanisms
6. Attacker uses this intelligence to plan privilege escalation or lateral movement attacks with understanding of available permissions

## Root cause
Non-production/test endpoints for the DataZone service are configured to accept standard IAM credentials and enforce IAM permission checks but lack integration with CloudTrail logging mechanisms. These endpoints appear to be employee test environments that were inadvertently exposed to standard credentials without proper isolation or logging controls.

## Attacker mindset
Permission enumeration is a standard reconnaissance activity after credential compromise. An attacker seeks to minimize detection by finding logging gaps in the AWS API infrastructure. Non-production endpoints are attractive targets as they are often overlooked by security teams. Silently enumerating permissions enables informed decision-making about which high-value operations to attempt.

## Defensive takeaways
- Ensure ALL API endpoints that accept IAM credentials, including non-production/test endpoints, log to CloudTrail consistently
- Isolate non-production environments on separate AWS accounts or endpoints that do not accept production IAM credentials
- Implement endpoint discovery detection to identify and alert on calls to unusual or non-standard API endpoints
- Monitor for permission enumeration patterns (multiple failed/successful API calls in sequence) even if individual calls log
- Remove employee names and aliases from endpoint URLs to reduce reconnaissance surface and endpoint discovery
- Establish automated compliance checks to verify CloudTrail logging is enabled for all accessible API endpoints
- Implement detective controls that alert on successful API calls from unexpected endpoints or with unusual patterns

## Variant hunting
Search for similar CloudTrail bypass patterns in other AWS services: Look for non-production, test, or staging endpoints that accept standard credentials but lack logging integration. Check services with multiple deployment environments or employee-specific endpoints. Previous similar findings reported for CloudWatch, Bedrock, Bedrock-Agent, and SSM services suggest this is a systemic issue. Examine any service with documented non-production endpoints that are network-accessible.

## MITRE ATT&CK
- T1526: Gather Victim Identity Information (AWS-specific - permission enumeration)
- T1087: Account Discovery
- T1078: Valid Accounts (using compromised credentials)
- T1526.004: Cloud Services Discovery
- T1555: Credentials from Password Stores (if credentials from vault)

## Notes
This represents a known class of vulnerability that AWS has explicitly acknowledged and requested reporting. The reporter has documented this pattern across multiple services and presented at major security conferences, indicating this is a systemic architectural issue rather than an isolated oversight. The CVSS score of 4.3 reflects the medium severity: requires initial credential compromise but enables silent reconnaissance. The lack of customer data access limits severity, but the silent enumeration capability creates detection blind spots critical for incident response. The presence of 44 endpoints suggests widespread non-production environment exposure.

## Full report
<details><summary>Expand</summary>

**Summary:** Typically, when an adversary gains access to stolen AWS IAM credentials they will [frequently](█████) test those credentials to see what access they have. They do this by performing API calls and seeing which succeed and which fail. There are even automated [tools](█████) to make this process easier. For defenders and security professionals, this behavior serves as a golden opportunity for detection as it likely involves generating a large number of failed API call attempts. If an adversary could enumerate permissions without logging to CloudTrail, they could perform this activity invisibly.

There are many categories of CloudTrail bypass. The specific variant we will be focussed on in this report has been referred to as “non-production endpoint permission enumeration CloudTrail bypass”. If you would like to learn more about it, you can find more details [here](███). 

**We have found 44 non-production endpoints for the Datazone service which can be used with standard IAM credentials, and do not log to CloudTrail.** While it is good that they don’t appear to have access to customer partition data, they can still be used for permission enumeration without logging to CloudTrail. 

AWS has previously [stated](████) that this type of vulnerability should be reported. Specifically, “For isolated non-production endpoints that do not log to CloudTrail but are otherwise callable with normal credentials and exhibit normal IAM permission behavior, AWS considers the CloudTrail logging bypass of such endpoints also to be a security issue. If you find an API or APIs on an endpoint with these characteristics, please contact the AWS Security Team at ███████”. 

As an aside, these endpoints appear to include AWS employee names or aliases in them. Presumably these are for test environments or something similar.

**Description:** 

## Steps To Reproduce:

To see an example of what should appear in CloudTrail when using normal production endpoints, perform the following AWS CLI operation with a sufficiently privileged IAM user or role:

```
aws datazone list-domains
```

Wait approximately 5-10 minutes and a log will appear in CloudTrail. Next, perform the following AWS CLI operation:

```
aws datazone list-domains --endpoint-url ██████
```

After waiting 5-10 minutes (or longer), notice that it does not generate a log in CloudTrail. An adversary can perform this operation and depending on the response of the API make a determination if an Identity they have compromised does, or does not have permission to perform the operation. 

## Supporting Material/References:

* Indicate the Amazon service or product that this vulnerability occurs on:  

datazone

* What type of Amazon AWS account(s) is needed to verify or reproduce this vulnerability?: 

Standard commercial partition account

* Estimated CVSS score and vector string: 

4.3 CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/CR:X/IR:X/AR:X

* Estimated CWEs (comma separated): 

CWE-778: Insufficient Logging

* Have you already publicly disclosed any information on this issue? If so, when and where?: 

This specific example? No. This general technique? Yes, a lot actually. I’ve blogged about it [here](████) and spoke about it at Black Hat USA █████ (██████) and fwd:cloudsec █████ (███████) [I have broken these links because HackerOne appeared to complain about them?] 

Additionally, we have reported similar findings for different services:
* [cloudwatch](█████████)
* [bedrock](█████████)
* [bedrock-agent](████)
* [ssm](███████)

The following is a list of endpoints we found that exhibited this behavior.

- ███████████████
- ███████████████████
- ██████████████
- █████████████
- ████████
- █████████████
- ███████████████
- █████████
- █████████████
- ███████████████
- ███████████████
- █████████
- ███████████████████
- ██████████
- ████████████
- ████████████████
- ████████████
- ████████████████
- ███████████████
- █████████████
- ████████████████
- ████████
- ██████████████
- █████████████
- █████████████
- ████████
- ███████
- ██████████████
- ████████
- ██████████████████
- ██████████████
- █████████
- ██████████████
- ███████████████
- ████████████
- ████████████████████
- ███████
- ██████████████
- █████████████
- ████████████
- ██████████
- ██████████████████
- ████████████
- ██████████

## Impact

## Summary: 
An adversary can enumerate permissions of compromised credentials for the datazone service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
