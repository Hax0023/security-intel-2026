# IDOR Vulnerability in Google Bard Vision Feature Allowing Unauthorized Image Access

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** high
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Unauthorized Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered an IDOR vulnerability in Google Bard's Vision feature that allowed attackers to view and describe other users' uploaded images without authorization. By intercepting and modifying the file path parameter in API requests, an attacker could substitute another user's image path and retrieve descriptions of arbitrary images belonging to different users.

## Attack scenario (step by step)
1. Attacker (User 1) uploads an image to Bard's Vision feature and intercepts the POST request to StreamGenerate API
2. Attacker extracts the file path from their own image request (e.g., /contrib_service/ttl_1d/1689251070jtdc4jkzne6a5yaj4n7m)
3. Attacker creates or hijacks a second user session (User 2)
4. Attacker uploads a dummy image from User 2's account and captures the StreamGenerate request
5. Attacker modifies the file path parameter in User 2's request to point to User 1's image path
6. Attacker sends the modified request and receives Bard's description of User 1's private image, confirming unauthorized access

## Root cause
The Vision API endpoint failed to implement proper authorization checks before processing image descriptions. The application relied on the client-supplied file path without validating that the requesting user had permission to access the image resource, allowing path traversal across user boundaries.

## Attacker mindset
An attacker with basic proxy interception knowledge could systematically enumerate file paths and harvest descriptions/metadata from arbitrary user images, potentially extracting sensitive visual information (documents, photos, personal items) from other users' accounts.

## Defensive takeaways
- Implement strict authorization checks on all resource access, verifying user ownership/permissions before processing requests
- Use cryptographically secure, unpredictable identifiers for user-uploaded resources instead of sequential or enumerable paths
- Store file paths and access tokens server-side; never trust client-supplied resource identifiers
- Apply the principle of least privilege to API endpoints - only return data the authenticated user is explicitly authorized to access
- Conduct security red teaming specifically for AI/LLM features, as they introduce novel attack surfaces
- Implement access logging and anomaly detection for bulk resource enumeration attempts

## Variant hunting
Similar IDOR patterns likely exist in other Google AI features (image generation, document analysis). Search for other endpoints accepting file paths or resource IDs as parameters without server-side authorization validation. Test cross-user scenarios in all file upload/processing features.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Reconnaissance/Enumerate resources
- T1530 - Data from Cloud Storage
- T1552 - Unsecured Credentials

## Notes
This vulnerability was discovered during an exclusive Google Bug Bounty event (LLM bugSWAT) in August 2024 at Defcon in Las Vegas. The collaborative effort between three researchers (rez0, Rhynorater, Lupin) demonstrates the effectiveness of team-based security research. The vulnerability affected Bard (now Gemini) Vision feature, a core AI capability. The $50,000 bounty reflects the severity and potential impact on user privacy. This finding highlights that major tech companies were prioritizing AI feature deployment over foundational security controls during the LLM boom.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
