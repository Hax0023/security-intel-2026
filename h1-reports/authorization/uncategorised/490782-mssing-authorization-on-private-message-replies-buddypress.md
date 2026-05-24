# Missing Authorization on Private Message Replies (BuddyPress)

## Metadata
- **Source:** HackerOne
- **Report:** 490782 | https://hackerone.com/reports/490782
- **Submitted:** 2019-02-03
- **Reporter:** klmunday
- **Program:** BuddyPress
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Missing Authorization Check, Broken Access Control, AJAX Action Authorization Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An authenticated attacker can reply to private message threads they are not a participant of by manipulating the thread_id parameter in the messages_send_reply AJAX action. While the attacker cannot view or track their injected messages, legitimate thread participants see the unauthorized replies, enabling spam and phishing attacks.

## Attack scenario
1. Attacker authenticates to BuddyPress site with valid account
2. Attacker identifies a private message thread they are not part of (thread_id=N)
3. Attacker crafts POST request to /wp-admin/admin-ajax.php with action=messages_send_reply and arbitrary thread_id parameter
4. Attacker includes malicious content, valid CSRF nonce, and their session cookie
5. Server processes request without verifying attacker is thread participant
6. Malicious message appears in legitimate participants' thread, visible to all members

## Root cause
The messages_send_reply AJAX action fails to verify that the authenticated user is an authorized participant of the target thread before accepting and processing reply messages. Authorization checks likely only validate that a user is authenticated (logged in) rather than checking thread membership.

## Attacker mindset
An attacker would recognize this as a mass messaging/spam vector. The attacker methodically develops an automated exploitation script to inject messages into all discoverable private message threads sequentially, maximizing reach for phishing or spam campaigns. The attacker understands the UI limitations (no visibility in their own inbox) don't prevent message delivery to legitimate participants.

## Defensive takeaways
- Implement explicit authorization checks verifying user participation in thread before accepting reply submissions
- Query user's thread membership from database: verify user_id exists in thread participants before processing messages_send_reply action
- Apply authorization validation consistently across all template packs (Legacy and Nouveau)
- Add server-side validation that thread_id references an actual thread the current user participates in
- Consider additional checks: verify thread is not archived/deleted, verify user hasn't been removed from thread
- Log suspicious AJAX requests attempting to reply to threads user doesn't participate in
- Implement rate limiting on messages_send_reply AJAX action to mitigate automated abuse

## Variant hunting
Check messages_send_private_message action for similar authorization bypass
Audit other AJAX actions in BuddyPress messaging component (messages_delete_thread, messages_star_message, etc.) for authorization issues
Review user profile update/delete AJAX actions for parameter tampering vulnerabilities
Test group messaging features for similar thread_id based authorization bypasses
Examine notification-related AJAX calls for improper authorization checks
Check if activity/stream components have similar issues with object_id parameter manipulation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1566 - Phishing
- T1537 - Transfer Data to Cloud Account

## Notes
Reporter notes this is particularly concerning when combined with other vulnerabilities (referenced #487081). The lack of visibility in attacker's inbox represents a UI-level control failure but doesn't prevent abuse. The sequential thread_id enumeration suggests BuddyPress uses predictable identifiers. Automated exploitation script provided demonstrates practical abuse potential. Both Legacy and Nouveau template packs affected indicates vulnerability is in core messaging logic, not template-specific code.

## Full report
<details><summary>Expand</summary>

## Description:
Users can reply to private message threads which they are not participants of by changing the `thread_id` parameter in the `messages_send_reply` ajax action. This affects both the Legacy and Nouveau Template packs.

## Steps To Reproduce:
1. Login to your account
2. Send the following request (change `Host`/`Cookie`/`nonce`/`thread_id` as needed)

>POST /wp-admin/admin-ajax.php HTTP/1.1
>Host: 127.0.0.1
>User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0
>Accept: */*
>Accept-Language: en-GB,en;q=0.5
>Accept-Encoding: gzip, deflate
>Referer: http://127.0.0.1/members/test2/messages/view/4/
>Content-Type: application/x-www-form-urlencoded; charset=UTF-8
>X-Requested-With: XMLHttpRequest
>Content-Length: 76
>Connection: close
>Cookie: >wordpress_ab0994624b8d5b17fddb1aec29329218=test2%7C1549395197%7ClRQfd96VkhuRpR4fpB3MhZOw2SGrl19nFG7wIClGYaf%7C64fbdf07238d2f448b8e53f6f1db7c64b014d7833386229505fefa70c9b2976e; wordpress_test_cookie=WP+Cookie+check; >wordpress_logged_in_ab0994624b8d5b17fddb1aec29329218=test2%7C1549395197%7ClRQfd96VkhuRpR4fpB3MhZOw2SGrl19nFG7wIClGYaf%7Ca309bfd19a1c2e4504e37959bd4ceac28944fce81857c2f7587022a4e6d2b7aa

>action=messages_send_reply&cookie=&_wpnonce=d037f67211&content=Test+Message&thread_id=1

## Notes:
Even though an attacker can send a reply to a thread, they cannot view the thread afterwards. The reply they send does not appear in the attackers sentbox (see image below)
{F417446}
Nor do any future replies appear in the attackers inbox, nor is the attacker able to star the reply. This means that there is no information exposure.

When participants view the thread they will see the attackers reply, however the attacker does not appear in the participants list (see images below)

__Inbox:__
{F417451}
__View:__
{F417444}

## Proof of Concept:
I have developed a small Python (3.6+) script to inject a message into every private message thread. It achieves this by creating a new conversation between the attacker and himself to get the current private message max index and then iterates from 1 -> max index, posting a message into each thread.
{F417456}
It will try to reply to threads that may have been deleted but since thread_id's are sequential, if every thread from 1 to the thread the attacker created is replied to then we can be sure that every thread that exists when the script is ran has been injected into.

## Impact

Just by itself this can only really lead to spam / phishing attacks. However, if the component is vulnerable to other flaws such as #487081 (not public) then it can widen an attack surface and becomes a more serious issue.

</details>

---
*Analysed by Claude on 2026-05-24*
