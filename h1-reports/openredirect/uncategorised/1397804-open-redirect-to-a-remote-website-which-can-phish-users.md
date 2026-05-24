# Open Redirect to Remote Website via Header Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 1397804 | https://hackerone.com/reports/1397804
- **Submitted:** 2021-11-10
- **Reporter:** adrian_t
- **Program:** Crayons (ps:crayons)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Open Redirect, Insecure Redirect, Header Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application is vulnerable to open redirect attacks when specific headers are injected into requests, allowing attackers to redirect users to arbitrary remote websites. This vulnerability can be exploited through MITM attacks, request smuggling, or header injection techniques, particularly when a reverse proxy is present, enabling credential theft via phishing or malware distribution.

## Attack scenario
1. Attacker identifies that custom headers in HTTP requests influence redirect behavior
2. Attacker crafts a malicious URL or request with injected headers pointing to attacker-controlled phishing domain
3. Attacker delivers the payload via MITM attack, request smuggling, or exploits reverse proxy header processing vulnerabilities
4. User clicks the link or is automatically redirected to the attacker's remote website
5. User is presented with a convincing phishing page that mimics the legitimate service login
6. User enters credentials which are captured by the attacker or malware is delivered to the user's computer

## Root cause
The application fails to properly validate and sanitize HTTP headers that influence redirect logic, allowing attackers to inject custom headers that override intended redirect destinations without adequate origin validation or whitelist enforcement.

## Attacker mindset
An attacker recognizes that header manipulation is often overlooked in security testing and can be chained with other vulnerabilities. By combining open redirect with header injection techniques and exploiting reverse proxy configurations, they can bypass restrictions and reliably redirect users to phishing sites, achieving high success rates for credential harvesting.

## Defensive takeaways
- Implement strict whitelist-based validation for all redirect destinations, rejecting any URLs not explicitly approved
- Sanitize and validate HTTP headers, especially those influencing redirect behavior
- Use secure redirect methods that do not rely on user-controllable input
- Implement Content-Security-Policy headers to restrict redirect destinations
- Validate request origin and implement CSRF protections
- Audit reverse proxy configurations to prevent header smuggling and injection attacks
- Use relative URLs instead of absolute URLs when possible for internal redirects
- Implement proper logging and monitoring for unexpected redirect attempts

## Variant hunting
Search for similar open redirect patterns in other endpoints handling redirects, authenticated flows, logout mechanisms, password reset flows, and OAuth callback handlers. Test with various header combinations (X-Forwarded-Host, X-Original-URL, X-Rewrite-URL, Host, Referer) and examine how reverse proxy configurations interact with redirect logic.

## MITRE ATT&CK
- T1190
- T1598
- T1598.003
- T1566.002

## Notes
The vulnerability appears to be related to improper trust of HTTP headers in redirect decision-making. The mention of reverse proxy abuse suggests the application may be failing to normalize or validate headers before processing redirects. This is particularly dangerous in cloud/load-balanced environments where header manipulation is more feasible.

## Full report
<details><summary>Expand</summary>

By Adding some extra headers in the request I noticed that  the user is redirected to a remote website. This can lead to stealing a user credentials (phishing) on a remote server.

These headers can be added either using a MITM attack or by chaining with another vulnerability such as request smuggling, header injection more commonly abusing a reverse proxy that sits in front of the website.

ps:crayons

## Impact

This can lead to stealing a user credentials (phishing) on a remote server or planting malware on the user's computer.

</details>

---
*Analysed by Claude on 2026-05-24*
