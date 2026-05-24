# inDriver Job - Admin Approval Bypass via Direct Status Modification

## Metadata
- **Source:** HackerOne
- **Report:** 1861487 | https://hackerone.com/reports/1861487
- **Submitted:** 2023-02-03
- **Reporter:** mikejohnson_1
- **Program:** inDriver
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Insufficient Input Validation, Improper Authorization Check
- **CVEs:** None
- **Category:** uncategorised

## Summary
The inDriver Job application allows attackers to bypass the mandatory admin approval process for job postings by directly modifying the vacancy status from 'MODERATION' to 'ACTIVE' in a GraphQL API request. This enables unauthorized publication of arbitrary content including scams, malware advertisements, and spam, potentially rendering the platform unusable for legitimate users.

## Attack scenario
1. Attacker registers as an employer on the platform
2. Attacker creates a malicious or scam job posting with all required fields filled
3. System automatically sets the posting status to 'MODERATION' requiring admin approval
4. Attacker intercepts the UpdateVacancyStatus GraphQL POST request using proxy tools
5. Attacker modifies the 'status' variable from 'MODERATION' to 'ACTIVE' and resends the request
6. Malicious job posting is immediately published and visible to all platform users, bypassing all moderation controls

## Root cause
The backend GraphQL endpoint UpdateVacancyStatus fails to validate user authorization before accepting status change requests. The server trusts client-supplied status values without verifying that the requester has appropriate permissions or that the status transition is legitimate. No server-side enforcement of the moderation workflow exists.

## Attacker mindset
An attacker with basic HTTP interception knowledge can exploit this vulnerability with minimal effort. The attack requires only intercepting a single request and changing one parameter value, making it easily discoverable and exploitable by opportunistic threat actors seeking to distribute scams, malware, or spam at scale.

## Defensive takeaways
- Implement strict authorization checks on all GraphQL mutations, verifying user role and permissions before allowing any status modifications
- Define and enforce a state machine on the server for vacancy status transitions, only allowing transitions from specific states to others (e.g., only admins can change MODERATION to ACTIVE)
- Never trust client-supplied data; all business logic decisions must be validated server-side
- Implement comprehensive audit logging for all critical operations, particularly status changes that affect content visibility
- Apply principle of least privilege: users should only be able to modify vacancies they own, and only to specific intermediate states
- Use role-based access control (RBAC) with explicit permission checks for sensitive operations
- Conduct security testing of GraphQL APIs specifically targeting authorization bypass scenarios

## Variant hunting
Look for similar patterns in other inDriver services or related job board platforms: (1) Check if other GraphQL mutations bypass authorization checks (e.g., UpdateUserRole, ApproveContent, PublishListing), (2) Search for other resources with mandatory approval workflows that can be bypassed via direct status manipulation, (3) Test if users can modify other users' vacancies or resources by ID, (4) Check if the vulnerability extends to other entity types requiring moderation (profiles, profile pictures, reviews), (5) Investigate whether the GraphQL API enforces rate limiting or request validation.

## MITRE ATT&CK
- T1190
- T1586
- T1566

## Notes
This is a classic authorization bypass vulnerability with severe business impact. The vulnerability is trivially exploitable and would have been caught by basic authorization testing. The attacker provided session cookies for reproduction, indicating good faith disclosure. The attack has dual impact: both enabling malicious content distribution and enabling denial of service through flooding. The report lacks specific bounty information, suggesting it may still be under review or resolution.

## Full report
<details><summary>Expand</summary>

## Summary:
A vulnerability has been found in "inDriver Job", an application located at https://injob.indriver.com/, a platform that allows employers to **publish job offers** and candidates to sign up for them. It seems like the application has **heavy use**, with a plethora of job offers in many categories.

In the app, anyone can request to **create job offers**, but, to prevent spam, scamming and phishing, every job offer creation and edit **has to be approved by a site admin** before being published. This is essential, since it prevents the app from getting **flooded with scammers**.

The vulnerability discovered allows an attacker to **completely bypass** this approval step, allowing the publishing of arbitrary content.

## Technical Details:
On the last step of the job offer creation, the application makes a final `POST` request to `/api/graphql`, calling for `UpdateVacancyStatus`.

```
{"operationName":"UpdateVacancyStatus","variables":{"vacancyId":"█████","status":"MODERATION"}
...
```
Re-sending this request, but modifying the **"status" variable to "ACTIVE"**, bypasses the need for a moderator approval, **publishing the ad**.

## Video POC
██████████

## Steps To Reproduce:
*Note for Triager: A phone number is required for signup. To skip this step, I've attached my session cookies. Using these, you could reproduce the steps noted below.*

(Please see video for in-depth demo)
  1. In employer mode, create a new job offer
  2. Fill in the required fields
  3. After the creation, the offer will appear as "Pending Approval"
  4. In Burp Proxy, send the last "UpdateVacancyStatus" request to Repeater, modifying "status":"ACTIVE"
  5. The arbitrary ad will now show up as "Active", it will have been verified and published. All users will be able to see it.

## Impact

An attacker can use this vulnerability to upload arbitrary content, for **scamming**, **malware** or even **advertising** purposes.
It is also possible to **flood the platform** with infinite offers, making it unusable for legitimate users.

</details>

---
*Analysed by Claude on 2026-05-24*
