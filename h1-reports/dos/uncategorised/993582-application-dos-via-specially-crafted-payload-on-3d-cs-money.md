# Application Denial of Service via Specially Crafted Payload on 3d.cs.money Search API

## Metadata
- **Source:** HackerOne
- **Report:** 993582 | https://hackerone.com/reports/993582
- **Submitted:** 2020-09-28
- **Reporter:** enigmaticjohn
- **Program:** CS.Money
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Denial of Service (DoS), Algorithmic Complexity Exploitation, Regular Expression Denial of Service (ReDoS)
- **CVEs:** None
- **Category:** uncategorised

## Summary
A single HTTP POST request with a specially crafted payload containing nested parentheses can cause the application search API to become unresponsive for several minutes. The duration of the denial of service is directly proportional to the complexity of the payload, allowing an attacker to control downtime duration with minimal resource investment.

## Attack scenario
1. Attacker navigates to the 3d.cs.money item search interface
2. Attacker intercepts the POST request to /api/skin/search endpoint
3. Attacker crafts a malicious payload with nested parentheses (e.g., '(((((()0)))))', '((((((()0))))))') in the 'name' parameter
4. Attacker sends a single HTTP request with the crafted payload to the server
5. Server attempts to process the payload, triggering expensive regex matching or parsing logic
6. Server becomes unresponsive and legitimate users experience service disruption for minutes

## Root cause
The search API endpoint likely uses an unoptimized regular expression or parsing algorithm to validate or process the 'name' parameter. Nested parentheses trigger catastrophic backtracking or exponential processing time, causing the CPU to spike and the service to become unresponsive. The application lacks input validation, payload complexity limits, and rate limiting on the search endpoint.

## Attacker mindset
An attacker could weaponize this vulnerability for competitive disruption (targeting a CS:GO skin trading platform), causing reputational damage, forcing users to alternative services, or creating opportunities for scams during outages. The ease of exploitation (single unauthenticated request) and controllable impact duration make it attractive for both opportunistic and targeted attacks.

## Defensive takeaways
- Implement strict input validation with length limits on search parameters (e.g., maximum 100 characters)
- Use non-catastrophic regex patterns or switch to robust parsing libraries that handle edge cases safely
- Add rate limiting and throttling on the /api/skin/search endpoint (e.g., 10 requests per minute per IP)
- Deploy request timeout mechanisms with maximum CPU/processing time limits per request
- Implement web application firewalls (WAF) to detect and block payloads with excessive nested structures
- Add comprehensive logging and alerting for abnormal API response times
- Conduct security code review of all regex patterns used in input processing
- Stress test the search functionality with fuzzing tools to identify algorithmic complexity vulnerabilities

## Variant hunting
Search for similar ReDoS vulnerabilities in other endpoints accepting string input (filters, tags, descriptions). Check for nested structure processing in JSON/XML parsers. Test other mathematical expression-like inputs (brackets, braces). Investigate if the vulnerability exists across other API versions or related domains (market.cs.money, etc.).

## MITRE ATT&CK
- T1498 - Network Denial of Service (Application-layer DoS)
- T1499 - Endpoint Denial of Service (Algorithmic Complexity)
- T1190 - Exploit Public-Facing Application

## Notes
The researcher appropriately flagged that this differs from typical DoS policies since it requires only a single request rather than volumetric attacks. This is a classic Regular Expression Denial of Service (ReDoS) or algorithmic complexity vulnerability. The linear scalability of impact with payload size suggests exponential processing complexity. No authentication or special privileges required, making this a critical finding for a public-facing API.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello Team,
While testing it was observed that on **3d.cs.money** a DOS is possible via specially crafted request using only single request from single machine on search bar.
Though I am aware of the Out of Scope policy "Any activity that could lead to the disruption of our service (DoS)", this scenario is different, here we are only using one Request and depending on the payload, the DOS time can be varied.

## Steps To Reproduce:

  1. Go to https://3d.cs.money/item/default
  2. Turn ON the intercept and type something in search box.
  3. A POST request will be captured as follows:

```
POST /api/skin/search HTTP/1.1
Host: 3d.cs.money
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json;charset=utf-8
Content-Length: 32
Origin: https://3d.cs.money
Connection: close
Referer: https://3d.cs.money/item/default
Cookie: __cfduid=d38bfad20d6ec52ba0a6af9014d27a2e81601313370; TEST_GROUP=2; UUID3D=to4nZuWnRSS4A7G; _ga=GA1.1.214308118.1601313374; _ga_HY7CCPCD7H=GS1.1.1601313373.1.1.1601316641.57; _gid=GA1.2.24460124.1601313377

{"name":"[Payload here]","item_name":"AK-47"}
```
  4. Send it to the Repeater.
  5. Put the following payload at [Payload here]
```(((((()0)))))```

  6. This will take down the host for few minutes.
  7. If we add more parenthesis like ```((((((()0))))))``` , the site will be down for more time.

## Supporting Material/References:
PFA screenshot.

## Impact

Web server can be made inaccessible for any amount of time using only single request.

</details>

---
*Analysed by Claude on 2026-05-24*
