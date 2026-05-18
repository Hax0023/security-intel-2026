# Leaking Google Cloud Projects via IAM pageToken Forgery

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Google Cloud Platform
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln types:** Authentication Bypass, Authorization Bypass, Information Disclosure, Broken Access Control
- **Category:** infra-cloud
- **Writeup:** https://www.ezequiel.tech/2020/08/leaking-google-cloud-projects.html

## Summary
A critical authentication bypass in Google Cloud's IAM API allowed attackers to list service accounts of any GCP project by forging pageToken values in the projects.serviceAccounts.list method. This vulnerability enabled disclosure of project IDs (considered PII) and service account details, which could be leveraged for further reconnaissance and attacks on GCP resources.

## Attack scenario (step by step)
1. Attacker discovers the projects.serviceAccounts.list API endpoint and its pageToken parameter
2. Attacker analyzes the pageToken format through legitimate requests to their own GCP project
3. Attacker crafts malicious pageToken values targeting other projects using known or enumerated project numbers
4. Attacker sends forged requests to list service accounts in victim projects without proper authorization
5. Attacker extracts service account emails, project IDs, and metadata from responses
6. Attacker uses disclosed information to scan for unsecured GCP resources like App Engine apps and Container Registry repositories

## Root cause
Insufficient validation of the pageToken parameter. The API implementation failed to properly verify that the pageToken was legitimately generated for the requested project, allowing attackers to forge tokens for arbitrary projects. The token structure was predictable or lacked cryptographic integrity checks.

## Attacker mindset
Reconnaissance-focused attacker seeking to enumerate GCP infrastructure. Approached the problem systematically by analyzing pagination mechanisms in sensitive APIs, understanding that even well-secured services may have overlooked edge cases. Leveraged the predictable nature of API tokens to escalate from self-enumeration to cross-project data disclosure.

## Defensive takeaways
- Implement cryptographic signing and validation for all pagination tokens to prevent forgery
- Validate that pagination tokens can only be used with the same project/resource context they were issued for
- Apply strict access control checks on all API methods, including list operations, regardless of perceived sensitivity
- Treat project IDs as sensitive (PII) and limit their disclosure to authorized users only
- Conduct security reviews of pagination implementations across all APIs, particularly those handling sensitive resources
- Implement rate limiting and anomaly detection for API enumeration attempts
- Use security testing frameworks to identify pagination bypass opportunities proactively

## Variant hunting
['Check other GCP APIs that implement pagination (Compute, Storage, BigQuery) for similar pageToken validation flaws', 'Test whether cursors/tokens in other Google services (Workspace, Maps, YouTube API) can be forged', 'Investigate if pageToken values can be reused across different API methods', 'Examine whether other query parameters (pageSize, filter) can bypass authorization checks', 'Test if sequential or predictable pageToken patterns exist in other IAM endpoints', 'Check if service account enumeration is possible through other IAM methods (roles.list, permissions.list)']

## MITRE ATT&CK
- T1190
- T1589
- T1526
- T1087
- T1550
- T1552

## Notes
This vulnerability demonstrates that even heavily scrutinized services can have subtle logic flaws. The impact chain (token forgery → unauthorized enumeration → PII disclosure → lateral reconnaissance) shows how seemingly minor issues compound into significant security risks. The writeup exemplifies good bug-hunting methodology: systematic exploration of underdocumented parameters and deep understanding of API implementation details.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
