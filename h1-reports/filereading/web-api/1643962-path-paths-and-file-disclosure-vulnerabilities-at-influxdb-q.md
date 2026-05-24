# Path Traversal and File Disclosure Vulnerabilities at influxdb.quality.gitlab.net

## Metadata
- **Source:** HackerOne
- **Report:** 1643962 | https://hackerone.com/reports/1643962
- **Submitted:** 2022-07-20
- **Reporter:** otoyyy_h1
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Information Disclosure, Debug Endpoint Exposure, Sensitive Data Exposure, Improper Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
Multiple debug and metrics endpoints on influxdb.quality.gitlab.net expose sensitive information including goroutine stacks, heap dumps, and application metrics without authentication. An unauthenticated attacker can access these endpoints to retrieve stack traces, memory profiles, and server statistics that may disclose application internals, credentials, and system information.

## Attack scenario
1. Attacker discovers influxdb.quality.gitlab.net domain through reconnaissance
2. Attacker accesses /debug/pprof endpoint which lists available profiling endpoints
3. Attacker retrieves goroutine dump via /debug/pprof/goroutine?debug=1 to analyze running threads and stack traces
4. Attacker accesses /debug/pprof/heap to inspect memory allocations and potentially discover sensitive data in memory
5. Attacker collects /debug/pprof/trace and /metrics/ data to understand application behavior and infrastructure
6. Attacker analyzes gathered data to identify credentials, API keys, or internal system details for further exploitation

## Root cause
Go's net/http/pprof debug package was enabled in production without authentication controls. The application exposed debugging endpoints that are intended for development only, allowing unauthenticated access to profiling data. Missing middleware or access controls to restrict these endpoints to authorized users or internal networks.

## Attacker mindset
An attacker performs reconnaissance to identify debug endpoints that are commonly left exposed. They recognize that pprof endpoints and metrics interfaces provide valuable information about application internals, memory state, and system configuration. The attacker exploits the lack of authentication to gather intelligence for privilege escalation or lateral movement attacks.

## Defensive takeaways
- Disable or remove debug endpoints (pprof, metrics, stats) from production environments entirely
- If debugging capabilities are required, implement strict authentication and authorization controls
- Restrict access to debug endpoints to internal networks or VPN-only via network segmentation
- Implement middleware to require authentication tokens or API keys for sensitive endpoints
- Regularly audit deployed services for exposed debug interfaces using automated scanning
- Use configuration management to ensure debug mode is disabled by default in production builds
- Monitor access logs for unusual requests to /debug/* and /metrics/ endpoints
- Implement Web Application Firewall (WAF) rules to block access to known debug paths from external sources

## Variant hunting
Search for other exposed debug endpoints: /debug/vars, /debug/pprof/allocs, /debug/pprof/mutex, /debug/pprof/block, /debug/pprof/threadcreate. Check for exposed metrics endpoints: /prometheus/metrics, /actuator/metrics (Spring Boot), /_status, /health with verbose output. Identify other services running on same infrastructure with similar misconfigurations (Prometheus, Grafana, ElasticSearch).

## MITRE ATT&CK
- T1190
- T1592
- T1526
- T1040
- T1213
- T1087

## Notes
Report submission appears incomplete or template-based with generic boilerplate text about 'heap files' and 'relational operators' that may not be relevant to the actual vulnerability. The core issue is straightforward: unauthenticated access to Go pprof debug endpoints in production. GitLab infrastructure team should immediately disable these endpoints on quality/staging domains and implement proper access controls for any environment requiring debugging capabilities.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please note that initial triage is handled by HackerOne staff. They are identified with a `HackerOne triage` badge and will escalate to the GitLab team any. Please replace *all* the (parenthesized) sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

### Summary

Path paths and file disclosure vulnerabilities at influxdb.quality.gitlab.net

Hi, I discovered a file disclosure vulnerability within the influxdb.quality.gitlab.net domain This allows attackers to only get arbitrary files from remote servers. Where the file stack trace can be viewed without authentication. A heap file is an unordered set of records, stored on a set of pages. This class provides basic support for inserting, selecting, updating, and deleting records. Temporary heap files are used for external sorting and in other relational operators. A sequential scan of a heap file (via the Scan class) is the most basic access method.

### Steps to reproduce
Vulnerability endpoint:
```
1. https://influxdb.quality.gitlab.net/debug/pprof
2. https://influxdb.quality.gitlab.net/debug/pprof/goroutine?debug=1
3. https://influxdb.quality.gitlab.net/debug/pprof/heap
4. https://influxdb.quality.gitlab.net/debug/pprof/trace
5. https://influxdb.quality.gitlab.net/metrics/
6. https://influxdb.quality.gitlab.net/stats.json
```

## Impact

allows an attacker to read arbitrary files on the server that is running an application. This might include application code and data, credentials for back-end systems, and sensitive operating system files. In some cases, an attacker might be able to write to arbitrary files on the server, allowing them to modify application data or behavior, and ultimately take full control of the server.

</details>

---
*Analysed by Claude on 2026-05-24*
