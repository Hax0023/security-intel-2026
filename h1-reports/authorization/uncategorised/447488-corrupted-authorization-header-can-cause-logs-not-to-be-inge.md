# Corrupted Authorization Header Causes Log Ingestion Failure Due to Unescaped Delimiters in nginx Log Format

## Metadata
- **Source:** HackerOne
- **Report:** 447488 | https://hackerone.com/reports/447488
- **Submitted:** 2018-11-20
- **Reporter:** jobert
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Log Injection, Log Parsing Failure, Information Disclosure, Incident Response Evasion
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker can inject whitespace characters into the Authorization header (via Basic auth credentials containing spaces) to corrupt the nginx access log format, causing log entries to be discarded by the log ingestion system. This allows attackers to evade logging and complicate incident response investigations by removing audit trails of their requests.

## Attack scenario
1. Attacker crafts HTTP request with Basic Authentication credentials containing spaces (e.g., '-u "- A:B"')
2. nginx receives request and extracts remote_user variable from decoded Authorization header as '- A'
3. nginx writes log entry with unescaped remote_user value containing whitespace, creating an additional field delimiter
4. Log ingestion system (███████) receives malformed log entry with unexpected number of fields
5. Log parser fails validation/schema validation and discards the entire log entry
6. Attacker's request is still processed by backend (Rails app accessible via logs), but load balancer access log is missing

## Root cause
nginx log format does not quote the $remote_user variable and does not escape special characters. When user credentials in the Authorization header contain whitespace, nginx includes these unescaped spaces in the log, breaking the field delimiter structure. The log ingestion system expects a fixed field count and discards entries with unexpected delimiters.

## Attacker mindset
Evade detection and logging mechanisms to hide malicious activity. An attacker would use this to conduct reconnaissance or attacks while remaining undetected in access logs, complicating forensic investigation. Since backend Rails logs are JSON-formatted, they remain intact, but the load balancer logs (often first point of analysis) are eliminated.

## Defensive takeaways
- Always quote variables in log formats that may contain untrusted user input: '$remote_user' should be '"$remote_user"'
- Implement strict field count validation in log parsers with clear error handling rather than silent discard
- URL-encode or escape special characters (whitespace, quotes, delimiters) in log output
- Design log parsers to be resilient to malformed entries (log and skip rather than silently discard)
- Use structured logging (JSON) instead of space-delimited formats where possible
- Monitor for log ingestion failures/gaps as a potential security indicator
- Validate Authorization header format before logging; sanitize or redact sensitive authentication data
- Maintain redundant logging sources (e.g., Rails JSON logs as backup) for critical security events

## Variant hunting
Check if $http_referer can be similarly exploited with newline injection (CRLF) to split log entries
Test $http_user_agent for whitespace/delimiter injection attacks
Investigate if $cookie___cfduid mentioned in report has same vulnerability
Examine other unquoted nginx variables for delimiter injection possibilities
Test if newline characters (\n, \r\n) in headers cause log entry splitting across multiple lines
Check if other log ingestion backends (ELK, Splunk, etc.) have similar parsing vulnerabilities with malformed fields
Review custom log format implementations in other services for similar unquoted variable patterns

## MITRE ATT&CK
- T1562.008 - Impair Defenses: Disable or Modify Logging
- T1036.005 - Masquerading: Match Legitimate Name or Location
- T1027 - Obfuscation of Command and Service Information
- T1070.001 - Indicator Removal: Clear Logs

## Notes
Low immediate impact due to redundant JSON logging in Rails backend, but highlights systemic risk in audit trail reliability. The root cause exists at multiple layers: nginx not escaping/quoting log variables, and log ingestion system not handling malformed entries gracefully. This is a defense-in-depth failure. Similar vulnerabilities likely exist in standard nginx deployments with default log formats. The fix should occur at both nginx configuration level (quote variables) and ingestion level (robust parsing). Reporter demonstrates good security thinking by identifying both the attack vector and systemic logging gaps.

## Full report
<details><summary>Expand</summary>

HackerOne ingests different logs in ██████, one of them being nginx access logs from our load balancers. The default log format of our load balancer configuration is shown below. As can be seen in the format, the HTTP user specified in the `Authorization` header (`$remote_user`) is placed between the `$remote_addr` and `[$time_local]`. A log entry is delimited with white space and the `$remote_user` variable isn't surrounded with quotes. When a user isn't specified, its value is set to `-`.

During a white box test of another component in a network, it was identified that an additional delimiter can be injected, which seems to cause ingestion of the log entry to fail and the log entry to be discarded.

**H1 nginx log format**
```
log_format cf_custom '$remote_addr - $remote_user [$time_local] '
                     '"$request" $status $body_bytes_sent '
                     '"$http_referer" "$http_user_agent" "$host" '
                     '$request_time $upstream_response_time $pipe '
                     '$http_cf_ray $cookie___cfduid '
                     '"$http_x_forwarded_proto" "$http_x_forwarded_for" '
                     '"$http_x_amzn_trace_id"';
```

Consider the following cURL command:

```
curl -X POST -u '- A:B' https://hackerone.com/graphql\?secret\=1
```

This will result in the following request being submitted:

**HTTP request**
```
POST /graphql?secret=1 HTTP/2
Host: hackerone.com
Authorization: Basic LSBBOkI=
User-Agent: curl/7.54.0
Accept: */*
```

When this request is processed by nginx, the `$remote_user` (`- A`) is being added to the log entry. However, since the delimiter (the whitespace) isn't escaped and no quotes are surrounding the value, an additional column is added to the log entry. When this is ingested by █████████, the log for that particular request doesn't seem to appear in the Events source. However, as the request itself is valid, it'll be proxied to the upstream.

Because our Rails logs have a different format (JSON), we do have the ability to still determine which requests were sent to our backend. There are very few requests who are stopped on our load balancer and none of them have the ability to interact directly with out database. This lowers the impact of the vulnerability. However, in order for us to rely on either access log that is being ingested, we should address this issue.

It is currently unknown where the root cause of this vulnerability lies. nginx, by default, uses a very similar log item format: http://nginx.org/en/docs/http/ngx_http_log_module.html. Similar to the HackerOne configuration, the `$remote_user` is not enclosed in double quotes. The fact that nginx doesn't encode the whitespace may actually be something they want to fix going forward. However, it seems rather odd that █████████ completely discards a log entry. Let's figure out where the vulnerability comes from and what we can do to fix it.

The `$cookie___cfduid` parameter may also be vulnerable to the same attack.

## Impact

This may impact our ability to give a conclusive answer during incident response or debugging based on the nginx load balancer access logs.

</details>

---
*Analysed by Claude on 2026-05-24*
