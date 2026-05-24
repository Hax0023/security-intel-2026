# Unauthorized Access to Protected Tweets via niche.co API

## Metadata
- **Source:** HackerOne
- **Report:** 273698 | https://hackerone.com/reports/273698
- **Submitted:** 2017-10-02
- **Reporter:** eidelweiss
- **Program:** Twitter/X
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Insecure Direct Object Reference (IDOR), Information Disclosure, Authorization Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
The niche.co API fails to properly enforce Twitter's tweet privacy settings, allowing unauthenticated attackers to access protected tweets from any user who has connected their Twitter account to niche.co. By directly accessing the API endpoint with the victim's user ID, attackers can retrieve tweets that should be private, completely bypassing Twitter's tweet protection mechanism.

## Attack scenario
1. Attacker identifies a target Twitter user with protected tweets and discovers they have linked their account to niche.co
2. Attacker navigates to niche.co API endpoint `/api/v1/users/[victim_twitter_handle]` without authentication
3. API returns sensitive information including the victim's user ID and associated account references
4. Attacker constructs the posts endpoint URL using the exposed user ID and accounts parameter: `/api/v1/users/[user_id]/posts?accounts=[account_id]`
5. Attacker accesses this endpoint and receives full list of protected tweets that are invisible on Twitter's public profile
6. Attacker gains complete visibility of private tweet history without victim's consent or knowledge

## Root cause
niche.co API lacks proper authorization validation and does not respect Twitter's privacy settings. The API exposes protected content through unauthenticated endpoints without checking if the requester has permission to access the data. The vulnerability stems from a failure to implement server-side access control that mirrors Twitter's privacy configurations.

## Attacker mindset
An attacker would recognize this as a high-value information disclosure opportunity since: (1) no authentication required, (2) accessible to anyone with internet access, (3) bypasses intentional user privacy controls, (4) affects all users connected to niche.co, and (5) victim has no way to detect unauthorized access. The attacker could use this for reconnaissance, harassment, corporate espionage, or privacy violation.

## Defensive takeaways
- Implement strict server-side access control checks on all API endpoints that reflect the original platform's privacy settings
- Require authentication for all API access and validate that the requester has legitimate permission to access user data
- Never expose protected/private content in API responses regardless of user connection status to third-party services
- Implement privacy inheritance: if content is private on the original platform, it must remain private in all integrated services
- Add audit logging for API access to protected content to detect unauthorized attempts
- Implement rate limiting and behavioral analysis to detect bulk harvesting of protected content
- Establish clear OAuth scopes that explicitly exclude access to protected/private content unless user explicitly grants it
- Regular security audits of third-party integrations to ensure they respect original platform privacy controls

## Variant hunting
Search for similar issues in other niche.co API endpoints that might expose private user data. Check if niche.co has other connected social platforms (Instagram, LinkedIn, TikTok) with similar authorization bypasses. Investigate whether the accounts parameter can be manipulated to access other users' posts. Test if unauthenticated access works for other endpoints like `/users/[id]/followers`, `/users/[id]/following`, or analytics endpoints.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Exposure of Resource in Network to Unauthorized Actors
- T1497.3 - Virtualization/Sandbox Evasion
- T1589 - Gather Victim Identity Information
- T1598 - Phishing for Information

## Notes
The report demonstrates good responsible disclosure practice by using the researcher's own account as the victim. The vulnerability is particularly severe because it requires no authentication, no special privileges, and provides complete bypass of Twitter's core privacy feature. The fact that attackers don't need a Twitter or niche.co account increases the potential attack surface significantly. This is a classic example of improper access control in third-party integrations that don't adequately mirror security controls from the primary platform.

## Full report
<details><summary>Expand</summary>

Hello,

**Summary:**
Normally If user __(victim)__ set to private / protect their tweets in setting Tweet privacy, other people/user will not able to see their recent or their pass status/twits when they visit his/her __(victim)__ profile. people only can see their __(victim)__ profile images and information about __how many tweet already post by that user__ , __how many followers and following by that account__ and __how many likes__ etc etc. but i found a way to view the protected tweets from other user who protect their tweets.


**Description:** 
in your policy i see there is new domain add as in scope target , and the domain is `niche.co` .
there is some condition needed to success reproduce this vulnerability:
1. the __victim__ need to connect their twitter account with `niche.co`
2. use the `niche.co` API to Access the Protected Tweets

## Steps To Reproduce:
_victim side_
 * victim account is `https://twitter.com/dummysystems`
  * lets say the victim already set to protect his/her tweets via `https://twitter.com/settings/safety`
{F225673}
  * now when other user try to visit victim profile it will look like this
{F225670}
  * now visit `https://www.niche.co/get-started` and chose twitter , allow and or Authorize Niche to use your account and complete the rest (including confirming your email address).

_attacker side_
  1. attacker no need to have twitter account and or no need to have `Niche` account here , this made the severity is high
  1. just visit `https://www.niche.co/api/v1/users/[victim_twitter_account]` ( in this case the victim is https://www.niche.co/api/v1/users/dummysystems , the attacker will show some important information disclosure regarding the victim account
   {F225668}
  1. scroll down the page till you see something like this `/users/52667/posts?accounts=162059`
  {F225669}
  1. and open it, so the full URI will become `https://www.niche.co/api/v1//users/52667/posts?accounts=162059`
  1. and BOOM! the attacker now have Access to Protected Tweets from victim account.
{F225671}
{F225672}

**noted**
to follow the rules, I use my own account as the __victim__, so there is no other / real account has been compromised.


Regards,

</details>

---
*Analysed by Claude on 2026-05-24*
