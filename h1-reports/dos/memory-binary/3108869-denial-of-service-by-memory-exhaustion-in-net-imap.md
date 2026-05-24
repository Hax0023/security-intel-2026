# Denial of Service by Memory Exhaustion in net/imap

## Metadata
- **Source:** HackerOne
- **Report:** 3108869 | https://hackerone.com/reports/3108869
- **Submitted:** 2025-04-26
- **Reporter:** masamune_
- **Program:** Ruby (net-imap library)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Improper Resource Validation, Unbounded Memory Allocation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The net-imap library in Ruby is vulnerable to denial of service through memory exhaustion when parsing IMAP server responses. A malicious or compromised IMAP server can send literal strings with arbitrarily large byte counts, causing the client to allocate excessive memory without any validation or limits. This leads to program crash or system instability when resources are exhausted.

## Attack scenario
1. Attacker sets up a malicious IMAP server or compromises an existing one
2. Victim's Ruby application connects to the attacker-controlled IMAP server using net-imap client
3. Server sends an IMAP response with a literal string prefix like {999999999999}\r\n
4. Client's receiver thread automatically calls IO#read with the attacker-specified size
5. IO#read immediately allocates memory for 999GB+ without sending actual data
6. System runs out of memory, application crashes or becomes unresponsive

## Root cause
The net-imap library does not validate or limit the size of literal strings declared in IMAP server responses before allocating memory via IO#read. The protocol implementation directly trusts server-provided byte counts and allocates the full requested memory immediately, with no safeguards against maliciously large values.

## Attacker mindset
An attacker seeks to disrupt a target application or system by causing resource exhaustion. This is particularly effective against applications connecting to untrusted IMAP servers, user-supplied hostnames, or compromised legitimate servers. The attacker requires no authentication and can trigger the vulnerability with a single malicious response.

## Defensive takeaways
- Implement strict limits on maximum literal string sizes accepted from IMAP servers
- Validate and sanitize protocol-provided size parameters before allocating resources
- Use incremental/streaming parsing instead of pre-allocating full buffer sizes
- Implement connection timeouts and resource monitoring for untrusted server connections
- Log and alert on suspicious literal size values that exceed reasonable thresholds
- Only connect to IMAP servers over secure, authenticated channels when possible
- Consider implementing configurable per-connection memory quotas

## Variant hunting
Check other Ruby protocol libraries (SMTP, POP3, HTTP) for similar unbounded allocation patterns
Search for IO#read calls in protocol parsers that directly use server-provided size values
Review other IMAP implementations in different languages for similar literal handling vulnerabilities
Test protocol libraries with extremely large declared sizes in responses
Look for missing validation on any protocol field that precedes resource allocation

## MITRE ATT&CK
- T1190
- T1657
- T1499

## Notes
This vulnerability is particularly dangerous because it requires no special privileges and can be triggered by any malicious or compromised IMAP server. The issue is exacerbated when applications connect to user-supplied hostnames or insecure (non-TLS) connections. Proper fix requires implementing configurable limits on literal sizes and validating these parameters before memory allocation.

## Full report
<details><summary>Expand</summary>

## Summary

There is a possibility for denial of service by memory exhaustion when net-imap reads server responses. At any time while the client is connected, a malicious server can send can send a "literal" byte count, which is automatically read by the client's receiver thread. The response reader immediately allocates memory for the number of bytes indicated by the server response.

This should not be an issue when securely connecting to trusted IMAP servers that are well-behaved. It can affect insecure connections and buggy, untrusted, or compromised servers (for example, connecting to a user supplied hostname).

## Details
The IMAP protocol allows "literal" strings to be sent in responses, prefixed with their size in curly braces (e.g. {1234567890}\r\n). When Net::IMAP receives a response containing a literal string, it calls IO#read with that size. When called with a size, IO#read immediately allocates memory to buffer the entire string before processing continues. The server does not need to send any more data. There is no limit on the size of literals that will be accepted.

## Impact

Memory exhaustion leading to program crash or system instability

</details>

---
*Analysed by Claude on 2026-05-24*
