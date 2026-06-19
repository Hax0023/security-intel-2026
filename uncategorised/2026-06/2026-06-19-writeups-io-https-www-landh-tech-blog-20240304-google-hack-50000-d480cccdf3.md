# IDOR Vulnerability in Google Bard Vision Feature - Unauthorized Image Access

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** High
- **Vuln types:** Insecure Direct Object Reference (IDOR), Authorization Bypass, Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered a critical IDOR vulnerability in Google Bard's Vision feature that allowed attackers to view and describe other users' uploaded images without authorization. By manipulating the file path parameter in API requests, an authenticated attacker could access arbitrary images belonging to different users, effectively bypassing access controls.

## Attack scenario (step by step)
1. Attacker creates two accounts (User 1 and User 2) on Google Bard
2. User 1 uploads an image and intercepts the POST request to StreamGenerate endpoint via proxy
3. Attacker extracts the file path from User 1's request (e.g., /contrib_service/ttl_1d/1689251070jtdc4jkzne6a5yaj4n7m)
4. User 2 uploads any image and captures their StreamGenerate request in a proxy/repeater
5. Attacker modifies the path parameter in User 2's request to use User 1's extracted path
6. System processes the request and describes User 1's image while authenticated as User 2, revealing unauthorized image access

## Root cause
The Vision feature's backend relied solely on user authentication without implementing object-level authorization checks. The API endpoint validated that a request came from an authenticated user but failed to verify that the user had permission to access the specific image resource identified by the file path parameter. The path parameter was user-controllable and not tied to the authenticated user's ownership.

## Attacker mindset
An attacker would recognize that file path parameters in API requests are common targets for IDOR vulnerabilities when authorization is missing. By observing the structure of legitimate requests and understanding that the Vision feature processes arbitrary images, they would attempt simple parameter manipulation to access other users' resources. The insight that 'no idea is stupid until we test them' drives systematic fuzzing of user-controllable identifiers.

## Defensive takeaways
- Implement object-level authorization checks before processing any user-submitted resource identifiers
- Avoid exposing direct file paths or sequential identifiers; use opaque tokens or UUIDs tied to user ownership
- Verify ownership of resources in the application logic, not just at the authentication layer
- Use security proxies and request validation to ensure path parameters match authenticated user context
- Apply the principle of least privilege: validate that the authenticated user has explicit permission to access each resource
- Conduct thorough authorization testing during security reviews of new AI/ML features with file upload capabilities
- Log and monitor access patterns to detect anomalous cross-user resource access

## Variant hunting
Search for similar IDOR patterns in: (1) Other Google AI features accepting file uploads (Gemini image analysis, NotebookLM document processing); (2) GraphQL endpoints handling file references without ownership validation; (3) Batch processing endpoints that accept multiple file identifiers; (4) Caching layers that serve images based on path parameters without re-validation; (5) Sharing/permission APIs that derive access from path manipulation rather than explicit permission records

## MITRE ATT&CK
- T1190
- T1566
- T1078
- T1526
- T1530

## Notes
This vulnerability was discovered during an exclusive, invitation-only bug bounty event at Defcon. The researchers were given direct access to Google security engineers for clarification, enabling rapid exploitation and verification. The vulnerability affected Bard (later renamed Gemini) Vision feature and demonstrates how rapid development of AI features can outpace security implementation. The research team's collaborative approach and access to insider information allowed them to identify and validate the flaw efficiently.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
