# IDOR Vulnerability in Google Bard Vision Feature Allowing Unauthorized Image Access

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** high
- **Vuln types:** Insecure Direct Object Reference (IDOR), Authorization Bypass, Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered an IDOR vulnerability in Google Bard's Vision feature that allowed attackers to access and describe images uploaded by other users without authorization. By intercepting and modifying the image path parameter in API requests, an attacker could retrieve arbitrary users' images. This vulnerability exposed sensitive user data and violated privacy controls in the image processing pipeline.

## Attack scenario (step by step)
1. User 1 uploads an image to Google Bard's Vision feature while intercepting traffic through a proxy
2. Attacker captures the POST request to StreamGenerate endpoint and extracts the image file path from the request body
3. Attacker creates a separate Bard session as User 2 and initiates an image upload request
4. Attacker intercepts User 2's StreamGenerate request and replaces the image path parameter with User 1's extracted path
5. Attacker forwards the modified request to Bard's API
6. The API processes the request and returns a description of User 1's image, despite User 2 having no authorization to access it

## Root cause
The application failed to validate that the authenticated user requesting image analysis actually owned or had permission to access the specified image resource. The API trusted the user-supplied image path parameter without server-side verification of ownership or access control lists.

## Attacker mindset
Methodical exploitation of inadequate authorization checks in AI service infrastructure. The attacker recognized that rapid AI feature deployment may prioritize functionality over security controls, and that image processing APIs commonly handle references (paths) that can be enumerated or manipulated if access controls are absent.

## Defensive takeaways
- Implement strict server-side authorization checks before processing any user-supplied resource identifiers
- Use indirect object references (session-based or random tokens) instead of predictable paths that users can enumerate
- Validate resource ownership on every API call, not just during initial upload
- Apply principle of least privilege: ensure vision/analysis features operate with minimal permissions
- Implement comprehensive audit logging for all image access and processing requests
- Conduct security reviews specifically for AI/LLM feature integrations before production deployment
- Use opaque identifiers that cannot be guessed or sequentially predicted

## Variant hunting
Similar IDOR patterns likely exist in other Google AI features handling user-generated content (documents, audio, video uploads). The vulnerability class affects any resource-based API where path/ID parameters control access to user data without proper authorization. Test other GenAI platforms' multimodal features for identical authorization bypass patterns.

## MITRE ATT&CK
- T1190
- T1566
- T1552
- T1040

## Notes
This vulnerability was discovered during Google's exclusive LLM bugSWAT event at DEFCON. The research team consisted of three collaborating security researchers (rez0, Rhynorater, Lupin). The event format allowed researchers direct access to Google security engineers for real-time clarification, accelerating vulnerability discovery. The vision feature was relatively new at the time of discovery, suggesting rushed deployment of AI capabilities without mature security practices. The vulnerability exemplifies how AI/LLM features introduced new attack surface areas that traditional web application security practices should have already covered.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
