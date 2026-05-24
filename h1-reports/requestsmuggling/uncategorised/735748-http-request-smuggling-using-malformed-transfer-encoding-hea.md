# HTTP Request Smuggling via Malformed Transfer-Encoding Header

## Metadata
- **Source:** HackerOne
- **Report:** 735748 | https://hackerone.com/reports/735748
- **Submitted:** 2019-11-12
- **Reporter:** erubinson
- **Program:** Unknown (PDF attachment referenced but not provided)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length Transfer-Encoding) Desynchronization, Header Parsing Vulnerability
- **CVEs:** CVE-2019-15605
- **Category:** uncategorised

## Summary
A vulnerability exists in HTTP request parsing where malformed Transfer-Encoding headers can be interpreted differently by frontend and backend servers, allowing an attacker to smuggle HTTP requests. This desynchronization enables request routing bypasses, cache poisoning, and credential theft.

## Attack scenario
1. Attacker crafts an HTTP request with a malformed Transfer-Encoding header that causes frontend/proxy server to misparse request boundaries
2. Frontend server forwards the malformed request to backend server, which interprets it differently due to varying parsing logic
3. Attacker's smuggled payload is attached to a legitimate user's request, causing the backend to process both as a single request
4. The smuggled request executes on the backend server under the context of the legitimate user's session
5. Attacker can bypass authentication, poison cached responses, or steal session credentials
6. Multiple requests can be chained to execute complex attack sequences

## Root cause
Inconsistent HTTP header parsing between frontend and backend servers, particularly around Transfer-Encoding handling. Different interpretations of malformed headers (e.g., spaces, multiple headers, invalid syntax) cause request boundaries to be computed differently, creating a desynchronization window for smuggling attacks.

## Attacker mindset
An attacker would systematically test HTTP header variations to find parsing inconsistencies between servers in the request pipeline. They would focus on edge cases in Transfer-Encoding parsing, recognizing that strict vs. lenient parsing creates exploitation opportunities for bypassing security controls and executing unauthorized actions.

## Defensive takeaways
- Implement strict and consistent HTTP header validation across all servers in the request chain
- Reject malformed Transfer-Encoding headers rather than attempting error recovery
- Ensure frontend proxies and backend servers use identical parsing logic for request boundaries
- Use HTTP/2 where possible, as it has stricter header validation requirements
- Implement request smuggling detection by normalizing requests before processing
- Clear or rewrite ambiguous headers (Content-Length, Transfer-Encoding) at trust boundaries
- Conduct regular security audits of HTTP parsing implementations
- Monitor for suspicious request patterns that could indicate smuggling attempts

## Variant hunting
Test CL.CL (duplicate Content-Length) desynchronization
Investigate TE.CL (Transfer-Encoding vs Content-Length) variants with different header orderings
Examine whitespace handling in Transfer-Encoding values (spaces, tabs, CRLF variations)
Test multiple Transfer-Encoding headers with conflicting values
Analyze chunked transfer encoding edge cases and malformed chunk sizes
Check for HTTP/1.1 vs HTTP/2 parsing differences in proxies

## MITRE ATT&CK
- T1190
- T1021
- T1598
- T1110

## Notes
The actual writeup PDF was not provided in the submission content, limiting detailed analysis. This analysis is based on typical HTTP request smuggling vulnerabilities involving Transfer-Encoding header malformation. The specific server software and attack vectors would be documented in the referenced PDF. HackerOne report #735748 likely contains proprietary details about the affected organization.

## Full report
<details><summary>Expand</summary>

Please see the attached PDF for a writeup of this vulnerability.

## Impact

Please see the attached PDF for a writeup of this vulnerability.

</details>

---
*Analysed by Claude on 2026-05-24*
