# Inconsistent URL Parsing in curl Leading to Potential SSRF and Access Control Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 2814750 | https://hackerone.com/reports/2814750
- **Submitted:** 2024-10-31
- **Reporter:** z3r0yu
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Server-Side Request Forgery (SSRF), Access Control Bypass, URL Parsing Inconsistency, RFC Non-Compliance
- **CVEs:** None
- **Category:** web-api

## Summary
libcurl incorrectly parses IPv6 addresses with zone identifiers (e.g., [fe80::1%25eth0]) by stripping the zone identifier, deviating from RFC 6874 compliance. This inconsistency enables attackers to bypass network interface restrictions and potentially conduct SSRF attacks by manipulating which network interface is used for requests.

## Attack scenario
1. Attacker identifies a web application using libcurl to fetch resources from user-supplied URLs with access controls based on network interfaces
2. Attacker submits a malicious URL containing an IPv6 address with zone identifier: http://[fe80::1%25eth0]/
3. libcurl's parser strips the %eth0 zone identifier and normalizes the hostname to [fe80::1]
4. Application's access control logic expecting the full zone identifier (fe80::1%eth0) fails to match, bypassing firewall rules
5. Request is routed through an unintended network interface, allowing access to restricted internal resources
6. Attacker gains unauthorized access to internal services, potentially exfiltrating sensitive data or compromising the system

## Root cause
libcurl's URL parsing implementation does not comply with RFC 6874, which specifies that IPv6 zone identifiers must be percent-encoded and preserved within the address literal. The parser incorrectly strips zone identifiers (%eth0) from IPv6 addresses during normalization, causing the parsed hostname to differ from what other URL parsers (Python urllib, Go net/url) produce.

## Attacker mindset
An attacker would recognize that inconsistent URL parsing across libraries creates a semantic gap that can be exploited. By crafting URLs with zone identifiers that libcurl strips but application logic expects, the attacker can bypass security controls that rely on the full address specification. The attacker understands network interface routing and SSRF mechanics, leveraging the parsing discrepancy to access restricted internal networks.

## Defensive takeaways
- Implement strict RFC 6874 compliance in URL parsing to ensure zone identifiers are preserved and validated
- Use consistent URL parsing libraries across the application stack and validate that all components handle IPv6 zone identifiers identically
- Apply additional input validation and normalization before using user-supplied URLs, explicitly checking for and validating zone identifiers when present
- Implement interface-level access controls that are independent of URL parsing, rather than relying on the parser to enforce interface restrictions
- Monitor and test for parsing inconsistencies between different libraries and frameworks used in the application
- Upgrade curl/libcurl to patched versions that correctly implement RFC 6874
- Use allowlist-based URL validation that explicitly specifies permitted IPv6 addresses and interfaces

## Variant hunting
Search for similar parsing inconsistencies in other URL components: hostname parsing with internationalized domain names (IDN), port number handling with IPv6 literals, userinfo parsing with special characters, path traversal sequences. Test other libraries (PHP cURL, Ruby Net::HTTP, Node.js http) for zone identifier handling. Investigate zone identifier handling in proxy libraries, HTTP clients, and API gateways. Check for similar RFC non-compliance in other protocol handlers (FTP, LDAP) that may use IPv6 addressing.

## MITRE ATT&CK
- T1190
- T1021
- T1552
- T1562

## Notes
This vulnerability represents a class of issues where parser inconsistencies become security weaknesses. The attack requires a multi-step setup where the application must rely on URL parsing for security decisions. The impact is amplified in environments with complex network segmentation using link-local IPv6 addresses. The reporter demonstrates good security research methodology by comparing parsing behavior across multiple implementations. Zone identifiers are critical for IPv6 link-local addresses in multi-interface environments, making this a real-world concern for systems using IPv6.

## Full report
<details><summary>Expand</summary>

## 0x01 Summary

An inconsistency in URL parsing within curl's URL handling leads to potential security risks such as Server-Side Request Forgery (SSRF) and access control bypasses. Specifically, when parsing URLs containing IPv6 addresses with zone identifiers (e.g., `http://[fe80::1%25eth0]/`), curl's parser omits the zone identifier, deviating from the expected behavior as per RFC 6874. This inconsistency may cause applications that rely on curl for URL validation and parsing to misinterpret network interfaces, leading to security vulnerabilities.

## 0x02 Details

### 2.1 Affected Components

- **curl**: All versions up to the latest release at the time of reporting.
- **libcurl**: All versions up to the latest release at the time of reporting.

### 2.2 Technical Background

According to RFC 6874, when including an IPv6 zone identifier in a URI, the zone identifier must be percent-encoded and included within the square brackets of the IPv6 address literal.

