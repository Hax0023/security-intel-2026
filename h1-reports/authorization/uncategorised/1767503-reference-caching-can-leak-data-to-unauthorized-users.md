# Reference caching can leak data to unauthorized users

## Metadata
- **Source:** HackerOne
- **Report:** 1767503 | https://hackerone.com/reports/1767503
- **Submitted:** 2022-11-08
- **Reporter:** systemkeeper
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Improper Access Control, Insufficient Cache Isolation, Information Disclosure
- **CVEs:** CVE-2023-22469
- **Category:** uncategorised

## Summary
The ReferenceManager in Nextcloud uses a cache with a user-agnostic prefix, allowing unauthorized users to access cached reference data if they know the card/board identifiers. The Deck application's CardReferenceProvider fails to include user context in its cache key, enabling information disclosure to users who should not have access to private deck cards.

## Attack scenario
1. User1 (Admin) shares a Deck card link in a Nextcloud Talk conversation, triggering reference resolution and caching of the card data with a cache prefix independent of user identity
2. The reference data is stored in cache with only the boardId/cardId as the cache key prefix, without including User1's userId
3. User2 (unauthorized, but with knowledge of the card link) makes a request that triggers the same reference resolution process
4. The ReferenceManager retrieves the previously cached card data from User1's access, even though User2 has no permission to view that card
5. User2 obtains sensitive information about the deck card (title, description, attachments, etc.) without proper authorization
6. If User2 knows multiple cardId/boardId combinations, they can enumerate and access all cached references

## Root cause
The Deck CardReferenceProvider implements a cache prefix that uses only board and card identifiers (boardId/cardId) without including the userId in the cache key. This allows the global cache to return the same reference data regardless of which user is requesting it, bypassing access control checks that would normally be performed on each request.

## Attacker mindset
An attacker with knowledge of Nextcloud's internal reference link structure and card identifiers can systematically extract sensitive information from deck cards by leveraging the shared cache. The attacker exploits the assumption that cache isolation is sufficient security, when in fact access control must be enforced at retrieval time regardless of cache state.

## Defensive takeaways
- Always include user context (userId, tenant ID, or similar) in cache keys for user-scoped data
- Perform access control validation before returning cached data, not just at cache storage time
- Audit all reference providers across integrations (GitHub, Deck, etc.) to ensure consistent cache key generation patterns
- Consider using user-specific cache stores or namespaces rather than global caches for sensitive data
- Implement cache versioning or invalidation mechanisms tied to permission changes
- Document cache key construction requirements in developer guidelines for reference providers

## Variant hunting
Check all reference providers in Nextcloud and integrations for proper userId inclusion in cache keys
Audit other collaboration features (comments, mentions, embedded resources) for similar cache isolation issues
Test whether cached references maintain permissions as users are removed from shares or groups
Investigate if cache can be poisoned by lower-privileged users to affect higher-privileged user views
Check if cache keys depend on mutable identifiers that could be enumerated or guessed

## MITRE ATT&CK
- T1190
- T1548
- T1528
- T1526
- T1087

## Notes
Reporter correctly notes this requires multiple conditions: cached reference, knowledge of identifiers, and timing. However, information disclosure still occurs. GitHub integration properly includes userId in cache prefix, showing this is a known pattern not followed consistently. The minimal impact assessment may underestimate risk in multi-tenant or high-security scenarios. Cache isolation without access control is a common architectural flaw in distributed systems.

## Full report
<details><summary>Expand</summary>

## Summary:
The [ReferenceManager](https://github.com/nextcloud/server/blob/master/lib/private/Collaboration/Reference/ReferenceManager.php) uses a cache to store information about previously accessed references. The used `cachePrefix` in deck ([see here](https://github.com/nextcloud/deck/blob/e55b3a0a26a65a01fae8cfdf83b1066616bfa6ee/lib/Reference/CardReferenceProvider.php#L154-L166)) is independent of the user. If User1 has access to a deck card and the reference data is stored in the cache, any user with knowledge of the boardId/cardId can access the information of that deck card.

## Steps To Reproduce:
  1. User1 has a deck card and shares the link in a talk conversation
  2. Any user of that conversation (or with knowledge of the link) is able to see the deck card, if the call to the reference provider was done for user1 before


## Supporting Material/References:
User "Admin":
{F2025386}

User "Test":
{F2025389}

## Impact

I think the impact should be minimal, because multiple things need to happen to leak information (the reference needs to be cached, another user needs to know the url, etc.).
The GitHub-Integration uses the `userId` as a cachePrefix, this so this shouldn't be a issue in that case, [see here](https://github.com/nextcloud/integration_github/blob/bb443c47fc8a9b0ba090456461040136a93c9214/lib/Reference/GithubReferenceProvider.php#L175-L182).
I haven't looked at other reference providers.

</details>

---
*Analysed by Claude on 2026-05-24*
