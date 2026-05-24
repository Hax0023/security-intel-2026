# Unauthenticated User Information Disclosure via JSON API

## Metadata
- **Source:** HackerOne
- **Report:** 152499 | https://hackerone.com/reports/152499
- **Submitted:** 2016-07-20
- **Reporter:** amirisme
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Improper Access Control, Missing Authentication
- **CVEs:** None
- **Category:** web-api

## Summary
The Nextcloud help forum exposes sensitive user profile information through an unauthenticated JSON API endpoint. Any attacker can enumerate user profiles, last activity timestamps, email information, and other personally identifiable details by accessing /users/<username>.json without authentication. This allows complete enumeration of all forum users and their activity patterns.

## Attack scenario
1. Attacker identifies the /users/<username>.json endpoint structure on help.nextcloud.com
2. Attacker systematically enumerates usernames through the forum or by brute-forcing common patterns
3. Attacker requests /users/<username>.json for each discovered username
4. Sensitive data is returned including user IDs, real names, avatar URLs, last activity times, trust levels, and group memberships
5. Attacker compiles comprehensive user database with activity patterns and profile information
6. This information can be used for targeted social engineering, account targeting, or activity correlation attacks

## Root cause
The API endpoint lacks proper authentication and authorization checks. The endpoint appears to be part of a Discourse forum installation integrated with Nextcloud. No access control validation is performed before returning user profile data in JSON format.

## Attacker mindset
An attacker would view this as a goldmine for user enumeration and reconnaissance. The ability to passively gather detailed user information without authentication enables profiling for social engineering campaigns, identifies active administrators/moderators, and reveals user activity patterns useful for timing targeted attacks.

## Defensive takeaways
- Implement authentication requirements for all user profile API endpoints
- Apply authorization checks to ensure users can only view permitted profile information
- Restrict sensitive fields (last_seen_at, last_posted_at, email) to authenticated users or user themselves
- Consider rate limiting on enumeration-friendly endpoints to prevent mass user discovery
- Audit all public API endpoints for unintended information disclosure
- Configure forum software to require authentication for user profile access by default
- Implement principle of least privilege for public API responses

## Variant hunting
Check for similar JSON endpoints: /users.json, /admin/users.json, /api/users/*
Test other Discourse/forum installations for the same pattern
Look for additional endpoints exposing user activity: /posts.json, /groups.json
Check if group memberships reveal sensitive organizational information
Test for timing-based user enumeration via response timing differences
Verify if deleted users or suspended accounts still return profile data
Check for PII in other profile fields: website_name, custom_fields, title

## MITRE ATT&CK
- T1590.002 - Gather Victim Identity Information: Email Addresses
- T1592 - Gather Victim Host Information
- T1598 - Phishing for Information
- T1589.001 - Gather Victim Identity Information: Credentials
- T1087 - Account Discovery

## Notes
This vulnerability was reported against help.nextcloud.com specifically, suggesting it may be a Discourse forum instance. The reporter provided clear proof of concept with actual user data. The vulnerability is a classic example of an improperly secured API endpoint that assumes security through obscurity rather than implementing proper access controls. The inclusion of timestamps (last_seen_at, last_posted_at) is particularly concerning as it reveals user activity patterns.

## Full report
<details><summary>Expand</summary>

Hello Nextcloud

go to https://help.nextcloud.com/users/<anyusername>.json
for example https://help.nextcloud.com/users/amirie.json

you can see the user information 


    {"user_badges":[{"id":1999,"granted_at":"2016-07-20T11:09:52.983Z","count":1,"badge_id":9,"user_id":1007,"granted_by_id":-1}],"badges":[{"id":9,"name":"Autobiographer","description":"Filled out <a href=\"/my/preferences\">profile</a> information","grant_count":46,"allow_title":false,"multiple_grant":false,"icon":"fa-certificate","image":null,"listable":true,"enabled":true,"badge_grouping_id":1,"system":true,"slug":"autobiographer","badge_type_id":3}],"badge_types":[{"id":3,"name":"Bronze","sort_order":7}],"users":[{"id":1007,"username":"amirie","avatar_template":"/user_avatar/help.nextcloud.com/amirie/{size}/621_1.png","name":"amirezat","moderator":false,"admin":false},{"id":-1,"username":"system","avatar_template":"/user_avatar/help.nextcloud.com/system/{size}/1_1.png","name":"system","moderator":true,"admin":true}],"user":{"id":1007,"username":"amirie","avatar_template":"/user_avatar/help.nextcloud.com/amirie/{size}/621_1.png","name":"amirezat","last_posted_at":"2016-07-20T11:10:10.064Z","last_seen_at":"2016-07-20T11:11:14.995Z","created_at":"2016-07-17T21:56:22.016Z","website_name":"help.nextcloud.com/users/amirie/preferences","can_edit":false,"can_edit_username":false,"can_edit_email":false,"can_edit_name":false,"can_send_private_messages":false,"can_send_private_message_to_user":false,"trust_level":0,"moderator":false,"admin":false,"title":null,"uploaded_avatar_id":621,"badge_count":1,"custom_fields":{},"pending_count":0,"profile_view_count":1,"invited_by":null,"groups":[{"id":10,"automatic":true,"name":"trust_level_0","user_count":903,"alias_level":0,"visible":true,"automatic_membership_email_domains":null,"automatic_membership_retroactive":false,"primary_group":false,"title":null,"grant_trust_level":null,"has_messages":false,"mentionable":false}],"featured_user_badge_ids":[1999],"card_badge":null}}
Best Regards,
Amir.


</details>

---
*Analysed by Claude on 2026-05-24*
