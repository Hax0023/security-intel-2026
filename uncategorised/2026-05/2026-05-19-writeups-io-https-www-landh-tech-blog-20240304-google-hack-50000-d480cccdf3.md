# IDOR Vulnerability in Google Bard Vision Feature - Unauthorized Access to Other Users' Images

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** high
- **Vuln types:** Insecure Direct Object Reference (IDOR), Authorization Bypass, Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered an IDOR vulnerability in Google Bard's Vision feature that allowed authenticated users to access and describe images uploaded by other users without authorization. By modifying the file path parameter in API requests, attackers could retrieve and process arbitrary users' images through the vision analysis function, leading to unauthorized information disclosure.

## Attack scenario (step by step)
1. Attacker creates a Google Bard account and uploads a test image while intercepting the request with a proxy tool
2. Attacker extracts the file path from the POST request to StreamGenerate endpoint, which contains a predictable or enumerable path structure
3. Attacker obtains or predicts another user's image file path (e.g., through path enumeration or leaked information)
4. Attacker modifies the path parameter in their own image upload request to point to the target user's file
5. Attacker sends the crafted request, and the Bard Vision API processes the unauthorized image and returns its description
6. Attacker gains access to sensitive information contained in other users' images without any authorization checks

## Root cause
The Bard Vision feature failed to implement proper authorization checks on file path parameters in the StreamGenerate API endpoint. The backend accepted file paths as user-controllable input without validating that the requesting user owned or had permission to access the specified file resource. The application relied on obscurity of file paths rather than cryptographic validation or server-side ownership verification.

## Attacker mindset
Opportunistic vulnerability researcher recognizing that new AI features prioritize functionality over security fundamentals. The attacker understood that rapid development cycles and novel feature implementations often overlook basic authorization checks. By testing object reference manipulation—a well-known vulnerability class—against emerging AI infrastructure, the researcher identified a gap in Google's security review process for new LLM-powered features.

## Defensive takeaways
- Implement server-side authorization checks before processing any file operations, verifying user ownership of resources independent of request parameters
- Use cryptographically signed or opaque tokens instead of predictable/enumerable file paths in API requests
- Apply the principle of least privilege: users should only access resources they explicitly own, default-deny model
- Conduct threat modeling specifically for new AI/ML features, recognizing that rapid development may skip security fundamentals
- Implement comprehensive access control testing as part of security testing for all new features, especially those handling user-generated content
- Use structured testing for IDOR vulnerabilities: enumerate identifiers, test authorization boundaries, verify object ownership validation
- Log and monitor access patterns to detect unusual cross-user resource access attempts

## Variant hunting
Similar IDOR patterns likely exist in other Google AI services: Google Lens API, Document AI features, Cloud Vision API integrations with Bard, any file upload features in experimental AI tools. Test all endpoints accepting user-supplied identifiers/paths: replace IDs with other users' values, test predictable ID sequences, attempt path traversal combinations with file operations, fuzz identifier parameters in LLM-related APIs.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1589: Gather Victim Identity Information
- T1566: Phishing
- T1528: Steal Application Access Token

## Notes
This vulnerability was discovered during an exclusive in-person bug bounty event at DEFCON/Venetian Hotel in August 2023. The collaborative approach of three researchers (rez0, Rhynorater, Lupin) with direct access to Google security engineers on-site enabled rapid validation and remediation. The IDOR on a Vision feature demonstrates that AI-powered services introduced new attack surfaces while occasionally neglecting foundational access control principles. The $50,000 bounty reflects the high-risk nature of unauthorized image access combined with the emerging AI security domain.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
