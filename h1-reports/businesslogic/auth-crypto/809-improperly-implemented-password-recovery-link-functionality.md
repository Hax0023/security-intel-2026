# Improperly implemented password recovery link functionality

## Metadata
- **Source:** HackerOne
- **Report:** 809 | https://hackerone.com/reports/809
- **Submitted:** 2014-01-27
- **Reporter:** dawidczagan
- **Program:** Unknown
- **Bounty:** $300
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
I took a look at live install of Phabricator (https://secure.phabricator.com/) and noticed, that the user gets automatically logged in after clicking the password recovery link (this link is sent to the user's mail). This authentication takes place before the user is asked to enter a new password twice. This can be used be the attacker to log in a user to the attacker's account - the attacker gene

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

I took a look at live install of Phabricator (https://secure.phabricator.com/) and noticed, that the user gets automatically logged in after clicking the password recovery link (this link is sent to the user's mail). This authentication takes place before the user is asked to enter a new password twice. This can be used be the attacker to log in a user to the attacker's account - the attacker generates a password recovery link to his account, sends it to the user and the user becomes logged in to the attacker's account, when he clicks the link delivered by the attacker.

</details>

---
*Analysed by Claude on 2026-05-24*
