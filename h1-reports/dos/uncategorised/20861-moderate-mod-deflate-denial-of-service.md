# mod_deflate Denial of Service via Request Body Decompression

## Metadata
- **Source:** HackerOne
- **Report:** 20861 | https://hackerone.com/reports/20861
- **Submitted:** 2014-02-19
- **Reporter:** gianko
- **Program:** Apache HTTP Server
- **Bounty:** Not specified
- **Severity:** moderate
- **Vuln:** Denial of Service, Resource Exhaustion, Algorithmic Complexity
- **CVEs:** CVE-2014-0118
- **Category:** uncategorised

## Summary
A resource consumption vulnerability in mod_deflate allows remote attackers to exhaust server memory and CPU resources when request body decompression is enabled. The attack exploits inefficient decompression handling in the DEFLATE input filter, causing significant system resource consumption.

## Attack scenario
1. Attacker identifies a target Apache server with mod_deflate configured to process compressed request bodies (DEFLATE input filter enabled)
2. Attacker crafts a malicious compressed payload designed to expand to extremely large sizes or cause algorithmic complexity issues during decompression
3. Attacker sends HTTP request with Content-Encoding: deflate header and the malicious compressed body
4. Server's mod_deflate processes the request and begins decompression, consuming excessive memory/CPU resources
5. Server performance degrades as decompression continues, affecting legitimate user requests
6. Continued attacks lead to denial of service as server becomes unresponsive

## Root cause
Inefficient or unbounded resource allocation during DEFLATE decompression of request bodies. The module likely lacks proper limits on decompressed output size, memory allocation during decompression, or fails to detect pathological compression patterns that expand exponentially.

## Attacker mindset
Adversary seeks to disable target service availability by leveraging a feature that is enabled but not properly resource-constrained. The attack is effective because request body decompression happens server-side with implicit trust, and the attacker can control the input compression format.

## Defensive takeaways
- Implement strict limits on maximum decompressed content size before processing
- Add timeouts for decompression operations to prevent indefinite resource consumption
- Monitor and limit memory allocation during decompression phases
- Use safe decompression libraries with built-in protections against zip bombs and similar attacks
- Only enable request body decompression when absolutely necessary
- Implement rate limiting for requests with Content-Encoding headers
- Configure alerts for abnormal CPU/memory usage patterns
- Regularly audit enabled Apache modules and disable unnecessary features

## Variant hunting
Similar vulnerabilities likely exist in other compression handlers (gzip, br, etc.). Search for: unbounded decompression in web servers, compression bomb handling in input filters, resource limits in mod_compress variants, algorithmic complexity attacks on zlib implementations.

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
This vulnerability is particularly insidious because request body decompression is transparent to administrators unfamiliar with mod_deflate configuration. The fix in Apache httpd 2.4.10 likely added bounds checking and resource limits. Zip bomb/decompression bomb techniques have long been known in security research and should be standard considerations for any decompression feature.

## Full report
<details><summary>Expand</summary>

A resource consumption flaw was found in mod_deflate. If request body decompression was configured (using the "DEFLATE" input filter), a remote attacker could cause the server to consume significant memory and/or CPU resources. The use of request body decompression is not a common configuration.

Acknowledgements: This issue was reported by Giancarlo Pellegrino and Davide Balzarotti

Resolved in Apache httpd 2.4.10-dev: http://httpd.apache.org/security/vulnerabilities_24.html


</details>

---
*Analysed by Claude on 2026-05-24*
