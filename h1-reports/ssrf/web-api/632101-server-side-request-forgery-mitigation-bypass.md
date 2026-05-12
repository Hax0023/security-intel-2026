# Server Side Request Forgery (SSRF) mitigation bypass via DNS resolution error handling

## Metadata
- **Source:** HackerOne
- **Report:** 632101 | https://hackerone.com/reports/632101
- **Submitted:** 2019-06-29
- **Reporter:** mclaren650sspider
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Server Side Request Forgery (SSRF), DNS Rebinding, Improper Input Validation
- **CVEs:** CVE-2019-5464
- **Category:** web-api

## Summary
GitLab's SSRF protection in the URL blocker fails to validate requests when DNS resolution encounters errors, allowing attackers to bypass DNS rebinding protections. By crafting malicious DNS responses that initially fail resolution, attackers can later resolve to internal network addresses, enabling access to sensitive local services like metadata endpoints.

## Attack scenario
1. Attacker creates a malicious DNS server hosting a domain (e.g., 990.hacker1.xyz) that returns NXDOMAIN or resolution errors on initial lookup
2. Attacker creates a webhook on GitLab.com pointing to the malicious domain, which passes initial validation due to DNS resolution failure
3. During the 10-15 second validation window, attacker's DNS server is reconfigured to return CNAME chains pointing to internal addresses like 169.254.169.254 (AWS metadata endpoint)
4. Attacker triggers the webhook test by clicking 'Test' and 'Push events'
5. GitLab's validation function skips DNS rebinding checks because the domain initially failed resolution, allowing the HTTP request to proceed
6. The webhook makes an outgoing request that resolves to the internal network address, returning sensitive metadata or local service responses

## Root cause
The URL blocker's validate() function fails to enforce DNS rebinding protection when DNS resolution encounters errors. The code returns early on resolution failures without caching the validation result, allowing subsequent resolution attempts to succeed with malicious responses. The protection mechanism assumes all domains will successfully resolve initially.

## Attacker mindset
Exploit DNS timing race conditions and error handling logic to circumvent security controls. Leverage publicly accessible infrastructure metadata endpoints (169.254.169.254 in AWS/GCP) to extract sensitive configuration and credentials that enable privilege escalation or lateral movement.

## Defensive takeaways
- Always validate DNS results even when initial resolution fails; implement mandatory re-validation or longer caching periods
- Cache DNS resolution results and validate all fields (A/AAAA records and CNAME chains) against blocked IP ranges
- Implement timeout-based validation where DNS resolution must complete within strict time windows before HTTP requests are allowed
- Use a whitelist approach for outgoing webhook URLs rather than blacklisting local IP ranges
- Implement secondary validation checks that verify the final resolved IP against blocked ranges immediately before making HTTP requests
- Log all failed DNS resolution attempts and subsequent webhook execution for anomaly detection
- Block access to metadata endpoints (169.254.169.254/32, 169.254.170.0/24) regardless of DNS resolution status

## Variant hunting
Search for similar SSRF implementations that trust DNS resolution errors as a security boundary. Examine other webhook/outgoing request systems that cache validation results without continuous re-validation. Look for time-of-check-time-of-use (TOCTOU) vulnerabilities in URL validation logic, particularly in systems using asynchronous DNS resolution or queueing mechanisms.

## MITRE ATT&CK
- T1190
- T1021
- T1078
- T1526

## Notes
The vulnerability is particularly severe in cloud environments where 169.254.169.254 provides unauthenticated access to instance metadata including IAM credentials. The attacker's PoC uses CNAME chains to prevent DNS caching, demonstrating sophisticated understanding of DNS timing attacks. The 10-15 second window between validation and execution is critical to exploitation success. This is a classic TOCTOU vulnerability where validation and usage of a resource occur at different times.

## Full report
<details><summary>Expand</summary>

### Summary

This vulnerability allows attacker to send arbitrary requests to local network which hosts GitLab and read the response. This is possible due to flawed DNS rebinding protection.

The attack is possible due to flaw here: https://gitlab.com/gitlab-org/gitlab-ce/blob/108c3cf16bed5733ffae086fb62c226961356560/lib/gitlab/url_blocker.rb#L59

The `validate` function performs DNS lookup to check whether the IP address of a domain belongs to the local network. If the IP address belongs to the local network, the `validate` function raises an error and no HTTP request is sent. Furthermore, `validate` returns URI as well as the IP address of the domain to protect against DNS rebinding attacks.
However, if `validate` encounters an error while resolving the domain (for example, the domain does not resolve), the DNS rebinding protection is not applied.

### Steps to reproduce
 1. Create a webhook for a repository on GitLab.com. Use the URL `http://990.hacker1.xyz`. It may return error but let's ignore it now.
 2. Wait about 10 seconds and test webhook by clicking on "Test" and "Push events".
 3. After the hook has executed, you should see content of `http://169.254.169.254` returned.

Wait about 15 seconds between testing attempts, otherwise it may not work due to DNS caching.

The code for proof-of-concept DNS server which hosts `hacker1.xyz` is attached. The PoC uses a chain of CNAME records to prevent caching.

### What is the current *bug* behavior?

The outgoing HTTP requests from webhooks can be sent to the internal network.

### What is the expected *correct* behavior?

It is expected that HTTP requests cannot be sent to the internal network.

### Relevant logs and/or screenshots

F519096
Content of `http://169.254.169.254`

F519095
Content of `http://127.0.0.1`

### Output of checks

This bug happens on GitLab.com

## Impact

Attacker can use SSRF to access sensitive information on the internal network. Furthermore, SSRF in Google Cloud can be leveraged to Remote Code Execution depending on the setup. Publicly disclosed $25,000 #341876 describes a way to gain root access to Google Cloud server via a SSRF vulnerability.

</details>

---
*Analysed by Claude on 2026-05-11*
