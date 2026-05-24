# curl Globbing Pattern DoS - Unbounded Range Expansion

## Metadata
- **Source:** HackerOne
- **Report:** 1572120 | https://hackerone.com/reports/1572120
- **Submitted:** 2022-05-16
- **Reporter:** iylz
- **Program:** curl
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Denial of Service, Resource Exhaustion, Uncontrolled Resource Consumption
- **CVEs:** None
- **Category:** memory-binary

## Summary
curl's URL globbing feature allows expansion of numeric ranges like [1-9999999999999999999] without reasonable limits, enabling attackers to trigger massive numbers of requests. This causes excessive CPU and network resource consumption on the client machine or can be weaponized to launch distributed DoS attacks against third-party servers.

## Attack scenario
1. Attacker crafts a malicious curl command with an extremely large numeric range glob pattern (e.g., [1-9999999999999999999])
2. Curl expands the glob pattern into hundreds of individual URLs without validating the range size
3. Client system initiates thousands of concurrent or sequential HTTP requests to the target server
4. Server resources (bandwidth, connections, processing) become exhausted handling the flood of requests
5. Legitimate traffic is unable to reach the target server, resulting in denial of service
6. Attack can be distributed by compromising multiple systems or scripting curl invocations

## Root cause
curl's globbing parser fails to implement bounds checking on numeric range expansion. The code accepts arbitrarily large range specifications (e.g., [1-9999999999999999999]) and attempts to expand them fully without limiting the number of resulting URLs or validating the range is reasonable.

## Attacker mindset
Exploit a built-in feature that was intended for legitimate batch URL requests (like [1-10]) by pushing it to extreme values. The attacker recognizes that curl trusts user input for glob patterns and doesn't validate expansion size, enabling trivial DoS without requiring network access to the target or special privileges.

## Defensive takeaways
- Implement strict limits on numeric range expansion in glob patterns (e.g., maximum 1000 URLs per pattern)
- Add warnings when glob expansion would produce excessive URLs and require explicit user confirmation
- Consider making globbing an opt-in feature rather than default behavior
- Validate range specifications before expansion and reject unreasonably large ranges
- Log and alert on unusual glob patterns that could indicate attack attempts
- Document safe globbing practices and warn users against untrusted glob pattern inputs

## Variant hunting
Test character range expansion [a-z] with extreme character sets
Investigate step parameter abuse: [1-9999999:999] to create massive stepped sequences
Check if multiple nested globs compound the expansion: [1-1000]/[1-1000]
Test globbing in other curl contexts: headers, POST data, cookie values
Examine if glob limits differ between sequential and parallel request modes
Research other URL parsing libraries for similar unbounded expansion vulnerabilities

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
The vulnerability demonstrates how legitimate features (globbing for batch operations) can become attack vectors when missing proper input validation and resource limits. The issue is particularly critical because curl's globbing is relatively transparent to users, who may not realize the resource implications of their patterns. Remediation should balance functionality with safety guardrails.

## Full report
<details><summary>Expand</summary>

## Summary:
[add summary of the vulnerability]

The curl "globbing" allows too much scope, which can cause the server to be denied service or used to attack third-party websites. The globbing allow [1-9999999999999999999] to parse in the url. So when curl request for 'http://127.0.0.1/[1-9999999999999999999]', the can cause 300 requests in the server.

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Listen 8000 port: python -m SimpleHTTPServer 8000
  2.  command: nohup ./curl -vv 'http://127.0.0.1:8000/[1-9999999999999999999]/' &
  3. Check the server resource process. There are a lot of network requests and CPU consumption. 

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * [attachment / reference]

## Impact

With this function, the resources of the server running curl request can be excessively consumed or a large number of URL accesses to other websites can be initiated, resulting in denial of service.

</details>

---
*Analysed by Claude on 2026-05-24*
