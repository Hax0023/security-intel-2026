# Stored XSS in assets.txmblr.com

## Metadata
- **Source:** HackerOne
- **Report:** 870703 | https://hackerone.com/reports/870703
- **Submitted:** 2020-05-11
- **Reporter:** keer0k
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
# Description

Hi, i would like to report a issue that i think is legitimate. to get this XSS we need to create a Post in the attacker account with a payload, after this, it's necessary that a victim reblog this post and so, enter in the edit mode of their own blog, after this the victim will see a button with "CLICK ME" value, so, when the victim click in "CLICK ME" the XSS will be triggerd.

PoC

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

# Description

Hi, i would like to report a issue that i think is legitimate. to get this XSS we need to create a Post in the attacker account with a payload, after this, it's necessary that a victim reblog this post and so, enter in the edit mode of their own blog, after this the victim will see a button with "CLICK ME" value, so, when the victim click in "CLICK ME" the XSS will be triggerd.

PoC payload:
```
<form>
<input type=submit formaction=javascript:alert(document.domain)>
</form>
```

# Steps to reproduce
1. go to your account
2. create a post with the payload mentioned before
3. victim reblog the post
4. victim enter in the edit mode of their own blog
5. victim click in "CLICK ME" button
6. XSS will be triggerd

## Impact

it is possible to perform malicious actions on the victim's account

</details>

---
*Analysed by Claude on 2026-05-24*
