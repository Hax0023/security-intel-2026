# html injection via invite members can be leads account takeover 

## Metadata
- **Source:** HackerOne
- **Report:** 1443567 | https://hackerone.com/reports/1443567
- **Submitted:** 2022-01-07
- **Reporter:** unnamedx
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** CVE-2022-1002
- **Category:** web-api

## Summary
Hi team,
I have found an vulnerability on your website .
step to reproduce :
1.navigate to : yourworkspace.cloud.mattermost.com
2.create new channel F1571445
3.there you will find a functionality invite members F1571448
4.click on invite members 
5 input your email address 
6.scroll down & click on invite as guest F1571456
7. on Add to channels input your channel name 
8.click on set a custom mess

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

Hi team,
I have found an vulnerability on your website .
step to reproduce :
1.navigate to : yourworkspace.cloud.mattermost.com
2.create new channel F1571445
3.there you will find a functionality invite members F1571448
4.click on invite members 
5 input your email address 
6.scroll down & click on invite as guest F1571456
7. on Add to channels input your channel name 
8.click on set a custom message , input this html payloads : <a href=evil.com>click</a>
<input type=x>
9. invite 
10.open inbox of  email that you have invited
as you can see  html injected & there's an input field & click button 

follow my video poc for better understanding & if you need any info let me know .
thanks for reading my report .God bless you

## Impact

As HTML injection worked in email an attacker can trick victim to click on such hyperlinks to redirect him to any malicious site and also can host a XSS page. All this will surely cause some damage to victim. This could lead to users being tricked into giving logins away to malicious attackers.

</details>

---
*Analysed by Claude on 2026-05-24*
