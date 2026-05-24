# Incorrect OAuth permissions screen allows DMs to be read without user knowledge

## Metadata
- **Source:** HackerOne
- **Report:** 434763 | https://hackerone.com/reports/434763
- **Submitted:** 2018-11-06
- **Reporter:** edent
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Incorrect Access Control, Misleading Authorization UI, Information Disclosure, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Twitter's OAuth permission screen incorrectly displayed that third-party apps could not access Direct Messages, when in fact the underlying API keys (iPhone and Google TV official keys) granted full DM read access. Users were misled during authorization, believing their DMs were protected when they were actually accessible to the application.

## Attack scenario
1. Attacker identifies that Twitter's official API keys (iPhone/Google TV) were publicly leaked on GitHub
2. Attacker creates or modifies a third-party Twitter application to use these leaked official API credentials
3. User initiates OAuth flow with the compromised application
4. OAuth permission screen displays 'Will not be able to: Access your direct messages'
5. User grants authorization, believing their DMs are protected based on the false permission statement
6. Application uses the official API keys to silently read and exfiltrate user's Direct Messages without actual permission

## Root cause
Mismatch between the OAuth permission UI (which indicated DM access was denied) and the actual API capabilities granted by the official API keys. The permission screen logic did not accurately reflect the true access levels provided by the compromised credentials.

## Attacker mindset
Opportunistic insider or sophisticated threat actor who discovered leaked official Twitter API keys and understood the OAuth permission screen inaccuracies could be exploited to gain unauthorized DM access while appearing legitimate to users.

## Defensive takeaways
- Implement real-time validation between permission UI display and actual underlying API token capabilities
- Never display permission statements that contradict actual API access levels
- Audit and rotate official API keys immediately upon detection of leaks
- Implement scope-based access control that enforces permission boundaries in the token validation layer, not just UI
- Add consent audit logging to detect discrepancies between displayed and granted permissions
- Implement rate limiting and anomaly detection for DM access patterns
- Consider requiring explicit user re-authorization if permission metadata mismatches are detected

## Variant hunting
Search for other OAuth implementations where permission screens may not accurately reflect token capabilities; check for other leaked official API credentials from major platforms; examine other OAuth flows where UI permissions differ from backend access controls; look for similar issues with other sensitive scopes (email, phone, location, contacts)

## MITRE ATT&CK
- T1566 - Phishing
- T1598 - Phishing for Information
- T1190 - Exploit Public-Facing Application
- T1550 - Use Alternate Authentication Material
- T1078 - Valid Accounts
- T1557 - Man-in-the-Middle

## Notes
This vulnerability represents a critical failure in the authorization flow trust model. Users make authorization decisions based on the permission screen, which serves as their primary mechanism for informed consent. When this screen is inaccurate, the entire OAuth trust chain breaks down. The use of publicly leaked official API keys compounds the issue by ensuring widespread access. GDPR implications are significant as users are not providing informed consent when shown false permission information.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

**Summary:** 
The OAuth screen can be tricked into saying that an app cannot read Direct Messages. Despite that, DMs can be read.

**Description:** 
The official Twitter API keys have been leaked and are in use in several popular apps.
The iPhone keys and Google TV keys (as seen on https://gist.github.com/shobotch/5160017) present an OAuth screen which says the app "Will not be able to:   Access your direct messages."
This is false.  The apps *can* read DMs.

## Steps To Reproduce:

(Add details for how we can reproduce the issue)

  1. Ask the user to do the OAuth dance with a token generated from the official keys.
  1. User sees that the app cannot read DMs.
  1. User authorises.
  1. App now has unauthorised access to DMs.
  1. User is sad that their privacy has been violated.

## Impact: [add why this issue matters]
A user may not want a 3rd party app to have access to their DMs.

They rely on the OAuth screen to adequately inform them of the permissions they are granting.

Is this a GDPR violation? I'm not sure. You are telling users that the 3rd party app can't read their private information - but that is false. These API keys do allow access from *any* app which integrates them.

## Supporting Material/References:

  * Screenshot of the OAuth screen for Google TV
  * Screenshot of the OAuth screen for iPhone

## Impact

Unauthorised access to Direct Messages.

</details>

---
*Analysed by Claude on 2026-05-24*
