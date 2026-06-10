# IDOR Vulnerability in Google Bard Vision Feature - Access to Other Users' Images

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Google LLM bugSWAT Bug Bounty Event
- **Bounty:** $50,000
- **Severity:** High
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Unauthorized Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered an IDOR vulnerability in Google Bard's Vision feature that allowed attackers to access and describe arbitrary images belonging to other users without authorization. By manipulating file path parameters in the StreamGenerate API request, an attacker could substitute another user's image identifier and retrieve descriptions of private images. This vulnerability exposed sensitive user data through the LLM's image analysis capabilities.

## Attack scenario (step by step)
1. Attacker authenticates to Google Bard as User A and uploads a test image while intercepting network traffic
2. Attacker identifies the POST request to BardFrontendService/StreamGenerate endpoint and extracts the image storage path from the request body
3. Attacker obtains or enumerates image identifiers belonging to User B through various means (timing attacks, brute force, social engineering)
4. Attacker modifies the image path parameter in their own request to reference User B's image identifier instead of their own
5. Attacker sends the modified request to the backend, which processes it without verifying ownership of the referenced image
6. The LLM Vision feature generates a detailed description of User B's private image, exposing sensitive information to the unauthorized attacker

## Root cause
The Bard Vision feature failed to implement proper authorization checks on image resource access. The backend accepted image file paths in user-controlled request parameters without verifying that the authenticated user had legitimate access to the specific image resource. The application relied on path obscurity rather than access control validation.

## Attacker mindset
Security researchers systematically tested parameter manipulation across the LLM platform's API endpoints. Upon discovering the IDOR vector, they recognized the severity: while image paths appeared randomized, the lack of server-side authorization validation meant any authenticated user could construct valid requests for arbitrary images, treating image identifiers as enumerable resources.

## Defensive takeaways
- Implement server-side authorization checks on all resource access requests, verifying user ownership or explicit permissions before returning data
- Use indirect object references (tokens/UUIDs that map to resources server-side) instead of exposing direct file paths in API responses
- Enforce principle of least privilege: image processing APIs should only accept pre-authenticated, user-specific resource identifiers
- Add comprehensive access logging and audit trails for all AI model processing requests, especially those involving user-generated content
- Conduct security reviews specifically for new AI/LLM features, as they often bypass traditional security patterns by processing arbitrary user inputs
- Implement rate limiting and anomaly detection on vision API endpoints to detect abuse patterns like rapid enumeration attempts
- Validate that LLM input sanitization doesn't bypass authentication checks - process only authorized content

## Variant hunting
Hunt for similar IDOR vulnerabilities in other Google AI features: Google's text generation endpoints, document processing APIs, and Gemini's file handling. Test parameter manipulation in batch processing requests, API exports, and audit log exports. Examine whether other cloud services with AI integration (Vertex AI, Cloud Storage integration with ML) properly validate resource ownership before processing.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate External Targets
- T1110 - Brute Force
- T1087 - Account Discovery
- T1526 - Scan for Accessibility and Discovery

## Notes
This vulnerability was discovered during Google's exclusive LLM bugSWAT event at DEFCON, demonstrating the early-stage security maturity of AI features. The research team of three collaborated during an in-person hacking session where they had direct access to Google security engineers for clarification. The $50,000 bounty reflects both the severity and the novelty of AI-specific vulnerabilities. The analog explanation (mailbox receiving neighbors' mail) effectively communicates IDOR risk to non-technical stakeholders. This finding exemplifies how traditional web security vulnerabilities remain highly relevant in AI systems, and basic access control principles are often overlooked in new technology rollouts.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
