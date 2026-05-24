# Full Path Disclosure via MySQL Connection Error - Internal Database Host Exposure

## Metadata
- **Source:** HackerOne
- **Report:** 157876 | https://hackerone.com/reports/157876
- **Submitted:** 2016-08-09
- **Reporter:** jamesclyde
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Information Disclosure, Path Traversal/Full Path Disclosure, Error-Based Information Leak, Infrastructure Reconnaissance
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An unhandled MySQL connection error on a Shopify service exposes detailed internal infrastructure information including database host names (shardm-reader.chi2.shopify.io), full application file paths, and framework architecture. The error response reveals sensitive details about the application's internal structure through verbose stack traces that should be suppressed in production environments.

## Attack scenario
1. Attacker discovers a Shopify-owned IP address (104.196.154.1) or associated domain
2. Attacker sends a request to the application which triggers a MySQL database connection attempt
3. The database host 'shardm-reader.chi2.shopify.io' is unreachable or misconfigured, causing a connection failure
4. Instead of generic error page, application returns unhandled exception with full stack trace to the attacker
5. Stack trace reveals internal code structure, file paths, gem versions, and database infrastructure names
6. Attacker uses gathered intelligence for further reconnaissance, targeting, or exploiting downstream services

## Root cause
Insufficient error handling in production environment where database connection exceptions are not caught and sanitized. The Rails application is returning verbose debug/development error pages with full stack traces in production, exposing internal implementation details through lib/patches/mysql_monitoring.rb and related middleware.

## Attacker mindset
Reconnaissance-focused reconnaissance. The attacker is mapping infrastructure, identifying internal service names and architecture patterns. This information is valuable for understanding Shopify's internal topology, database sharding strategy (chi2 shard), and potential attack surface for lateral movement or targeted exploits against database connection pools or monitoring systems.

## Defensive takeaways
- Implement generic error responses in production - never expose stack traces, file paths, or internal hostnames to end users
- Configure Rails error handling to suppress sensitive details (config.consider_all_requests_local = false in production)
- Use custom error pages that log full details server-side but return minimal information to clients
- Implement centralized exception handling middleware to catch and sanitize database connection errors before response
- Monitor and alert on database connection failures rather than exposing them publicly
- Implement DNS security and internal service naming that doesn't expose shard topology (use opaque identifiers)
- Regular security audits of error handling across all controllers and middleware layers
- Use Web Application Firewalls to detect and block requests triggering verbose error responses

## Variant hunting
Hunt for similar verbose error responses in other Shopify services by: (1) Testing invalid database configurations on other IPs/domains, (2) Triggering various exception types (Redis, Memcached, API timeouts) to see if they leak similar information, (3) Examining other middleware that might wrap database calls (connection.rb, benchmarking.rb patterns), (4) Testing different HTTP methods and headers that might bypass error sanitization, (5) Looking for similar infrastructure naming patterns in cached responses or headers

## MITRE ATT&CK
- T1590.004 - Gather Victim Network Information (DNS)
- T1592.004 - Gather Victim Host Information (Client Configurations)
- T1217 - Browser Bookmark Discovery
- T1040 - Traffic Sniffing (passive infrastructure enumeration)
- T1580 - Cloud Infrastructure Discovery

## Notes
This is a classic information disclosure vulnerability in production environments. While not directly exploitable for code execution or data access, the exposed infrastructure names (shardm-reader.chi2.shopify.io) and application paths significantly reduce the reconnaissance effort required for sophisticated attacks. The 'chi2' shard identifier suggests Shopify's multi-region/multi-shard database architecture. The stack trace also reveals dependency versions (ruby 2.2.0, statsd-instrument, semian for circuit breaking) which could have known vulnerabilities. Reports shows good security awareness by reporter but lacks impact assessment details.

## Full report
<details><summary>Expand</summary>

Hello,

Found a website of you guys that is poiting to: shardm-reader.chi2.shopify.io' 
This domain is disclosure fill path because there is none MySQL server host.

POC: https://104.196.154.1/

Response a whole page with path disclosures:

lib/patches/mysql_monitoring.rb:19:in `connect'
lib/patches/mysql_monitoring.rb:19:in `block in raw_connect_with_monitoring'
lib/patches/mysql_monitoring.rb:18:in `raw_connect_with_monitoring'
lib/routing/connection.rb:15:in `connection'
app/models/concerns/benchmarking.rb:15:in `block (2 levels) in add_benchmark_around_method'
app/models/concerns/benchmarking.rb:24:in `with_benchmark'
app/models/concerns/benchmarking.rb:14:in `block in add_benchmark_around_method'
app/models/shop.rb:619:in `for_domain'
app/controllers/application_controller.rb:303:in `shop_for'
app/controllers/application_controller.rb:96:in `with_shop_fallback'
app/controllers/application_controller.rb:87:in `with_shop'
app/controllers/application_controller.rb:73:in `set_billing_api_request_id'
app/controllers/application_controller.rb:64:in `add_request_id_to_log_context'
app/controllers/application_controller.rb:245:in `conditionally_enable_debug_log'
app/controllers/application_controller.rb:54:in `block in identity_cache_memoization'
app/controllers/application_controller.rb:54:in `identity_cache_memoization'
/artifacts/ruby/2.2.0/bundler/gems/statsd-instrument-50b2496ea65b/lib/statsd/instrument.rb:284:in `call'
/artifacts/ruby/2.2.0/bundler/gems/statsd-instrument-50b2496ea65b/lib/statsd/instrument.rb:284:in `block in measure'
/artifacts/ruby/2.2.0/bundler/gems/statsd-instrument-50b2496ea65b/lib/statsd/instrument.rb:53:in `duration'
/artifacts/ruby/2.2.0/bundler/gems/statsd-instrument-50b2496ea65b/lib/statsd/instrument.rb:284:in `measure'
/artifacts/ruby/2.2.0/bundler/gems/statsd-instrument-50b2496ea65b/lib/statsd/instrument.rb:75:in `block (3 levels) in statsd_measure'
/artifacts/ruby/2.2.0/bundler/gems/statsd-instrument-50b2496ea65b/lib/statsd/instrument.rb:284:in `call'
/artifacts/ruby/2.2.0/bundler/gems/statsd-instrument-50b2496ea65b/lib/statsd/instrument.rb:284:in `block in measure'
/artifacts/ruby/2.2.0/bundler/gems/statsd-instrument-50b2496ea65b/lib/statsd/instrument.rb:53:in `duration'
/artifacts/ruby/2.2.0/bundler/gems/statsd-instrument-50b2496ea65b/lib/statsd/instrument.rb:284:in `measure'
/artifacts/ruby/2.2.0/bundler/gems/statsd-instrument-50b2496ea65b/lib/statsd/instrument.rb:75:in `block (2 levels) in statsd_measure'
semian (0.4.1) lib/semian/mysql2.rb:82:in `block in connect'


Please let me know!!

</details>

---
*Analysed by Claude on 2026-05-24*
