# Ability to Subscribe to Inactive Post+ Creators via blogMembershipsId Substitution

## Metadata
- **Source:** HackerOne
- **Report:** 1322334 | https://hackerone.com/reports/1322334
- **Submitted:** 2021-08-28
- **Reporter:** ajoekerr
- **Program:** Tumblr
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Authorization Bypass, Business Logic Flaw, Account Takeover (Indirect)
- **CVEs:** None
- **Category:** business-logic

## Summary
A vulnerability in Tumblr's Post+ subscription system allows users to subscribe to creators who have deactivated their Post+ membership by substituting an inactive creator's blogMembershipsId into an active creator's payment URL. This reactivates the inactive creator's Post+ status without their consent, though exploitation requires knowledge of the target's blogMembershipsId and appears to be a one-time use vulnerability.

## Attack scenario
1. Attacker obtains the blogMembershipsId of a creator who previously had Post+ enabled but has since deactivated it
2. Attacker retrieves a valid Post+ subscription payment URL from an active Post+ creator
3. Attacker modifies the payment URL by replacing the active creator's blogMembershipsId with the target inactive creator's ID
4. Attacker completes the checkout process using the modified URL
5. Upon successful payment, the inactive creator's Post+ membership is reactivated without their knowledge or consent
6. The creator page redirects but loads, and verification shows the previously inactive Post+ blog is now active with a confirmed subscription

## Root cause
Insufficient server-side validation of the blogMembershipsId parameter in the Post+ payment flow. The system trusts the blogMembershipsId embedded in the payment token without verifying that it matches the actual creator's intent or current enrollment status, and does not validate that the creator has active Post+ enabled before processing subscription activation.

## Attacker mindset
An attacker with knowledge of specific creators' blogMembershipsIds could reactivate dormant Post+ memberships to generate unauthorized revenue or disrupt creator accounts. The vulnerability is somewhat opportunistic—the attacker discovered this by having legitimate access to a creator's ID, then tested parameter manipulation.

## Defensive takeaways
- Implement strict server-side validation of all payment parameters, including blogMembershipsId, before processing transactions
- Verify that creators have explicit, current Post+ enrollment status before allowing subscription activation
- Enforce immutability of critical payment parameters by binding them cryptographically to the payment intent
- Implement audit logging for Post+ activations and require explicit creator action to re-enable Post+ after deactivation
- Add rate limiting and anomaly detection for subscription attempts on recently-deactivated accounts
- Validate token integrity and prevent substitution of component IDs within payment URLs

## Variant hunting
Test if other creator program IDs (blogId, userId) can be similarly substituted in payment flows
Attempt to reactivate Post+ multiple times using the same payment URL to determine if 'one-time use' is enforced
Check if inactive creator data persists and can be leveraged in other API endpoints
Investigate whether payment tokens can be reused across different creator IDs
Test if other Tumblr monetization features (ads, tips) have similar parameter validation weaknesses
Examine if creator reactivation triggers notifications or if changes occur silently

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1578: Modify Cloud Compute Infrastructure
- T1583: Acquire Infrastructure

## Notes
Low severity impact but notable due to account state manipulation without creator consent. The 'one-time use' limitation significantly reduces exploitability. The reporter demonstrated good security ethics by self-assessing severity and offering to self-close. The vulnerability requires knowledge of target blogMembershipsId, which creates a practical barrier to widespread exploitation but is not impossible to enumerate. High bar to reproduce due to payment URL invalidation post-exploitation.

## Full report
<details><summary>Expand</summary>

Hey y'all! 👋 Hope all is well!

## Summary:
In testing Tumblr's Post+, I've found that it's possible to subscribe to creators that, at one point, opted into Post+ but had opted out after some point. As I note later on, it appears that this is a "one time use only" as the Payment URL becomes invalid after activating Post+ for the inactive Post+ blog.

## Platform(s) Affected:
N/A

## Steps To Reproduce:
In order to reproduce, you need the `blogMembershipsId` of an inactive Post+ blog. This creates a high bar to actually exploit this but, for some reason, I had the `blogMembershipsId` of `███████`, who had deactivated Post+ shortly after launch (the membership ID is `█████`).

1. Get an active Post+ subscription URL (I used `██████.tumblr.com`'s subscription URL).
2. Replace the active Post+ blog's `blogMemershipsId` with the inactive blog's `blogMembershipsId` (if using `███████`, you should have a url like `https://███.payment.tumblr.com/checkout/?token=<token>`).
    * As a heads up, it actually looks like this URL is no longer valid after activating my Post+ subscription for `█████████`.
3. Complete checkout as normal.
4. After checkout, it will redirect back to the active Post+ blog's creator page but it will never load.
5. Verify that the creator page for the previously inactive Post+ blog is active again and that the subscription is active for the inactive Post+ blog.

## Supporting Material/References:
Unfortunately, this looks like a "one time use" only vulnerability as the WooCommerce payment URL is no longer active for `██████` after I attempted to subscribe so I was unable to get a PoC video. However, I've uploaded the receipt in case having the `payment_intent` ID helps at all!

## Impact

As of right now, the only impact I've been able to see is that the inactive Post+ blog's creator page became active, even without them enrolled into Post+: https://www.tumblr.com/creator/█████. However, I would also consider the fact that a page would show the blog name & avatar for the Post+ blog noted in the token but the checkout URL corresponds to the `blogMembershipsId` as unexpected behavior but, as far as I can tell, it would be somewhat of a "self-pwn" 😅.

If y'all don't necessarily consider this a security risk, please let me know and I will self-close this report! To be honest, with what I can see, I consider this to be fairly low impact but I wanted to let y'all know anyway. 🙂

</details>

---
*Analysed by Claude on 2026-05-24*
