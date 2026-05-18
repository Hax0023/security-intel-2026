# IDOR Vulnerability in Google Bard Vision Feature - Unauthorized Access to Other Users' Images

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** high
- **Vuln types:** Insecure Direct Object Reference (IDOR), Authorization Bypass, Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered an IDOR vulnerability in Google Bard's Vision feature that allowed attackers to access and describe other users' uploaded images without authorization. By manipulating the file path parameter in the StreamGenerate API request, an attacker could substitute another user's image path and gain unauthorized access to their private images. This vulnerability exposed sensitive user data and violated fundamental authorization principles.

## Attack scenario (step by step)
1. Attacker (User A) uploads an image to Google Bard's Vision feature and intercepts the POST request to StreamGenerate API using a proxy
2. Attacker extracts the file path from the request body, which contains an identifier like '/contrib_service/ttl_1d/1689251070jtdc4jkzne6a5yaj4n7m'
3. Attacker enumerates or obtains another user's (User B) file path through fuzzing, timing attacks, or other reconnaissance
4. Attacker modifies their own Vision feature request, replacing their file path with User B's path in the StreamGenerate API call
5. Attacker sends the modified request, causing Bard to process and describe User B's image instead of their own
6. Bard processes the request and returns a detailed description of User B's private image, exposing its contents without authorization

## Root cause
The application implements direct object references to user-uploaded images using predictable path identifiers without server-side authorization checks. The backend fails to verify that the requesting user owns or has permission to access the image at the specified path before processing it through the Vision AI model. The vulnerability stems from trusting client-supplied file paths without validating ownership.

## Attacker mindset
An attacker would recognize that file paths in API requests are often enumerable or predictable, especially when they contain timestamps or sequential identifiers. The lack of authorization checks on the backend presents an easy win - simply modify the path parameter and observe if another user's data is returned. This is a classic IDOR pattern that demonstrates how developers sometimes implement object references without considering that users could modify these references.

## Defensive takeaways
- Implement server-side authorization checks on every request - verify the authenticated user owns/has access to the requested resource before processing
- Use unpredictable, non-sequential identifiers for resources (UUIDs instead of timestamps or sequential IDs)
- Implement indirect reference maps - map user input to server-stored references rather than exposing direct object identifiers
- Add access control validation at the application layer, not just at the presentation layer
- Log and monitor for suspicious access patterns - multiple requests with varying file path parameters may indicate enumeration attempts
- When processing user-uploaded files, always bind them to the authenticated user and verify this relationship on access
- Consider implementing rate limiting on file processing endpoints to detect enumeration attacks

## Variant hunting
Look for similar IDOR vulnerabilities in other GenAI features: image generation with retrieval, document processing, video analysis, or any feature that stores and retrieves user-specific data. Check GraphQL endpoints (mentioned in the writeup title) for IDOR patterns - GraphQL queries may expose object IDs in different ways. Examine other Bard/Gemini features like file sharing, model fine-tuning data, or conversation history exports. Investigate if the same ttl_1d path structure is used elsewhere for other user assets.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566: Phishing
- T1555: Credentials from Password Stores
- T1526: Enumerate External Targets
- T1592: Gather Victim Identity Information

## Notes
This vulnerability was part of Google's LLM bugSWAT event during DEF CON. The research team consisted of Joseph 'rez0' Thacker, Justin 'Rhynorater' Gardner, and Roni 'Lupin' Carta. The vulnerability affected Bard (now Gemini) Vision feature. The writeup highlights the importance of security research in emerging AI/LLM technologies, which often lack the security maturity of traditional applications. The collaborative approach to bug hunting and direct interaction with Google security engineers accelerated vulnerability discovery. The affected endpoint uses the BardFrontendService/StreamGenerate pattern with GraphQL-like service routing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
