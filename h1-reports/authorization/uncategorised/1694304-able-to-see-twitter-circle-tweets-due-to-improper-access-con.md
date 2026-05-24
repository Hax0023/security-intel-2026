# Information Disclosure: Unauthorized Access to Twitter Circle Tweets via Improper Access Control on FavoriteTweet Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1694304 | https://hackerone.com/reports/1694304
- **Submitted:** 2022-09-08
- **Reporter:** bugra
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Improper Authorization, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
Twitter's FavoriteTweet endpoint lacks proper access control, allowing any authenticated user to like tweets restricted to Twitter Circle groups. While the liked tweets remain invisible in the normal UI, the data export feature reveals the full content of liked Twitter Circle tweets, enabling unauthorized information disclosure of private communications.

## Attack scenario
1. Attacker identifies a target user's Twitter Circle tweet ID through various reconnaissance methods (e.g., timing attacks, inference from engagement patterns, or leaked IDs)
2. Attacker sends a POST request to the FavoriteTweet endpoint with the Twitter Circle tweet ID, bypassing client-side visibility restrictions
3. Server returns 200 OK response, successfully recording the like despite authorization checks not validating Circle membership
4. Attacker navigates to Twitter's data download feature and requests a personal data archive
5. After 24 hours, attacker downloads the data archive containing all liked tweets
6. Attacker extracts the liked.js file or HTML export to reveal full content of the previously-inaccessible Twitter Circle tweets

## Root cause
The FavoriteTweet endpoint performs authentication checks but fails to validate whether the authenticated user has authorization to access the specific tweet being liked. The authorization logic does not verify Circle membership or tweet visibility constraints. The data export functionality compounds the issue by including all liked tweets without re-validating their original access restrictions at export time.

## Attacker mindset
A curious security researcher or competitive attacker seeking to gather private information about target users. The attacker exploits a disconnect between two systems: the API's broken access control and the data export feature's blind inclusion of restricted content. The attacker leverages the legitimate data download feature as an amplification vector to exfiltrate otherwise hidden information.

## Defensive takeaways
- Implement authorization checks on all endpoints that interact with user-generated content, verifying not just authentication but also access rights (e.g., Circle membership)
- Enforce consistent visibility rules across all data access points, including APIs and data export features
- Validate tweet visibility status before including content in data archives; respect original privacy constraints even in personal data exports
- Implement rate limiting and monitoring on the FavoriteTweet endpoint to detect unusual like patterns targeting Circle tweets
- Apply the principle of least privilege to data export operations; only include data the requesting user had legitimate visibility into
- Add audit logging for access to privacy-restricted content to detect and investigate suspicious patterns

## Variant hunting
Check if other 'like' or engagement endpoints (retweet, reply, bookmark) have similar authorization bypass issues with restricted tweets
Test whether private/protected account tweets can be liked by non-followers through the same API endpoint
Investigate if data export includes other restricted content (DMs, archived tweets, blocked user data) without proper visibility validation
Probe whether the vulnerability extends to other social features like adding tweets to collections or lists
Test if tweet metadata (view count, like count from Circles) leaks through public endpoints for Circle-restricted tweets
Check if the vulnerability exists in API v1.1, v2, and GraphQL implementations with different parameter structures

## MITRE ATT&CK
- T1190
- T1566
- T1087
- T1589

## Notes
The vulnerability is particularly subtle because the attack vector requires patience (24-hour wait for data export) and doesn't trigger obvious security alerts. The researcher demonstrated strong methodology by understanding the complete attack surface beyond the immediate endpoint response. Twitter's data export feature, while a privacy-positive feature in principle, inadvertently amplified the impact of the broken access control vulnerability by including unauthorized content without re-validation. The report suggests potential for large-scale exploitation if attackers can enumerate Circle tweet IDs.

## Full report
<details><summary>Expand</summary>

**Description:** 
Hi,

Twitter Circle is a new feature that allows posting tweets to a specific group selected by the user. However, I noticed any user can like the Twitter Circle tweets by modifying the "like" request.

That's our request to like a tweet :

████

If you change the tweet ID to a Twitter Circle tweet, you're able to like it. That's a bug, but it doesn't have a considerable impact because we cannot see the tweet.
I went to my profile's "Likes" tab but I also couldn't see the tweet on that page. I checked other endpoints but couldn't find anything.
Then I remembered something, on all social media platforms, we can request our data from the company. That data includes everything about our account, so I checked if Twitter has this feature, and, yes!
Twitter allows us to download our data, so I requested my data on https://twitter.com/settings/download_your_data, and waited 24 hours, then I downloaded my data archive.
In my data archive, I could see the liked Tweets, and it also contains the Twitter Circle tweet that I liked!

███

## Steps To Reproduce:

  1.Turn on your proxy program and like any tweet on Twitter
  1. You will send a POST request to the `FavoriteTweet` endpoint
  1. Change the `tweet_id` to a Twitter Circle tweet ID, it should give `200 OK` on the response.
  1. Now go to https://twitter.com/settings/download_your_data and request your data.
  1. Twitter will send an email when the data is ready, so you just need to wait until the data
  1. In the data archive, open the HTML file or check the `data/like.js` file. You will see the content of the Twitter Circle tweet that you liked.

## Impact

Twitter Circle is a feature that limits tweets to a specific group selected by the user. And the user can post sensitive things to his/her Twitter Circle group.
Any attacker can see these tweets by abusing this vulnerability. That leads to information disclosure as these tweets can contain private things.

</details>

---
*Analysed by Claude on 2026-05-24*
