# Auth Bypass: Leaking Google Cloud Service Accounts and Projects via Forged pageToken

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Google Cloud Platform (GCP)
- **Bounty:** Unknown
- **Severity:** high
- **Vuln types:** Authorization Bypass, Information Disclosure, Broken Access Control, Pagination Token Forgery
- **Category:** infra-cloud
- **Writeup:** https://www.ezequiel.tech/2020/08/leaking-google-cloud-projects.html

## Summary
The IAM API's projects.serviceAccounts.list method was vulnerable to pagination token forgery, allowing attackers to list service accounts from any GCP project given only its project number. This vulnerability could leak GCP project IDs and service account details, which are considered PII and could be leveraged to discover and scan for unsecured cloud resources.

## Attack scenario (step by step)
1. Attacker obtains or enumerates a target GCP project number through various reconnaissance methods
2. Attacker makes a normal request to projects.serviceAccounts.list with a small pageSize parameter to obtain a legitimate nextPageToken
3. Attacker analyzes the pageToken structure and crafts a forged token by manipulating its contents
4. Attacker submits the forged pageToken with the target project number to bypass authorization checks and retrieve service account listings from arbitrary projects
5. Attacker extracts service account emails, project IDs, and metadata from the unauthorized response
6. Attacker uses leaked project IDs to enumerate and scan for additional unsecured resources like App Engine instances, Container Registry repositories, and Cloud Storage buckets

## Root cause
The pageToken validation logic in the IAM API did not properly verify that the token corresponded to the requested project, allowing tokens to be reused or forged across different projects. The API relied on the token's internal structure without cryptographic validation or binding to the specific project context.

## Attacker mindset
The researcher approached a sensitive API (IAM) with the assumption that pagination logic might be overlooked compared to core authorization mechanisms. By testing parameter manipulation on a list operation, they discovered that pagination tokens were not cryptographically bound to specific projects, treating them as predictable or reusable credentials.

## Defensive takeaways
- Implement cryptographic binding of pagination tokens to specific resource contexts (project IDs) and user sessions
- Use signed/HMAC-protected tokens that include the project context and cannot be forged without the server's secret key
- Validate pagination tokens on every request to ensure they correspond to the requested project and the authenticated user has access
- Apply the same authorization checks to paginated responses as to initial list requests
- Treat project IDs as sensitive information requiring protection, not as public identifiers in error messages or responses
- Implement rate limiting and anomaly detection for repeated access attempts across different projects
- Conduct comprehensive security reviews of pagination implementations across all list/enumerate operations in APIs

## Variant hunting
['Test pagination tokens from one resource type against different resource types in the same project', 'Attempt to forge pageTokens for other Google Cloud APIs (Compute, Storage, Kubernetes, etc.)', 'Check if pageTokens from one user account can be reused by another authenticated user', 'Test whether manipulation of pageToken encoding (base64, hex, etc.) yields different project access', 'Enumerate whether other list operations (roles.list, policies.list) have similar pagination vulnerabilities', 'Investigate if pageTokens leak timing information or patterns that could aid in enumeration', 'Test cross-organization pagination token reuse if GCP supports multi-organization scenarios']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate Cloud Resources
- T1518 - Gather Victim Identity Information
- T1589 - Gather Victim Identity Information
- T1538 - Cloud Service Abuse
- T1562 - Impair Defenses

## Notes
This vulnerability demonstrates how pagination mechanisms, often overlooked in security reviews, can become significant attack vectors. The issue is particularly severe in cloud environments where project IDs can be leveraged for reconnaissance of entire infrastructure. The researcher's methodical approach—analyzing API documentation, testing parameter manipulation, and understanding token structure—exemplifies effective bug hunting methodology. Google's heavy security scrutiny of the IAM API may have focused on authorization logic while missing pagination edge cases.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
