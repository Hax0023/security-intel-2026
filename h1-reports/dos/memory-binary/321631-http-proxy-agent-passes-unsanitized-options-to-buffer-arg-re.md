# http-proxy-agent Buffer Allocation Vulnerability - DoS and Memory Leak

## Metadata
- **Source:** HackerOne
- **Report:** 321631 | https://hackerone.com/reports/321631
- **Submitted:** 2018-03-03
- **Reporter:** chalker
- **Program:** http-proxy-agent npm package
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Improper Input Validation, Unsafe Buffer Constructor Usage, Denial of Service, Information Disclosure, CWE-400: Uncontrolled Resource Consumption, CWE-476: NULL Pointer Dereference
- **CVEs:** None
- **Category:** memory-binary

## Summary
The http-proxy-agent module passes unsanitized user-supplied auth options directly to the Buffer constructor without validation, allowing attackers to trigger CPU/memory exhaustion DoS attacks. On Node.js versions <8.x, this vulnerability also leaks uninitialized memory containing sensitive server data.

## Attack scenario
1. Attacker controls or influences the 'auth' parameter in proxy configuration (e.g., via JSON API input, environment variables, or configuration files)
2. Attacker supplies a large numeric value (e.g., 1e9) or malformed data type as the auth parameter
3. The vulnerable code passes this unsanitized value directly to Buffer constructor: Buffer(auth)
4. Buffer constructor interprets numeric argument as allocation size, attempting to allocate enormous heap memory
5. System CPU spikes to 100% during allocation attempt, causing severe performance degradation or complete DoS
6. On Node.js <8.x, uninitialized memory chunks containing potentially sensitive data are returned to attacker

## Root cause
The module at line 80 of index.js directly passes the auth option to the Buffer constructor without type checking or validation. The old Buffer() constructor API (deprecated in Node.js 6.0) treats numeric arguments as allocation sizes rather than data to encode, creating a semantic gap between developer intent and actual behavior.

## Attacker mindset
An attacker exploiting this would seek to cause service disruption by exhausting system resources. Secondary motivation includes memory content exfiltration on older Node.js versions. The attack is trivial to execute with minimal code and requires only influence over proxy configuration parameters.

## Defensive takeaways
- Always validate and sanitize user-supplied options before passing to Buffer constructor or other low-level APIs
- Use Buffer.from(data, 'utf8') or Buffer.alloc(size) instead of deprecated Buffer(arg) constructor
- Implement strict type checking on configuration parameters - validate auth is a string before buffer operations
- Apply allowlist validation for proxy configuration inputs rather than relying on implicit type coercion
- Keep Node.js updated to >=8.x to eliminate uninitialized memory exposure (though DoS remains possible)
- Add input sanitization tests that specifically target numeric and unexpected type inputs
- Use resource limits and timeouts on buffer allocation operations to catch excessive memory requests

## Variant hunting
Similar vulnerabilities likely exist in: (1) https-proxy-agent package (acknowledged as separate but similar), (2) Any proxy agent modules accepting user-controlled auth parameters, (3) Other modules passing unvalidated options to deprecated Buffer() constructor, (4) Modules constructing buffers from user input in authentication/header processing logic, (5) Proxy middleware in Express/Node frameworks handling authentication options

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1499: Endpoint Denial of Service
- T1557: Man-in-the-Middle
- T1005: Data from Local System
- T1040: Network Sniffing

## Notes
This report demonstrates critical importance of understanding API semantic changes in Node.js. The deprecated Buffer() constructor behavior change between versions is a common source of vulnerabilities. The researcher responsibly disclosed but did not directly contact maintainer initially. The vulnerability affects extremely popular package (2.9M+ monthly downloads), making impact substantial. Memory leak aspect only manifest on Node.js <8.x but DoS works on all versions. Attack complexity is extremely low - one-liner modification to proxy config suffices.

## Full report
<details><summary>Expand</summary>

I would like to report a Buffer allocation vulnerability in `http-proxy-agent`.

In setups where auth argument is user-controlled, it allows to:

cause Denial of Service by trivially consuming all the available CPU resources
extract uninitialized memory chunks from the server on Node.js <8.x.
# Module

**module name:** `http-proxy-agent`
**version:** 2.0.0
**npm page:** `https://www.npmjs.com/package/http-proxy-agent`

## Module Description

> This module provides an http.Agent implementation that connects to a specified HTTP or HTTPS proxy server, and can be used with the built-in http module.

## Module Stats

112 721 downloads in the last day
707 979 downloads in the last week
2 953 077 downloads in the last month

# Vulnerability

## Vulnerability Description

`http-proxy-agent` passes `auth` option to the Buffer constructor without proper sanitization, resulting in DoS and uninitialized memory leak in setups where an attacker could submit typed input to the 'auth' parameter (e.g. JSON).

The exact line: https://github.com/TooTallNate/node-http-proxy-agent/blob/master/index.js#L80

## Steps To Reproduce:

### DoS

```js
var url = require('url');
var http = require('http');
var HttpProxyAgent = require('http-proxy-agent');

var proxy = {
  protocol: 'http:',
  host: "127.0.0.1",
  port: 8080
};

setInterval(() => {
  proxy.auth = 1e9; // a number as 'auth'
  var opts = url.parse('http://example.com/');
  var agent = new HttpProxyAgent(proxy);
  opts.agent = agent;
  console.time('tick');
  http.get(opts);
  console.timeEnd('tick');
}, 200);
```

Observe how this is consuming memory and CPU — each request takes >1 second in the main thread on my setup.

### Uninitialized memory leak

```js
// listen with: nc -l -p 8080

var url = require('url');
var http = require('http');
var HttpProxyAgent = require('http-proxy-agent');

var proxy = {
  protocol: 'http:',
  host: "127.0.0.1",
  port: 8080
};

proxy.auth = 500; // a number as 'auth'
var opts = url.parse('http://example.com/');
var agent = new HttpProxyAgent(proxy);
opts.agent = agent;
http.get(opts);
```

Listen with `nl -l -p 8080` to see requests.

Execute on various Node.js versions — 4.x LTS, 6.x LTS, 8.x LTS / 9.x.

This leaks uninitialized Buffer memory on Node.js <8.x.
On ≥8.x those Buffers (that are using the deprecated API) are zero-filled.

## Supporting Material/References:

> State all technical information about the stack where the vulnerability was found

- OS: Arch Linux current
- Node.js 9.5.0
- npm 5.6.0
- gnu-netcat 0.7.1

# Wrap up

- I contacted the maintainer to let them know: N
- I opened an issue in the related repository: N

# Note

Almost entirely similar to `https-proxy-agent`, but this is a separate package, a separate GitHub repo, different version numbers, different lines in code, different download stats.

## Impact

Denial of service
Sensitive data leak (on Node.js <8.0)

</details>

---
*Analysed by Claude on 2026-05-24*
