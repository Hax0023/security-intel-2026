# Privilege Escalation: Posting in Channel Without Required Permissions via Request Replay

## Metadata
- **Source:** HackerOne
- **Report:** 1114617 | https://hackerone.com/reports/1114617
- **Submitted:** 2021-03-02
- **Reporter:** fuzzsqlb0f
- **Program:** Mattermost
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Privilege Escalation, Broken Access Control, Insecure Direct Object References (IDOR), Missing Authorization Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A user can post comments in a channel where they lack permission by replaying an authenticated POST request captured from a channel where they had posting privileges. The application fails to re-validate channel-specific permissions on each comment submission, allowing privilege escalation through request replay.

## Attack scenario
1. Attacker joins a public channel where they have posting permissions and creates a test message
2. Attacker intercepts the POST request used to create the message and stores it in a proxy repeater tool
3. Channel owner revokes the attacker's posting permissions via System Console > Channel > Permissions
4. Attacker receives 'This channel is read only' error when attempting to post normally through the UI
5. Attacker replays the captured POST request from step 2, modifying only the channel ID to target a restricted channel
6. The server processes the request and posts the comment despite the attacker lacking permissions in the target channel

## Root cause
The application performs initial authorization checks (likely during request routing or UI rendering) but does not re-validate channel-specific posting permissions when processing the actual POST request that creates the message. The server trusts the authenticated session without verifying real-time permission state at message creation time.

## Attacker mindset
An attacker with access to intercept requests recognizes that permission checks may be performed inconsistently across the request lifecycle. By capturing a valid request from an authorized context and replaying it against restricted channels, they can bypass permission enforcement and post content where restricted.

## Defensive takeaways
- Implement server-side permission checks at message creation time, not just at UI/routing layer
- Validate channel-specific permissions for every POST request, even if the user is authenticated
- Use server-generated tokens or nonces that are bound to specific actions and channels to prevent replay attacks
- Log all permission checks and their results for security auditing
- Implement rate limiting and anomaly detection on comment creation requests
- Ensure permission state is checked immediately before database write operations
- Add integrity validation to prevent request tampering (CSRF tokens, HMAC signatures)

## Variant hunting
Test other channel operations (pin message, delete message, edit message) with captured requests from authorized contexts
Attempt to post in private channels after capturing a request from a public channel
Test permission bypass on direct messages and group chats
Verify if reactions, file uploads, and mentions can be similarly exploited
Check if guest users can escalate to member-level operations through request replay
Test cross-workspace permission escalation if applicable
Attempt to modify message content or metadata using replayed requests with altered payloads

## MITRE ATT&CK
- T1078 - Valid Accounts (leveraging legitimate session)
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism (privilege escalation)
- T1556 - Modify Authentication Process
- T1566 - Phishing (indirect, if posting malicious content)

## Notes
The report indicates the issue was reproduced in mattermost.cloud with video evidence. The vulnerability appears to stem from separation of authorization concerns between UI/routing layer and business logic layer. Request replay attacks are effective because the server does not implement request idempotency or binding tokens.

## Full report
<details><summary>Expand</summary>

Hi H1,

mattermost.cloud has a feature of making a channel and once its set to public any other user can join the channel and post comments on that channel. In System Console --> Channel --> Permission channel owner can assign wether member can post comment or not. Once channel owner selects that channel member can not post even than they can post the comment in channel.


Steps To Reproduce:


- Step1: user1 `█████` created a channel which is public and under System Console --> Channel --> Permission gives guest and members to post comment.

- Step2: user2 `█████` joined user1 channel `mikefourchannel`  (already joined)

- Step3: user2 posted comment `has permission to comment in channel` in `mikefourchannel`  and captured the request and send it to repeater (

- Step3: user2 `███████` also created a channel `privilegeescalation` (already done)

- Step4: user1 `█████` and under System Console --> Channel --> Permission  guest and members removes right to comment.

- Step5: user2 `████████` now can not post any comment `This channel is read only. Only members with permission can post here`

- Step6: user2 `██████` goes to channel `privilegeescalation` and posted comment and captures the request and used post request which was captured in `Step3`

Note:
In video POC at time 0:01:42 user2 commenting when he was having privilege of commenting in channel and there is only that comment `has permission to comment in channel` below there is no other comment now plz go to time 0:04:29  you can see user2 commented `commenting in mike4 channel even no privielge` in user1 channel without proper privileges

Video POC attached for your reference.

Result:

user2 `███` posted comment in user1 channel `mikefourchannel` even user2 dosen't have privilege to do so.

## Impact

Impact:

Privilege escalation leading to comment on channel.

</details>

---
*Analysed by Claude on 2026-05-24*
