# Leaking Google Cloud Projects via IAM API pageToken Forgery

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Google Cloud Platform
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Authentication Bypass, Authorization Bypass, Information Disclosure, Insecure Direct Object Reference (IDOR)
- **Category:** infra-cloud
- **Writeup:** https://www.ezequiel.tech/2020/08/leaking-google-cloud-projects.html

## Summary
A pageToken forgery vulnerability in the IAM API's projects.serviceAccounts.list method allowed attackers to enumerate service accounts from any GCP project given only the project number. This disclosure vulnerability could expose sensitive project identifiers and service account details, enabling further reconnaissance attacks against GCP infrastructure.

## Attack scenario (step by step)
1. Attacker obtains or enumerates a target GCP project number (considered PII in GCP)
2. Attacker crafts malicious pageToken parameter by analyzing token structure and patterns
3. Attacker sends forged pageToken to projects.serviceAccounts.list API endpoint with target project number
4. API bypasses authorization checks and returns service account listings from target project
5. Attacker enumerates all service accounts and project details from victim's GCP project
6. Attacker uses disclosed project IDs to scan for other exposed GCP resources (App Engine, Container Registry, etc.)

## Root cause
Insufficient validation of pageToken parameter in the IAM API's list method. The API failed to properly validate that the pageToken belonged to the authenticated user's project or had authorization context tied to it. The token implementation likely used predictable or forgeable encoding without cryptographic integrity checks.

## Attacker mindset
Researcher methodically analyzing API pagination mechanisms, recognizing that pagination tokens are often overlooked security controls. Intuited that pageToken validation might be weak compared to other authorization checks in sensitive APIs. Leveraged design flaw to escalate from listing own resources to arbitrary project enumeration.

## Defensive takeaways
- Implement cryptographically signed or encrypted pagination tokens (HMAC/JWT) that are impossible to forge
- Bind pagination tokens to specific authenticated user/project context with server-side validation
- Apply consistent authorization checks to all API methods including pagination parameters
- Treat GCP project numbers as sensitive identifiers requiring protection equivalent to project IDs
- Implement rate limiting and anomaly detection for IAM API list operations
- Audit all pagination implementations across APIs for similar authorization gaps
- Use opaque tokens where token content is not derived from user input or predictable patterns

## Variant hunting
['Check other GCP APIs using pagination (Compute, Storage, Kubernetes) for similar pageToken validation bypasses', "Test if pageToken from one project context can be used in another project's API calls", 'Examine other Google APIs (Gmail, Workspace, YouTube) for pagination token forgery vulnerabilities', 'Investigate if nextPageToken/pageToken patterns in other cloud providers (AWS, Azure) have similar flaws', 'Look for predictable or base64-encoded pagination tokens that reveal structure', 'Test whether combining modified pageToken with different authentication contexts bypasses checks']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1526: Enumerate Cloud Resources
- T1538: Cloud Service Discovery
- T1087: Account Discovery
- T1580: Cloud Infrastructure Discovery

## Notes
This vulnerability is significant because it breaks the trust boundary between GCP projects. Project numbers are typically not publicly disclosed but are considered PII and sensitive. The ability to enumerate service accounts across projects enables reconnaissance for supply chain attacks, lateral movement planning, and identification of high-value targets. The fix required cryptographic integrity validation of pagination tokens rather than relying on client-provided tokens for authorization context.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
