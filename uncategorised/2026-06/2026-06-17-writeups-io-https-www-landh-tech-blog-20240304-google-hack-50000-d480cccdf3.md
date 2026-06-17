# IDOR Vulnerability in Google Bard Vision Feature Leading to Unauthorized Image Access

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** High
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Insufficient Authorization Verification
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered a critical IDOR vulnerability in Google Bard's Vision feature that allowed attackers to access and describe other users' uploaded images without authorization. By manipulating file path parameters in API requests, an attacker could retrieve and process arbitrary images belonging to different users. This vulnerability completely bypassed access controls on sensitive user-uploaded image data.

## Attack scenario (step by step)
1. Attacker (User 1) uploads an image to Google Bard's Vision feature while intercepting traffic with a proxy tool (Burp Suite)
2. Attacker captures the POST request to assistant.lamda.BardFrontendService/StreamGenerate and extracts the file path identifier from the request body (e.g., /contrib_service/ttl_1d/1689251070jtdc4jkzne6a5yaj4n7m)
3. Attacker switches to a different account (User 2) and uploads a benign image to establish a valid request context
4. Attacker intercepts User 2's Vision request and modifies the file path parameter to point to User 1's uploaded image
5. Attacker submits the modified request, and the backend processes User 1's image without verifying ownership or permissions
6. Bard Vision feature returns a detailed description of User 1's private image, exposing its contents to the unauthorized attacker

## Root cause
The backend API failed to implement proper authorization checks before processing image paths. The system trusted user-supplied file path parameters without validating that the requesting user owns or has permission to access the referenced image file. No ownership verification occurred between the authenticated user context and the image resource identifier.

## Attacker mindset
The attacker recognized that object identifiers (file paths) in API requests often lack proper authorization enforcement, a classic IDOR pattern. By understanding the API structure and testing with multiple accounts, the attacker could systematically enumerate and access other users' resources. The direct exposure of file paths in requests suggested weak separation between authentication (you are who you say you are) and authorization (you can access this specific resource).

## Defensive takeaways
- Implement strict authorization checks on all resource access: verify that the authenticated user owns or has explicit permission to access each resource before processing
- Never rely on user-supplied identifiers or paths alone; maintain server-side mappings between users and their resources
- Use indirect object references (UUIDs, random tokens) instead of predictable sequential IDs or file paths exposed to clients
- Implement consistent access control patterns across all API endpoints, especially for AI/ML services handling user-generated content
- Add logging and monitoring for cross-user resource access attempts to detect exploitation
- Conduct thorough security testing of new AI features before production release, focusing on multi-user scenarios and data isolation

## Variant hunting
Similar IDOR vulnerabilities likely exist in other Google AI services (Gemini, Google Photos integration, Imagen). Test other image processing endpoints, file upload features, and content delivery APIs. Check for IDORs in model-specific features like conversation history access, cached results, or shared analysis outputs. Look for authorization bypass in batch processing endpoints or administrative features exposed to LLM APIs.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566: Phishing - could use stolen images for social engineering
- T1526: Reconnaissance - enumerate other users' private images
- T1530: Data from Cloud Storage - access unprotected cloud-hosted images
- T1213: Data from Information Repositories - extract sensitive information from private images

## Notes
This vulnerability was discovered during Google's exclusive LLM bugSWAT event at DEFCON. The researcher team of Joseph 'rez0' Thacker, Justin 'Rhynorater' Gardner, and Roni 'Lupin' Carta collaborated effectively to identify the flaw. The vulnerability demonstrates that even mature companies like Google can overlook basic access control principles when rapidly deploying new AI features. The IDOR pattern remains one of the most common and impactful vulnerabilities in modern web applications, especially in emerging AI/ML services. Reproduction was straightforward, requiring only proxy interception and parameter manipulation, indicating the vulnerability was trivial to exploit at scale.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
