# Unauthorized Access to Offline Publication Cover Pages via SOURCE_DOCUMENT_ID

## Metadata
- **Source:** HackerOne
- **Report:** 2357113 | https://hackerone.com/reports/2357113
- **Submitted:** 2024-02-06
- **Reporter:** giwadaoud
- **Program:** Undisclosed (██████████)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Broken Access Control, Information Disclosure, Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
A vulnerable endpoint discloses cover page URLs for offline publications when provided a sourceDocumentId parameter, bypassing intended access restrictions. The returned URLs contain sensitive identifiers (user ID and main publication ID) and allow unauthorized viewing of offline publication cover pages that should only be accessible to account owners.

## Attack scenario
1. Attacker creates an account on the vulnerable platform
2. Attacker identifies or obtains a valid sourceDocumentId from any offline publication
3. Attacker crafts a request to the vulnerable endpoint with the sourceDocumentId parameter
4. Vulnerable endpoint processes request without proper authorization checks and returns cover page URL
5. Attacker extracts user ID and publication main ID from the returned URL
6. Attacker accesses the cover page URL to view sensitive content from offline publications they do not own

## Root cause
Missing authorization validation on the endpoint that generates cover page URLs. The system validates that a sourceDocumentId exists but fails to verify that the requesting user has legitimate access to view that publication before returning the URL. The endpoint treats all valid sourceDocumentIds equally regardless of publication visibility status (offline vs online) or ownership.

## Attacker mindset
An attacker recognizes that APIs often leak object identifiers and that endpoints generating resource URLs may not properly check authorization. By enumerating or discovering sourceDocumentIds (through various means), they can systematically extract cover pages from offline publications. The disclosure of user IDs and publication IDs in URLs provides additional reconnaissance data for account enumeration or targeted attacks.

## Defensive takeaways
- Implement proper authorization checks before returning any resource URLs, verifying the requester owns or has explicit access to the resource
- Separate authorization logic for listing resources from authorization logic for accessing resources - do not assume valid object IDs mean the user should access them
- Treat offline/unpublished content with the same strict access controls as highly sensitive data
- Avoid including sensitive identifiers (user IDs, internal publication IDs) in URLs when possible; use opaque tokens or implement proper access controls
- Apply consistent access control validation across all endpoints that return resource URLs, not just direct resource requests
- Implement rate limiting and logging on endpoints that generate URLs to offline resources to detect enumeration attempts
- Conduct security testing specifically for IDOR vulnerabilities on all endpoints that reference objects by ID

## Variant hunting
Check other document/publication-related endpoints (thumbnails, previews, metadata) for similar authorization bypasses
Test with different object ID parameters (mainId, userId) to see if they bypass authorization individually
Attempt to access cover pages of deleted, archived, or private publications using the same endpoint
Try accessing draft or revision versions of publications through sourceDocumentId parameter
Check if batch requests with multiple sourceDocumentIds reveal cover pages the user shouldn't access
Test if modifying sourceDocumentId slightly (incrementing, fuzzing) allows accessing related publications
Investigate whether the cover page URL itself contains exploitable parameters or further IDOR vulnerabilities

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1526: Reconnaissance (Resource Discovery through ID enumeration)
- T1040: Traffic Interception (analyzing response URLs)
- T1087: Account Discovery (user ID enumeration from URLs)

## Notes
This is a classic IDOR vulnerability combined with broken access control. The vulnerability is particularly concerning because it affects offline/unpublished content, suggesting users explicitly intended this content to be private. The disclosure of internal IDs (user ID, publication ID) in the response URL amplifies the impact by enabling further reconnaissance. The fix requires authorization checks at the endpoint level, not relying on the resource URL generation mechanism to enforce access control.

## Full report
<details><summary>Expand</summary>

I discovered a vulnerability that is related to accessing publication cover pages via a specific request using **sourceDocumentId**. When sending a request with the **source ID**, the system responds with a URL to the cover page of that publication. However,  the cover page is intended to be offline and not publicly accessible and the offline publication are only accessible by the account users. Beside that in the URL there is also the user id and the main id corresponding to that publication. So, due to a vulnerable endpoint we are able to disclose the cover page of an offline publication that we don't own.

{F3033179}

Vulnerable endpoint: ██████████

* Steps to Reproduce: 
1. Create account on ██████.
2. Create a new offline publication and take the **sourceDocumentId** of it.
3. Send a request to the program's endpoint with a valid **SOURCE_ID** corresponding to a specific publication.
4. Analyze the response to retrieve the URL of the publication's cover page.
5. Access the URL provided in the response, which contains both the user ID and the main ID of the publication.

## Impact

This vulnerability allows unauthorized access to offline publication cover pages, which may contain sensitive information not intended for public viewing. An attacker could potentially view confidential content from the cover pages of unpublished publications.

</details>

---
*Analysed by Claude on 2026-05-24*
