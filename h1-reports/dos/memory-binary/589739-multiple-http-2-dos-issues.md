# Multiple HTTP/2 Denial of Service Vulnerabilities in Node.js

## Metadata
- **Source:** HackerOne
- **Report:** 589739 | https://hackerone.com/reports/589739
- **Submitted:** 2019-05-24
- **Reporter:** jasnell
- **Program:** Node.js
- **Bounty:** Not specified (under embargo at time of report)
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Memory Leak, CPU Exhaustion, Protocol Implementation Flaw
- **CVEs:** None
- **Category:** memory-binary

## Summary
Multiple HTTP/2 implementation flaws in Node.js allow attackers to cause denial of service through various resource exhaustion vectors including memory buffering, CPU priority tree churn, stream reset queuing, and header allocation attacks. Each attack exploits different aspects of Node.js's HTTP/2 handling, ranging from internal data buffering issues to improper queue management of control messages. Combined or individually, these vulnerabilities can crash the server or severely degrade service availability.

## Attack scenario
1. Attacker identifies that Node.js queues HTTP/2 data internally by manipulating window sizes and stream priorities across multiple parallel streams
2. Attacker sends large response requests (1MB+) across 100+ concurrent streams with carefully crafted flow control parameters to force byte-by-byte queuing
3. Server memory (RSS) balloons significantly as Node.js buffers responses internally, with observed increases of 688MB-1.2GB+ depending on request packing
4. Attacker alternatively exploits priority shuffling to force excessive CPU consumption on the priority tree, or sends stream resets to queue RST messages until OOM
5. Server becomes unresponsive or crashes when memory threshold is exceeded, affecting all legitimate user connections
6. Attacker can also send zero-length headers or flood control frames to achieve similar memory/CPU exhaustion with minimal bandwidth

## Root cause
Node.js HTTP/2 implementation lacks proper resource constraints on internal queuing mechanisms. Specifically: (1) insufficient backpressure handling when TCP write buffers are blocked while HTTP/2 windows remain open, (2) unbounded queuing of stream reset messages, (3) inefficient priority tree data structure causing excessive CPU churn during priority updates, (4) memory allocation for headers without proper aggregation validation, and (5) continued request processing and response queueing even when output cannot be transmitted, violating flow control semantics.

## Attacker mindset
Sophisticated protocol fuzzer or security researcher systematically identifying implementation gaps in HTTP/2 spec compliance. Attacker understands flow control semantics, frame prioritization, and resource queuing behavior. Focuses on edge cases where servers violate backpressure principles (e.g., continuing to queue while unable to transmit). Exploits the gap between HTTP/2 window management and underlying TCP write buffer blocking.

## Defensive takeaways
- Implement strict per-connection and per-stream memory limits for buffered data that account for both HTTP/2 window state and TCP write buffer capacity
- Add rate limiting and queue size caps for control frames (RSTs, PINGs) to prevent unbounded accumulation
- Optimize priority tree operations to prevent O(n) churn during frequent updates; consider debouncing or batching priority changes
- Validate header count and implement per-header-set memory budgets independent of cumulative name/value length to catch zero-length header attacks
- Implement proper backpressure: pause reading from TCP socket when unable to write due to blocked output buffers or memory pressure
- Add monitoring/alerting for anomalous patterns: rapid stream resets, priority shuffling, zero-length headers, or mismatched window/buffer states
- Consider connection-level reset limits and stream-level resource quotas per originating IP/flow

## Variant hunting
Test other streaming protocols (gRPC, QUIC, HTTP/3) for similar window vs. buffer confusion attacks
Investigate multiplexing implementations in other languages (Python, Go, Rust HTTP/2 libraries) for identical queuing vulnerabilities
Probe header handling in other servers for zero-length or minimal-size header bypass of validation logic
Examine priority tree implementations in alternative HTTP/2 stacks for CPU-based DoS via rapid reprioritization
Test interaction between HTTP/2 flow control and TLS record buffering in other implementations
Hunt for similar resource exhaustion in WebSocket, SPDY, or HTTP/1.1 pipelining implementations

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
Report was under embargo at submission time. Researcher responsibly disclosed six distinct attack vectors rather than lumping under single CVE, requiring individual fixes. Node.js behavior differs from nginx/libnghttp2—notably shows less CPU churn but higher memory consumption. Crash scenarios documented: 100K requests over single connection caused 12GB temporary RSS spike on session close. Practical impact confirmed on loopback with 10Mb/s traffic causing single-threaded CPU saturation. Report demonstrates need for protocol-level testing and flow control semantics validation in HTTP/2 implementations. All vectors exploitable with low bandwidth/connection requirements, making them practical DoS attacks.

## Full report
<details><summary>Expand</summary>

