# Fastify Denial of Service via allErrors: true AJV Configuration

## Metadata
- **Source:** HackerOne
- **Report:** 903521 | https://hackerone.com/reports/903521
- **Submitted:** 2020-06-20
- **Reporter:** chalker
- **Program:** Fastify
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Algorithmic Complexity
- **CVEs:** CVE-2020-8192
- **Category:** memory-binary

## Summary
Fastify uses allErrors: true in AJV configuration by default, which causes the validator to continue checking all schema constraints even after encountering errors. This allows attackers to craft payloads that trigger expensive validation operations (pattern matching, uniqueItems checks) on large inputs that would otherwise be rejected by maxLength/maxItems limits, causing CPU exhaustion and denial of service.

## Attack scenario
1. Attacker identifies a Fastify endpoint with a schema containing both a length constraint (maxLength, maxItems) and an expensive validator (pattern, uniqueItems)
2. Attacker crafts a payload exceeding the length limit but designed to trigger expensive validation logic (e.g., large array for uniqueItems check, long string for regex pattern matching)
3. Payload is sent to the vulnerable endpoint
4. Due to allErrors: true, AJV validates the entire payload against all constraints instead of short-circuiting at the maxLength/maxItems check
5. Expensive operations (regex engine backtracking, O(n²) uniqueItems comparison) execute on the full payload causing high CPU usage
6. Repeated requests exhaust server resources, resulting in denial of service

## Root cause
Fastify PR #1398 introduced allErrors: true as the default AJV configuration to provide more detailed validation error messages. However, this setting prevents short-circuit evaluation of validation constraints, forcing AJV to validate entire payloads against all schema rules regardless of length constraints that would normally reject them early. The security implications of this setting were not documented.

## Attacker mindset
An attacker recognizes that schema authors often implement length constraints (maxLength, maxItems) as DoS protections, assuming validation will fail fast on oversized inputs. By enabling allErrors mode through default configuration, the framework inadvertently negates these protections by forcing full validation of expensive operations on the unconstrained payload before the length check causes rejection.

## Defensive takeaways
- Disable allErrors in production unless detailed error reporting is absolutely required; default to fail-fast validation
- Document security implications of validation configuration options in official guides
- Order JSON Schema constraints logically with cheap checks (length limits) evaluated before expensive ones (pattern matching, uniqueItems)
- Provide security-focused configuration presets separate from developer-friendly defaults
- Add warnings or validation to alert users when potentially risky schema patterns are detected
- Implement timeout mechanisms for validation operations to prevent runaway execution
- Consider implementing AJV cache warming and complexity analysis for schemas

## Variant hunting
Check other frameworks using AJV for similar default configurations (express-json-schema-validator, etc.)
Investigate if other validation libraries have allErrors or equivalent modes enabled by default
Test whether other constraint combinations create DoS vectors (format validators, custom keywords with expensive logic)
Examine if serialization uses similar allErrors patterns that could expose internal data
Look for cascading validation in multi-schema scenarios where allErrors could compound complexity
Test conditional schemas (if/then/else) with allErrors to identify exponential validation branches

## MITRE ATT&CK
- T1498.2
- T1499.4

## Notes
This vulnerability is particularly insidious because schema authors may implement what they believe are secure constraints (length limits) without realizing that framework-level configuration undermines those protections. The issue highlights the importance of secure defaults and transparent documentation of security-relevant settings. The workaround is straightforward (disable allErrors), but required explicit user action and knowledge of the problem. This was introduced in a feature release meant to improve error handling, demonstrating the tension between developer experience and security.

## Full report
<details><summary>Expand</summary>

I would like to report a denial of service vulnerability in fastify
It allows to cause a DoS with some schemas that were otherwise assumed to be secure against DoS by their authors

# Module

**module name:** fastify
**version:** `2.14.1`, `3.0.0-rc.4`
**npm page:** `https://www.npmjs.com/package/fastify`

## Module Description

> An efficient server implies a lower cost of the infrastructure, a better responsiveness under load and happy users. 

## Module Stats

114 076 weekly downloads

# Vulnerability

## Vulnerability Description

See <https://github.com/ajv-validator/ajv#security-risks-of-trusted-schemas>:

> **Please note:** The suggestions above to prevent slow validation would only work if you do NOT use `allErrors: true` in production code (using it would continue validation after validation errors).

`fastify` uses `allErrors: true` by default which makes it susceptible to DoS attacks even when schemas are otherwise safe.

E.g. a (sub-)schema `{ uniqueItems: true, maxItems: 10 }` is otherwise safe against DoS as `maxItems` is checked **first** and validation fails there on long arrays, _but that applies to only not in `allErrors: true` case_. 

Neither https://github.com/fastify/fastify/blob/master/docs/Validation-and-Serialization.md nor https://github.com/fastify/fastify/blob/master/docs/Recommendations.md mentions this directly.

Introduced in https://github.com/fastify/fastify/pull/1398

## Steps To Reproduce:

```js
/* Client */

const fetch = require('node-fetch')
const request = body => {
  const json = JSON.stringify(body)
  console.log(`Payload size: ${Math.round(json.length / 1024)} KiB`)
  return fetch('http://127.0.0.1:3000/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: json
  })
}

const fireRequests = async () => {
  await request({ string: '@'.repeat(90000) })
  await request({ array: Array(20000).fill().map(() => ({x: Math.random().toString(32).slice(2)})) })
}

/* Server */

const fastify = require('fastify')({ logger: true })

const schema = {
  body: {
    type: 'object',
    properties: {
      array: { uniqueItems: true, maxItems: 10 },
      string: { pattern: "^[^/]+@.+#$", maxLength: 20 },
    }
  },
}

fastify.post('/', { schema }, (request, reply) => {
  reply.send({ hello: 'world', body: request.body })
})

fastify.listen(3000, (err, address) => {
  fastify.log.info(`server listening on ${address}`)
  fireRequests()
})
```

https://gist.github.com/ChALkeR/15e758d3fc5cbba0840b6a03a070c838

## Patch

Revert https://github.com/fastify/fastify/pull/1398

## Work-around

Use https://github.com/fastify/fastify/blob/master/docs/Server.md#ajv to override `allErrors` to `false` in ajv configuration.

# Wrap up

- I contacted the maintainer to let them know: N
- I opened an issue in the related repository: N

## Impact

Cause DoS in a presence of potentially slow pattern / format or `uniqueItems` in the schema, even when schema author guarded that with a length check to be otherwise immune to DoS.

</details>

---
*Analysed by Claude on 2026-05-24*
