# Support Incident Creation and PII Exposure via Unrestricted Access Control

## Metadata
- **Source:** HackerOne
- **Report:** 869450 | https://hackerone.com/reports/869450
- **Submitted:** 2020-05-09
- **Reporter:** z32
- **Program:** Air University (inferred from content)
- **Bounty:** Not specified in provided content
- **Severity:** High
- **Vuln:** Broken Access Control, Insufficient Authorization, Information Disclosure, Social Engineering Vector
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated or low-privileged user can create support incidents on behalf of any other user and monitor their responses. The vulnerability also exposes personally identifiable information (PII) through an informational button adjacent to the caller field, enabling social engineering attacks and phishing campaigns.

## Attack scenario
1. Attacker creates account on the support platform and navigates to the incident creation page
2. Attacker selects arbitrary victim user from the assignee dropdown field without authorization checks
3. Attacker crafts phishing message in incident comments and optionally attaches malicious files
4. Attacker views victim PII via the information button (name, email, contact details) to enhance social engineering credibility
5. Victim receives email notification of incident assignment and logs in to respond
6. Attacker monitors incident activity, reads victim responses, and can impersonate administrator to solicit sensitive information

## Root cause
The incident creation endpoint lacks proper authorization validation to verify the authenticated user has permission to create incidents for other users. The PII disclosure endpoint similarly fails to enforce access controls, allowing unauthenticated access to user information through information lookup functions.

## Attacker mindset
An attacker would exploit this to conduct targeted phishing campaigns against employees, impersonating trusted administrative contacts. By leveraging legitimate platform infrastructure and real user data, the attack appears authentic, increasing success rates for credential harvesting or malware distribution.

## Defensive takeaways
- Implement role-based access control (RBAC) restricting incident creation to administrators or the user themselves
- Validate authorization on every incident submission, ensuring the creator matches the assignee or has admin privileges
- Restrict PII disclosure endpoints to authenticated users with legitimate need-to-know, implement granular permission checks
- Audit all user-facing forms that allow selection of other users; apply strict authorization validation
- Implement logging and alerting for suspicious incident creation patterns (bulk creation, cross-user creation)
- Add email verification steps for incidents created by non-administrators
- Disable or heavily restrict file attachments in user-created incidents or implement additional validation
- Apply principle of least privilege to support system access

## Variant hunting
Check other user-assignment fields (escalation, delegation, transfer) for similar authorization bypasses
Test whether attackers can modify existing incidents assigned to other users
Verify if PII exposure exists in other endpoints (user search, directory, reporting features)
Examine bulk operations to see if authorization checks are bypassed at scale
Test whether internal notes or admin-only fields are accessible through the incident API
Check if incident templates with preset user assignments bypass authorization validation

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1598
- T1199
- T1021
- T1040

## Notes
This is a critical security flaw combining multiple attack vectors: unauthorized access control, information disclosure, and social engineering enablement. The platform's trust model assumes only legitimate administrators create incidents, creating significant reputational and compliance risk. The ability to monitor victim responses provides real-time feedback loop for attacker refinement.

## Full report
<details><summary>Expand</summary>

**Summary:**
A malicious user can open an incident for any user via the ████/████████ page. This would allow the attacker to trick the victim into taking actions such as clicking a link or opening a file that has been attached to the incident.

## Impact
A victim could be tricked into visiting a link, opening a file, or sending PII to the attacker via the incident. Because the attacker opened the incident, they can see all comments left by the victim.

## Step-by-step Reproduction Instructions

1. Browse to ████ and create an account or login.
2. Browse to ██████████/█████████. You will be able to create an incident on this page.
3. In the `█████████` field, you can select any user you want to assign the incident to. The `i` button beside the caller field also allows you to view various PII about the user.
███████
██████
4. You can attach files in the top right corner using the attachment button.
5. Once you have chosen a victim (`██████`) and filled in the `additional comments` section with your phishing message, you can click `Submit` in the top right corner.
██████
6. Browse to ███████/home.do and you can see a list of your open incidents. You may need to filter by `All`. 
7. Click the incident that you assigned to the victim. 
███████
8. You can now use this page to monitor the victims response. This could be used to communicate with the victim, posing as an administrator and soliciting PII or causing other malicious effects.
█████████
9. The victim will receive an e-mail that the incident has been submitted on their behalf. Once they log-in, they will see the following:
██████████
███████
10. Obviously an adversary would create an account posing as an Air University administrator or something believable, but here is what a phishing attempt could look like using this vulnerability:
███
11. Meanwhile, the attacker is monitoring the incident waiting on the victim to respond and can even see when the victim has viewed the incident.
███

## Suggested Mitigation/Remediation Actions
This feature should be locked down to administrative access only. Regular users should not be allowed to submit tickets directly to other users or view other users PII.

## Impact

A victim could be tricked into visiting a link, opening a file, or sending PII to the attacker via the incident. Because the attacker opened the incident, they can see all comments left by the victim.

</details>

---
*Analysed by Claude on 2026-05-24*
