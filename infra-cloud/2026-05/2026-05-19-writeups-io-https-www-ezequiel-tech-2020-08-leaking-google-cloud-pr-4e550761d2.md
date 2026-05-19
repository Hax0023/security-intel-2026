# Leaking Google Cloud Projects via IAM Service Accounts List API - pageToken Forgery

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Google Cloud Platform
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Broken Access Control, Authentication Bypass, Information Disclosure, Improper Input Validation
- **Category:** infra-cloud
- **Writeup:** https://www.ezequiel.tech/2020/08/leaking-google-cloud-projects.html

## Summary
An attacker could forge pageToken parameters in the IAM API's projects.serviceAccounts.list method to enumerate service accounts and leak GCP project IDs from any project given only the project number. This information disclosure could facilitate further reconnaissance attacks against GCP resources including App Engine apps and Container Registry repositories.

## Attack scenario (step by step)
1. Attacker obtains or guesses a target GCP project number (which can be derived from project IDs or discovered through various means)
2. Attacker crafts requests to the projects.serviceAccounts.list API endpoint with a forged pageToken parameter
3. The improperly validated pageToken allows the API to return service accounts from the target project without proper authorization checks
4. Attacker enumerates all service accounts in the target project, extracting email addresses and metadata
5. Attacker uses discovered project IDs and service account information to identify other GCP resources (Container Registry, App Engine, Cloud Storage)
6. Attacker performs further reconnaissance or targeted attacks against these discovered resources

## Root cause
Insufficient validation and authorization checks on the pageToken parameter in the projects.serviceAccounts.list API method. The API failed to properly verify that the requester had authorization to access the specified project before returning paginated results. The pageToken was either predictable, or the API did not properly bind pagination state to the original authorized request context.

## Attacker mindset
Opportunistic security researcher testing GCP APIs for common authorization flaws. Recognized that pagination mechanisms are often overlooked in security reviews and that pageToken parameters frequently lack proper validation. Understood that GCP project IDs are sensitive information that enable further reconnaissance.

## Defensive takeaways
- Always validate and authorize pageToken parameters - never trust client-supplied pagination tokens without verification
- Bind pagination state cryptographically to the original request context (user identity, project, timestamp)
- Implement server-side session state management for pagination rather than relying on client-provided tokens
- Apply the same authorization checks to paginated API responses as to the initial request
- Treat project IDs and project numbers as sensitive information requiring proper access control
- Conduct security reviews specifically targeting pagination logic in list/enumerate operations
- Implement rate limiting on enumeration APIs to prevent bulk reconnaissance
- Log and alert on suspicious pagination patterns or high-volume list requests

## Variant hunting
['Test other GCP APIs with list/pagination functionality (Compute, Storage, Kubernetes) for similar pageToken validation flaws', 'Attempt to forge pageTokens for other resource enumeration endpoints across Google Cloud services', 'Test whether pageTokens from one project can be reused across different projects or resource types', 'Examine other cloud providers (AWS, Azure) for similar pagination bypass vulnerabilities', 'Investigate whether pageToken format is predictable or contains encodable metadata', 'Test cursor-based pagination in other Google APIs for authorization bypass patterns']

## MITRE ATT&CK
- T1526 - Reconnaissance: Cloud Service Discovery
- T1087 - Account Discovery
- T1526 - Cloud Service Enumeration
- T1550 - Use Alternate Authentication Material
- T1078 - Valid Accounts

## Notes
This is a sophisticated authorization bypass targeting a core GCP service. The vulnerability leveraged pagination functionality, which is often a blind spot in security reviews. The writeup demonstrates good security research methodology by systematically testing API parameters. Project IDs/numbers are critical to GCP reconnaissance, making this a high-impact information disclosure. The researcher appropriately disclosed responsibly to Google.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
