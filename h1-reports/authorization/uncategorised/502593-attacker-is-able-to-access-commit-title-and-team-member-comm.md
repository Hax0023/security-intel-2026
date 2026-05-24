# Private Commit Titles and Team Comments Exposed via Email Notifications

## Metadata
- **Source:** HackerOne
- **Report:** 502593 | https://hackerone.com/reports/502593
- **Submitted:** 2019-02-27
- **Reporter:** yashrs
- **Program:** Unknown (GitLab or similar platform based on context)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Improper Access Control, Authorization Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker can subscribe to email notifications for a victim's profile and receive notifications containing private commit titles and team member comments from internal projects, bypassing the intended access controls. The vulnerability allows unauthorized users to view sensitive information that should only be visible to team members despite proper visibility settings being configured.

## Attack scenario
1. Attacker creates an account and identifies a target victim's profile on the platform
2. Attacker navigates to victim's profile and subscribes to all events from the victim
3. Victim creates or works with an internal project with visibility restricted to 'Only Team Members'
4. Victim or team members comment on commits within the internal project
5. Platform sends email notifications to attacker containing full commit titles and comment contents
6. Attacker gains unauthorized access to sensitive project information despite not being a team member

## Root cause
The notification system does not properly enforce repository access control checks before sending email notifications. When a user subscribes to another user's events, the platform sends notifications without verifying whether the subscriber has permission to view the referenced content. The visibility settings applied to the project are not considered during the email notification generation process.

## Attacker mindset
An attacker with basic technical knowledge can perform reconnaissance on target organizations by subscribing to developers' profiles, systematically harvesting internal project information, commit messages, and team discussions without requiring legitimate access or team membership. This is a low-effort, high-reward reconnaissance technique.

## Defensive takeaways
- Implement pre-send authorization checks for all notifications to verify subscriber has access to the referenced resource
- Enforce repository visibility settings consistently across all notification channels (UI, email, webhooks, API)
- Sanitize or redact sensitive content in notifications when full access cannot be verified
- Implement rate limiting and monitoring on event subscription functionality to detect suspicious behavior
- Add audit logging for cross-user event subscriptions
- Require explicit permission or team membership before sending notifications containing private project data
- Regularly test notification systems with privilege boundary testing

## Variant hunting
Check if other notification channels (Slack, Webhook, RSS) have similar authorization bypass
Test if watching/starring a private repository bypasses visibility controls in notifications
Verify if subscribing to organization events exposes private project information
Check if email digest summaries properly filter inaccessible projects
Test if API endpoints used for notifications properly validate access controls
Verify team member list visibility in notifications from private projects

## MITRE ATT&CK
- T1190
- T1199
- T1526
- T1087

## Notes
This is a classic authorization bypass where one security control (project visibility settings) is bypassed through an uncontrolled notification pathway. The vulnerability is particularly effective because email notifications are often trusted and users may not expect them to be a information disclosure vector. The bug required two accounts but could be automated at scale for reconnaissance.

## Full report
<details><summary>Expand</summary>

**Summary:** [add summary of the vulnerability]

**Description:** [add more details about this vulnerability]

## Steps To Reproduce:

To reproduce this vulnerability, we need two accounts, lets say those accounts are:
-> victim@gmail.com
-> attacker@gmail.com

- Create a project from account victim@gmail.com with the following permissions:
{F432203}
Note that the project visibility should be `internal`.

- Go to profile of `victim@gmail.com` from `attacker@gmail.com`  and subscribe to all events, like this:
{F432204}

- From victim account, comment on any commit, and you should receive it's notification on attacker@gmail.com, like this:
{F432207}

As you can see, the message of the commit, team members who commented, what the comment was, everything is visible from the email received. This shouldn't be sent via email because the settings selected for repository is 'Only Team Members' whereas attacker@gmail.com is not a team member.

I have tried my best to have perfect steps to reproduce this, still do tell me if you need more info :)

Thanks,
Yash :)

## Impact

An attacker will be able to view any commit titles, and all comments which shouldn't be visible to him using this vulnerability

</details>

---
*Analysed by Claude on 2026-05-24*
