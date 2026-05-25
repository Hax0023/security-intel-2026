# IDOR: Facebook Malicious Person Add People to the Top Fans List Without Consent

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Facebook
- **Bounty:** Not specified in writeup
- **Severity:** Medium
- **Vuln types:** Insecure Direct Object Reference (IDOR), Broken Access Control, Missing Authorization Checks, Privacy Violation
- **Category:** web-api
- **Writeup:** https://medium.com/@UpdateLap/idor-facebook-malicious-person-add-people-to-the-top-fans-4f1887aad85a

## Summary
An IDOR vulnerability in Facebook's Top Fans feature allowed attackers to add any user to a page's Top Fans list without the victim's knowledge or consent. The vulnerable endpoint failed to verify that the requester was the actual user being added, allowing parameter manipulation to add arbitrary users to Top Fans lists.

## Attack scenario (step by step)
1. Attacker receives a legitimate Top Fans opt-in notification from Facebook for a page they follow
2. Attacker clicks the notification link containing their own user ID and page ID parameters
3. Attacker intercepts the HTTP request sent when confirming Top Fans status
4. Attacker modifies the fan_id parameter in the request from their own ID to the victim's user ID
5. Attacker modifies creator_id to target a specific page they control or monitor
6. Attacker sends the modified request, causing the victim to be added to Top Fans without consent or knowledge

## Root cause
The endpoint /top_fans/fan_opt_in/ did not implement proper authorization checks to verify that the user submitting the request was the same user being added to the Top Fans list. The API accepted arbitrary fan_id and creator_id parameters without validating the requester's identity or relationship to the resource being modified.

## Attacker mindset
An attacker could leverage this to perform privacy mapping and create false associations between users and page interests. By adding users to Top Fans lists of pages they don't actually endorse, the attacker could damage reputations, manipulate social graphs, or gather intelligence on user interests without detection.

## Defensive takeaways
- Always validate that the authenticated user performing an action is the same user whose data is being modified (use session context, not user-supplied IDs)
- Implement strict authorization checks on all state-changing operations, especially those affecting user privacy
- Never trust user-supplied IDs in parameters; cross-reference with authenticated session identity
- Apply principle of least privilege: users should only be able to modify their own account settings and preferences
- Log and audit all opt-in/opt-out actions with timestamp and originating IP for forensic analysis
- Consider requiring additional confirmation (email, SMS) for privacy-sensitive changes

## Variant hunting
['Check other opt-in/opt-out mechanisms on Facebook (mailing lists, group memberships, interest lists) for similar IDOR patterns', 'Audit all endpoints accepting user IDs as parameters to ensure proper authorization validation', 'Search for other social features where user association is modified (followers, connections, recommendations) that may not verify requester identity', "Test role-based features where one user can designate another user's status or membership without explicit consent", 'Look for similar patterns in feature flags or preference settings that can be toggled on behalf of other users']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1566 - Phishing
- T1589 - Gather Victim Identity Information

## Notes
The timeline shows Facebook took 23 days to patch the vulnerability after initial report, with a re-opening required on 05-Jul due to incomplete fixes. The researcher correctly identified this as primarily a privacy issue rather than a data breach risk, though the impact extends to reputation and social graph manipulation. The vulnerability demonstrates the importance of distinguishing between authentication (is the user who they claim) and authorization (does this user have permission to modify this resource).

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
