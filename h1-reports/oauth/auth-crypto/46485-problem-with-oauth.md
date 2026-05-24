# Problem with OAuth

## Metadata
- **Source:** HackerOne
- **Report:** 46485 | https://hackerone.com/reports/46485
- **Submitted:** 2015-02-04
- **Reporter:** sandeep10092819
- **Program:** Unknown
- **Bounty:** $1,260
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
There are many website that tracks the unfollowers and all like:
http://unfollowerstats.com
[Steps]:
1. Login with ur twitter account, i.e. abcd@mail.com
2. Open http://unfollowerstats.com, This will ask you to login with twitter:
3. you will get a link like this:
https://api.twitter.com/oauth/authenticate?oauth_token=xpXP21WOzwvsocu7yjQBafl8BKRtKdeH

4.
Open Another browser and login wit

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

There are many website that tracks the unfollowers and all like:
http://unfollowerstats.com
[Steps]:
1. Login with ur twitter account, i.e. abcd@mail.com
2. Open http://unfollowerstats.com, This will ask you to login with twitter:
3. you will get a link like this:
https://api.twitter.com/oauth/authenticate?oauth_token=xpXP21WOzwvsocu7yjQBafl8BKRtKdeH

4.
Open Another browser and login with some other user i.e. : xyz@mail.com
5.
Open this  oAuth link(https://api.twitter.com/oauth/authenticate?oauth_token=xpXP21WOzwvsocu7yjQBafl8BKRtKdeH) on the other browser
6. 
Authorize this OAuth with user xyz@mail.com

7. Go to the first browser, and refresh the page and continue to authorize. You will be logged into http://unfollowerstats.com with xyz@mail.com user


-- Tested with 2 such websites


</details>

---
*Analysed by Claude on 2026-05-24*
