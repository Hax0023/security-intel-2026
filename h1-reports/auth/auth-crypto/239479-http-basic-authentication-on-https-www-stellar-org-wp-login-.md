# HTTP - Basic Authentication on https://www.stellar.org/wp-login.php

## Metadata
- **Source:** HackerOne
- **Report:** 239479 | https://hackerone.com/reports/239479
- **Submitted:** 2017-06-13
- **Reporter:** mrnull1337
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Greetings, noticed https://www.stellar.org/wp-login.php using basic authentication.

#PoC:
YWRtaW46YWRtaW4= is base64 encode of admin:admin
#Impact:

Vulnerable to client side attacks.
Vulnerable to MITM attack.
Vulenrable to Eavesdropping attack.
Vulnerable to Brute force attacks.

#Fix:
HTTP-Basic Authentication should be changed for HTTP-Digest Authentication.

Let me know if any further info i

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

Greetings, noticed https://www.stellar.org/wp-login.php using basic authentication.

#PoC:
YWRtaW46YWRtaW4= is base64 encode of admin:admin
#Impact:

Vulnerable to client side attacks.
Vulnerable to MITM attack.
Vulenrable to Eavesdropping attack.
Vulnerable to Brute force attacks.

#Fix:
HTTP-Basic Authentication should be changed for HTTP-Digest Authentication.

Let me know if any further info is required.

Regards,
Mr.R3boot.

</details>

---
*Analysed by Claude on 2026-05-24*
