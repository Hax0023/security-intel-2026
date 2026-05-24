# Denial of Service in RSKJ Server via Malformed RLP Packet Processing

## Metadata
- **Source:** HackerOne
- **Report:** 2105808 | https://hackerone.com/reports/2105808
- **Submitted:** 2023-08-10
- **Reporter:** spacewasp
- **Program:** RSK Smart Bitcoin
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Infinite Loop, Memory Exhaustion, Input Validation Flaw
- **CVEs:** None
- **Category:** memory-binary

## Summary
A malformed RLP-encoded UDP packet sent to the RSKJ server's UDPv6 listener (port 5050) causes an infinite loop in packet processing, preventing the server from accepting new packets and eventually leading to out-of-memory crashes. The vulnerability exists in the RLP decoding logic where bytesToLength() can return -5, resulting in zero length and an unchanging position pointer that creates an infinite processing loop.

## Attack scenario
1. Attacker crafts a malicious RLP-encoded UDP packet with specific byte sequences that cause bytesToLength() to return -5
2. Attacker sends the malformed packet to the target RSKJ server listening on UDPv6 port 5050
3. The server's UDP handler invokes decode2() which calls bytesToLength(), receiving -5 as return value
4. The length variable is set to 0 and the position pointer remains unchanged, creating a loop condition
5. The server becomes stuck processing only this single packet indefinitely, unable to handle new incoming packets
6. Over time, memory accumulates as the application fails to release resources, eventually crashing with out-of-memory error

## Root cause
The RLP.decode2() function in RSKJ's RLP decoder does not properly validate the output of bytesToLength(), which can legitimately return negative values (such as -5) to indicate invalid input. When bytesToLength() returns -5, the length is set to 0 and the position index does not advance, creating an infinite loop condition where the same malformed bytes are processed repeatedly without progression.

## Attacker mindset
An attacker with network access to the RSKJ node would exploit this as a simple, reliable denial-of-service vector requiring minimal resources - just a single crafted UDP packet can incapacitate the entire node's networking capability. This is an attractive attack because it's reproducible, requires no authentication, and causes a complete service disruption.

## Defensive takeaways
- Implement strict input validation on RLP-encoded data with clear error handling for negative return values from parsing functions
- Add loop detection or maximum iteration counters in packet processing logic to prevent infinite loops
- Validate that parsing position advances with each iteration; if position fails to change, break the loop and reject the packet
- Implement rate limiting and blacklisting for clients sending malformed packets
- Add comprehensive monitoring for UDP processing anomalies and packet drop rates
- Conduct code review of all usages of vulnerable decode2() function throughout the codebase
- Implement timeouts for individual packet processing operations
- Add memory pressure monitoring and circuit breakers to gracefully degrade under attack

## Variant hunting
Search the codebase for other instances of bytesToLength() usage, particularly in P2P protocol handlers, blockchain synchronization logic, and transaction validation paths. Review all RLP decoding entry points for similar infinite loop vulnerabilities. Examine other network protocols (TCP, WebSocket) that may accept RLP-encoded data. Look for similar unbounded loops in other message parsing functions.

## MITRE ATT&CK
- T1499
- T1498
- T1190

## Notes
The vulnerability was discovered during investigation of a related closed report (ID #2102315). The attacker references specific GitHub lines showing the problematic logic flow. The proof-of-concept requires a Python script that generates the specific malformed RLP payload. The issue affects not just UDPv6 but potentially other entry points using the vulnerable decode2() function. The crash mechanism involves both immediate DoS (packet processing hang) and eventual OOM crash, making it a two-stage failure mode.

## Full report
<details><summary>Expand</summary>

Due of closing of report (ID #2102315) I will summarize total reproducible report here

## Summary:
DOS of RSKJ server

## Steps To Reproduce:

  1. download https://github.com/rsksmart/rskj/releases/download/FINGERROOT-5.0.0/rskj-core-5.0.0-FINGERROOT-all.jar
  2. at server side run
```
 java -classpath rskj-core-5.0.0-FINGERROOT-all.jar -Drpc.providers.web.cors=* -Drpc.providers.web.ws.enabled=true co.rsk.Start
```
it opens `UDPv6` port `5050`

  3. at client side install python3 and library `pip install pysha3`, download  {F2591198},  modify `HOST` inside and run it against server.
  4.the `UDPServer` is going to process *only* one UDP packet forever and it prevents to process other packages received from different nodes. In a while (some minutes left) the application crashes.

## Supporting Material/References:
The root cause:
bytesToLength returns -5 and length becomes 0
https://github.com/rsksmart/rskj/blob/master/rskj-core/src/main/java/org/ethereum/util/RLP.java#L432
this is legal
https://github.com/rsksmart/rskj/blob/master/rskj-core/src/main/java/org/ethereum/util/RLP.java#L440
and position is unchangeable
https://github.com/rsksmart/rskj/blob/master/rskj-core/src/main/java/org/ethereum/util/RLP.java#L405
https://github.com/rsksmart/rskj/blob/master/rskj-core/src/main/java/org/ethereum/util/RLP.java#L403

## Impact

Server stops to process the incoming traffic at `UDPv6` port `5050`. In a while the application crashes as Out of memory.
due of everywhere usage of vulnerable function `decode2` there may be affected another entry points of service.

</details>

---
*Analysed by Claude on 2026-05-24*
