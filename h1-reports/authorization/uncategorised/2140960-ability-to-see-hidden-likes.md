# Ability to View Hidden Likes via GraphQL API Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 2140960 | https://hackerone.com/reports/2140960
- **Submitted:** 2023-09-08
- **Reporter:** mirhat
- **Program:** Twitter/X
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Broken Access Control, Information Disclosure, Improper Authorization, API Security Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
Twitter's premium feature allowing users to hide their likes could be bypassed by directly querying the GraphQL API endpoint, exposing liked tweets regardless of privacy settings. An unauthenticated or low-privileged user could retrieve another user's hidden likes by sending a crafted API request with the target user's ID.

## Attack scenario
1. Attacker identifies a Twitter/X user with hidden likes (visible via privacy indicator)
2. Attacker obtains or brute-forces the target user's numeric ID
3. Attacker crafts a GraphQL query to the /i/api/graphql/lVf2NuhLoYVrpN4nO7uw0Q/Likes endpoint with the target userId parameter
4. Attacker sends the HTTP GET request with appropriate headers and variables
5. API endpoint returns JSON data containing the target user's liked tweets despite privacy setting
6. Attacker can iterate through results using cursor pagination to enumerate all hidden likes

## Root cause
Client-side privacy enforcement: The 'hide likes' setting was enforced only at the UI/frontend layer rather than implemented as server-side access control on the GraphQL API endpoint. The API endpoint failed to validate whether the requesting user has permission to view another user's likes based on that user's privacy settings.

## Attacker mindset
A bug bounty researcher or privacy-conscious user discovered that X's backend GraphQL API did not respect the premium 'hide likes' feature, allowing unauthorized access to sensitive user activity data through direct API manipulation.

## Defensive takeaways
- Always enforce privacy and authorization rules at the API/backend layer, never rely solely on client-side enforcement
- Implement proper access control checks on all API endpoints before returning sensitive user data
- Create a privacy policy matrix: map which user types can access which data fields and enforce it consistently across all API operations
- Validate that user privacy settings (public/private/hidden) are checked server-side before returning user activity data
- Conduct security review of all GraphQL operations, particularly those returning user-specific data like likes, bookmarks, and follows
- Implement audit logging for API access to sensitive user activity endpoints
- Use API gateway controls to enforce privacy settings before reaching business logic
- Test privacy features with direct API calls, not just UI interactions

## Variant hunting
Check if other hidden user activities (bookmarks, followers, following lists) bypass privacy settings via GraphQL
Test if direct REST API endpoints for likes have the same vulnerability
Verify if the vulnerability affects other premium privacy features like hidden retweets or quote tweets
Check if authenticated requests with low-privilege accounts can access other users' hidden activity
Test if the same bypass works for private/protected accounts' activity streams
Investigate other GraphQL operations that may not respect user privacy settings
Check historical API versions to see if this was a regression

## MITRE ATT&CK
- T1190
- T1592
- T1526

## Notes
This vulnerability demonstrates the critical importance of server-side authorization enforcement. While the reporter could not access high-value user data with premium account detection required, the unauthorized disclosure of liked content violates user privacy expectations and could be used for profiling, social engineering, or harassment. The fact that premium features can be bypassed via API calls is a significant finding. Reports mention cookies and authorization headers were redacted, suggesting the researcher had authenticated access, though the vulnerability may also work for unauthenticated users depending on Twitter's API policies.

## Full report
<details><summary>Expand</summary>

**Summary:**

Twitter/X recently added an feature that allows you to hide your likes. It's still possible to see the liked tweets via graphql API.

**Description:** 
I was testing the GraphQL API and it's still possible to view tweets.
You need to be subscribed to X premium to hide your likes. However you don't need a premium account to reproduce this vulnerability.

Twitter user with the id of `████████`has their likes hidden. However if you copy the request below and send it you will see JSON data of likes returned back to you. 

## Steps To Reproduce:

  1. Copy the raw http request below
  1. Paste it into your proxy (change the userId in the url if you want to test against another user. %22%3A%22████%22%2C%22 )
  1. Send the request

## Supporting Material/References:

Vulnerable HTTP request

``` 
GET /i/api/graphql/lVf2NuhLoYVrpN4nO7uw0Q/Likes?variables=%7B%22userId%22%3A%22██████████%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Afalse%2C%22withClientEventToken%22%3Afalse%2C%22withBirdwatchNotes%22%3Afalse%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Afalse%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D HTTP/2
Host: twitter.com
Cookie: 
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0
Accept: */*
Accept-Language: tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://twitter.com/██████/likes
Content-Type: application/json
X-Twitter-Auth-Type: OAuth2Session
X-Csrf-Token:
X-Twitter-Client-Language: en
X-Twitter-Active-User: yes
X-Client-Transaction-Id: 
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Authorization: 
```

## Impact

Viewing hidden likes

</details>

---
*Analysed by Claude on 2026-05-24*
