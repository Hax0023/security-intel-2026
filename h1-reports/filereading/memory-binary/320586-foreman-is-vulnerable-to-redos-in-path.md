# ReDoS (Regular Expression Denial of Service) in foreman path parsing

## Metadata
- **Source:** HackerOne
- **Report:** 320586 | https://hackerone.com/reports/320586
- **Submitted:** 2018-02-28
- **Reporter:** chalker
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Regular Expression Denial of Service (ReDoS), Denial of Service (DoS)
- **CVEs:** None
- **Category:** memory-binary

## Summary
The foreman npm package (v2.0.0) contains a vulnerable regex pattern in path parsing that allows attackers to cause denial of service through ReDoS attacks. By supplying a crafted path with repeated characters, an attacker can cause the regex engine to enter catastrophic backtracking, blocking requests for ~5 seconds each.

## Attack scenario
1. Attacker identifies that foreman service is running and listening on a network port (e.g., 9999)
2. Attacker crafts a malicious HTTP request with a path containing repeated characters (e.g., http://0000...0000 with ~81000 characters)
3. Attacker sends the crafted request to the foreman service
4. The vulnerable regex `/http://[^/]*:?[0-9]*(/.*)$/` attempts to parse the path and enters catastrophic backtracking
5. The regex engine blocks for approximately 5 seconds processing the malicious input
6. Attacker can repeat requests in intervals to maintain continuous denial of service against the target service

## Root cause
The regex pattern `/http://[^/]*:?[0-9]*(/.*)$/` is vulnerable to ReDoS due to nested quantifiers and overlapping character classes. The `[^/]*` followed by optional `:?[0-9]*` creates ambiguous matching paths that cause exponential backtracking when the regex engine fails to match input, especially with long strings of repeated characters.

## Attacker mindset
An attacker seeks to disrupt service availability by exploiting inefficient regex processing. The attack requires minimal resources (a single script sending periodic requests) to cause significant impact (5-second blocking per request). The vulnerability is attractive because it requires no authentication and can be exploited from a remote client.

## Defensive takeaways
- Avoid using complex regex patterns with nested quantifiers and overlapping character classes; use simpler, non-backtracking patterns or dedicated URL parsing libraries
- Use timeout mechanisms or regex engine limits to prevent long-running regex operations
- Implement rate limiting and request validation to reject obviously malformed paths before regex processing
- Use library functions like URL.parse() or node's built-in url module instead of custom regex patterns for URL parsing
- Conduct security testing for ReDoS vulnerabilities in any user-controlled input matched against regex patterns
- Apply input length restrictions to paths and validate format before expensive processing
- Monitor service performance and set alerts for requests causing abnormal CPU consumption

## Variant hunting
Search for other regex patterns in foreman codebase and similar Node.js packages that parse URLs or paths. Look for patterns with: (1) nested quantifiers like `*+`, `*?`, `+*`, (2) alternation with overlapping patterns, (3) character classes followed by overlapping quantifiers. Test other packages in strongloop ecosystem that may share similar URL parsing logic.

## MITRE ATT&CK
- T1190
- T1498

## Notes
The reporter did not contact the maintainer or open an issue before disclosure. The vulnerability affects ~1.7M estimated annual downloads of the package, indicating broad potential impact. The ReDoS is triggered during HTTP request parsing in the forward proxy functionality of foreman. Mitigation should prioritize replacing the custom regex with standard URL parsing methods.

## Full report
<details><summary>Expand</summary>

I would like to report ReDoS in `foreman`.
It allows to cause denial of service by suppling a crafted path.

# Module

**module name:** foreman
**version:** 2.0.0
**npm page:** `https://www.npmjs.com/package/foreman`

## Module Description

> Node Foreman is a Node.js version of the popular Foreman tool, with a few Node specific changes.

## Module Stats

5 296 downloads in the last day
30 879 downloads in the last week
141 342 downloads in the last month

~1 696 104 estimated downloads per year

# Vulnerability

## Vulnerability Description

ReDoS.

Regex: `/http:\/\/[^/]*:?[0-9]*(\/.*)$/`
Evil string: `http://${Array(81000).join('0')}` (unwrap js template)
Line: https://github.com/strongloop/node-foreman/blob/v2.0.0/forward.js#L30
Blocks for ~5 seconds per request.

## Steps To Reproduce:

`nf start -f 9999`

```js
const net = require('net');
const tick = function() {
const client = net.createConnection({ port: 9999 }, () => {
  client.write(`GET http://${Array(81000).join('0')} HTTP/1.1
Host: localhost:9999


"`);
  });
}
setInterval(tick, 1000)
```

## Supporting Material/References:

- OS: Arch Linux current
- Node.js 9.5.0
- npm 5.6.0

# Wrap up

- I contacted the maintainer to let him know: N
- I opened an issue in the related repository: N

## Impact

Denial of Service by passing crafted paths.

</details>

---
*Analysed by Claude on 2026-05-24*
