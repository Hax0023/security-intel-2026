# IDOR and DoS Vulnerabilities in Google's Bard/Gemini AI During LLM bugSWAT Event

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Google Bug Bounty - LLM bugSWAT Event
- **Bounty:** $50,000
- **Severity:** HIGH
- **Vuln types:** Insecure Direct Object Reference (IDOR), Unauthorized Access, Path Traversal, Denial of Service
- **Category:** uncategorised
- **Writeup:** https://www.landh.tech/blog/20240304-google-hack-50000/

## Summary
Researchers discovered an IDOR vulnerability in Google's Bard Vision feature that allowed unauthorized access to other users' uploaded images by manipulating file paths in API requests. The vulnerability enabled attackers to describe and access arbitrary images without permission, bypassing all authorization checks in the image processing pipeline.

## Attack scenario (step by step)
1. Attacker creates account (User 1) and uploads an image to Bard's Vision feature while intercepting traffic
2. Attacker captures the StreamGenerate API request and extracts the image file path from the request body
3. Attacker creates second account (User 2) and initiates image upload with Vision feature
4. Attacker intercepts User 2's StreamGenerate request and modifies the image path parameter to reference User 1's file path
5. Attacker sends modified request to Bard's backend service
6. Backend processes the request without validating file ownership, returning description of User 1's image while authenticated as User 2

## Root cause
The Vision feature's backend API (assistant.lamda.BardFrontendService/StreamGenerate) failed to implement proper authorization checks on image file access. The API accepted user-controlled file paths without verifying that the authenticated user had permission to access the specified image resource. File paths were predictable and based on timestamps and sequential identifiers, making enumeration trivial.

## Attacker mindset
Researchers approached this as a systematic authorization testing exercise, recognizing that new AI features often lack mature security controls. They leveraged request interception to understand the API contract, identified that file paths were user-controllable and unvalidated, and realized the path format was guessable. The collaborative approach allowed cross-validation of assumptions and rapid iteration on exploitation techniques.

## Defensive takeaways
- Implement server-side authorization checks on all resource access, verifying authenticated user ownership before processing file requests
- Use opaque, non-sequential identifiers for sensitive resources (UUIDs) instead of predictable timestamp-based paths
- Never trust user-supplied file paths or identifiers in API requests without validation against a user-resource mapping
- Apply the principle of least privilege - image processing should run under service accounts with minimal required permissions
- Implement access control at multiple layers: API gateway, application logic, and storage backend
- Add comprehensive logging and monitoring for cross-user resource access attempts
- Conduct security reviews specifically for newly released features before production deployment
- Establish threat modeling for AI/ML features that processes user-generated content

## Variant hunting
Similar IDOR patterns likely exist in other Google AI features processing user content (Gemini file upload, Google Photos integration, document processing). Look for predictable resource identifiers in: image generation history, conversation logs, model fine-tuning datasets, and any multi-tenant features. Test authorization on derived resources (thumbnails, cached versions, embeddings). Check for time-based path generation patterns across Google's ML services.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1526 - Reconnaissance for Vulnerability Research
- T1548 - Abuse Elevation Control Mechanism

## Notes
This writeup is incomplete (cuts off mid-reproduction steps). The $50,000 bounty suggests HIGH severity classification. The vulnerability was discovered during an official Google-sanctioned bug bounty event with direct access to security engineers, allowing real-time validation of findings. The collaborative three-person approach (rez0, Rhynorater, Lupin) demonstrates how diverse expertise accelerates vulnerability discovery. The vulnerability highlights the maturity gap in AI product security compared to traditional web services.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
