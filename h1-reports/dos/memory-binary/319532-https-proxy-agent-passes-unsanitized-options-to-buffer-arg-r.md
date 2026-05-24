# https-proxy-agent Buffer allocation vulnerability via unsanitized auth parameter

## Metadata
- **Source:** HackerOne
- **Report:** 319532 | https://hackerone.com/reports/319532
- **Submitted:** 2018-02-25
- **Reporter:** chalker
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Improper Input Validation, Buffer Overflow / Allocation Abuse, Denial of Service, Information Disclosure, CWE-400: Uncontrolled Resource Consumption
- **CVEs:** None
- **Category:** memory-binary

## Summary
https-proxy-agent versions ≤2.1.1 pass unsanitized user-controlled auth parameters directly to the Buffer constructor, allowing attackers to trigger excessive memory allocation and CPU consumption. On Node.js versions prior to 8.x, this vulnerability also enables leakage of uninitialized memory containing sensitive data.

## Attack scenario
1. Attacker identifies an application using https-proxy-agent with user-controlled proxy configuration (e.g., JSON API accepting auth parameter)
2. Attacker submits a large numeric value (e.g., 1e9) as the auth parameter instead of a string
3. The vulnerable code invokes Buffer(auth) where auth is the numeric value, triggering allocation of gigabytes of memory
4. Memory allocation consumes available RAM and causes CPU spinning during initialization
5. On Node.js <8.x, attacker receives uninitialized buffer contents in HTTP responses, leaking sensitive server memory
6. Repeated requests cause complete application DoS and potential system-level resource exhaustion

## Root cause
Line 207 in index.js passes the auth parameter directly to Buffer constructor without type checking or sanitization. In Node.js, Buffer(number) allocates that many bytes of memory. When auth is user-controlled and typed as a number, this creates arbitrary allocation primitive.

## Attacker mindset
An attacker would recognize this as a classic typed-input vulnerability in a widely-used library (81M+ annual downloads). The low barrier to exploitation (single numeric parameter) combined with high impact (DoS + memory leak) makes this an attractive target. The vulnerability affects LTS versions of Node.js including 4.x and 6.x, ensuring broad applicability.

## Defensive takeaways
- Always validate and sanitize user input before passing to security-sensitive APIs like Buffer constructors
- Implement explicit type checking on all user-controlled parameters, especially in proxy/network configuration
- Use Buffer.alloc() with explicit size validation rather than legacy Buffer(size) constructor when size is derived from user input
- Enforce input schema validation at API boundaries (e.g., auth must be string or null, never number)
- Apply fuzzing and property-based testing to library initialization code with varied input types
- Review changelog for Buffer allocation changes between Node.js versions (8.0 introduced zero-fill breaking change)
- Implement resource limits and timeouts around proxy agent initialization

## Variant hunting
Search for similar patterns: (1) Buffer constructors receiving unvalidated parameters in http-proxy-agent, proxy-agent, and related networking libraries; (2) Other Node.js modules passing user input to size-sensitive allocators without type checking; (3) Proxy libraries with similar auth parameter handling in request header construction; (4) Code using deprecated Buffer APIs with numeric arguments derived from configuration

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1499: Endpoint Denial of Service
- T1040: Traffic Capture or Redirection (memory leak aspect)

## Notes
Reporter did not contact maintainer or open issues prior to submission. Vulnerability is in a core dependency used by millions of applications. The memory leak aspect (uninitialized buffer contents) is particularly severe on older Node.js versions still in use at time of report (Node 4/6 LTS). Fix should involve: (1) type coercion/validation, (2) string encoding of auth for Buffer operations, or (3) refactoring to avoid Buffer constructor entirely. Wide attack surface due to library popularity and common pattern of accepting proxy configs from environment/configuration sources.

## Full report
<details><summary>Expand</summary>

I would like to report a Buffer allocation vulnerability in `https-proxy-agent`.

In setups where `auth` argument is user-controlled, it allows to:
1. cause Denial of Service by trivially consuming all the available CPU resources
2. extract uninitialized memory chunks from the server on Node.js <8.x.

# Module

**module name:** https-proxy-agent
**version:** 2.1.1 
**npm page:** `https://www.npmjs.com/package/https-proxy-agent`

## Module Description

> This module provides an http.Agent implementation that connects to a specified HTTP or HTTPS proxy server, and can be used with the built-in https module.

## Module Stats

114 304 downloads in the last day
1 668 955 downloads in the last week
6 758 891 downloads in the last month

~81 106 692 estimated downloads per year

# Vulnerability

## Vulnerability Description

`https-proxy-agent` passes `auth` option to the Buffer constructor without proper sanitization, resulting in DoS and uninitialized memory leak in setups where an attacker could submit typed input to the 'auth' parameter (e.g. JSON).

The exact line: https://github.com/TooTallNate/node-https-proxy-agent/blob/2.1.1/index.js#L207

## Steps To Reproduce:

### DoS
```js
var url = require('url');
var https = require('https');
var HttpsProxyAgent = require('https-proxy-agent');

var proxy = {
  protocol: 'http:',
  host: "127.0.0.1",
  port: 8080
};

setInterval(() => {
  proxy.auth = 1e9; // a number as 'auth'
  var opts = url.parse('https://example.com/');
  var agent = new HttpsProxyAgent(proxy);
  opts.agent = agent;
  console.time('tick');
  https.get(opts);
  console.timeEnd('tick');
}, 200);
```

Observe how this is consuming memory and CPU — each request takes >1 second in the main thread on my setup.

### Uninitialized memory leak

```js
// listen with: nc -l -p 8080

var url = require('url');
var https = require('https');
var HttpsProxyAgent = require('https-proxy-agent');

var proxy = {
  protocol: 'http:',
  host: "127.0.0.1",
  port: 8080
};

proxy.auth = 500; // a number as 'auth'
var opts = url.parse('https://example.com/');
var agent = new HttpsProxyAgent(proxy);
opts.agent = agent;
https.get(opts);
```

Listen with `nl -l -p 8080` to see requests.

Execute on various Node.js versions — 4.x LTS, 6.x LTS, 8.x LTS / 9.x.

This leaks uninitialized Buffer memory on Node.js <8.x.
On ≥8.x those Buffers (that are using the deprecated API) are zero-filled.

## Supporting Material/References:

- OS: Arch Linux current
- Node.js 9.5.0
- npm 5.6.0
- gnu-netcat 0.7.1

# Wrap up

- I contacted the maintainer to let him know: N
- I opened an issue in the related repository: N

## Impact

Denial of service
Sensitive data leak (on Node.js <8.0)

</details>

---
*Analysed by Claude on 2026-05-24*
