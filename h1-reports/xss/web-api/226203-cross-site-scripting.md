# Cross-site-Scripting

## Metadata
- **Source:** HackerOne
- **Report:** 226203 | https://hackerone.com/reports/226203
- **Submitted:** 2017-05-04
- **Reporter:** test_this
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
step:
1: goto https://bridge.cspr.ng/my/account of your account
2. in "Custom Profile field option" check the box and enter xss payload in "display name" field
       payload: "p<script>alert('xss')</script>"
3. update the information 
4. open the account in INTERNET EXPLORER 11 and xss will executed

note: here server is not sanitize the user input properly,
         payload will not work in fire

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

step:
1: goto https://bridge.cspr.ng/my/account of your account
2. in "Custom Profile field option" check the box and enter xss payload in "display name" field
       payload: "p<script>alert('xss')</script>"
3. update the information 
4. open the account in INTERNET EXPLORER 11 and xss will executed

note: here server is not sanitize the user input properly,
         payload will not work in firefox,chrome browser due to "content-security-policy"
         But internet explorer does not Support "Content-Security-Policy"  so xss will execut

this is stored xss and the display name will visible to everywhere, so its possible to account takeover of ther user

</details>

---
*Analysed by Claude on 2026-05-24*
