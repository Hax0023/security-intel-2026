# IDOR Vulnerability in Google Bard Vision Feature Allowing Access to Other Users' Images

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Google LLM bugSWAT (Bug Bounty Event)
- **Bounty:** $50,000
- **Severity:** High
- **Vuln types:** Insecure Direct Object Reference (IDOR), Authorization Bypass, Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered an IDOR vulnerability in Google Bard's Vision feature that allowed attackers to access and describe images uploaded by other users without authorization. By manipulating the file path parameter in API requests, an authenticated user could retrieve and process arbitrary images belonging to other Bard users. This vulnerability exposed sensitive user data through the image analysis functionality.

## Attack scenario (step by step)
1. Attacker creates a Google Bard account and authenticates as User A
2. Attacker uploads a benign image while intercepting the POST request to StreamGenerate endpoint
3. Attacker extracts the file path from the response (format: /contrib_service/ttl_1d/[timestamp][random_string])
4. Attacker creates another Bard account as User B and uploads a different image
5. Attacker intercepts User B's StreamGenerate request and replaces the file path parameter with User A's extracted path
6. Attacker sends the modified request and receives detailed description of User A's private image

## Root cause
The Bard Vision API endpoint failed to implement proper authorization checks on file path parameters. The application trusted user-supplied file paths without verifying that the requesting user had permission to access the specified image resource. The lack of access control validation allowed direct object reference exploitation.

## Attacker mindset
An attacker with valid Bard credentials could systematically enumerate file paths and access other users' private images. The predictable path format and absence of permission checks made this an easily exploitable vulnerability. The attacker could harvest sensitive information from images across the user base.

## Defensive takeaways
- Implement robust authorization checks on all file access operations - verify user ownership before processing
- Use opaque, non-sequential identifiers for file references instead of predictable timestamp-based paths
- Apply principle of least privilege - validate that authenticated users can only access their own resources
- Implement server-side file path validation and sanitization to prevent direct object manipulation
- Add comprehensive audit logging for image access and AI processing requests
- Conduct security review of all LLM-integrated features with focus on indirect resource access patterns
- Use indirect references (database IDs with ownership mapping) rather than exposing actual file paths

## Variant hunting
Similar IDOR patterns likely exist in other Google AI features handling user-uploaded content (Gemini image generation, Drive AI integration, YouTube features). Check for authorization bypass in document processing APIs, email analysis tools, or any GenAI feature accepting user files. Look for predictable resource identifiers in vision APIs, audio processing endpoints, and document analysis services.

## MITRE ATT&CK
- T1190
- T1566
- T1552
- T1526
- T1087

## Notes
This vulnerability was discovered during Google's exclusive LLM bugSWAT event in Las Vegas (August 2023) by a three-person research team: Joseph Thacker (rez0), Justin Gardner (Rhynorater), and Roni Carta (Lupin). The event format with direct access to Google engineers and source code review enabled rapid validation. The vulnerability exemplifies how companies prioritizing rapid LLM deployment may inadvertently revert to pre-cloud-era security mistakes. The $50,000 bounty reflects high severity of information disclosure from multi-user platform.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
