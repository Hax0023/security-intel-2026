# SAML entityId Whitespace Bypass Enabling SSO DOS and Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 976603 | https://hackerone.com/reports/976603
- **Submitted:** 2020-09-08
- **Reporter:** cache-money
- **Program:** Grammarly
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** SAML Authentication Bypass, Logic Error in Identity Resolution, Denial of Service, Account Takeover, Insufficient Input Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can create a malicious SSO integration with an entityId identical to a legitimate organization's but with a trailing space, causing the application to prioritize the attacker's organization during user provisioning. This enables DOS of legitimate SSO access and provisional account takeover by redirecting authenticated users to the attacker's organization despite valid SAML responses from the original issuer.

## Attack scenario
1. Attacker identifies target organization's SAML entityId (e.g., 'myentity')
2. Attacker creates new Grammarly business account and configures SSO with entityId 'myentity ' (with trailing space) and their own keypair
3. Legitimate user attempts to SSO login; SAML response validates correctly against trimmed entityId but application matches untrimmed entityId
4. Application prioritizes attacker's organization due to whitespace variant, provisioning user there instead of legitimate org (DOS condition)
5. Attacker deletes original user from victim org; user retries SSO and gets provisioned to attacker's org despite authenticating with victim's keypair
6. Attacker changes their entityId to new value and uses victim's keypair to login and access compromised account

## Root cause
Inconsistent string comparison logic: SAML response validation uses trim(issuer) for cryptographic verification, but organization matching/provisioning logic uses untrimmed entityId comparison, allowing whitespace variants to be treated as distinct entities with higher priority during user routing.

## Attacker mindset
Sophisticated threat actor understands SAML mechanics and exploits inconsistent normalization across validation and routing layers. Persistence in discovering zero-interaction variants suggests intent to fully automate account compromise. Multi-step exploitation path maximizes impact.

## Defensive takeaways
- Normalize all entity identifier comparisons consistently (trim, lowercase) across authentication AND provisioning logic
- Implement strict entityId validation to reject whitespace-variant registrations or enforce exact-match requirements
- Use constant-time comparison for identity resolution to prevent bypass techniques
- Perform cryptographic binding between SAML issuer verification and user organization assignment (don't allow post-auth remapping)
- Add audit logging for organization routing decisions and alert on mismatches between authenticated issuer and target organization
- Require DNS/certificate validation of entityIds to prevent arbitrary registration of lookalike identifiers
- Implement rate limiting on SAML assertion processing per issuer to mitigate DOS attempts

## Variant hunting
Test other whitespace characters (tabs, newlines, unicode spaces) in entityId variants
Investigate case-sensitivity bypasses (myEntity vs myentity)
Probe URL-encoded variations in entityId submission
Test entityId with leading whitespace instead of trailing
Examine if similar bypass works with other SAML attributes (NameID, Audience)
Check if entity priority logic applies to other identifier types
Test whether SAML response signature validation is performed AFTER routing decision

## MITRE ATT&CK
- T1190
- T1556
- T1556.003
- T1021.007
- T1078
- T1078.004
- T1499
- T1499.004

## Notes
This is a high-sophistication vulnerability requiring deep SAML protocol knowledge. The whitespace bypass is subtle but devastating. The core issue is business logic flaw rather than cryptographic weakness - SAML signatures remain valid, but routing logic is broken. The DOS component is immediate/reliable while full account takeover requires additional steps. Reporter demonstrates professional analysis and incremental escalation attempts. The finding that authentication issuer != provisioning organization is the critical insight revealing systemic validation gaps.

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
