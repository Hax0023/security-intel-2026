# Rack Multi-part Request Parsing DoS - Worse-than-Linear Performance Vulnerability

## Metadata
- **Source:** HackerOne
- **Report:** 431561 | https://hackerone.com/reports/431561
- **Submitted:** 2018-10-31
- **Reporter:** bjeanes
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Denial of Service, Algorithmic Complexity, Resource Exhaustion
- **CVEs:** CVE-2018-16470
- **Category:** uncategorised

## Summary
Rack's multi-part body parser exhibits worse-than-linear performance degradation relative to the number of parts in a request, enabling attackers to cause multi-second response times with specially crafted requests. A single request with 10,000 parts can cause 15-25 second delays on major services like GitHub API, and distributed attacks can exhaust web server resources.

## Attack scenario
1. Attacker generates a multi-part form request with 10,000+ parts using provided script or crafted HTML form
2. Request is sent to target Rails/Rack application with intentionally large number of boundary delimiters
3. Rack's parser begins processing multi-part body with quadratic or worse time complexity
4. Single request ties up thread/process for 15-25+ seconds before completing
5. Attacker distributes multiple such requests to exhaust available worker threads and cause gateway timeouts
6. Legitimate users experience service degradation or complete unavailability due to resource starvation

## Root cause
Rack's multi-part parser implements an algorithm with worse-than-linear time complexity O(n²) or worse when processing multiple form parts. Each additional part compounds processing time disproportionately, likely due to inefficient string operations, repeated buffer allocations, or nested loops in boundary detection logic.

## Attacker mindset
Low effort, high impact attack requiring only HTML form generation. Attacker recognizes that algorithmic weaknesses in parsing libraries can be exploited at scale without sophisticated techniques. The ability to trigger via simple web forms makes this particularly attractive for mass exploitation, especially when combined with XSS or botnet distribution.

## Defensive takeaways
- Implement timeout limits on multi-part request parsing to prevent indefinite resource consumption
- Set maximum limits on number of form parts accepted per request
- Use streaming parsers with linear O(n) complexity instead of buffering entire requests
- Monitor request processing times and alert on anomalously slow requests
- Implement rate limiting per IP/user to mitigate distributed DoS attempts
- Profile and optimize boundary detection algorithms in parsing libraries
- Add request size limits and part count limits at reverse proxy/WAF level
- Consider using dedicated parsing libraries optimized for performance and security

## Variant hunting
Test other Rack-based frameworks (Sinatra, Hanami, Padrino) for similar parsing vulnerabilities
Investigate XML parsing libraries for similar algorithmic complexity issues in entity handling
Check JSON parsing implementations for ReDoS or similar algorithmic attacks
Examine URL-encoded form parsing for similar linear vs quadratic complexity issues
Test multipart parsing in other languages (PHP, Java, Python, Node.js) for equivalent vulnerabilities
Research boundary delimiter handling in different parser implementations for optimization opportunities

## MITRE ATT&CK
- T1499.4
- T1190

## Notes
Vulnerability discovered by Bo Jeanes and Jack Chen, verified by Charlie Somerville. Independently disclosed to both Rails team and Rack core mailing list. The benchmarking data clearly demonstrates quadratic degradation (1000 parts: 0.25s, 10000 parts: 12s, 20000 parts: 28s). Attack surface is extremely broad as every Rails application depends on Rack for request parsing. The ease of exploit (simple HTML form) combined with severe impact makes this critical infrastructure risk.

## Full report
<details><summary>Expand</summary>

The multi-part body parsing in Rack and consequently Rails has a worse-than-linear performance relative to the number of parts in the request body.

In small scale (i.e. non-disruptive) tests on a variety of Rails applications on the internet, including my own, GitHub.com, Heroku API, Instacart, Shopify, Bugcrowd, and others, it was trivial to cause request servicing to take long enough to cause gateway timeouts. It would not be particularly difficult to generate enough of these requests to tie up the majority of web serving resources for a typical Rails application.

This vulnerability has also been separately disclosed to rack-core mailing list by me.

## Steps To Reproduce:

I've created a script that can be run here against any Rack-based application: https://gist.github.com/bjeanes/63580e27c197885d4b07160fae132108

By default it generates a request body with 10,000 parts which, in my testing, was enough to cause GitHub API to take between 15-25 seconds to service the request once the request transfer had completed.

## Addendum

Some benchmarking of Rack is included here, which was also sent to rack-core:

```
N = number of parts, 
boundary used is as generated by Chrome, but larger boundaries cause
higher impact

Rehearsal --------------------------------------------
N: 1       0.032670   0.006635   0.039305 (  0.044159)
N: 100     0.008245   0.001319   0.009564 (  0.009971)
N: 1000    0.149332   0.079087   0.228419 (  0.255769)
N: 2000    0.398711   0.276931   0.675642 (  0.691356)
N: 5000    2.254126   1.569181   3.823307 (  3.871649)
N: 10000   7.134949   4.350681  11.485630 ( 12.083888)
N: 20000  15.946187  10.491861  26.438048 ( 28.684177)
---------------------------------- total: 42.699915sec

               user     system      total        real
N: 1       0.000372   0.000003   0.000375 (  0.000371)
N: 100     0.004889   0.000021   0.004910 (  0.004977)
N: 1000    0.117571   0.015548   0.133119 (  0.192915)
N: 2000    0.468934   0.309703   0.778637 (  0.870675)
N: 5000    2.086055   1.482317   3.568372 (  3.830543)
N: 10000   7.110589   4.488229  11.598818 ( 12.110710)
N: 20000  14.559701   9.948678  24.508379 ( 25.537332)
```

This is not technically in the Rails codebase, but it is in a non-optional dependency of every Rails application. Furthermore, I did receive some feedback from core members that a Rack vulnerability is likely to be eligible for this bounty: https://twitter.com/_matthewd/status/1057266505056800768.

Discovered by Bo Jeanes (@bjeanes) and Jack Chen (@chendo) and vetted after the fact by Charlie Somerville (@charliesome).

## Impact

Resource starvation of web request servicing, by causing multiple long-running requests. Attack can be constructed with just a HTML web form, making it literally click-button easy. That it can be generated from a form also has potential implications when combined with XSS or some other mechanism where an attacker could cause arbitrary user agents en masse to send such requests.

</details>

---
*Analysed by Claude on 2026-05-24*
