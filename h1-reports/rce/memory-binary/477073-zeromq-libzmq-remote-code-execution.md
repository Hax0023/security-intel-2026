# ZeroMQ libzmq Remote Code Execution via Malformed Packet

## Metadata
- **Source:** HackerOne
- **Report:** 477073 | https://hackerone.com/reports/477073
- **Submitted:** 2019-01-09
- **Reporter:** guido
- **Program:** ZeroMQ (libzmq)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Remote Code Execution, Buffer Overflow, Memory Corruption, Improper Input Validation
- **CVEs:** CVE-2019-6250
- **Category:** memory-binary

## Summary
A vulnerability in libzmq allows remote code execution through malformed packets that bypass input validation. The flaw affects older versions that were not resilient against fuzzing attacks, enabling attackers to corrupt memory and execute arbitrary code on victim systems.

## Attack scenario
1. Attacker crafts a malformed ZeroMQ protocol packet with invalid data structure
2. Attacker sends the malformed packet to a vulnerable libzmq instance exposed over the internet
3. The vulnerable library fails to properly validate the packet structure
4. Memory corruption occurs due to improper bounds checking or buffer handling
5. Attacker achieves code execution through the corrupted memory state
6. System compromise and arbitrary command execution becomes possible

## Root cause
Insufficient input validation and error handling for malformed packets in libzmq. The library did not properly assert and validate packet structure before processing, allowing corrupted or garbage data to cause memory corruption rather than safe failure.

## Attacker mindset
Attacker recognizes that ZeroMQ is widely deployed across multiple language ecosystems (Go, Python, Java, Node.js). They identify that the FAQ itself acknowledges historical fuzzing vulnerabilities and exploit this by crafting packets that bypass the validation mechanisms to achieve RCE.

## Defensive takeaways
- Implement strict input validation and sanitization for all network protocol parsers
- Use safe bounds checking and buffer overflow protections
- Establish clear security disclosure procedures separate from standard bug reporting
- Add fuzzing as part of continuous security testing for network-facing libraries
- Maintain version tracking and ensure all dependencies are updated to patched versions
- Monitor for assertions triggered by untrusted network data as indicators of vulnerability
- Implement defense-in-depth with network segmentation to limit ZeroMQ exposure

## Variant hunting
Search for similar input validation bypasses in other messaging protocols (RabbitMQ, Kafka, NATS). Check for packet parsing vulnerabilities in other distributed systems using custom protocols. Review fuzzing test results for assertions caused by malformed packets in protocol implementations.

## MITRE ATT&CK
- T1190
- T1203
- T1055

## Notes
The reporter responsibly disclosed through GitHub issues despite lack of formal security disclosure policy. The FAQ ironically documents that older versions had assertion failures from malformed data, but this specific RCE variant bypassed those protections. Wide adoption across language ecosystems multiplies the impact potential.

## Full report
<details><summary>Expand</summary>

Bug report and exploit: https://github.com/zeromq/libzmq/issues/3351
Fix by me: https://github.com/zeromq/libzmq/pull/3353

My motive for full disclosure is as follows:

```
Is it true that it is not safe to use ZeroMQ over the internet because it will crash?

Earlier versions of the ZeroMQ library (before 2.1) were not very resilient against "fuzzing" attacks. A malformed packet or garbage data could cause an old version of the library to assert and exit. Since the release of 2.1, all reported cases of assertions caused by bad data have been fixed. If your testing uncovers a problem in this area, please file a bug report.
```
Source: http://zeromq.org/area:faq

The issue reporting page (http://zeromq.org/docs:issue-tracking) instructs to open a Github issue, with no special procedure for security issues, so I went ahead and did just that.

libzmq appears to be widely used and has wrapper implementations for Go, Python, Java, Node.js, etc.

## Impact

Running arbitrary code on the victim's system.

</details>

---
*Analysed by Claude on 2026-05-12*
