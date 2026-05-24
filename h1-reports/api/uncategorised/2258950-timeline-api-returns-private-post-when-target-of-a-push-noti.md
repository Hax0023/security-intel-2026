# Timeline API returns private post when target of a push notification

## Metadata
- **Source:** HackerOne
- **Report:** 2258950 | https://hackerone.com/reports/2258950
- **Submitted:** 2023-11-21
- **Reporter:** nightpool
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** uncategorised

## Summary
## Summary:
If the user has the post ID of a private post, they're able to use the timeline API to retrieve it, even though they don't have access

## Platform(s) Affected:
API

## Steps To Reproduce:

  1. Receive an Android push notification targeting a post (e.g. "Look at what your tumblr crush @april posted")
  1. Between receiving and sending the push notification, have the post in question b

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

## Summary:
If the user has the post ID of a private post, they're able to use the timeline API to retrieve it, even though they don't have access

## Platform(s) Affected:
API

## Steps To Reproduce:

  1. Receive an Android push notification targeting a post (e.g. "Look at what your tumblr crush @april posted")
  1. Between receiving and sending the push notification, have the post in question be set to private
  1. click on the push notification and have it open in the Android app (at the top of the timeline, showing the "From your fav" banner)
  1. see that the mobile app is able to successfully retrieve the post, but the post is marked as "private" and cannot be interacted with. 

## Supporting Material/References:

  * Attached see a screenshot of a private post rendered in the app after being returned by the API

## Impact

Presumably, look up and receive any information based on a post ID regardless on if the post has been set to private or not. That is, at worst, full disclosure of private posts if the attacker has or can guess the post ID. Possibly there are some other required preconditions i'm not thinking about though.

</details>

---
*Analysed by Claude on 2026-05-24*
