# Node.js HTTP Unbounded Chunk Extension DoS (CVE-2024-22019)

## Metadata
- **Source:** HackerOne
- **Report:** 2375446 | https://hackerone.com/reports/2375446
- **Submitted:** 2024-02-15
- **Reporter:** bart
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Denial of Service, Resource Exhaustion, Improper Input Validation
- **CVEs:** CVE-2024-22019
- **Category:** memory-binary

## Summary
Node.js HTTP parser fails to properly validate chunk extensions in chunked transfer encoding, allowing attackers to consume unbounded CPU and network resources. Standard mitigation techniques like request timeouts and body size limits are ineffective against this vector.

## Attack scenario
1. Attacker sends HTTP request with chunked transfer encoding enabled
2. Attacker crafts malicious chunk extensions with unbounded size
3. HTTP parser processes chunk extensions without proper length validation
4. Server allocates excessive memory/CPU parsing the malformed extensions
5. Multiple concurrent requests amplify resource consumption
6. Legitimate requests timeout or are dropped, causing denial of service

## Root cause
The http parser does not enforce bounds on chunk extension length during parsing of Transfer-Encoding: chunked requests, allowing arbitrary resource consumption without triggering configured request body limits or timeouts.

## Attacker mindset
Exploit protocol parsing weaknesses to bypass standard DoS protections; focus on edge cases in HTTP/1.1 chunked encoding that escape conventional rate limiting and size restriction mechanisms.

## Defensive takeaways
- Implement strict limits on chunk extension sizes in HTTP parsers
- Add timeout mechanisms specifically for chunk parsing phases
- Monitor and limit per-connection resource consumption during request parsing
- Upgrade Node.js to patched versions immediately
- Deploy reverse proxy/WAF with configurable chunk extension validation
- Implement circuit breakers for slow/malformed request clients

## Variant hunting
Search for similar unbounded parsing in other HTTP protocol elements: headers, trailers, multipart boundaries; examine other Node.js http methods for chunk extension handling; test other runtimes (Go, Python) for identical chunked encoding parser issues.

## MITRE ATT&CK
- T1499.4 - Application Layer Denial of Service

## Notes
CVE-2024-22019 demonstrates how HTTP/1.1 protocol edge cases can circumvent higher-level request validation. The effectiveness bypass of timeouts and body limits indicates parser-level vulnerability rather than application logic flaw. Coordination with Node.js security team resulted in February 2024 patch.

## Full report
<details><summary>Expand</summary>

I'd like to report Node.js vulnerability (CVE-2024-22019) that was recently fixed:
- HackerOne report: https://hackerone.com/reports/2233486
- Release notes: https://nodejs.org/en/blog/vulnerability/february-2024-security-releases

## Impact

This is a major issue because it allows unbounded resource (CPU, network bandwidth) consumption of the standard Node.js http server. The standard methods which could help blocking a malicious requests like timeouts and limiting request body size do not seem to work.

</details>

---
*Analysed by Claude on 2026-05-24*
