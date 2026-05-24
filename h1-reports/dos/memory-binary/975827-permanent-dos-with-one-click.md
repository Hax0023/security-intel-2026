# Permanent DoS with one click - Account deletion leaves orphaned messages causing victim account unusability

## Metadata
- **Source:** HackerOne
- **Report:** 975827 | https://hackerone.com/reports/975827
- **Submitted:** 2020-09-06
- **Reporter:** try_to_hac
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Denial of Service, Data Integrity Issue, Improper Error Handling, Cascade Delete Failure
- **CVEs:** None
- **Category:** memory-binary

## Summary
When a user deletes their account, messages they sent to other users become orphaned references that cause a permanent Denial of Service for the recipient. The victim's account becomes completely unusable after the attacker deletes their account, preventing any further platform interaction.

## Attack scenario
1. Attacker creates an account and sends a message to the victim's account
2. Attacker deletes their account, triggering account deletion logic
3. System fails to properly handle or cascade delete the sent messages
4. Victim logs into their account to check messages
5. System attempts to load/render the orphaned message reference
6. Application crashes or becomes permanently unusable for the victim due to broken data references

## Root cause
Improper cascade delete or cleanup logic during account deletion. When a user deletes their account, the application fails to properly handle messages authored by that deleted user. This results in orphaned foreign key references or corrupt data that breaks the messaging system for recipients, likely causing application errors when attempting to display the inbox.

## Attacker mindset
Low-effort griefing attack requiring minimal technical skill. Attacker recognizes that the application doesn't properly validate or clean up message references after account deletion, allowing permanent disruption of victim accounts through a simple two-step attack requiring only knowledge of the victim's account.

## Defensive takeaways
- Implement proper cascade delete or soft delete strategies for user accounts
- Ensure all foreign key constraints are properly defined in the database schema
- Handle orphaned or deleted-user messages gracefully (display as 'deleted user' or remove entirely)
- Add referential integrity tests to catch orphaned data scenarios
- Implement comprehensive data cleanup procedures before account deletion completes
- Use database transactions to ensure account deletion is atomic and complete
- Add validation checks to prevent account state transitions that leave orphaned data
- Implement monitoring/alerting for orphaned data references

## Variant hunting
Test other user-generated content deletion (comments, posts, files) for similar cascade delete issues
Verify if sharing features with deleted users cause similar DoS
Test group/channel memberships when moderator/creator deletes account
Check notifications/mentions system for broken references from deleted users
Test collaborative features (shared documents, projects) with account deletion
Verify friend/follower lists don't break when one user deletes account

## MITRE ATT&CK
- T1499.4 - Application Exhaustion
- T1499 - Endpoint Denial of Service
- T1531 - Account Access Removal

## Notes
One-click attack requiring only knowledge of victim's identifier and the ability to create an account. No authentication bypass or privilege escalation needed. High impact despite low complexity. Report demonstrates the vulnerability with clear reproduction steps and video PoC. The vulnerability affects account availability and usability rather than data confidentiality.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello Team, messages of a user who deletes their account leave DoS effects on another user.


## Platform(s) Affected:
[website/mobile app/service]

## Steps To Reproduce & PoC:
Before you start testing, create two accounts.
cyanpiny+attacker@gmail.com
cyanpiny+victim@gmail.com
Confirm e-mails to send messages.

  1. Log into the attacker's account.
  2. Message the victim from the attacker's account.
  3. Delete the attacker's account.
  4. Log into the victim's account.
  5. Check the victim's message box.
  6. The victim cannot use the account again.

Video:
{F978195}

## Impact

The victim cannot use the account again.

</details>

---
*Analysed by Claude on 2026-05-24*
