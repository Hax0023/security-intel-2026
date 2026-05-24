# (Part 2) Non-Production API Endpoints for the Datazone Service Fail to Log to CloudTrail Resulting in Silent Permission Enumeration

## Metadata
- **Source:** HackerOne
- **Report:** 3014785 | https://hackerone.com/reports/3014785
- **Submitted:** 2025-02-26
- **Reporter:** nick_frichette_dd
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insufficient Logging
- **CVEs:** None
- **Category:** uncategorised

## Summary
This is a continuation of a [previous report](████████) which is now locked. 

Hey friends, I'm terribly sorry to do this to you, but just minutes ago I found 3 more endpoints which exhibit the vulnerable behavior. They just came down through my certificate transparency monitoring so I think they were created in the past 24 hours. It is otherwise identical to that previous report.

- ██████████
- 

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

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
