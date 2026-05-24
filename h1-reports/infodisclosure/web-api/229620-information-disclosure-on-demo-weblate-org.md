# Information Disclosure on demo.weblate.org

## Metadata
- **Source:** HackerOne
- **Report:** 229620 | https://hackerone.com/reports/229620
- **Submitted:** 2017-05-18
- **Reporter:** sp1d3rs
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
##Description
The demo instance, located on https://demo.weblate.org is leaking user's IP-adresses in the Activity log.
{F185728}

##Impact
The authenticated user can disclose valid IP adresses of other users through Activity log. The feature works as it should (*so no changes should be made on the GitHub or other sites like hosted.weblate.org*), but i still recommend you to hide IPs that do not b

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

##Description
The demo instance, located on https://demo.weblate.org is leaking user's IP-adresses in the Activity log.
{F185728}

##Impact
The authenticated user can disclose valid IP adresses of other users through Activity log. The feature works as it should (*so no changes should be made on the GitHub or other sites like hosted.weblate.org*), but i still recommend you to hide IPs that do not belong to the user only on this particular instance, because user do not know before login, that his IP will become accessible to the public.

##Reproduction Steps
1) Login at the https://demo.weblate.org as demo:demo
2) Go to the https://demo.weblate.org/accounts/profile/#audit

##Suggested fix
The sensitive information can be hided in various ways - for example `x.x.x.x` or similar. It do not require code changes on your GitHub repositories, just in this particular instance.


</details>

---
*Analysed by Claude on 2026-05-24*
