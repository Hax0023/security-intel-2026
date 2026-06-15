# IDOR Vulnerability in Google Bard Vision Feature - Unauthorized Access to Other Users' Images

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** High
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Insufficient Authorization Verification
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered an IDOR vulnerability in Google Bard's Vision feature that allowed attackers to access and describe images belonging to other users without authorization. By manipulating the file path parameter in API requests, an authenticated user could retrieve and process arbitrary other users' uploaded images, leading to unauthorized access to private user content.

## Attack scenario (step by step)
1. Attacker (User A) authenticates to Google Bard and uploads an image while intercepting traffic via HTTP proxy
2. Attacker identifies the POST request to StreamGenerate endpoint and extracts the file path from the response body (format: /contrib_service/ttl_1d/[timestamp][random_string])
3. Attacker authenticates as User B and initiates a legitimate image upload request, intercepting it with the proxy
4. Attacker modifies the file path parameter in User B's StreamGenerate request to point to User A's previously extracted image path
5. Attacker sends the modified request to the Bard backend, which processes the request without verifying ownership or access rights
6. Bard's Vision function describes User A's image, granting User B unauthorized access to another user's private content

## Root cause
The Vision feature endpoint failed to implement proper authorization checks before processing image files. The application relied solely on the file path/object reference as a unique identifier without verifying that the requesting user owns or has permission to access that specific resource. Direct object references were exposed in API responses without sufficient access control validation.

## Attacker mindset
Opportunistic and methodical - researchers systematically tested authorization boundaries by examining request/response patterns during normal usage, then attempted path parameter manipulation. The collaborative approach of three experienced bug bounty hunters allowed for rapid hypothesis testing and idea validation, demonstrating how specialized knowledge in API security and web proxying can uncover authorization flaws quickly.

## Defensive takeaways
- Implement server-side authorization checks on every resource access, not just at the UI layer - verify the authenticated user owns the resource before processing
- Use indirect references (e.g., database IDs mapped to user accounts) instead of exposing direct file paths in API responses
- Apply the principle of least privilege - ensure each API endpoint validates user permissions against the specific resource being accessed
- Conduct comprehensive access control testing across all new AI features, especially those handling user-generated content
- For LLM/AI features, ensure authorization checks occur before any content is processed by the model to prevent information disclosure
- Implement consistent authorization patterns across all API endpoints to reduce variation and missed checks
- Log and monitor suspicious patterns of file access requests that deviate from normal usage (multiple different file paths from single user)
- Conduct security reviews specifically focused on object reference exposure in API design before feature release

## Variant hunting
['Test for IDOR in other vision/image processing features by manipulating file path parameters', 'Examine other Bard features that accept file uploads (documents, videos, audio) for similar authorization flaws', "Check if the same file path format is used elsewhere in Google's AI products, potentially allowing cross-feature exploitation", 'Test permission escalation through path manipulation - can users access admin or premium content?', "Investigate whether file paths can be enumerated or brute-forced to discover other users' content systematically", "Check if timestamps in file paths are predictable, enabling easier discovery of other users' files", 'Test for race conditions between file upload, path assignment, and authorization enforcement', "Examine other AI-powered services (Google's Cloud AI, Vertex AI) for similar authorization weaknesses in model input handling"]

## MITRE ATT&CK
- T1190
- T1566
- T1530
- T1526
- T1518

## Notes
This vulnerability was discovered during an exclusive, in-person bug bounty event at DEFCON/Venetian Hotel in August 2023, demonstrating the value of direct collaboration between researchers and security teams. The IDOR affected a cutting-edge AI feature (Bard Vision), highlighting that new technologies often inherit authorization weaknesses from foundational design flaws. The fact that this was found in a mature Google product underscores that even well-resourced companies can overlook basic access control principles when rushing to market with new AI capabilities. The $50,000 bounty reflects the severity and potential impact of unauthorized access to private user content processed by AI systems.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
