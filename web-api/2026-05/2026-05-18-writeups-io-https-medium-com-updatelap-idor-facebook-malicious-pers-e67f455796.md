# IDOR Facebook - Malicious Person Add People to the Top Fans

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Facebook
- **Bounty:** Not specified in writeup
- **Severity:** Medium
- **Vuln types:** Insecure Direct Object Reference (IDOR), Authorization Bypass, Missing User Consent Verification
- **Category:** web-api
- **Writeup:** https://medium.com/@UpdateLap/idor-facebook-malicious-person-add-people-to-the-top-fans-4f1887aad85a

## Summary
A researcher discovered an IDOR vulnerability in Facebook's 'Top Fans' feature that allowed attackers to add arbitrary users to a page's Top Fans list without their knowledge or consent. The vulnerability stemmed from insufficient server-side verification of the requester's identity when processing Top Fans opt-in requests. While no sensitive data could be directly accessed, the exploit violated user privacy by manipulating their visibility status.

## Attack scenario (step by step)
1. Attacker receives a Top Fans notification from Facebook for a page they follow
2. Attacker clicks the notification link and initiates the Top Fans opt-in dialog request
3. Attacker intercepts the HTTP request before submission using a proxy tool
4. Attacker modifies the fan_id parameter to target a victim's user ID instead of their own
5. Attacker forwards the modified request to Facebook's API endpoint
6. Server processes request without verifying the attacker is actually the specified fan_id, adding victim to Top Fans without consent

## Root cause
The server-side endpoint processing Top Fans opt-in requests did not verify that the authenticated user making the request matched the fan_id parameter being modified, allowing arbitrary fan_id values to be added by any authenticated attacker.

## Attacker mindset
The attacker approached this by systematically analyzing Facebook's notification flows and HTTP request patterns. Upon discovering the Top Fans feature, they examined the request structure and tested whether server-side authorization checks were in place, ultimately finding that parameter manipulation alone was sufficient for privilege escalation.

## Defensive takeaways
- Always validate that the authenticated user performing an action matches the subject of that action on the server-side
- Implement strict authorization checks beyond authentication; verify user intent and consent before modifying user state
- Avoid relying on client-provided user identifiers; derive subject identity from session/authentication context
- Consider requiring explicit confirmation from the target user before applying irreversible privacy-impacting changes
- Implement audit logging for all user status modifications to detect and investigate suspicious patterns
- Apply principle of least privilege - opt-in features should require explicit action from the affected user only

## Variant hunting
Search for other Facebook features involving user categorization or status lists (Featured Friends, Close Friends, Followers lists). Look for similar opt-in/opt-out endpoints that accept user identifiers as parameters. Examine any feature allowing one user to modify another user's visibility or association status.

## MITRE ATT&CK
- T1548.001 - Abuse Elevation Control Mechanism: Bypass User Account Control
- T1190 - Exploit Public-Facing Application

## Notes
The vulnerability was reported on 27-Jun-2018 and accepted the same day, but required reopening on 05-Jul-2018 after initial patch failed. Final patch was confirmed on 17-Jul-2018. This is a classic IDOR vulnerability with privacy impact rather than direct data breach risk, yet still represents a serious authorization flaw in a major social platform.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
