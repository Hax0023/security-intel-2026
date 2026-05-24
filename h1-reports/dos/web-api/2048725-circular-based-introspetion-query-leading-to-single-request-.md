# Circular Introspection Query Leading to Single-Request Denial of Service on api.sorare.com/graphql

## Metadata
- **Source:** HackerOne
- **Report:** 2048725 | https://hackerone.com/reports/2048725
- **Submitted:** 2023-07-03
- **Reporter:** thebeast99
- **Program:** Sorare
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Denial of Service, Resource Exhaustion, Missing Input Validation, Excessive Query Depth
- **CVEs:** None
- **Category:** web-api

## Summary
The GraphQL API at api.sorare.com/graphql lacks query depth limits and allows unauthenticated introspection queries, enabling attackers to craft circular recursive queries against the __schema field that cause excessive memory consumption and processing delays. A single malicious introspection query can generate 3.7MB+ of duplicated data and cause 5-7 second response times, effectively achieving denial of service without requiring authentication or bypassing Cloudflare protection.

## Attack scenario
1. Attacker identifies that api.sorare.com/graphql has introspection enabled and no depth limits enforced
2. Attacker crafts a circular introspection query recursively querying __schema.types[].fields[].type.fields[].type.fields recursively without bounds
3. Attacker sends a single POST request with the malicious query to /graphql endpoint
4. GraphQL server processes the deeply nested query, exponentially expanding and duplicating data across recursion levels
5. Server consumes excessive CPU and memory resources, returning 3.7MB+ responses with multi-second latency
6. Legitimate user requests experience severe degradation or timeout, resulting in denial of service across both api.sorare.com/graphql and api.sorare.com/federal/graphql instances

## Root cause
The GraphQL server implementation lacks two critical security controls: (1) query depth limiting to restrict recursive traversal of the schema, and (2) query complexity analysis to detect and reject computationally expensive introspection patterns. Introspection is enabled for developer convenience without corresponding safeguards against abuse.

## Attacker mindset
An attacker recognizes that introspection is a powerful reconnaissance tool that also exposes the schema structure for exploitation. They realize that recursively querying the type system without limits creates exponential expansion, and that a single unauthenticated request can trigger resource exhaustion. This is attractive because it bypasses rate limiting at the HTTP/Cloudflare layer (single request), requires no authentication, and is deterministic and reproducible.

## Defensive takeaways
- Implement query depth limits in GraphQL server configuration (Apollo: use depthLimit plugin, typical limit 10-15 levels)
- Enable query complexity analysis to reject queries exceeding computational budgets before execution
- Consider disabling introspection on production endpoints or restrict it to authenticated/whitelisted clients only
- Implement request-level timeout enforcement with aggressive defaults (1-2 seconds max)
- Add per-query resource monitoring to detect and terminate runaway queries
- Implement rate limiting at the GraphQL layer, not just HTTP layer, to catch single-request attacks
- Monitor query patterns for circular/recursive __schema traversal and alert on anomalies
- Use persisted queries or query whitelisting to prevent arbitrary query submission

## Variant hunting
Test other recursive introspection patterns: __type().ofType().ofType().ofType() chains on OBJECT_TYPE fields
Query __schema.directives recursively to find alternative expansion vectors
Combine introspection with fragment recursion to bypass simple depth counters
Test if mutations/subscriptions endpoints have identical vulnerabilities
Attempt alias-based query expansion to bypass depth limits that only count nesting levels
Fuzz with mixed recursive patterns combining __schema, __type, and field traversal
Test federation (_service query) if GraphQL federation is enabled for similar issues

## MITRE ATT&CK
- T1190
- T1499
- T1565

## Notes
The report correctly identifies that this vulnerability bypasses Cloudflare DDoS protection because it's a single legitimate-looking request rather than volumetric attack traffic. The dual-instance architecture (api.sorare.com/graphql and api.sorare.com/federal/graphql sharing same database) means one attack impacts both endpoints simultaneously. The 3.7MB response size suggests exponential expansion across roughly 6-8 recursion levels, indicating the schema has deeply nested type relationships. CVSS score of 9.3 is justified given unauthenticated access, high availability impact, and trivial exploitation. The reporter's Apollo documentation reference to TN0021 is highly relevant and shows security awareness.

## Full report
<details><summary>Expand</summary>

## Summary:

Hi Team, Hope you are doing great Sorare graphql Api has introspection enabled by default as per the policy it's meant to be public so they can facilitate their users with Graphql Playground.

So https://api.sorare.com/federal/graphql is for the users and clients using the web application and https://api.sorare.com/graphql is a playground for the developers and clients. They both share the same domain and database just a different graphql instance We can execute the same query on both graphql servers parallelly. But the catch here is because of the no-depth limits an attacker can execute a circular introspection query which is leading to a single request denial of service which is affecting both instances same time. Users don't need to be authenticated for this attack which is an extreme condition.

APIs are always the backbone of the organization and a firm. If left vulnerable that kinda attack requires a single request to take down the server and can Impact the Availability of the company. And bypassing the `Cloudflare DDOS` which is playing a role as a frontier to prevent such cases.
You have to consider this that it is not a typical DOS attack that requires so many bots or computational power a single query can Do pretty much damage.




## Steps To Reproduce:

Its been years now and we all know what an introspection query looks like but with the graphql feature, we can also retrieve just one query time at a time from  `__schema` we can just retrieve all fields of `mutations`, `queries` and `subscription`. By calling fields and their types.

***Here is the request***:
```
POST /graphql HTTP/2
Host: api.sorare.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: application/json
Accept-Language: en-US
Accept-Encoding: gzip, deflate
Referer: https://api.sorare.com/graphql/playground
Content-Type: application/json
Origin: https://api.sorare.com
Content-Length: 262
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Te: trailers

{"operationName":null,"variables":{},"query":"query {\r\n __schema {\r\n   types { \r\n    fields {\r\n      type {\r\n    fields {\r\n      type { \r\n    fields {\r\n      type {\r\n     fields {\r\n     name\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}"}
```
From the above query, you will get the `3728114` bytes of data in the single query which is obviously duplicated can be seen in the query request and the delay will be around `5 to 7 seconds` which is extreme degradation condition for a backend server.

***Response In my case***:
{F2465261}

You can Add more recursive loops `the more loop the more delay`
***Here is the query with one more circular recursive loop***

```
{"operationName":null,"variables":{},"query":"query {\r\n __schema {\r\n   types { \r\n    fields {\r\n      type {\r\n    fields {\r\n      type { \r\n    fields {\r\n      type {\r\n     fields {\r\n     type {\r\n     fields {\r\n      name\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}\r\n}"}

```
 Now you can see more delay.

I hope you can see the impact of this vulnerability. If there is anything the team wants to know I would be grateful!

 Best & kind regards
@thebeast99

## Supporting Material/References:

Here is the official Apollo guide regarding the depth limits.
https://www.apollographql.com/docs/technotes/TN0021-graph-security/#limit-query-depth

Note: I set the cvss as per the bug But because the scope is `High asset` my report automatically scored as 9.3 critical whereas in other cases it's always standard `7.5` High.

## Impact

An attacker can take down the server with few or a single graphql request. Which will cost Availability to sorare.com

</details>

---
*Analysed by Claude on 2026-05-24*
