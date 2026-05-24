# Non-Production API Endpoints for DataZone Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3014785 | https://hackerone.com/reports/3014785
- **Submitted:** 2025-02-26
- **Reporter:** nick_frichette_dd
- **Program:** AWS Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Missing audit logging, Information disclosure, Permission enumeration, API endpoint misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple non-production DataZone API endpoints fail to log API calls to CloudTrail, allowing attackers to enumerate IAM permissions on compromised credentials without detection. An attacker can probe which DataZone operations are permitted by observing error messages while remaining invisible to audit logs.

## Attack scenario
1. Attacker discovers non-production DataZone endpoint URLs through certificate transparency monitoring or similar reconnaissance
2. Attacker compromises AWS credentials with unknown DataZone IAM permissions
3. Attacker uses the non-production endpoint to call DataZone API operations (e.g., ListDomains, DescribeDomains)
4. Error messages reveal whether operations are permitted or denied without triggering CloudTrail logs
5. Attacker maps complete permission profile of compromised identity through systematic API enumeration
6. Attacker uses gathered intelligence to escalate privileges or move laterally, with attack pattern remaining undetected in audit logs

## Root cause
Non-production API endpoints for the DataZone service are not configured to log API calls to CloudTrail, unlike their production counterparts. This allows API requests and responses (including permission denial messages) to be processed without audit trail records, enabling silent reconnaissance.

## Attacker mindset
A sophisticated attacker performing post-exploitation reconnaissance on compromised AWS credentials. By using non-production endpoints, the attacker can enumerate IAM permissions and plan further attacks without triggering security monitoring. The use of certificate transparency monitoring suggests advanced threat actor actively hunting for new or misconfigured infrastructure.

## Defensive takeaways
- Ensure all API endpoints across all environments (production and non-production) are configured to log to CloudTrail without exception
- Implement CloudTrail logging at the organization level and prevent service-level disabling of logs
- Monitor for repeated AccessDeniedException errors from a single principal as potential permission enumeration attempts
- Apply consistent security configurations across all deployment environments; avoid divergence between prod and non-prod security posture
- Regularly audit CloudTrail log coverage to identify blind spots and services not properly instrumented
- Implement rate limiting on API endpoints to detect systematic permission enumeration probing
- Use detective controls to alert on authentication failures from new or suspicious endpoint addresses

## Variant hunting
Search for other AWS services with distinct production vs. non-production endpoints that may have inconsistent CloudTrail logging. Investigate recently created or internal-only API endpoints across all services for logging gaps. Check for any service-specific endpoint configurations that bypass CloudTrail at the regional level.

## MITRE ATT&CK
- T1526 - Gather Victim Identity and Access Infrastructure (certificate transparency discovery)
- T1087 - Account Discovery (permission enumeration)
- T1580 - Cloud Infrastructure Discovery
- T1526 - Cloud Service Discovery

## Notes
This is a continuation of a previously reported vulnerability, indicating AWS had time to patch the original endpoints but failed to apply the same fixes to newly created endpoints discovered through certificate transparency monitoring within 24 hours. The consistency of the vulnerability across three separate endpoints suggests a systematic misconfiguration in how new DataZone endpoints are provisioned rather than an isolated issue.

## Full report
<details><summary>Expand</summary>

This is a continuation of a [previous report](████████) which is now locked. 

Hey friends, I'm terribly sorry to do this to you, but just minutes ago I found 3 more endpoints which exhibit the vulnerable behavior. They just came down through my certificate transparency monitoring so I think they were created in the past 24 hours. It is otherwise identical to that previous report.

- ██████████
- ████
- █████

```
█████████ ~ % export AWS_PROFILE=admin
█████ ~ % aws datazone list-domains --endpoint-url ███

An error occurred (AccessDeniedException) when calling the ListDomains operation: Invalid endpoint or operation type
██████████ ~ % export AWS_PROFILE=noperm
██████████ ~ % aws datazone list-domains --endpoint-url ██████

An error occurred (AccessDeniedException) when calling the ListDomains operation: User: arn:aws:sts::█████████:assumed-role/noperm/noperm is not authorized to perform: datazone:ListDomains on resource: arn:aws:datazone:us-east-1:████:domain/*


██████████ ~ % export AWS_PROFILE=admin
███████ ~ % aws datazone list-domains --endpoint-url ████

An error occurred (AccessDeniedException) when calling the ListDomains operation:
███ ~ % export AWS_PROFILE=noperm
████ ~ % aws datazone list-domains --endpoint-url ███

An error occurred (AccessDeniedException) when calling the ListDomains operation: User: arn:aws:sts::███████:assumed-role/noperm/noperm is not authorized to perform: datazone:ListDomains on resource: arn:aws:datazone:us-east-1:███████:domain/*


██████ ~ % export AWS_PROFILE=admin
█████ ~ % aws datazone list-domains --endpoint-url ████

An error occurred (AccessDeniedException) when calling the ListDomains operation:
█████████ ~ % export AWS_PROFILE=noperm
██████ ~ % aws datazone list-domains --endpoint-url ████

An error occurred (AccessDeniedException) when calling the ListDomains operation: User: arn:aws:sts::█████:assumed-role/noperm/noperm is not authorized to perform: datazone:ListDomains on resource: arn:aws:datazone:us-east-1:████:domain/*
```

## Impact

Summary:
An adversary can enumerate permissions of compromised credentials for the datazone service without logging to CloudTrail.

</details>

---
*Analysed by Claude on 2026-05-24*
