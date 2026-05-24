# Race condition on Federalist API endpoints leads to Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 249319 | https://hackerone.com/reports/249319
- **Submitted:** 2017-07-13
- **Reporter:** sp1d3rs
- **Program:** Federalist (GSA)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Denial of Service (DoS), Rate Limiting Bypass, Race Condition, Resource Exhaustion
- **CVEs:** None
- **Category:** business-logic

## Summary
The Federalist API lacks rate limiting, allowing authenticated users to send thousands of parallel requests that are all executed simultaneously, causing server resource exhaustion and complete instance unavailability. Each parallel request triggers database queries that consume CPU and memory resources, making the application unresponsive to legitimate users.

## Attack scenario
1. Attacker authenticates to the Federalist instance using valid credentials
2. Attacker identifies the /v0/me endpoint (or other API endpoints) through reconnaissance
3. Attacker configures a tool (Burp Intruder, Charles, custom script) to send 1000+ parallel GET/PUT requests
4. API server accepts all requests without rate limiting and executes them simultaneously
5. Each request triggers PostgreSQL database operations, consuming system resources exponentially
6. Server becomes unresponsive, denying legitimate users access to the platform (DoS condition)

## Root cause
The API lacks rate limiting mechanisms at the application level. The server processes all incoming requests concurrently without enforcing per-user or per-IP request throttling, allowing attackers to overwhelm the backend database and system resources through parallel request amplification.

## Attacker mindset
An attacker with basic authentication credentials can easily weaponize this vulnerability using automated tools to launch a low-sophistication, high-impact DoS attack. The attacker recognizes that cloud environments may have limited resource constraints, making parallel request amplification particularly effective. The simplicity of exploitation (merely repeating requests) requires minimal technical skill.

## Defensive takeaways
- Implement rate limiting on all API endpoints using libraries like express-rate-limit or similar middleware
- Enforce per-user request throttling (e.g., max 5 concurrent requests per authenticated user)
- Implement request queuing to process user requests sequentially rather than in parallel
- Add circuit breakers and bulkheads to isolate resource consumption
- Monitor and alert on unusual request patterns and resource consumption spikes
- Configure cloud load balancers with rate limiting and DDoS protection
- Implement database connection pooling with limits to prevent resource exhaustion
- Add request authentication and validation at the API gateway level
- Conduct load testing to establish safe concurrency thresholds

## Variant hunting
Check other endpoints beyond /v0/me for similar rate limiting bypasses (especially write operations like PUT/POST)
Test with unauthenticated requests to determine if DoS is possible without credentials
Attempt HTTP pipelining to bypass per-request rate limits
Test for race conditions in state-changing operations (settings updates, deployments)
Verify if concurrent request limits exist per IP address vs per user
Check if websocket or long-polling connections have similar protections
Test for resource exhaustion on file upload endpoints
Verify rate limiting effectiveness across different API versions

## MITRE ATT&CK
- T1499
- T1499.001
- T1499.004

## Notes
The researcher demonstrates responsible disclosure by testing on localhost rather than production. The impact is partially theoretical due to inability to test against production infrastructure with unknown protections (load balancers, WAF, etc.). The vulnerability is particularly concerning for government services where availability is critical. The suggested fixes are practical and well-researched, showing the reporter's security maturity.

## Full report
<details><summary>Expand</summary>

##Description
Hello. I discovered that the Federalist API doesn't have rate limiting in place, and executes any amount of request to the endpoint in parallel mode.

##The impact
Since you are using the cloud, and i can't test the production environment, impact is theoretical in this case - it can be a problem, or it not.
On my localhost instance executing of 1000 parallel GET requests to the http://localhost:1337/v0/me endpoint on behalf of authenticated user was lead to the complete instance inaccessibility. It is a light enough request, and executing of 1000 PUT requests (for example, saving site settings) will have greater impact.
{F202845}
Each request cause execution of the PostgreSQL command, which can lead to the high resource usage.
{F202846}

##Reproduction steps
1) Login to the Federalist instance (unauthenticated requests is possible too, but it have too low impact)
2) Look to the request to the `/v0/me` endpoint. Using Burp Intruder or Charles, repeat the request 1000 times in parallel mode. The server will accept and try to execute all of them in the same time. You can notice increased server resource consumption.
3) You can repeat the test with more heavily site settings saving request.

##Suggested fix
You can consider to implement rate-limiting on the API endpoints (for example, executing not more than 5 API requests in same time from the single user), or implement queue (accept requests from single user in сonsistent mode instead parallel), or use module like https://www.npmjs.com/package/express-rate-limit. 

If your production environment somehow mitigates this issue (e.g. has load balancers in place, etc), let me know - i'll close the ticket.


</details>

---
*Analysed by Claude on 2026-05-24*
