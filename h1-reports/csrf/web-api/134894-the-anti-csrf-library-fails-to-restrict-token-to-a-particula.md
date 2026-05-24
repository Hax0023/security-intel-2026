# The Anti-CSRF Library fails to restrict token to a particular IP address when being behind a reverse-proxy/WAF

## Metadata
- **Source:** HackerOne
- **Report:** 134894 | https://hackerone.com/reports/134894
- **Submitted:** 2016-04-27
- **Reporter:** sc0
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
The Anti-CSRF Library provides the ability to restrict token to a particular IP address using the variable "$hmac_ip". 

When "$hmac_ip" is set to "true", the token is generated using the predefined variable "$_SERVER['REMOTE_ADDR']" which gives the IP address of the client. However, when the web server is behind a reverse-proxy/WAF/Load-balancer/whatever, which is nowadays often the case, this va

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

The Anti-CSRF Library provides the ability to restrict token to a particular IP address using the variable "$hmac_ip". 

When "$hmac_ip" is set to "true", the token is generated using the predefined variable "$_SERVER['REMOTE_ADDR']" which gives the IP address of the client. However, when the web server is behind a reverse-proxy/WAF/Load-balancer/whatever, which is nowadays often the case, this variable will always return the IP address of the reverse-proxy/WAF/Load-balancer/whatever, failing to restrict the token to the client real IP address.

In order to restrict the token to the user real IP address, the Anti-CSRF Library should also check for the X-Forwared-For HTTP header. However, be advised this header can easily be spoofed. To my knowledge, one cannot ensure a client real IP address.

Both version 1.0.0 and 2.0.0 are affected.

</details>

---
*Analysed by Claude on 2026-05-24*
