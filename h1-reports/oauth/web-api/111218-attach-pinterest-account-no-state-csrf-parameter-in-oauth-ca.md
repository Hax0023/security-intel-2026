# Attach Pinterest account - no State/CSRF parameter in Oauth Call back

## Metadata
- **Source:** HackerOne
- **Report:** 111218 | https://hackerone.com/reports/111218
- **Submitted:** 2016-01-17
- **Reporter:** akhil-reni
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
**Hello**

There is no csrf protection for oauth call backs to attach a pinterest account.
An attacker can escalate this to attach his account with the victims profile and monitor his activities.

**Vulnerable URL:**
https://pinterest-commerce.shopifyapps.com/auth/pinterest/callback?code=fe373552c348b50000b4951184e86224ddde63c4

**Vulnerable request:**
```
GET /auth/pinterest/callback?code=fe37355

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

**Hello**

There is no csrf protection for oauth call backs to attach a pinterest account.
An attacker can escalate this to attach his account with the victims profile and monitor his activities.

**Vulnerable URL:**
https://pinterest-commerce.shopifyapps.com/auth/pinterest/callback?code=fe373552c348b50000b4951184e86224ddde63c4

**Vulnerable request:**
```
GET /auth/pinterest/callback?code=fe373552c348b50000b4951184e86224ddde63c4 HTTP/1.1
Host: pinterest-commerce.shopifyapps.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://www.pinterest.com
Cookie: <redacted>
Connection: keep-alive
```

**Regards,
WeSecureApp**

</details>

---
*Analysed by Claude on 2026-05-24*
