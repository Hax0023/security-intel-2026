# Unauthenticated User Information Disclosure via sam.gov API Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1218461 | https://hackerone.com/reports/1218461
- **Submitted:** 2021-06-06
- **Reporter:** toormund
- **Program:** sam.gov (General Services Administration)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Missing Authentication, Information Disclosure, Sensitive Data Exposure, Broken Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
An unauthenticated API endpoint at sam.gov/api/prod/iam/cws/v1/applications/ exposed sensitive system account information including user emails, personal names, organizational details, IP addresses, and physical locations. The endpoint returned draft application objects containing personally identifiable information and infrastructure details without requiring any authentication or authorization checks.

## Attack scenario
1. Attacker discovers the publicly accessible API endpoint through reconnaissance or documentation review
2. Attacker sends HTTP GET request to the applications endpoint without any authentication credentials
3. API returns complete JSON objects containing system account information with no access restrictions
4. Attacker extracts user emails, names, and organizational details from the response objects
5. Attacker correlates disclosed information to identify government contractors and their infrastructure
6. Attacker uses gathered intelligence for social engineering, targeted phishing, or supply chain reconnaissance

## Root cause
The API endpoint was deployed without implementing authentication/authorization controls, allowing unauthenticated requests to retrieve sensitive application data. The developers failed to enforce identity verification before exposing the /applications/ endpoint, likely due to inadequate security requirements in the API design phase or misconfiguration during deployment.

## Attacker mindset
An attacker would recognize this as low-effort reconnaissance opportunity. The open endpoint provides high-value intelligence about government systems and contractors with minimal operational risk. The attacker could systematically enumerate all applications to build a comprehensive mapping of federal agencies, their technologies, security implementations (Okta usage), and points of contact for further exploitation.

## Defensive takeaways
- Implement mandatory authentication and authorization checks on all API endpoints before returning any data
- Classify and segment sensitive data; prevent exposure of PII, emails, and infrastructure details in API responses
- Apply principle of least privilege: require explicit permissions for accessing application records
- Conduct security-first API design reviews that identify and eliminate unauthenticated data exposure paths
- Implement API rate limiting and monitoring to detect suspicious enumeration attempts
- Regularly audit API endpoints for missing authentication controls through automated and manual testing
- Use API gateways to enforce authentication policies consistently across all endpoints
- Separate draft/incomplete records from production data and restrict access accordingly

## Variant hunting
Search for other sam.gov API endpoints following similar patterns (/api/prod/iam/cws/v1/*) that may lack authentication. Examine other GSA or federal systems using similar API structures. Test related endpoints like /users/, /organizations/, /systems/, /integrations/ for similar unauthenticated exposure. Review whether other sensitive government platforms implement similar unprotected information disclosure patterns.

## MITRE ATT&CK
- T1190
- T1589
- T1598
- T1592
- T1526
- T1046

## Notes
This vulnerability affected a federal government system (sam.gov) managing System for Award Management data. The exposure of contractor email addresses and infrastructure details is particularly dangerous as it enables supply chain targeting and social engineering of government technology providers. The vulnerable endpoint returned draft applications suggesting incomplete data validation and access controls. The presence of direct access without authentication indicates a fundamental architectural flaw rather than a simple misconfiguration.

## Full report
<details><summary>Expand</summary>

## Summary:

It appears that the requests for "system accounts" are fully available via an API endpoint that does not require authentication. 

The main issue is that among the information disclosed are user emails (many with gmail addresses) but the individual applications also include information that the user provides about their organization/integration such as IP addresses, physical locations and whether or not the system uses okta. 

## Steps To Reproduce:

Navigate to the following URL:  https://sam.gov/api/prod/iam/cws/v1/applications/

## Supporting Material/References:

Help desk article about what the [system accounts are](http://www.fsd.gov/gsafsd_sp?id=gsafsd_kb_articles&sys_id=c8d50f1d1b187c909ac5ddb6bc4bcbe2)

Here is an example object of what is returned from the endpoint:

```
{"uid":12345,"systemAccountName":"POC","interfacingSystemVersion":"beta.POCcom","systemDescriptionAndFunction":"example of data thgat is leaked","systemAdmins":"[]","systemManagers":"[{\"commonName\":\"James Bond\",\"uid\":\"fakepassword@gmail.com\",\"mail\":\"fake-fun@opayq.com\",\"name\":\"James Bond\",\"isGov\":false,\"id\":\"fake-fun@opayq.com\"}]","contractOpportunities":"","contractData":"","entityInformation":"","federalHierarchy":"","wageDeterminations":"","assistanceListings":"","referenceData":"","ipAddress":"","typeOfConnection":"","physicalLocation":"","securityOfficialName":"","securityOfficialEmail":"","uploadAto":"","authorizationConfirmation":false,"authorizingOfficialName":"","submittedDate":"2021-06-06T06:49:17.130+0000","submittedBy":"fake-fun@opayq.com","securityApprover":"","rejectedBy":"","rejectionReason":"","applicationStatus":"Draft","isGov":false,"migratedToOkta":false,"fips199Categorization":""}
```

## Impact

A threat actor could view personal information about users on the platform.

It is also theoretically possible that a threat actor could use information gathered from this endpoint to identify future targets and footholds.

</details>

---
*Analysed by Claude on 2026-05-24*
