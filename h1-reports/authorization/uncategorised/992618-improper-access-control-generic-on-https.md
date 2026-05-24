# Improper Access Control - Unauthorized Ticket Access and Deletion

## Metadata
- **Source:** HackerOne
- **Report:** 992618 | https://hackerone.com/reports/992618
- **Submitted:** 2020-09-28
- **Reporter:** fiveguyslover
- **Program:** Unknown - Subdomain Redacted
- **Bounty:** Not Specified
- **Severity:** High
- **Vuln:** Improper Access Control, Missing Authentication, Broken Access Control, Insufficient Authorization Checks
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated attacker can access sensitive ticket information on a subdomain without proper authorization checks. Additionally, the application allows deletion of tickets using HTTP DELETE requests without verifying user permissions, enabling unauthorized modification of ticket data.

## Attack scenario
1. Attacker discovers the vulnerable subdomain during reconnaissance or through directory enumeration
2. Attacker accesses /latest endpoint without authentication to view current ticket information
3. Attacker accesses /all endpoint to enumerate all tickets across the system
4. Attacker observes sensitive ticket details including progress, status, and metadata
5. Attacker crafts DELETE HTTP requests targeting specific ticket identifiers
6. Attacker successfully deletes tickets, causing data loss and disrupting operations

## Root cause
The application implements insufficient access control mechanisms on ticket endpoints. The API likely fails to validate user authentication/authorization before returning sensitive data or processing destructive operations, relying instead on security-by-obscurity or missing authentication middleware entirely.

## Attacker mindset
An opportunistic attacker seeking to explore application boundaries, likely discovering this through manual endpoint testing or API enumeration. The attacker prioritizes transparency by reporting the vulnerability rather than exploiting it maliciously.

## Defensive takeaways
- Implement mandatory authentication checks on all endpoints returning sensitive data
- Enforce role-based access control (RBAC) to restrict ticket visibility to authorized users
- Require explicit authorization verification before processing destructive operations (DELETE, PUT, PATCH)
- Apply principle of least privilege - default deny for unauthenticated requests
- Implement audit logging for all ticket access and modifications
- Use consistent authentication middleware across all API endpoints
- Validate HTTP methods and implement proper CORS/CSRF protections
- Conduct regular access control testing and security code reviews

## Variant hunting
Check other CRUD endpoints (/edit, /update, /create) for similar authorization bypasses
Test other resource types (users, reports, settings) on the same subdomain
Enumerate related subdomains for similar access control weaknesses
Test whether direct object reference (IDOR) allows access to other users' tickets
Verify if HTTP methods override (X-HTTP-Method-Override headers) bypass controls
Check for authentication bypass through cookie manipulation or header spoofing

## MITRE ATT&CK
- T1190
- T1589
- T1592
- T1110
- T1562

## Notes
The vulnerability demonstrates classic broken access control patterns. The inclusion of multiple endpoints (/latest, /all) and the explicit mention of DELETE capability suggests this was discovered through systematic API endpoint testing. The report lacks technical depth (no HTTP responses, headers, or timestamps) but clearly communicates impact. This is a textbook case of inadequate authorization checking commonly found in hastily developed internal tools or poorly maintained legacy systems.

## Full report
<details><summary>Expand</summary>

Greetings, I found on one of your sub-domains some tickets that are not supposed to be readable by everyone, we even have the possibility to delete the tickets.
Link : 
https://███/█████/latest
https://█████/███████/all
https://█████/███████ (DELETE HEADER METHOD)

Best regards,
frenchvlad

## Impact

a malicious person can delete tickets and see the progress of tickets in progress

</details>

---
*Analysed by Claude on 2026-05-24*
