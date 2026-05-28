# IDOR Vulnerability in Google Bard Vision Feature Allowing Unauthorized Image Access

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT
- **Bounty:** $50,000
- **Severity:** High
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Inadequate Authorization Verification
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered a critical IDOR vulnerability in Google Bard's Vision feature that allowed authenticated users to view and describe arbitrary other users' images without authorization. By manipulating image file paths in API requests, attackers could access private images of any user, effectively bypassing access control mechanisms designed to protect user privacy.

## Attack scenario (step by step)
1. Attacker creates two Google accounts and authenticates with both
2. Attacker uploads an image as User 1 and intercepts the POST request to StreamGenerate API using a proxy tool
3. Attacker extracts the file path from User 1's image from the API request (e.g., /contrib_service/ttl_1d/1689251070jtdc4jkzne6a5yaj4n7m)
4. Attacker switches to User 2 account and uploads a dummy image, then intercepts that request
5. Attacker modifies the file path parameter in User 2's request to match User 1's image path
6. Attacker sends the modified request and successfully receives descriptions of User 1's private image, demonstrating unauthorized access

## Root cause
The Vision feature implemented insufficient authorization validation on image file access. The API endpoint used predictable or sequential file paths without implementing proper access control checks to verify that the requesting user owns or has permission to access the specified image resource. The system relied on implicit trust rather than explicit permission verification.

## Attacker mindset
An attacker would recognize that file path manipulation is a common attack vector in APIs. The predictable path structure combined with the Vision feature's need to retrieve images creates an opportunity to enumerate and access other users' private data. The attacker would systematically test whether authorization is checked server-side or if the path parameter alone grants access.

## Defensive takeaways
- Implement strict server-side authorization checks before accessing any user resource, verifying user ownership or explicit permissions
- Use unpredictable, non-sequential resource identifiers (UUIDs/GUIDs) instead of predictable paths that can be enumerated
- Implement access control at the file storage layer, not just the API layer
- Add audit logging for file access attempts including failed authorization attempts
- Conduct security reviews of all new AI/ML features with focus on data access controls
- Use parameterized requests and avoid exposing internal file paths in API responses
- Implement rate limiting on vision processing requests to limit enumeration attacks

## Variant hunting
Similar IDOR vulnerabilities likely exist in other Google AI features that process user-uploaded content (Gemini image analysis, Google Photos integration, document processing). Other GenAI platforms (Meta, Microsoft, OpenAI) using similar path-based file access patterns warrant investigation. Document processing features, audio transcription services, and any multi-user AI collaboration features should be tested for similar authorization bypass.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1555 - Credentials from Password Stores
- T1566 - Phishing
- T1552 - Unsecured Credentials
- T1526 - Exposure of Sensitive Data

## Notes
This vulnerability was discovered during an exclusive Google Bug Bounty event (LLM bugSWAT) in Las Vegas during DEFCON. The research team collaborated on-site with Google security engineers who could provide contextual guidance. The writeup emphasizes that emerging AI/ML features often lack foundational security practices. The $50,000 bounty reflects the sensitivity of unauthorized access to user image data. The team's collaborative approach and real-time feedback from Google engineers accelerated vulnerability discovery.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
