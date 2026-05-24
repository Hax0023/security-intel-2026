# Unauthorized Disclosure of Private Emails via WakaTime Private Leaderboards

## Metadata
- **Source:** HackerOne
- **Report:** 3279508 | https://hackerone.com/reports/3279508
- **Submitted:** 2025-07-31
- **Reporter:** ctrl_cipher
- **Program:** WakaTime
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Information Disclosure, Privacy Bypass, Inadequate Access Controls, PII Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
WakaTime's private leaderboard feature exposes users' private email addresses to leaderboard creators and members despite users having their email privacy settings configured as private. The vulnerability bypasses intended privacy controls, allowing any authenticated user to harvest email addresses by creating leaderboards and inviting targets to join.

## Attack scenario
1. Attacker creates a WakaTime account and establishes a private leaderboard with an enticing name (e.g., 'Top Developers 2024')
2. Attacker identifies target users via WakaTime's public directory or social engineering and sends leaderboard invitations
3. Target users, unaware of privacy implications, accept the invitation and join the leaderboard
4. Attacker accesses the leaderboard page or API endpoint and retrieves the email addresses of all joined members
5. Attacker harvests emails for phishing campaigns, spam, or sale to third parties
6. Attacker repeats process at scale to build comprehensive email lists of WakaTime users

## Root cause
The application fails to implement privacy-aware data filtering before returning leaderboard member information. The backend likely includes all user fields (including email) in API responses or database queries without checking user privacy preferences or consent settings. No authorization logic verifies that email visibility is appropriate before disclosure.

## Attacker mindset
An attacker recognizes that leaderboards represent a social engineering vector—users trust invitations from perceived legitimate competitions. By exploiting the gap between user privacy expectations (email marked private) and actual implementation (email always exposed in leaderboards), the attacker efficiently harvests PII at scale with minimal detection risk.

## Defensive takeaways
- Implement field-level access control: always check user privacy preferences before including PII in API responses
- Apply privacy-sensitive data masking in leaderboard contexts—only expose data users have explicitly consented to share in that specific context
- Separate data models for public vs. private views; never default to exposing sensitive fields
- Add consent prompts when users join leaderboards clearly stating what information will be visible to other members
- Audit all features that aggregate or display user data for unintended PII exposure
- Implement privacy-by-design: treat email, phone, and other PII as opt-in for visibility rather than opt-out
- Log and monitor leaderboard member enumeration to detect bulk harvesting patterns

## Variant hunting
Check if other aggregation features (teams, projects, groups) expose private user data without consent
Test whether API endpoints return more PII than the UI displays (API over-exposure)
Verify if user privacy settings for other platforms (GitHub integration, etc.) are similarly bypassed
Examine whether profile endpoints leak email when accessed via leaderboard context vs. direct access
Investigate if exported leaderboard data (CSV, reports) contains unfiltered PII
Test if moderators, admins, or workspace owners have privilege escalation paths to access private user data

## MITRE ATT&CK
- T1190
- T1589
- T1598
- T1566

## Notes
This vulnerability is a textbook example of inadequate authorization and privacy control implementation. The attack surface is high because any authenticated user can initiate the exploit, and the social engineering component (invitations) increases success rates. The GDPR/CCPA implications significantly elevate severity despite the technical simplicity of the vulnerability. The report demonstrates good security researcher practices by providing clear reproduction steps and impact analysis, though no financial bounty amount is disclosed in the excerpt provided.

## Full report
<details><summary>Expand</summary>

## Summary:
WakaTime allows users to create private leaderboards and invite others to join. However, once a user accepts the invite and joins the leaderboard, their private email address becomes visible to the leaderboard creator or other members, even if the user has not chosen to make their email public.
This bypasses intended privacy controls and could be exploited to harvest emails of unsuspecting WakaTime users.

## Steps to Reproduce:
1. Sign in to WakaTime.com and create a new private leaderboard.

{F4630919}

{F4630942}

2. Invite another WakaTime user to join the leaderboard using their WakaTime username or public profile link:

{F4630944}

3. Have the invited user accept the invite and join the leaderboard.
4. Once joined, visit the leaderboard page and observe that it contains their emails despite of them setting it as private:

{F4630953}

## Observed Result:
You can view the email address of the invited user in the leaderboard data or UI, even if their email was never made public in their settings.

## Impact

- Violation of user privacy expectations and configurations.
- Could be used for email harvesting or targeted phishing.
- Low barrier to exploitation: any user with an account can create a leaderboard and bait others to join.
- GDPR/CCPA risk due to unconsented exposure of personally identifiable information (PII).

## Expected Behavior:
- Users' email addresses must remain hidden unless they have explicitly chosen to display them publicly.
- Leaderboards should only display public data, not private or sensitive identifiers like email addresses.

## Recommendations:
- Ensure that private fields (like email) are never included in leaderboard-related responses unless the user has opted in to show them.
- Perform a privacy filter before returning leaderboard member data to clients.
- Add a notice or confirmation prompt when joining leaderboards about what information will be visible to other members.

</details>

---
*Analysed by Claude on 2026-05-24*
