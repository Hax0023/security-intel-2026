# Ability to Obtain Twitter Blue Verified Badge Without Purchase

## Metadata
- **Source:** HackerOne
- **Report:** 1841064 | https://hackerone.com/reports/1841064
- **Submitted:** 2023-01-20
- **Reporter:** alp
- **Program:** Twitter (HackerOne)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Business Logic Flaw, Subscription Verification Bypass, Badge Persistence After Cancellation
- **CVEs:** None
- **Category:** business-logic

## Summary
A business logic vulnerability allows users to obtain a permanent Twitter Blue verified badge without maintaining an active subscription by triggering a review process before cancellation. The flaw exploits the asynchronous review system where badge status remains during the review period even after subscription expiration.

## Attack scenario
1. Attacker purchases a Twitter Blue subscription to their account
2. One day before subscription expiration, attacker changes their profile photo to trigger review process
3. Badge enters 'under review' state while subscription is still active
4. Attacker cancels subscription and waits for expiration
5. Review completes during post-expiration period, badge is restored permanently
6. Attacker retains verified badge without active subscription or ongoing payment

## Root cause
Twitter's verification badge logic does not validate active subscription status when finalizing badge restoration after review completion. The system assumes users under review are legitimate subscribers, failing to cross-check subscription status at review finalization time.

## Attacker mindset
Economically motivated - retain premium status indicator without recurring payment. Reputationally motivated - obtain credibility signal for impersonation, scam, or influence operations without financial commitment.

## Defensive takeaways
- Implement synchronous subscription validation checks at all badge state transitions
- Revoke badges immediately upon subscription cancellation rather than maintaining review state
- Add subscription status as a gating condition in badge finalization logic
- Implement audit logging for badge grants with subscription validation proof
- Create monitoring for badge grants to cancelled accounts post-expiration
- Set maximum review duration limits before automatic badge revocation
- Require re-verification of subscription status before badge restoration

## Variant hunting
Profile metadata changes (bio, display name) triggering similar review mechanisms
Other Twitter features with deferred validation (edit tweets, creator fund access)
Subscription products with review/appeal processes (Twitter Blue features, creator programs)
Time-of-check-time-of-use (TOCTOU) conditions in other subscription gates
Delayed webhook/event processing causing state inconsistencies

## MITRE ATT&CK
- T1078 - Valid Accounts
- T1534 - Internal Spearphishing
- T1589 - Gather Victim Identity Information
- T1619 - Impersonation

## Notes
Report lacks financial impact quantification and concrete timeline. Severity is medium rather than high because: (1) requires initial legitimate purchase, (2) relies on predictable review timing, (3) scope limited to badge cosmetics rather than functionality. However, cumulative abuse could generate significant revenue loss. Suggested fix is straightforward subscription-status validation.

## Full report
<details><summary>Expand</summary>

**Summary:** 

Hi there. In this report, I submit a bug about getting Twitter Blue verified badge without purchasing it. 

## Steps To Reproduce:

1. First, you should buy a Twitter Blue subscription for your account. 
2. Change the profile photo of your Twitter account 1 day before your Twitter Blue subscription expires.
3. Check your Twitter profile and ensure your verified badge is gone for review by the Twitter team. (note that, this review will take 1-2 days but it might be good to check from time to time if your account has been reviewed - if it's reviewed and your verified badge is there, you should change again your profile picture before your Twitter Blue subscription is expired)
4. Go to the `App Store` -> `Your App Store Account` > `Subscriptions` section and cancel your Twitter Blue subscription.
5. You should wait one day for your subscription to expire. (please read the note written in step 3)
6. After the subscription expired, try change to your account details if your verified badge still is not there. You'll get a message about your Twitter account is still under review.

Now you have to wait for 2-3 days (no eta about review times but it takes at least 3 days) then the Twitter team will give back your verified badge even your Twitter Blue subscription is expired.

## Impact: 

This can harm financial damages to the Twitter team, and malicious actors can't be tracked since they do not pay for the Blue subscription. 

## Supporting Material/References:

I recorded this video on PC, and showed that I can't edit any new tweet and I'm no longer a Twitter Blue subscriber :

███

I recorded this video on my iPhone device, and showed that I can't edit any new tweet, I'm no longer a Twitter Blue subscriber and went to my Subscriptions section on App Store to show my Twitter Blue subscription is ended on January 13 2023  :

█████

## Impact

This can harm financial damages to Twitter, Inc., and malicious actors can't be tracked since they do not pay for the Blue subscription.

</details>

---
*Analysed by Claude on 2026-05-24*
