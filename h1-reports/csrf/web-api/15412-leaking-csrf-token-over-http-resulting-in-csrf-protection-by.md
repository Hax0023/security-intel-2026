# Leaking CSRF token over HTTP resulting in CSRF protection bypass

## Metadata
- **Source:** HackerOne
- **Report:** 15412 | https://hackerone.com/reports/15412
- **Submitted:** 2014-06-07
- **Reporter:** anshuman_bh
- **Program:** Unknown
- **Bounty:** $1,000
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
1. Start a proxy tool like Burp.
2. Authenticate to the Coinbase application.
3. Navigate to the URL https://coinbase.com/docs/api/overview
4. Under Developer Updates, enter your email address and click "Subscribe".
5. Notice that this request is sent over HTTP with the CSRF token in the body of the POST request. 

This means that an attacker can easily perform a MiTM attack and gain access 

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

1. Start a proxy tool like Burp.
2. Authenticate to the Coinbase application.
3. Navigate to the URL https://coinbase.com/docs/api/overview
4. Under Developer Updates, enter your email address and click "Subscribe".
5. Notice that this request is sent over HTTP with the CSRF token in the body of the POST request. 

This means that an attacker can easily perform a MiTM attack and gain access to this CSRF token. The attacker can then trick this authenticated Coinbase user to perform CSRF attacks since the attacker now knows the CSRF token associated with this user. This results in bypassing the existing CSRF protection in the Coinbase application. 

</details>

---
*Analysed by Claude on 2026-05-24*
