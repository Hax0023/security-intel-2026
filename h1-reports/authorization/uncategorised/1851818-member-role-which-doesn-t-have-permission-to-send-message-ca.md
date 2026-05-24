# Authorization Bypass: Member Without Message Permission Can Post via Channel Commands

## Metadata
- **Source:** HackerOne
- **Report:** 1851818 | https://hackerone.com/reports/1851818
- **Submitted:** 2023-01-30
- **Reporter:** ramsakal7582
- **Program:** Mattermost
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Authorization Bypass, Access Control, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A member role without explicit permission to post messages in a channel can bypass message restrictions by executing slash commands. The command execution endpoint (/api/v4/commands/execute) fails to properly validate channel message permissions before processing and posting command output.

## Attack scenario
1. Attacker identifies a channel where they have member role but lack 'post message' permission
2. Attacker crafts a POST request to /api/v4/commands/execute endpoint with valid channel_id and team_id
3. Attacker includes a slash command (e.g., '/echo ami') in the request body
4. Server processes the command without checking if user has message posting permissions
5. Command output is posted to the channel, bypassing access controls
6. Attacker successfully delivers unauthorized message despite lacking post permission

## Root cause
The command execution endpoint implements insufficient permission validation. While the channel's message posting restrictions are enforced for direct POST requests, the command execution pathway does not perform equivalent authorization checks before processing and posting command results to the channel.

## Attacker mindset
An attacker with limited channel access seeks to communicate in restricted channels. They recognize that command execution may have different permission enforcement than direct messaging, and exploit this discrepancy to post content where their role should prevent it.

## Defensive takeaways
- Enforce consistent permission checks across all code paths that result in posting to a channel
- Validate user permissions at the command execution handler, not just at direct message endpoints
- Implement a centralized authorization function for channel posting rather than duplicating checks
- Apply the principle of least privilege: commands should inherit the same restrictions as direct messages
- Add logging and monitoring for permission bypass attempts via command execution
- Regularly audit API endpoints for authorization inconsistencies between similar operations

## Variant hunting
Search for other endpoints that post content to channels (reactions, webhooks, bot posts, command previews) and verify they implement identical permission checks. Test whether other command types have the same bypass. Examine if similar issues exist in thread permissions, channel visibility, or other message-related features.

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1548 Abuse Elevation Control Mechanism

## Notes
This is a classic authorization bypass where different code paths implementing similar functionality have divergent security controls. The /echo command is built-in and suggests command execution permissions are overly broad. The vulnerability likely affects any slash command that generates output posted to the channel.

## Full report
<details><summary>Expand</summary>

## Summary:
Someone with a member permission who hasn't been given access to post message to the channel can post it by executing commands.

## Steps To Reproduce:

```
POST /api/v4/commands/execute HTTP/1.1
Host: test3.cloud.mattermost.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0
Accept: */*
Accept-Language: en
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
X-CSRF-Token:5 [ jkue786iyfd6dkpiq7ftisys6y
Content-Type: application/json
Content-Length: 104
Origin: https://test3.cloud.mattermost.com
Connection: close
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin

{"command":"/echo ami","channel_id":"khhnkrf5wf8yibwx8bd14s6fbw","team_id":"8jdphis493d4pbq3u1bagz643r"}
```

* Executing above command will post the message to the given channelID and TeamID when you try to reproduce it with your cookie.

## Impact

Someone who doesn't have permission to post message to the channel can still post it by executing channel commands.

</details>

---
*Analysed by Claude on 2026-05-24*
