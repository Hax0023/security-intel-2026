# SSO Authentication Bypass and Denial of Service via EntityID String Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 976603 | https://hackerone.com/reports/976603
- **Submitted:** 2020-09-08
- **Reporter:** cache-money
- **Program:** Grammarly
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Authentication Bypass, Denial of Service, Account Takeover, SAML Misconfiguration, String Matching Logic Error
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can create an SSO organization with an entityId identical to a legitimate organization except for a trailing space, causing authentication logic to prioritize the malicious entityId during user provisioning while correctly validating the SAML response. This enables denial of service attacks against legitimate organizations and account takeover by provisioning users into attacker-controlled organizations.

## Attack scenario
1. Attacker creates a new Grammarly business account and configures SSO with an entityId matching a target organization's entityId plus a trailing space (e.g., 'myentity ' instead of 'myentity')
2. Attacker generates a different keypair for their malicious SSO instance and waits 2 minutes for propagation
3. Legitimate users attempting to login through the victim organization's SSO now authenticate against the correct SAML issuer but get provisioned into the attacker's organization due to prioritization logic
4. Existing organization members receive authentication errors, effectively disabling SSO access (DOS)
5. Attacker deletes the user from the victim organization or targets new users who then authenticate against the legitimate SAML issuer but get added to the attacker's organization
6. Attacker changes their entityId to a new value and uses their keypair to access the provisioned victim accounts, including personal documents from converted personal accounts

## Root cause
The application implements inconsistent string matching logic between SAML response validation and user provisioning. The SAML issuer validation uses trim() on the entityId, correctly matching 'myentity' and 'myentity '. However, the provisioning logic queries for organizations by exact entityId match without trimming, allowing the malicious 'myentity ' entry to be prioritized. The database query or ORM likely returns results without consistent sorting or filtering, allowing the space-suffixed entityId to take precedence during user assignment.

## Attacker mindset
The attacker demonstrates sophisticated understanding of SAML authentication flows and database query behavior. They recognized that whitespace differences bypass string comparison logic while remaining invisible to users. The ability to DOS services combined with account takeover capability was viewed as a potential escalation vector for complete organizational compromise. The attacker methodically tested edge cases (existing vs. new users) to understand the full scope of exploitation.

## Defensive takeaways
- Normalize all string identifiers (trim, lowercase, etc.) consistently across all code paths before comparison and storage
- Implement whitelist-based validation for SAML entityId values to reject suspicious patterns (trailing/leading spaces, unusual characters)
- Apply the same validation and normalization logic in both SAML response validation AND user provisioning workflows
- Use database constraints (unique indexes) on entityId to prevent near-duplicate entries with whitespace variations
- Implement SAML issuer pinning per organization with cryptographic validation rather than string matching
- Add monitoring and alerting for multiple failed authentication attempts or mismatched SAML issuer/organization pairs
- Require explicit re-authorization or confirmation when provisioning users into organizations during SSO flows
- Audit SSO configuration changes and log all entityId modifications with admin approval workflows
- Validate SAML responses cryptographically throughout the entire provisioning process, not just at initial validation

## Variant hunting
Test other whitespace variations (tabs, newlines, unicode spaces) in entityId fields across all IdP integrations
Search for similar string matching logic in other multi-tenant systems handling SAML, OAuth, or OIDC
Investigate whether other identifiers (organizationId, domain, etc.) are validated inconsistently across different code paths
Test case sensitivity issues in entityId matching (e.g., 'MyEntity' vs 'myentity')
Check for similar issues in SCIM provisioning endpoints which may also use entityId for routing
Examine SAML assertion validation to see if signature validation could be bypassed with entityId manipulation
Test whether metadata endpoints respect the space-suffixed entityId, potentially serving incorrect certificates
Investigate if this affects SAML attribute mapping or role-based provisioning decisions

## MITRE ATT&CK
- T1190
- T1199
- T1556
- T1021
- T1098

## Notes
This report represents a well-executed chained vulnerability combining DOS and account takeover. The attacker's observation about inconsistent trim() behavior between validation and provisioning stages is the key technical insight. The fact that new/deleted users could be provisioned to attacker organizations while existing users were denied access suggests the application maintains separate lookups or caching mechanisms that weren't properly synchronized. The 2-minute propagation delay indicates data replication issues in distributed systems which could be exploited further. The reporter's methodical approach (testing existing vs. new users, attempting zero-interaction escalation) demonstrates mature vulnerability research.

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
