# IDOR and GraphQL DoS vulnerabilities in Google Bard/Gemini AI

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** High
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Denial of Service (DoS), GraphQL Injection, LLM-specific security flaws
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered critical IDOR vulnerabilities in Google's Bard (Gemini) Vision feature that allowed unauthorized access to other users' uploaded images and their descriptions. The exploitation involved intercepting and modifying file path references in POST requests to the BardFrontendService, bypassing access control mechanisms entirely. This demonstrates how rapidly deployed AI features can introduce fundamental security gaps when established security principles are overlooked.

## Attack scenario (step by step)
1. Attacker creates two Google accounts (User A and User B) and logs into Bard with User A
2. User A uploads an image while monitoring network traffic through a proxy tool (Burp Suite)
3. Attacker identifies the POST request to StreamGenerate endpoint and extracts the file path identifier (e.g., /contrib_service/ttl_1d/1689251070jtdc4jkzne6a5yaj4n7m)
4. Attacker switches to User B's session and uploads any image, capturing that request
5. Attacker modifies User B's image path parameter to User A's path identifier and forwards the request
6. Bard processes the request and returns a description of User A's image, confirming unauthorized cross-user image access

## Root cause
The Vision feature implementation failed to properly validate ownership of image resources. The backend system relied on predictable, sequential file path identifiers without sufficient authorization checks. The API endpoint accepted user-supplied file paths without verifying that the requesting user had permissions to access those specific resources. The developers prioritized rapid feature deployment over implementing proper access control matrices and resource ownership validation.

## Attacker mindset
The researchers approached this as a systematic security assessment, leveraging their experience with common authorization flaws. They recognized that new AI features often lack mature security controls and focused on fundamental OWASP Top 10 issues (IDOR, broken access control). The collaboration methodology - brainstorming and testing assumptions - reflects professional red-team thinking. They understood that LLM products represent low-hanging fruit for security testing because they're built quickly and often lack security review cycles.

## Defensive takeaways
- Implement server-side authorization checks on every API endpoint - verify user owns/has permission for requested resources regardless of feature maturity
- Never rely on opaque file identifiers without cryptographic binding to user identity and session context
- Use non-sequential, cryptographically random identifiers (UUIDs v4 or similar) for resource references
- Enforce API authorization at multiple layers: authentication, resource ownership validation, and ACL verification
- Conduct threat modeling specifically for new AI/LLM features before deployment, treating them as high-risk additions
- Implement comprehensive API request logging to detect cross-user resource access patterns
- Establish mandatory security review checkpoints for AI features independent of standard feature release cycles
- Test access control with multiple user accounts during pre-release testing phases
- Apply the principle of least privilege - AI services should only access resources explicitly authorized for their user context

## Variant hunting
Hunt for similar IDOR vulnerabilities in: other Google AI features (Duet AI, MakerSuite, Vertex AI), GraphQL endpoints that return user-generated content (search similar patterns in Vision API, Document AI), file storage services with predictable naming schemes, any endpoint accepting file paths as parameters, other Google LLM products that were rapidly deployed during 2023-2024 AI rush, cached responses that might leak other users' AI descriptions, batch processing endpoints that might expose user data in progress tracking

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566: Phishing (could use stolen images for social engineering)
- T1530: Data from Cloud Storage
- T1526: Reconnaissance - could enumerate user IDs through image paths
- T1087: Account Discovery (enumerate valid user image paths)
- T1078: Valid Accounts (leverage legitimate Bard access for unauthorized data access)

## Notes
The writeup is incomplete in the provided content (cuts off mid-sentence during reproduction steps), but the described vulnerability is classic IDOR with significant real-world impact in an AI context. The $50,000 bounty reflects the severity and potential for mass data exposure. The collaboration aspect highlights how security research benefits from diverse perspectives. This case exemplifies the 'security debt' incurred by rapid AI feature deployment - companies deployed LLM capabilities faster than they could establish security maturity. The researchers' access to Google engineers during the event was invaluable for clarification, suggesting bug bounty programs should consider in-person events for complex vulnerability research. The vulnerability was particularly dangerous because image descriptions generated by LLMs could leak sensitive information about other users' content (financial documents, private photos, etc.) with added context value from the AI analysis.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
