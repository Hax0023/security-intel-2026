# IDOR and GraphQL DoS Vulnerabilities in Google Bard/Gemini AI

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** High
- **Vuln types:** Insecure Direct Object Reference (IDOR), Improper Access Control, Denial of Service (DoS), GraphQL Query Manipulation
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered an IDOR vulnerability in Google Bard's Vision feature that allowed attackers to access and describe other users' images without authorization by manipulating file paths in API requests. The attack exploited weak access controls in the image processing pipeline, enabling unauthorized access to private user-uploaded content.

## Attack scenario (step by step)
1. Attacker creates two accounts for Google Bard/Gemini
2. As User 1, attacker uploads an image and intercepts the POST request to StreamGenerate endpoint using an HTTP proxy
3. Attacker extracts the file path from the request body (format: /contrib_service/ttl_1d/[timestamp][random_string])
4. As User 2, attacker uploads a different image and captures the corresponding request
5. Attacker modifies the file path parameter in User 2's request to reference User 1's file path
6. Attacker resends the manipulated request, gaining access to User 1's image description without authorization

## Root cause
The Vision feature in Bard/Gemini failed to implement proper authorization checks when processing image file paths. The API accepted user-controlled file path parameters without verifying that the requesting user owned or had permission to access the referenced image resource.

## Attacker mindset
Security researchers systematically probed the AI service's file handling mechanisms by intercepting API communications and testing whether access controls were enforced on object references. They recognized that file path manipulation is a classic IDOR attack vector and applied it to newly-released AI features that likely received less security scrutiny than core products.

## Defensive takeaways
- Implement strict authorization checks before serving any user-generated content, verifying ownership and permissions on every access
- Use opaque, non-sequential, cryptographically random identifiers instead of predictable file paths that can be enumerated or guessed
- Avoid exposing internal file paths to client-side requests; instead use database lookups with proper ownership validation
- Apply consistent security testing to AI features with the same rigor as traditional services, as they introduce new interaction paradigms
- Implement comprehensive access control lists (ACLs) at the file service layer, not just at application level
- Log and monitor all file access attempts for anomalies indicating IDOR exploitation

## Variant hunting
Similar IDOR patterns likely exist in other Google AI features: Google's Document AI service (form processing), Gemini's document upload feature, any file-processing endpoints in Google Cloud AI services, and vision-capable features in Google Assistant or Workspace AI integrations. Test for sequential IDs, timestamp-based identifiers, and user ID manipulation across all AI product file operations.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1199 - Trusted Relationship
- T1526 - Reconnaissance

## Notes
The writeup indicates this was part of an exclusive in-person hacking event at DEFCON/Venetian Hotel in August 2023, suggesting Google's early recognition of LLM security risks. The collab between rez0, Rhynorater, and Lupin demonstrates value of team-based vulnerability research. The $50,000 bounty reflects both the IDOR severity and the exclusivity of the event. The vulnerability affected Bard's Vision feature specifically, which was a newly released capability at the time, highlighting that novel AI features often ship with baseline security implementation. The researcher noted they planned to discuss a GraphQL DoS variant but the writeup appears truncated.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
