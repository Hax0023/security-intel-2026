# memjs Buffer Allocation Vulnerability - DoS and Uninitialized Memory Exposure

## Metadata
- **Source:** HackerOne
- **Report:** 319809 | https://hackerone.com/reports/319809
- **Submitted:** 2018-02-26
- **Reporter:** chalker
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Improper Input Validation, Buffer Overflow, Uninitialized Memory Access, Denial of Service, Information Disclosure
- **CVEs:** CVE-2018-3767
- **Category:** memory-binary

## Summary
memjs passes user-supplied values directly to the Buffer constructor without sanitization, allowing attackers to allocate excessive memory (DoS) or leak uninitialized heap memory containing sensitive data. The vulnerability affects setups where typed input (e.g., JSON numbers) can reach the storage value parameter.

## Attack scenario
1. Attacker submits JSON payload with large numeric value to application using memjs for caching
2. Application calls client.set() with attacker-controlled numeric value without type checking
3. memjs converts numeric value to Buffer constructor call: Buffer(2e9) allocates 2GB of memory
4. Repeated requests cause memory exhaustion, triggering DoS and application crash
5. On Node.js < 8.0, attacker retrieves stored value and accesses uninitialized heap memory
6. Uninitialized memory may contain sensitive data (credentials, encryption keys, user data)

## Root cause
The memjs library directly passes the `value` parameter to the Buffer constructor without type validation. When a number is passed instead of a string/buffer, Buffer(n) interprets it as a size allocation rather than data to store, causing unbounded memory allocation. Additionally, the uninitialized buffer is returned as-is on older Node.js versions before automatic zeroing was implemented.

## Attacker mindset
An attacker seeks to (1) exhaust server resources and crash the application via repeated large numeric allocations, or (2) extract sensitive in-memory data by exploiting uninitialized buffer returns. This is particularly attractive in multi-tenant environments or where JSON input is directly forwarded to cache operations without validation.

## Defensive takeaways
- Always validate and sanitize input types before passing to Buffer constructors
- Explicitly convert values to strings before storage operations
- Implement type checking/schema validation on user inputs (especially JSON)
- Use allowlists for acceptable data types in cache operations
- Consider wrapper functions that enforce parameter types
- Update Node.js to 8.0+ for automatic buffer zeroing
- Monitor memory allocation patterns and set resource limits
- Add input size limits to prevent DoS attacks

## Variant hunting
Check other memcache client libraries for similar Buffer constructor misuse
Search for direct Buffer(untrustedValue) patterns in npm ecosystem
Examine other serialization functions that accept numeric inputs without validation
Look for cases where JSON.parse() output is directly passed to Buffer operations
Investigate redis clients and other caching libraries for equivalent vulnerabilities
Search codebases for Buffer constructor calls without explicit string conversion

## MITRE ATT&CK
- T1190
- T1499
- T1557
- T1565

## Notes
The vulnerability demonstrates the critical importance of input validation when interfacing with system-level operations like memory allocation. The dual impact (DoS + information disclosure) makes this particularly severe. The fact that the maintainer was not contacted before disclosure is notable. This is a textbook example of type confusion vulnerability where implicit type coercion creates security boundaries.

## Full report
<details><summary>Expand</summary>

I would like to report a Buffer allocation vulnerability in `memjs`.

In cases when the attacker is able to pass typed input (e.g. via JSON) to the storage, it allows to cause DoS (on all Node.js versions) and to store (and potentially later extract) chunks of uninitialized server memory containing sensitive data.

# Module

**module name:** `memjs`
**version:** 1.1.0
**npm page:** `https://www.npmjs.com/package/memjs`

## Module Description

> MemJS is a pure Node.js client library for using memcache, in particular, the MemCachier service. It uses the binary protocol and support SASL authentication.

## Module Stats

186 downloads in the last day
2 903 downloads in the last week
12 037 downloads in the last month

~144 444 estimated downloads per year *(yay, a pretty number)*

# Vulnerability

## Vulnerability Description

`memjs` passes `value` option to the Buffer constructor without proper sanitization, resulting in DoS and uninitialized memory leak in setups where an attacker could submit typed input to the 'value' parameter (e.g. JSON).

## Steps To Reproduce:

`memcached` should be up and running.

### DoS

```js
var client = require('memjs').Client.create()
function tick() {
  var value = 2e9;
  client.set('key', value, {expires: 600 }, () => {});
}
setInterval(tick, 200);
```

### Uninitialized memory exposed (when running on Node.js below 8.0)

```js
var client = require('memjs').Client.create()
var value = 100;
client.set('key', value, {expires: 600 }, () => {});
client.get('key', (err, val) => console.log(val));
```

## Supporting Material/References:

- OS: Arch Linux current
- Node.js 9.5.0
- npm 5.6.0
- memcached 1.5.5

# Wrap up

- I contacted the maintainer to let him know: N
- I opened an issue in the related repository: N

## Impact

Denial of service
Sensitive data leak (on Node.js < 8.x)

</details>

---
*Analysed by Claude on 2026-05-24*
