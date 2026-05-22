# Google Bard/Gemini IDOR Vulnerability - Unauthorized Access to Other Users' Images

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** High
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Insufficient Authorization Verification
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered an IDOR vulnerability in Google Bard's Vision feature that allowed authenticated users to access and describe images belonging to other users by manipulating file path parameters in API requests. The vulnerability bypassed all authorization checks, enabling attackers to view arbitrary user images without permission. This critical access control flaw was discovered during Google's exclusive LLM bugSWAT event in Las Vegas.

## Attack scenario (step by step)
1. Attacker authenticates as User A and uploads an image to Bard's Vision feature
2. Attacker intercepts the POST request to StreamGenerate endpoint and extracts the file path parameter from the response (e.g., /contrib_service/ttl_1d/1689251070jtdc4jkzne6a5yaj4n7m)
3. Attacker creates a new image upload request as User B and intercepts it before sending
4. Attacker modifies the file path parameter in User B's request to point to User A's uploaded image file
5. Attacker forwards the modified request to the Bard service
6. The Vision API processes the request and returns a description of User A's image, confirming unauthorized access across user boundaries

## Root cause
The backend implementation failed to validate that the requested file resource belongs to the authenticated user. The file path parameter was accepted at face value without checking ownership or authorization, relying solely on the client-provided path identifier. The API lacked proper access control checks between resource ownership and request authentication.

## Attacker mindset
An attacker would recognize that file path parameters in Vision API requests are predictable and enumerable, allowing horizontal privilege escalation. They would systematically test path parameter manipulation to access other users' private data. The attacker would focus on privacy breaches, potentially harvesting sensitive images, documents, or confidential information from other users.

## Defensive takeaways
- Implement strict authorization checks on all resource access - verify that the authenticated user owns or has explicit permission to access the requested resource
- Use non-sequential, cryptographically random identifiers for sensitive resources instead of predictable paths
- Apply the principle of least privilege - users should only access resources they created or were explicitly granted access to
- Implement server-side session validation to tie resources to user context, not client-provided identifiers
- Conduct comprehensive access control testing across all new AI/ML features, especially those handling user-uploaded content
- Add audit logging for resource access attempts to detect and investigate unauthorized access patterns
- Use consistent authorization middleware across all API endpoints to prevent bypasses

## Variant hunting
Search for similar IDOR vulnerabilities in: Google Photos/Drive integration with Gemini, other Google AI features accepting file uploads, Gemini's file analysis features, concurrent Google Cloud Storage object access patterns, and any GraphQL endpoints handling user resources without proper authorization checks. Test parameter manipulation on related Google services using predictable identifiers.

## MITRE ATT&CK
- T1190
- T1552
- T1526
- T1087

## Notes
Vulnerability discovered during an exclusive, in-person bug bounty event with direct access to Google security engineers for clarification. The collaborative approach of three researchers (Thacker, Gardner, Carta) demonstrated the value of teamwork in security research. Google's willingness to host physical events and allow researchers to bring additional expertise shows mature bug bounty program management. The Vision feature was relatively new at the time, suggesting rushed deployment without comprehensive security review of new AI capabilities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