**RFC 6874 Section 4**:

> *"This document specifies that the zone identifier is to be appended to the address literal, following a percent sign. The percent sign is URL-escaped in URIs, so that the zone identifier is properly identified as part of the address literal and not as a port or userinfo component."*

### 2.3 Inconsistent Parsing Behavior

The following table demonstrates how different libraries parse URLs containing IPv6 addresses with zone identifiers:

#### Table: Parsing Results for `http://[fe80::1%25eth0]/` and Variants

| Payload                    | Browser (Chrome) | Rust                 | libcurl     | Go `net/url`   | Python `urllib` | Python `urllib3` |
| -------------------------- | ---------------- | -------------------- | ----------- | -------------- | --------------- | ---------------- |
| `http://[fe80::1%25eth0]/` | Invalid URL      | Invalid IPv6 address | `[fe80::1]` | `fe80::1%eth0` | `fe80::1%eth0`  | `[fe80::1%eth0]` |
| `http://[fe80::1%251]/`    | Invalid URL      | Invalid IPv6 address | `[fe80::1]` | `fe80::1%1`    | `fe80::1%1`     | `[fe80::1%1]`    |
| `http://[fe80::1]/`        | `[fe80::1]`      | `[fe80::1]`          | `[fe80::1]` | `fe80::1`      | `fe80::1`       | `[fe80::1]`      |

- **Observation**: libcurl strips the zone identifier `%eth0` from the hostname, resulting in `[fe80::1]`. In contrast, Go's `net/url` and Python's `urllib` preserve the zone identifier as `fe80::1%eth0`.

### 2.4 Explanation of the Issue

- **Deviation from RFC 6874**: The zone identifier is essential for IPv6 link-local addresses to specify the network interface. Omitting it can lead to incorrect network routing or unintended interface usage.
- **Inconsistent Parsing**: Curl's omission of the zone identifier means that applications using libcurl may inadvertently connect to the wrong interface or fail to connect entirely.
- **Security Implications**: This behavior can be exploited to bypass network restrictions, leading to SSRF attacks or unauthorized access to resources.

## 0x03 Attack Scenario

### 3.1 SSRF Scenario

1. **Application Setup**: A web application uses libcurl to fetch resources from user-supplied URLs. It relies on libcurl for URL parsing and trusts that requests to link-local addresses are confined to specific interfaces.

2. **Attacker's Input**: An attacker submits a URL like `http://[fe80::1%25eth0]/`.

3. Parsing Behavior

   :

   - **Expected**: The application expects the hostname to be `fe80::1%eth0`, ensuring the request goes through the `eth0` interface.
   - **Actual**: libcurl parses the hostname as `fe80::1`, ignoring the `%eth0` zone identifier.

4. **Exploitation**: The request is sent to `fe80::1` on the default network interface rather than the intended `eth0`. An attacker can manipulate the zone identifier to force requests through unintended interfaces, potentially accessing restricted networks or services.

### 3.2 Access Control Bypass

1. **Firewall Rules**: An application has firewall rules that allow traffic only through specific interfaces identified by zone identifiers.
2. **Bypassing Controls**: By exploiting the parsing inconsistency, an attacker can omit the zone identifier, causing the request to bypass the interface restrictions enforced by the application logic.

## 0x04 Impact
- **Server-Side Request Forgery (SSRF)**: Attackers can manipulate requests to access internal resources.
- **Access Control Bypass**: Security policies based on network interfaces can be circumvented.
- **Information Leakage**: Potential exposure of sensitive data if internal services are accessed.


## 0x05 Mitigation

- **Update Parsing Logic**: Modify libcurl to adhere strictly to RFC 6874, ensuring that zone identifiers are correctly parsed and preserved.
- **Input Validation**: Applications should implement additional checks to verify that zone identifiers are present and correctly formatted.
- **Upgrade**: Encourage users to update to the patched version of curl once a fix is released.

## 0x06 References

1. **RFC 6874**: Representing IPv6 Zone Identifiers in Address Literals and Uniform Resource Identifiers
2. **CWE-939**: Improper Handling of URL Encoded Syntax
3. **CWE-918**: [Server-Side Request Forgery (SSRF)](https://cwe.mitre.org/data/definitions/918.html)

## Impact

- **Server-Side Request Forgery (SSRF)**: Attackers can manipulate requests to access internal resources.
- **Access Control Bypass**: Security policies based on network interfaces can be circumvented.
- **Information Leakage**: Potential exposure of sensitive data if internal services are accessed.

</details>

---
*Analysed by Claude on 2026-05-24*
