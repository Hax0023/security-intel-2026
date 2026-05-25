# Auth Bypass: Leaking Google Cloud Service Accounts and Projects via Forged pageToken

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Google Cloud Platform (GCP)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Authorization Bypass, Information Disclosure, Insufficient Input Validation, Pagination Token Forgery
- **Category:** infra-cloud
- **Writeup:** https://www.ezequiel.tech/2020/08/leaking-google-cloud-projects.html

## Summary
An authorization bypass vulnerability in the IAM API's projects.serviceAccounts.list method allowed attackers to forge pageToken parameters to list service accounts from any GCP project by knowing only the project number. This could be chained to enumerate and leak GCP project IDs (classified as PII) and identify unsecured resources across the platform.

## Attack scenario (step by step)
1. Attacker obtains or brute-forces a target GCP project number
2. Attacker crafts a request to projects.serviceAccounts.list with a forged pageToken parameter
3. Due to insufficient validation, the forged token bypasses authorization checks on the pagination mechanism
4. API returns service account details including email addresses, display names, and unique IDs
5. Attacker enumerates additional project numbers using leaked project IDs
6. Attacker scans enumerated projects for unsecured resources (App Engine, Container Registry, etc.)

## Root cause
The pageToken parameter in the IAM API's pagination implementation was not properly validated or cryptographically signed, allowing attackers to forge arbitrary tokens. The API did not verify that the token was legitimately issued for the requesting user or that the user had permission to access the specified project. The pagination logic trusted client-supplied tokens without sufficient authentication context.

## Attacker mindset
An attacker would recognize that pagination tokens are often overlooked security-critical components. By analyzing the API's pagination behavior and attempting token manipulation, the attacker discovered that the validation was superficial. This represents a methodical vulnerability research approach targeting high-value but well-protected services, betting that edge cases in pagination logic might be missed.

## Defensive takeaways
- Implement cryptographically signed or encrypted pagination tokens that cannot be forged by clients
- Validate pageToken integrity and ensure tokens were legitimately issued for the requesting principal
- Include authorization context in pagination logic—verify user permissions for each page independently
- Apply the same authorization checks to list operations regardless of pagination parameters
- Treat project numbers/IDs as sensitive data requiring protection equivalent to API keys
- Implement rate limiting and anomaly detection on API enumeration patterns
- Conduct security reviews specifically focused on pagination, filtering, and query parameter handling
- Consider server-side pagination state management instead of client-supplied tokens

## Variant hunting
['Test pageToken manipulation in other list methods across GCP APIs (compute.instances.list, storage.buckets.list, etc.)', 'Attempt pageToken reuse across different projects or users', 'Try encoding/decoding pageToken formats to identify weak cryptography or predictable patterns', 'Test negative page numbers, zero values, or oversized tokens for boundary conditions', 'Look for similar pagination bypass patterns in other Google APIs and services', 'Enumerate other query parameters that might affect authorization (pageSize, filter, orderBy)', 'Test for token expiration bypass by using very old or future-dated tokens']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate Cloud Resources
- T1087 - Account Discovery
- T1580 - Cloud Infrastructure Discovery
- T1538 - Cloud Service Discovery
- T1552 - Unsecured Credentials

## Notes
This vulnerability is particularly severe because: (1) GCP project numbers and IDs are meant to be somewhat hidden, making this enumeration capability valuable for reconnaissance; (2) the IAM API is a critical security service, making any bypass concerning; (3) the fix likely required changes to token generation and validation logic across a major API; (4) the writeup demonstrates excellent security research methodology by examining commonly overlooked pagination mechanisms; (5) the chain from service account enumeration to project discovery represents a significant information disclosure risk in multi-tenant cloud environments.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
