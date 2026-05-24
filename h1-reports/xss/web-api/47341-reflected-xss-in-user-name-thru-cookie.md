# Reflected xss in user name thru cookie

## Metadata
- **Source:** HackerOne
- **Report:** 47341 | https://hackerone.com/reports/47341
- **Submitted:** 2015-02-10
- **Reporter:** 4lemon
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Imagine, that we have user A with name - name<script>alert(1)</script>
And user B
User B request a sim card and the Add authorization to user A (of course this is not the common way to exploit).
As a result we have xss thru user name in flash message thru cookie.
And (!) we got properly singed cookie with xss payload
messages="29972147bc558baf382bbeb0b829d4efec82de2f$[[\"__json_message\"\0540

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

Imagine, that we have user A with name - name<script>alert(1)</script>
And user B
User B request a sim card and the Add authorization to user A (of course this is not the common way to exploit).
As a result we have xss thru user name in flash message thru cookie.
And (!) we got properly singed cookie with xss payload
messages="29972147bc558baf382bbeb0b829d4efec82de2f$[[\"__json_message\"\0540\05425\054\"Authorization will be given to name<script>alert(1)</script> once this user confirms.\"]]"; Path=/


</details>

---
*Analysed by Claude on 2026-05-24*
