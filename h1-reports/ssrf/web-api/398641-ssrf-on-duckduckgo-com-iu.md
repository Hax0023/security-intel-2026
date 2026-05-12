# SSRF on duckduckgo.com/iu/ via Insufficient Domain Validation

## Metadata
- **Source:** HackerOne
- **Report:** 398641 | https://hackerone.com/reports/398641
- **Submitted:** 2018-08-23
- **Reporter:** d0nut
- **Program:** DuckDuckGo
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Server-Side Request Forgery (SSRF), Cross-Site Port Attack (XSPA), Information Disclosure, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
The /iu/ endpoint on duckduckgo.com implements domain validation by checking for the presence of 'yimg.com' string anywhere in the URL, rather than validating the actual target domain. An attacker can bypass this check by injecting 'yimg.com' as a query parameter while requesting arbitrary internal services. This enables port scanning of localhost and information disclosure from internal services.

## Attack scenario
1. Attacker identifies that the /iu/ endpoint validates requests by checking if 'yimg.com' appears somewhere in the URL
2. Attacker crafts a malicious URL that requests an internal service (e.g., http://127.0.0.1:6868/status/) while appending 'yimg.com' as a query parameter
3. The server's validation check finds 'yimg.com' in the URL and allows the request through, believing it is legitimate
4. The request is forwarded to the internal service at localhost:6868, which responds with sensitive data
5. Attacker systematically scans common ports (22, 25, 80, 443, 587, 6380, 6432, 6767, 6868, 8000) to discover running services
6. Attacker extracts sensitive information such as Redis URLs, deployment environment, and internal service status from responses

## Root cause
The domain validation logic uses a substring match check (looking for 'yimg.com' presence) instead of properly parsing and validating the request target URL. The check examines the entire URL as a string rather than validating the actual network destination, allowing attackers to inject the whitelisted domain as a parameter while requesting arbitrary targets.

## Attacker mindset
An attacker would recognize that simple string matching on URLs is a common anti-pattern in security filtering. By understanding that 'yimg.com' is a trusted domain, they would attempt various parameter injection techniques to satisfy the validation while requesting internal resources. The discovery of exposed internal services would motivate further exploitation attempts, particularly against Redis which often lacks proper authentication.

## Defensive takeaways
- Never use substring matching for domain/URL validation; properly parse URLs and validate the host/domain component
- Implement allowlist validation by parsing the target URL and comparing the actual hostname, not string presence
- Consider using URL parsing libraries that separate components rather than regex or string matching
- Validate that the target scheme, hostname, and port are explicitly whitelisted, not just that certain strings appear in the URL
- Implement SSRF protections by blocking requests to private IP ranges (127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, etc.)
- Monitor and log all requests through the /iu/ endpoint, especially those targeting internal services
- Restrict outbound connections from image proxy services to only necessary external domains
- Implement network segmentation to isolate internal services from servers that handle user input
- Apply rate limiting to detect port scanning attempts

## Variant hunting
Look for similar issues in other image serving or proxy endpoints that may perform domain validation. Check for other endpoints accepting user-controlled URLs (redirects, webhooks, image processing services). Search for variations where validation checks for domain strings in query parameters, fragments, or through URL encoding bypasses. Test whether other whitelisted domains can be bypassed similarly.

## MITRE ATT&CK
- T1190
- T1498
- T1526
- T1057
- T1087
- T1552
- T1021

## Notes
This is a classic SSRF with insufficient input validation. The report demonstrates good security research methodology by showing progression from normal usage to exploitation, and includes concrete examples of information disclosure (Redis service details, deployment environment). The vulnerability is particularly severe because it exposes both internal service discovery and sensitive configuration data. The attacker could potentially escalate this to RCE or data exfiltration depending on what those internal services accept.

## Full report
<details><summary>Expand</summary>

Normally, a call to `https://duckduckgo.com/iu` contains a query parameter (`u`) with some path using the domain `yimg.com`. This call will succeed in most cases.
{F337121}

And if we change that path to something like `https://google.com` it's rejected.
{F337118}

However, it appears that the check that ensures that `yimg.com` is the target domain is solely based on whether or not that string appears in the url, independent of where. This means we can stuff it in a query parameter and bypass this check.

{F337120}

Furthermore, with this bypass we can hit localhost and perform a port scan (see [XSPA](https://indiatriks.blogspot.com/2012/07/xspa-cross-site-port-attack.html)). 

For example, I have been able to conclude that services are running on the following ports:
```
22
25
80
443
587
6380
6432
6767
6868
8000
```

Some of these services don't like talking HTTP (like `22` and `25`) so they never respond, but other services seem to talk HTTP and will return seemingly sensitive data about redis. 
For example:
`https://duckduckgo.com/iu/?u=http://127.0.0.1:6868%2fstatus%2f?q=http://yimg.com/` returns the following:
```
{
  "current_time": "2018-08-23T17:56:06",
  "deployment_environment": "prod",
  "redis_local_last_successful_ping": "2018-08-23T13:56:05",
  "redis_local_url": "redis://127.0.0.1:6380",
  "redis_regional_last_successful_ping": "2018-08-23T13:56:05",
  "redis_regional_url": "redis://cache-services.duckduckgo.com:6380",
  "stat_blocked_ips_removed_since_launch": 8787,
  "stat_blocked_ips_since_launch": 12185,
  "stat_ipset_blocks": 266,
  "stat_redis_local_messages_received": 3613,
  "stat_redis_regional_messages_received": 10211,
  "status": "up"
}
```

## Impact

This could be used to interact with services that are not intended to be exposed. This also enables an XSPA attack. Additionally, information disclosure about a redis service. 

Lastly, an attack on redis may be possible even though the requests seem restricted to http.

</details>

---
*Analysed by Claude on 2026-05-11*
