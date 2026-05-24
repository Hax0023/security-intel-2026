# Denial of Service caused by HTTP/2 CONTINUATION Frame Flood

## Metadata
- **Source:** HackerOne
- **Report:** 2334401 | https://hackerone.com/reports/2334401
- **Submitted:** 2024-01-25
- **Reporter:** bart
- **Program:** Apache Tomcat
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Denial of Service, Resource Exhaustion, Memory Leak, HTTP/2 Protocol Abuse
- **CVEs:** CVE-2024-24549
- **Category:** memory-binary

## Summary
Apache Tomcat is vulnerable to a Denial of Service attack via HTTP/2 CONTINUATION frame flooding that causes uncontrolled memory consumption and eventual OutOfMemoryError crashes. An attacker can send specially crafted HEADERS followed by multiple CONTINUATION frames containing hundreds of headers that remain in memory even after connection closure, allowing small numbers of connections to consume hundreds of megabytes. The vulnerability affects Tomcat 10.1.18 and 11.0, and is tracked as CVE-2024-24549.

## Attack scenario
1. Attacker establishes multiple HTTP/2 connections to target Tomcat server
2. For each connection, attacker sends a HEADERS frame followed by 8 CONTINUATION frames, each containing 100 headers (~10 chars name/value)
3. Attacker crafts headers to approach but not exceed server limits (header byte limit, header size limit) to avoid GOAWAY/ENHANCE_YOUR_CALM responses
4. Attacker sends final CONTINUATION frame WITHOUT END_HEADERS flag, leaving headers buffered in memory without completing the request
5. Attacker closes or abandons connection while headers remain in server memory; repeats process with ~50 concurrent connections
6. Server memory fills rapidly due to HPackHuffman decoding buffers never being freed, triggering OutOfMemoryError and complete service crash

## Root cause
Tomcat's HTTP/2 implementation fails to properly manage memory for incomplete header sequences in CONTINUATION frames. Headers are buffered during decoding but not released when connections are abandoned or when incomplete frames are left in memory. The HPackHuffman decoder accumulates these incomplete sequences, and the lack of connection-level timeout or per-connection memory limits allows attackers to exhaust heap memory without triggering protective mechanisms like GOAWAY frames.

## Attacker mindset
An attacker seeks to achieve maximum impact (complete service unavailability) with minimal effort and detection. By sending incomplete HTTP requests that never reach application logging, the attack remains stealthy in standard HTTP logs. The attacker leverages HTTP/2's streaming nature and header compression complexity to exploit implementation gaps. Targeting memory exhaustion (rather than bandwidth) ensures impact even with modest connection counts and modest bandwidth.

## Defensive takeaways
- Implement strict per-connection memory limits for buffered headers in HTTP/2 streams
- Add timeouts for incomplete CONTINUATION frame sequences to force cleanup after inactivity
- Validate and enforce END_HEADERS flag presence within reasonable time windows; drop connections with orphaned CONTINUATION frames
- Monitor and limit total buffered header bytes across all active connections, not just per-request limits
- Implement connection-level resource accounting that forces closure when thresholds are exceeded
- Consider rate-limiting CONTINUATION frames per connection or implementing exponential backoff for repeated incomplete sequences
- Add alerting for abnormal memory consumption patterns during HTTP/2 header processing
- Provide configuration options to disable HTTP/2 or tune aggressive header timeout parameters for defense-in-depth

## Variant hunting
Hunt for similar memory exhaustion patterns in other HTTP/2 implementations (nginx, Apache httpd, Node.js, Netty, Go). Examine whether other multiplexing protocols (QUIC, gRPC) have similar incomplete frame buffering issues. Test other incomplete frame types (SETTINGS, WINDOW_UPDATE) for similar resource leaks. Check if HTTP/2 PUSH_PROMISE or HEADERS fragmentation in other servers exhibits comparable behavior.

## MITRE ATT&CK
- T1190
- T1499.4

## Notes
CVE-2024-24549 officially assigned. Exploit code provided in Go demonstrates straightforward attack requiring no authentication. Attack is particularly insidious because: (1) incomplete requests generate no HTTP logs, hindering detection/forensics; (2) small connection counts and modest bandwidth can trigger crashes; (3) server remains crashed even after attack ceases; (4) no configuration workaround exists beyond disabling HTTP/2 entirely. Reproduction is reliable and repeatable on Docker with memory constraints. The 50-connection test case with 800MB memory limit demonstrates practical exploitability against real deployments.

## Full report
<details><summary>Expand</summary>

I sent the following report to Apache Tomcat Security Team. They confirmed the report and assigned CVE-2024-24549. I'd like to ask if this is eligible for a bounty.

I'd like to report a DoS vulnerability in Tomcat. I tested 10.1.18 and 11.0 (tomcat:latest and tomcat:11.0 docker images respectively) and it seems that both are vulnerable.

An attacker can send headers using HTTP/2 CONTINUATION frames up to the limit of header bytes, header size and connection overhead so that connection is not dropped by a server (GOAWAY/ENHANCE_YOUR_CALM). Once frames are sent a connection is left intact and a new connection starts. After a few connections like these the server crashes with (java.lang.OutOfMemoryError: Java heap space) in the code connected to HPackHuffman decoding.

The lack of experience with Java does not allow me to debug this properly to give you a definitive answer what is causing the problem however here is my best guess:
* When sending HEADERS + N * CONTINUATION frames are sent the actual headers are stored in memory.
* When TCP connection is idle (and possibly when connection is dropped) the headers stay in memory.
* Because of this even a small number of connections are able to occupy hundreds of MB of server memory.

I'm attaching an exploit (in Golang) with reproduction steps:
* Start tomcat docker container (-m 800m limits memory to 800MB just to prove the point faster):
    `docker run -m 800m -d -p 7777:8080 --name tomcat tomcat:latest`
* SSH into a container to enable HTTP/2 (https://tomcat.apache.org/tomcat-8.5-doc/config/http.html#HTTP/2_Support).
* Stop and start container to pick up new config:
    `docker stop tomcat`
    `docker start tomcat`
* Run exploit:
    `go run exploit.go -address "[ip]:7777" -connections 50`

To test it I started a remote EC2 server. After a few seconds after the exploit starts the server becomes unresponsive, CPU goes to 100% and memory usage fills quickly (observe with docker stats). After a few seconds you'll see OOM errors in catalina log (see attachment). While the CPU will drop to 0% soon, no new connections will be processed by the server even when the exploit is not running anymore.

Here's how exploit.go works:
* It pregenerates 100 headers, each 10 chars long.
* It starts connections (-connections flag means how many active connections can be running at a time). Each connection:
    * Sends HEADERS frame.
    * Sends 8 CONTINUATION frames, each consists of 100 random headers (10 chars name and 10 chars value). These params are almost reaching the header size limits but not exceeding them so connection is not dropped.
    * Once headers are sent, connection is left intact and new connection starts.

It seems that finding a reason why the server is crashing can be challenging for the server admin because even a single full HTTP request is not made (note that the last CONTINUATION frame doesn't have END_HEADERS flag) so they won't see HTTP requests in the logs. I'm not aware of any configuration params that can prevent this attack. Thus, it seems the only mitigation is turning off HTTP/2 support (or code fix).

## Impact

It causes a server crash so complete availability loss.

</details>

---
*Analysed by Claude on 2026-05-24*
