# IDOR - Delete All Licenses and Certifications from Users Account via CreateOrUpdateHackerCertification GraphQL Query

## Metadata
- **Source:** HackerOne
- **Report:** 2122671 | https://hackerone.com/reports/2122671
- **Submitted:** 2023-08-24
- **Reporter:** harshdranjan
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Missing Authorization Check
- **CVEs:** None
- **Category:** web-api

## Summary
The CreateOrUpdateHackerCertification GraphQL mutation fails to validate authorization before modifying or deleting certification records. An authenticated attacker can modify the ID parameter in the GraphQL query to delete licenses and certifications belonging to other users. This allows complete destruction of any user's professional credentials on the platform.

## Attack scenario
1. Attacker authenticates to their own HackerOne account
2. Attacker creates or edits a license/certification and intercepts the GraphQL CreateOrUpdateHackerCertification mutation request
3. Attacker modifies the certification ID parameter to target a victim user's certification ID
4. Attacker submits the modified request with the victim's certification ID
5. Server processes the request without verifying the attacker owns the targeted certification
6. Victim's license or certification is deleted from their profile

## Root cause
The GraphQL mutation endpoint performs object operations based on user-supplied ID parameters without validating that the requesting user is the legitimate owner of the resource. The application trusts the client-side ID value and fails to cross-reference ownership before executing delete operations.

## Attacker mindset
An authenticated attacker seeks to cause denial of service or reputation damage by systematically deleting professional credentials from competitors or targets. The IDOR vulnerability allows enumeration of valid certification IDs and mass deletion with minimal effort.

## Defensive takeaways
- Implement ownership verification on all mutation operations - verify the requesting user's ID matches the resource owner before processing
- Use UUID or other non-sequential identifiers instead of numeric IDs to prevent easy enumeration
- Apply consistent authorization checks at the resolver level for all GraphQL mutations, not just queries
- Implement resource-based access control that validates ownership for every mutation operation
- Add audit logging for all certification modifications and deletions
- Implement rate limiting on mutation operations to prevent bulk deletions
- Use field-level permissions in GraphQL schema to restrict mutation inputs
- Conduct security review of all GraphQL mutations for similar authorization bypasses

## Variant hunting
Check UpdateUserProfile, UpdateHackerProfile, and similar mutation endpoints for identical IDOR patterns
Test other certification/credential mutations (Delete, Archive operations) for authorization bypasses
Examine mutations that accept user/hacker IDs as parameters for owner verification
Audit mutations that perform soft or hard deletes for missing authorization checks
Review skill endorsements, education records, and other user profile mutations for similar flaws
Test bulk operations and batch mutations that may have authorization gaps

## MITRE ATT&CK
- T1190
- T1566
- T1199

## Notes
This is a classic IDOR vulnerability in GraphQL context. The sequential numeric ID format enables easy exploitation and enumeration. The vulnerability affects core profile data, making it high impact for user reputation and professional standing on the platform. The attack requires only authentication to succeed, making it easily exploitable by any registered user.

## Full report
<details><summary>Expand</summary>

**Summary:**
Hey team,

While editing our **Licenses and certifications** if we change the ID number we can delete other users **Licenses and certifications**. it simply can be done by editing the ID number in our graphql query.
If change the ID from 1 to X possible range then we can delete all the **Licenses and certifications** present between these.


### Steps To Reproduce

1. Log in to your own account in two browsers A and B with User A and User B
2. Create your own **Licenses and certifications* in both the account
3. Now edit your own **Licenses and certifications* and Intercept this using a Burp Proxy 
4. Now In the body change the **ID** number and you will be able to delete all the **Licenses and certifications** present in HackerOne 
5. For now change the ID to the **Licenses and certifications** ID of the Other account and it will be deleted.

PoC Video: ████

## Impact

Able to delete all the **Licenses and certifications** present in HackerOne

</details>

---
*Analysed by Claude on 2026-05-11*
