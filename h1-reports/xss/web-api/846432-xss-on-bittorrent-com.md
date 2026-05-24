# xss on bittorrent.com

## Metadata
- **Source:** HackerOne
- **Report:** 846432 | https://hackerone.com/reports/846432
- **Submitted:** 2020-04-10
- **Reporter:** aslanemre
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
hi team 
i realized xss bug on  headers.php.

https://www.bittorrent.com/scripts/site/headers.php?_=1586521900793&callback=<PAYLOAD>
https://www.bittorrent.com/scripts/social/get_tweet.php?_=1586521900791&callback=<PAYLOAD>
its works on IE browsers.

## Impact

fix them

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

hi team 
i realized xss bug on  headers.php.

https://www.bittorrent.com/scripts/site/headers.php?_=1586521900793&callback=<PAYLOAD>
https://www.bittorrent.com/scripts/social/get_tweet.php?_=1586521900791&callback=<PAYLOAD>
its works on IE browsers.

## Impact

fix them

</details>

---
*Analysed by Claude on 2026-05-24*
