# Web Cache Poisoning on help.nextcloud.com via X-Forwarded-Host Header

## Metadata
- **Source:** HackerOne
- **Report:** 429747 | https://hackerone.com/reports/429747
- **Submitted:** 2018-10-27
- **Reporter:** g4mm4
- **Program:** Nextcloud
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Web Cache Poisoning, HTTP Header Injection, Stored XSS
- **CVEs:** None
- **Category:** uncategorised

## Summary
The help.nextcloud.com domain is vulnerable to web cache poisoning through the X-Forwarded-Host HTTP header. An attacker can inject malicious content that gets cached by the server, causing subsequent users to receive poisoned responses containing XSS payloads or malware URLs.

## Attack scenario
1. Attacker identifies that help.nextcloud.com caches responses based on query parameters but fails to properly validate the X-Forwarded-Host header
2. Attacker crafts a request with a malicious X-Forwarded-Host header containing XSS payload (e.g., 'cyberjutsu.io/#')
3. Attacker repeatedly sends requests with query parameter (qwKzzSR=649227948379) to force the server to cache the poisoned response
4. Server caches the malicious response associating it with the query parameter, treating X-Forwarded-Host as legitimate
5. Subsequent legitimate users visiting the same URL receive the cached poisoned response containing attacker-controlled content
6. Users' browsers execute the XSS payload, redirect to malware site, or browsers flag the domain as malicious

## Root cause
The server fails to properly validate and sanitize the X-Forwarded-Host header before using it to generate cached responses. The cache key likely does not include header variations, allowing attackers to poison cache entries that will be served to other users. Insufficient input validation on HTTP headers combined with improper cache key construction enables the attack.

## Attacker mindset
Low-cost, high-impact attack requiring minimal technical skill. Attacker seeks to compromise website reputation, perform phishing, inject malware redirects, or achieve stored XSS against all subsequent visitors without authentication. Demonstrates cache inconsistency for weaponization.

## Defensive takeaways
- Implement strict X-Forwarded-Host header validation against a whitelist of allowed hosts
- Include all security-relevant headers in cache key computation to prevent poisoning
- Sanitize and validate all HTTP headers before rendering in responses
- Implement cache busting mechanisms for sensitive pages
- Use Content-Security-Policy headers to prevent XSS execution
- Monitor cache hit rates and response anomalies for poisoning detection
- Disable or restrict X-Forwarded-* headers if not explicitly needed for application logic
- Implement request signing to prevent header manipulation

## Variant hunting
Look for similar header injection patterns using X-Forwarded-Proto, X-Forwarded-For, X-Original-Host. Test other Nextcloud domains and self-hosted instances. Check for cache poisoning via other headers like Host, Referer, User-Agent. Test GET parameter combinations with header manipulation across different URL patterns.

## MITRE ATT&CK
- T1190
- T1598
- T1583
- T1608

## Notes
PoC uses wget in loop to demonstrate cache poisoning. Attack requires attacker to have network-level or DNS control to inject X-Forwarded-Host effectively, OR the target must be behind a proxy that respects this header. Severity depends on cache TTL and whether XSS payloads can execute in cached HTML. Report lacks evidence of actual XSS execution in cached response (only shows header presence in image).

## Full report
<details><summary>Expand</summary>

Hi there,
I just found the website:
https://help.nextcloud.com
is infected with "Web cache poisoning"
Abuse this bug, Attacker can:
1. Poison your cache with HTTP header with XSS included. This attack may leads to Stored XSS
2. Poison your website contains malware url (cache poisoned by attacker), maybe the user's browser (like Firefox, Chrome) will block your website (https://help.nextcloud.com)

How to reproduce the issue:

    In the 1st terminal, run command likes this: 
$ while true; do wget "https://help.nextcloud.com/?qwKzzSR=649227948379" --header 'X-Forwarded-Host: cyberjutsu.io/#' -qO->/dev/null; echo "poisoning...";done
    In the 2nd terminal, run command below for confirmation this attack is successful: 
while true; do wget "https://help.nextcloud.com/?qwKzzSR=649227948379" -qO-|grep "cyberjutsu.io"; echo "ping my payload..." ;done

Finally, this link bellow: https://help.nextcloud.com/?qwKzzSR=649227948379 was infected with "Web Cache poisoning attack".
Please see the attached image for details.

Impact
Stored XSS attack, deface website ....
Cheers,
~g4mm4

## Impact

Stored XSS attack, deface website, phishing for funs :)

</details>

---
*Analysed by Claude on 2026-05-24*
