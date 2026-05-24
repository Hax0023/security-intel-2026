# XSS because of Akamai ARL misconfiguration on ████

## Metadata
- **Source:** HackerOne
- **Report:** 1305477 | https://hackerone.com/reports/1305477
- **Submitted:** 2021-08-14
- **Reporter:** pirneci
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hello team,
I hope you're doing well & healthy.
I found a reflected XSS because of the misconfiguration of Akamai ARL.

███████

## References

      - https://github.com/war-and-code/akamai-arl-hack
      - https://twitter.com/SpiderSec/status/1421176297548435459
      - https://warandcode.com/post/akamai-arl-hack/
      - https://github.com/cybercdh/goarl
      - https://community.akamai.com/cus

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

Hello team,
I hope you're doing well & healthy.
I found a reflected XSS because of the misconfiguration of Akamai ARL.

███████

## References

      - https://github.com/war-and-code/akamai-arl-hack
      - https://twitter.com/SpiderSec/status/1421176297548435459
      - https://warandcode.com/post/akamai-arl-hack/
      - https://github.com/cybercdh/goarl
      - https://community.akamai.com/customers/s/article/WebPerformanceV1V2ARLChangeStartingFebruary282021?language=en_US

## Impact

If an attacker can control a script that is executed in the victim's browser, then they can typically fully compromise that user. Amongst other things, the attacker can:
    Perform any action within the application that the user can perform.
View any information that the user is able to view.
Modify any information that the user is able to modify.
Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user.

## System Host(s)
███████

## Affected Product(s) and Version(s)
Akamai ARL

## CVE Numbers


## Steps to Reproduce
Here is the **PoC**

http://███/7/0/33/1d/www.citysearch.com/search?what=x&where=place%22%3E%3Csvg+onload=confirm(document.location)%3E

## Suggested Mitigation/Remediation Actions
Web application owners should keep their infrastructure up to date, and follow secure development best practices, avoiding Open Redirects and XSS vulnerabilities.
Setting up specific WAF rules to detect and block XSS attacks and Open Redirects will increase the level of protection as well, and provide visibility to URLs that malicious users attempt to target.

Best regards.
@pirneci



</details>

---
*Analysed by Claude on 2026-05-24*
