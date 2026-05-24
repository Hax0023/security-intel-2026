# Broken Access Control Exposes Email Verification Status and Privacy Settings via API Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 3114132 | https://hackerone.com/reports/3114132
- **Submitted:** 2025-04-26
- **Reporter:** ctrl_cipher
- **Program:** WakaTime
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Broken Access Control, Information Disclosure, Improper Authorization, Account Enumeration
- **CVEs:** None
- **Category:** uncategorised

## Summary
The /api/v1/users/{username} endpoint fails to properly validate authorization, allowing any authenticated user to retrieve sensitive email-related metadata for arbitrary users including is_email_confirmed and is_email_public fields. This enables account enumeration and privacy violations by distinguishing verified accounts and inferring user privacy preferences.

## Attack scenario
1. Attacker authenticates to the application as a valid user
2. Attacker intercepts their own profile request to /api/v1/users/attacker_user and observes the response structure
3. Attacker systematically modifies the username parameter to iterate through common usernames or harvested username lists
4. For each request, attacker extracts is_email_confirmed boolean to identify active/verified accounts
5. Attacker cross-references is_email_public field to build profile of target users' privacy settings
6. Attacker uses enumerated verified accounts for targeted credential stuffing, phishing campaigns, or as inputs for chained vulnerabilities

## Root cause
The API endpoint implements object-level authorization checks that only verify the requester is authenticated, but fail to enforce ownership or role-based access controls. The endpoint returns sensitive metadata fields without verifying the authenticated user has permission to view that specific user's data.

## Attacker mindset
Reconnaissance-focused attacker seeking to identify high-value targets (verified accounts with confirmed emails) for downstream exploitation. The ability to enumerate valid accounts and infer privacy preferences reduces attack cost and increases targeting precision for credential attacks or social engineering.

## Defensive takeaways
- Implement object-level authorization checks: verify the authenticated user owns the requested resource or has explicit permission to view it
- Apply principle of least privilege: exclude sensitive fields (is_email_confirmed, is_email_public, email address variants) from responses when querying other users' profiles
- Implement field-level authorization: return different response schemas based on whether the requester is querying their own profile vs. another user's public profile
- Add rate limiting to user enumeration endpoints to slow systematic account enumeration attacks
- Log and alert on repeated access to different user profiles by the same authenticated session
- Conduct regular authorization testing across all API endpoints, especially those returning user metadata
- Consider removing email confirmation status from API responses entirely if it provides no business value to users querying other profiles

## Variant hunting
Check /api/v1/users endpoint (without username parameter) for batch user enumeration or list leaks
Test other user-facing API endpoints (/api/v1/users/{id}, /api/v1/profile, /api/v1/account) for similar authorization gaps
Review endpoints returning user lists (search, directory, teams/projects/organizations) for is_email_confirmed leakage
Test GraphQL APIs if present for user field authorization bypasses
Check if private fields leak in error messages or HTTP headers (e.g., X-User-Status)
Test whether unauthenticated requests return different responses than authenticated ones (partial information disclosure)
Hunt for similar patterns in related endpoints: /api/v1/users/{username}/settings, /api/v1/users/{username}/preferences
Verify if admin/elevated user endpoints return additional sensitive fields without proper authorization

## MITRE ATT&CK
- T1087
- T1590
- T1598
- T1110
- T1040

## Notes
This vulnerability is a textbook case of CWE-639 (Authorization Bypass Through User-Controlled Key). The is_email_public field is particularly revealing as it leaks privacy intent even when the actual email is hidden. The vulnerability is low-effort to exploit at scale and provides valuable reconnaissance for account targeting. Consider this a chain-enabler that significantly reduces the effort required for credential stuffing or phishing campaigns by pre-filtering verified accounts.

## Full report
<details><summary>Expand</summary>

The /api/v1/users/{username} endpoint leaks sensitive email-related metadata (e.g., is_email_confirmed, is_email_public) without proper authorization checks. Attackers can abuse this to:
Identify verified/active accounts for targeted attacks.
Determine users’ email privacy preferences (even if the email itself is hidden).
This behavior allows me to distinguish whether an account's email address is confirmed or not.

#Steps to Reproduce
1. Authenticate as a valid user (e.g. user/current).
2. Intercept a request to your own profile:
>GET /api/v1/users/attacker_user HTTP/2  
Host: wakatime.com  
Cookie: 
3. Modify the username in the URL to access another user’s data:
>GET /api/v1/users/<any name> HTTP/2  
Host: wakatime.com  
Cookie: 
4. Observe the response:
>{
  "is_email_confirmed": true,
  "is_email_public": false,
  "public_email": null,
  // ... other sensitive fields
}

## Impact

Account Enumeration:
Attackers can confirm valid/verified accounts (is_email_confirmed: true), enabling targeted credential stuffing or phishing.

Privacy Violations:
Knowing a user’s email privacy preference (is_email_public: false) leaks their intent to keep their email private.

Attack Surface Expansion:
Combined with other vulnerabilities (e.g., password reset flaws), attackers can prioritize high-value accounts.

</details>

---
*Analysed by Claude on 2026-05-24*
