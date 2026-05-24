# HTTP-Basic Authentication on logs.nextcloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 198673 | https://hackerone.com/reports/198673
- **Submitted:** 2017-01-16
- **Reporter:** rbcafe
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Greetings,

While visiting https://logs.nextcloud.com/ , I noticed that this server use HTTP-Basic Authentication.

{F152730}

POC :
------

    GET https://logs.nextcloud.com/ HTTP/1.1
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
   

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

Greetings,

While visiting https://logs.nextcloud.com/ , I noticed that this server use HTTP-Basic Authentication.

{F152730}

POC :
------

    GET https://logs.nextcloud.com/ HTTP/1.1
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: br
    DNT: 1
    Connection: keep-alive
    Upgrade-Insecure-Requests: 1
    Authorization: Basic cmJjYWZlOnJiY2FmZQ==
    Host: logs.nextcloud.com

Result : 
------

cmJjYWZlOnJiY2FmZQ== is the base64 of rbcafe:rbcafe and it's transmitted plaintext

Risk : 
------

- Vulnerable to client side attacks.
- Vulnerable to MITM attack.
- Vulenrable to Eavesdropping attack.
- Vulnerable to Brute force attacks.

Possible fix :
------

HTTP-Basic Authentication should be changed for HTTP-Digest Authentication.

Best regards
@rbcafe

</details>

---
*Analysed by Claude on 2026-05-24*
