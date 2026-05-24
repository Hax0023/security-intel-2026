# Multiple XSS in Camptix Event Ticketing Plugin

## Metadata
- **Source:** HackerOne
- **Report:** 152958 | https://hackerone.com/reports/152958
- **Submitted:** 2016-07-21
- **Reporter:** thezawad
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,
As discussed in #151561 submitting the report here.

I have got some more bugs in Camptix Event Ticketing plugin.

Well, the first one is a ticket page xss caused by the **Ticket Title**
And the second one is kind of self-xss, caused by also the **Ticket title** of the plugin but in the coupons page.
I have added a video *PoC* for your clarification with step by step reproduction.
As I have se

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

Hi,
As discussed in #151561 submitting the report here.

I have got some more bugs in Camptix Event Ticketing plugin.

Well, the first one is a ticket page xss caused by the **Ticket Title**
And the second one is kind of self-xss, caused by also the **Ticket title** of the plugin but in the coupons page.
I have added a video *PoC* for your clarification with step by step reproduction.
As I have seen in #9391 you've fixed self-xss, I have created this report.

I think both of the bugs should be fixed.

I expect you fix both of them.


https://drive.google.com/open?id=0B0Ah8VhxGMynZXUwbGlaMm5iVDQ


--------
Zawad


</details>

---
*Analysed by Claude on 2026-05-24*