A security researcher has conducted a broad survey of HTTP/2 implementations to investigate common Denial of Service attack vectors. The Node.js implementation has been found to be subject to a number of these issues. (On the plus side, we're not the only ones! ;-) ...)

This work is still under embargo and has not yet been disclosed. 

Specifically:

* Data Dribble Attack: "This program will request 1MB of data from a specified resource. It will request this same resource over 100 streams (so, 100MB total). It manipulates window sizes and stream priority to force the server to queue the data in 1-byte chunks."

* Ping Flood (nginx variant):  "Nginx and libnghttp2 (used by Apache, Tomcat, node.js, and others) has a 10K-message limit on the number of control messages it will queue. Sending a controlled number of messages may enable an attacker to force the server to hold 10K messages in memory..."

* Resource Loop: "(actually, it should be called “Priority Shuffling”): This program continually shuffles the priority of streams in a way which causes substantial churn to the priority tree. Node.js [is] particularly impacted."

* Reset Flood: "This opens a number of streams and sends an invalid request over each stream. In some servers, this solicits a string of stream RSTs. In [Node.js] the servers may queue the RSTs internally until they run out of memory."

* O-Length Headers Leak: "This sends a stream of headers with a 0-length header name and 0-length header value. [Node.js] allocates memory for these headers and keeps the allocation alive until the session dies. Because the names and values are 0 bytes long, the cumulative length never exceeds the header size limit."

* Internal Data Buffering: "This opens the HTTP/2 window so the server can send without constraint; however, it leaves the TCP window closed so the server cannot actually write (many of) the bytes on the wire. Then, the client sends a stream of requests for a large response object which the target queues internally. This appears to work to create a long-ish standing queue in node.js"

Each is a distinct issue that will need to be looked at individually. I've edited the descriptions to remove references to vulnerabilities in other HTTP/2 implementations that have not yet been disclosed.

---

Additional details from the report:

```
“Data Dribble” on node.js: node.js seems to queue the data internally. For a 1MB output file
requested 100 times in parallel fast enough that node.js is constantly processing input,
node.js’s RSS rises by 808MB and then falls by 120MB (for an aggregate rise of 688MB).
(Actually, it looks like the numbers vary a bit across tests, but I think the end result is “a lot”.)
However, node.js does not have the excess CPU utilization which Nginx exhibits. If you
instead delay the sends considerably so that node.js has time to try to send in the meantime, it
looks like node.js will kill off the session before the input queue grows more than a few
hundred MB.

“Internal Data Buffering” on node.js: For a 1MB output file requested 100 times in parallel
(but sent with 24 requests per SSL frame), node.js behaves in an interesting way. It appears to
buffer some, but not all, data internally. It seems to continue reading (and processing requests
and queueing data to satisfy those requests) for as many streams as it can until it can’t read
any more. Once it can’t read anymore, it appears to try to write and realize the writing is
blocked. At that point, it seems to switch to reading frames from the wire and queuing the
requests internally (without processing them). (All of this is conjecture and is based on what
I’ve observed rather than a detailed analysis of the code.) So, if you pack the 100 requests
into a single SSL frame, node.js’s RSS increases by approximately 246MB. Or, if you send
585 requests in a single SSL frame, node.js’s RSS increases by approximately 1,296MB. For
reasons that are not entirely clear to me, if you send 100K requests each on three different
connections (approximately 2.8MB of request data per connection, node.js will run out of
memory and crash. The other interesting thing that happens is on the session ending. When
the session ends, it looks like node.js temporarily starts reading everything which is left in the
input queue, tries to process the requests, and store the request output in memory. So,
sending 100,000 requests (approximately 2.8MB of request data) and then closing the
connection can make node.js temporarily use 12GB of RSS.

Resource Loop on node.js: Over the loopback interface, node.js can handle roughly ~10 Mb/s
before the assigned thread uses 100% of its CPU core (on an m5.24xlarge). RSS rose from
50MB at the start of the test to 236MB by the end of test (~3 minutes). RSS rose another
156MB when a second stream was added. With two streams, serving of content to another
(non-attacking) connection was severely impacted.

Zero-length Headers on node.js: With truly 0-length headers (i.e. the payload is 0 bytes), the
server will accept and process an unlimited number; however, they don’t seem to create a
standing queue on the server side. The processing overhead is much lighter than the
“Resource Loop” test. (Roughly 25 Mb/s only produces a 75% CPU load on the server.) With
0-length headers which are Huffman encoded into 1-byte or greater headers, the server input
for that socket (and only that socket) seems to get blocked for ~ 2 minutes, until the
connection is killed off. It appears that the server will hold the connection open even if the
client goes away. That behavior allows a different kind of DoS attack (exhaust server file
descriptors or kernel receive buffers).

Reset Flood on node.js: The server queue grows without an obvious bound until the
connection dies or the server runs out of memory and dies. After the connection ends, the
server is unresponsive while GC runs
```

## Impact

Multiple denial of service vectors.

</details>

---
*Analysed by Claude on 2026-05-24*
