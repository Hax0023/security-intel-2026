# IDOR Vulnerability in Google Bard Vision Feature - Unauthorized Access to Other Users' Images

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** High
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Insufficient Authorization Verification
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered a critical IDOR vulnerability in Google Bard's Vision feature that allowed attackers to describe and access images belonging to other users without authorization. By manipulating the image path parameter in API requests, an authenticated user could retrieve and process arbitrary images from other users' accounts. This vulnerability exposed sensitive user data and violated fundamental access control principles.

## Attack scenario (step by step)
1. Attacker (User A) authenticates to Google Bard and uploads an image while monitoring network traffic
2. Attacker captures the POST request to StreamGenerate endpoint and extracts the image path/resource ID from the request body
3. Attacker creates a second account (User B) or uses a different authenticated session
4. Attacker uploads a different image as User B and intercepts the corresponding StreamGenerate request
5. Attacker modifies the image path parameter in User B's request to reference User A's image path
6. Attacker sends the modified request and successfully retrieves descriptions of User A's image, confirming unauthorized access

## Root cause
The Vision feature implementation failed to properly validate that the requesting user has authorization to access the specified image resource. The server accepted user-controlled image path parameters without verifying ownership or permissions, relying on path obfuscation rather than proper access control checks.

## Attacker mindset
An attacker would recognize that image processing features typically assign unique identifiers to uploaded resources. By observing the API request structure, they would hypothesize that predictable or discoverable paths could be manipulated to access other users' data. The mailbox analogy suggests they would test whether the application enforces compartmentalization between user contexts.

## Defensive takeaways
- Implement proper authorization checks on all API endpoints - verify user ownership of resources before processing
- Use server-side session context to determine accessible resources rather than relying on user-supplied identifiers
- Generate unpredictable resource IDs using cryptographically secure random values instead of sequential or time-based identifiers
- Enforce principle of least privilege - only expose resources the authenticated user owns or has explicit permission to access
- Conduct security reviews specifically for new AI/ML features, as teams may overlook traditional security controls when focused on feature functionality
- Implement comprehensive logging and monitoring to detect access patterns that suggest IDOR exploitation
- Test access control across all permission boundaries in bug bounty programs before public release

## Variant hunting
Similar IDOR vulnerabilities likely exist in other AI-powered features at Google or competitors: Gemini's file handling, document processing features, email attachments in Gmail's AI summaries, Drive's AI preview functionality, and any user-generated content processing endpoints. Researchers should focus on features that process user-supplied data and return processed results, testing whether resource IDs can be enumerated or manipulated across user sessions.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (malicious input via API)
- T1199 - Trusted Relationship (exploiting feature trust model)
- T1526 - Reconnaissance (enumeration of resource paths)
- T1555 - Credentials from Password Stores (potential exposure of sensitive image content)
- T1020 - Automated Exfiltration (systematic access to other users' data)

## Notes
This writeup documents a collaborative bug hunting effort at Google's official LLM bugSWAT event at DEFCON. The vulnerability represents a fundamental access control failure in a high-profile Google product (Bard/Gemini). The $50,000 bounty reflects the severity and potential impact on millions of users. The researchers' approach of collaboration and brainstorming, combined with direct access to Google engineers for clarification, exemplifies effective bug bounty methodology. The vulnerability demonstrates that AI/ML features, despite their sophistication, require the same rigorous security fundamentals as traditional applications.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
