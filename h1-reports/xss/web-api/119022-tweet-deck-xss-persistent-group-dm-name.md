# Tweet Deck XSS- Persistent- Group DM name

## Metadata
- **Source:** HackerOne
- **Report:** 119022 | https://hackerone.com/reports/119022
- **Submitted:** 2016-02-26
- **Reporter:** akhil-reni
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
**Hello**

Group names in tweetdeck.twitter.com aren't filtered properly, giving scope for Cross site vulnerability attacks.
Challenge I have faced while escalating the xss:
- group name can only be 9 character long.

How i bypassed it:
Set multiple group names with different payloads, which means we can craft a good lengthy xss exploit using multiple group names.

Steps to reproduce:
- Create a T

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

**Hello**

Group names in tweetdeck.twitter.com aren't filtered properly, giving scope for Cross site vulnerability attacks.
Challenge I have faced while escalating the xss:
- group name can only be 9 character long.

How i bypassed it:
Set multiple group names with different payloads, which means we can craft a good lengthy xss exploit using multiple group names.

Steps to reproduce:
- Create a Twitter DM group on twitter.com with group name ``<script>alert(1);//``
- go to https://tweetdeck.twitter.com/ to trigger the xss

Exploitation:
Group names can be changed by any user in the group
you can invite any user to https://tweetdeck.twitter.com/

Screenshot attached.

Environment : 
Works on all modern browsers

**Regards,
WeSecureApp**

</details>

---
*Analysed by Claude on 2026-05-24*
