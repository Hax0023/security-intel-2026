# SSO Bypass via EntityID Whitespace Manipulation Leading to DOS and Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 976603 | https://hackerone.com/reports/976603
- **Submitted:** 2020-09-08
- **Reporter:** cache-money
- **Program:** Grammarly
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Authentication Bypass, SAML Injection, Denial of Service, Account Takeover, String Parsing Vulnerability
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can create a malicious SSO integration with an entityId identical to a legitimate organization's except for a trailing space character. This causes the application to prioritize the attacker's organization during user provisioning despite correct SAML validation, resulting in DOS of legitimate SSO and potential account takeover of victim users. The vulnerability stems from inconsistent string comparison logic where SAML issuer validation uses trimmed values but organization lookup does not.

## Attack scenario
1. Attacker identifies target organization's SSO entityId (e.g., 'myentity')
2. Attacker creates new Grammarly account and configures SSO with entityId 'myentity ' (with trailing space) and unique keypair
3. Legitimate users attempting to SSO to original organization authenticate successfully against correct SAML issuer but get mapped to attacker's organization instead
4. Organization suffers DOS as legitimate users receive errors and cannot access their accounts
5. If victim user is deleted from original organization, they re-authenticate but get provisioned into attacker's organization
6. Attacker gains control of victim account and changes malicious entityId to new value, then logs in with their keypair to access victim's data

## Root cause
Inconsistent string handling in SAML processing logic. The application validates SAML Response issuer against a trimmed entityId value (`trim(issuer)` matching), but when determining which organization to provision the user into, it queries organization records without trimming, causing the whitespace-padded attacker entityId to be selected preferentially. This indicates a mismatch between authentication validation layer and user provisioning layer, likely due to different code paths or ORM query behavior.

## Attacker mindset
The attacker demonstrates sophisticated understanding of SAML flows and edge cases in string comparison. They methodically tested the application to discover that authentication and provisioning use different comparison logic. The discovery of being able to authenticate against one issuer while being provisioned to another shows creative fuzzing of SAML parameters. The ability to escalate from DOS to account takeover by deleting the victim user first indicates deep knowledge of application state management.

## Defensive takeaways
- Implement consistent string normalization (trim, lowercase) across all authentication and provisioning code paths
- Use cryptographic entity identifiers instead of mutable string-based entityIds
- Validate that SAML issuer exactly matches the organization's configured entityId in both authentication and provisioning stages
- Implement organization entityId uniqueness constraint with normalization (reject 'entity' if 'entity ' exists)
- Add logging and alerting when SAML issuer doesn't match the organization used for provisioning
- Perform identity verification before allowing entityId changes for existing SSO configurations
- Use database constraints to enforce that entityId lookups use normalized values
- Implement rate limiting on SSO configuration changes and monitor for suspicious patterns
- Require additional verification (email confirmation) before new SSO configurations become active
- Add security tests covering SAML validation with whitespace variants

## Variant hunting
Test other whitespace characters (tabs, newlines, non-breaking spaces) in entityId
Investigate whether case sensitivity differences exist (entityId vs EntityId)
Check if URL-encoded variants (%20, %09) are handled inconsistently
Test whether entityId comparison is vulnerable to unicode normalization attacks
Examine if other SAML attributes (NameID, Subject) have similar parsing inconsistencies
Test whether entityId can contain special characters that bypass validation in one layer but not another
Check if organization lookup uses LIKE queries that might match partial strings
Investigate if there are race conditions when multiple organizations have similar entityIds

## MITRE ATT&CK
- T1190
- T1078.004
- T1021.005
- T1556.003
- T1110

## Notes
This is a high-quality security report demonstrating excellent research methodology. The reporter clearly explained the unusual behavior, reproduced steps, and showed awareness of potential escalation. The root cause appears to be a classic engineering mistake: two different code paths handling the same data without consistent normalization. The trailing space attack is subtle and easy to miss in code review. The report's admission that account takeover requires user interaction ('join' click) is honest, but the DOS impact alone is critical. The researcher's statement about potentially achieving zero-interaction ATO suggests they suspected SQL injection or other vulnerabilities existed but couldn't prove them.

## Full report
<details><summary>Expand</summary>

**Summary:**
There's an interesting issue I've spent quite a few days trying to escalate but can't figure out. The impact at this point is that I can DOS any SSO integration making it so nobody in that organization can login. I can also get users to inadvertently SSO into my attacker organization, and then take over their account from there. For existing accounts this would require a victim to click "join", however I think that's likely given the fact that they are SSOing for the first time expecting to join an organization.

The strange behavior and why I think it *might* be possible to escalate further, is that I can have you authenticate against one SSO instance, but have you get added to a completely separate one. So that means there is some sketchy logic which can potentially allow an attacker to authenticate against their own SSO instance, and get added to someone else's organization. I'm not sure if it's possible to get this with zero user interaction, but I will keep trying and update the report if I figure out a way.

The bug stems from the fact that you can create an `entityId` identical to that of another organization **except** with a space ` ` at the end. The application logic then prioritizes that new entityId to add the user to after authenticating against the correct one. So if you have `myentity` as the legitimate entity, and an attacker sets their entity to `myentity[SPACE]` (with a space at the end); users attempting to authenticate into the legitimate `myentity` will technically authenticate against it, but then the application attempts to log them into the attacker's organization. The result of this is a DOS since legitimate users can no longer access their organization. The interesting part of the bug is that if the user is deleted from their original organization (or a **new** user attempts to SSO), they will then be authenticating against their original organization, but get added into the attacker's organization. So it seems the SAML Response is checked against a `trim(issuer)`, but when trying to place the user into an organization, the entity with the space is always prioritized.

The steps below will demonstrate this behavior:

## Steps To Reproduce:
1. Setup SSO and confirm you can login.
2. Create a **new** Grammarly business account and use the same `entityId` (Identity Provider Issuer) you used in step 1, except add a space to the end of it. Use a different keypair for this organization as well.
3. Wait 2 minutes for the change to propagate, then try logging into the same account from step 1, and notice you now get an error.
4. At this point the victim organization is DOS'd. To confirm the strange behavior discussed above, you can delete that user from the victim organization and attempt to login again. Notice you will now end up getting provisioned to the attacker's organization, even though you signed the SAML Response with the victim organization's private key.
5. Once you are provisioned into the attacker's organization, the attacker can then change their `entityId` to something brand new, and login to the victim's account using the keypair they own. If this was a converted personal account, you can then access that user's personal documents.

## Impact

- Ability to effectively disable SSO for any organization.
- Ability to get users provisioned into an attacker's account, which they can then takeover.

Thanks,
-- Tanner

</details>

---
*Analysed by Claude on 2026-05-24*
