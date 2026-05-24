# Stored XSS on https://apps.topcoder.com/wiki/pages/editpage.action

## Metadata
- **Source:** HackerOne
- **Report:** 867133 | https://hackerone.com/reports/867133
- **Submitted:** 2020-05-06
- **Reporter:** meryem0x
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi :) There is a stored XSS on wiki pages and it executes when editing page.

## Steps To Reproduce:
After I submitted #867125, i realized that the vote macro causes stored XSS on wiki edit page. 
A user can edit wiki pages on https://apps.topcoder.com/wiki/pages/editpage.action?pageId=. Users can insert macros to pages. Vote macro is vulnerable to XSS. 

Go to a wiki page, edit it and

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

## Summary:
Hi :) There is a stored XSS on wiki pages and it executes when editing page.

## Steps To Reproduce:
After I submitted #867125, i realized that the vote macro causes stored XSS on wiki edit page. 
A user can edit wiki pages on https://apps.topcoder.com/wiki/pages/editpage.action?pageId=. Users can insert macros to pages. Vote macro is vulnerable to XSS. 

Go to a wiki page, edit it and type

```
{vote:What is your favorite vulnerability?}
RCE
SSRF
XSS"><img src=X onerror=alert(document.domain)>
{vote}
```
and save it. When an other user edit this page, XSS will execute.

PoC:
https://apps.topcoder.com/wiki/pages/editpage.action?pageId=165871793
{F817588}

Note: This only works to signed-in users. Because unauthorized users cannot edit pages. I think there is a mistake on https://apps.topcoder.com/wiki/login.action now. If you encounter an error, you can login on main site (https://accounts.topcoder.com/member) then try.

## Impact

XSS can use to steal cookies or to run arbitrary code on victim's browser.

</details>

---
*Analysed by Claude on 2026-05-24*
