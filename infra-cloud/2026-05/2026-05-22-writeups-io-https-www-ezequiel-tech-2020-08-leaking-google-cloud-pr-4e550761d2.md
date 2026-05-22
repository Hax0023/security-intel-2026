# Auth Bypass: Leaking Google Cloud Service Accounts and Projects via pageToken Forgery

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Google Cloud Platform
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Authorization Bypass, Information Disclosure, Pagination Token Manipulation, Access Control Weakness
- **Category:** infra-cloud
- **Writeup:** https://www.ezequiel.tech/2020/08/leaking-google-cloud-projects.html

## Summary
The IAM API's projects.serviceAccounts.list method was vulnerable to authorization bypass through pageToken forgery, allowing attackers to enumerate service accounts in any GCP project given only its project number. This vulnerability exposed sensitive PII (GCP project IDs) and service account details that could be leveraged for further reconnaissance and exploitation of cloud resources.

## Attack scenario (step by step)
1. Attacker obtains a valid GCP project number (often publicly available or discoverable)
2. Attacker crafts malicious pageToken values to manipulate pagination logic in the IAM API
3. Attacker sends forged requests to projects.serviceAccounts.list with crafted pageToken parameter
4. Due to insufficient token validation, API returns service accounts from target project without authorization checks
5. Attacker extracts service account emails, unique IDs, and display names from responses
6. Attacker uses collected project IDs and service account information to scan for additional unsecured resources (App Engine, Container Registry, etc.)

## Root cause
The pageToken pagination parameter was not properly validated or cryptographically signed, allowing attackers to forge tokens and bypass authorization checks. The API failed to verify that the pagination token originated from a legitimate request to the same project, instead trusting token content at face value.

## Attacker mindset
Opportunistic cloud reconnaissance attacker seeking to map target GCP infrastructure and service accounts without authorization. The attacker recognized that pagination tokens are often an overlooked security control and that enumeration of service accounts could enable lateral movement or privilege escalation in cloud environments.

## Defensive takeaways
- Implement cryptographically signed or encrypted pagination tokens that cannot be forged
- Always validate pagination tokens are associated with the correct resource/project context
- Apply authorization checks at every API method, regardless of whether the request uses pagination
- Consider treating GCP project IDs and service account information as sensitive data requiring protection
- Implement rate limiting on list operations to prevent enumeration attacks
- Audit all API methods that use pagination tokens for similar bypass vulnerabilities
- Log and alert on unusual pagination token patterns or repeated failed authorization attempts

## Variant hunting
['Test other GCP API list methods (compute.instances.list, storage.buckets.list, etc.) for similar pageToken bypass vulnerabilities', 'Examine pageToken format and validation in other Google APIs and services', 'Look for pagination implementations that use stateless tokens without cryptographic validation', 'Test whether pageTokens from one project/resource can be used to access other projects/resources', 'Fuzz pageToken parameters with various encodings and values to identify validation gaps', 'Check if pageToken validation differs based on authentication context or account type', "Research other cloud providers' pagination implementations for similar weaknesses"]

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate Cloud Resources
- T1589 - Gather Victim Identity Information
- T1538 - Cloud Service Dashboard
- T1526.001 - Enumerate Cloud Storage

## Notes
This vulnerability demonstrates a critical flaw in assuming pagination parameters are inherently trustworthy. The impact was amplified because GCP project numbers, while not secret, are difficult to discover without enumeration—the vulnerability enabled large-scale discovery of projects. The writeup highlights the importance of security review for 'boring' infrastructure components like pagination, which are often overlooked by security teams.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
