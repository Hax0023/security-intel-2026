# Server Side Request Forgery (SSRF) in Webhook Functionality via IPv6 Address Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 2301565 | https://hackerone.com/reports/2301565
- **Submitted:** 2024-01-02
- **Reporter:** madara_
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Server-Side Request Forgery (SSRF), Input Validation Bypass, IPv6 to IPv4 Mapping Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
An SSRF vulnerability was discovered in the webhook functionality that allows attackers to bypass anti-SSRF filters by leveraging IPv6 addresses mapped to IPv4 format (e.g., ::ffff:a9fe:a9fe). This enables server-side requests to internal resources like AWS metadata endpoints that were previously protected. The vulnerability demonstrates insufficient input validation that fails to account for alternative IP address representations.

## Attack scenario
1. Attacker identifies the webhook functionality in a target organization's program settings on HackerOne
2. Attacker creates a public PHP server with a redirect script targeting an IPv6-formatted internal address (e.g., [::ffff:169.254.169.254])
3. Attacker creates a webhook in the target organization pointing to their malicious PHP server URL
4. Attacker triggers a test request on the webhook to cause the server to make a request through their redirect
5. The server follows the redirect to the IPv6-formatted address, bypassing IPv4 SSRF filters
6. Attacker receives responses from internal AWS metadata service revealing server information (e.g., 'server: EC2ws' header)

## Root cause
The webhook validation logic implements SSRF protections for IPv4 addresses but fails to normalize or filter IPv6 address representations, particularly IPv6-mapped IPv4 addresses (::ffff:x.x.x.x format). The application does not properly validate that different IP address formats (IPv4, IPv6, IPv6-mapped IPv4) all map to the same internal resources.

## Attacker mindset
An attacker would recognize that security filters often focus on traditional IPv4 CIDR ranges and overlook the alternate IPv6 representation of the same addresses. By chaining this with HTTP redirects, they can further obscure the final destination and evade simple string-matching filters. The attacker understands network protocol details and actively hunts for format bypass opportunities.

## Defensive takeaways
- Normalize all IP address formats (IPv4, IPv6, IPv6-mapped IPv4) to a canonical representation before validation
- Implement comprehensive IP address filtering that covers both IPv4 and IPv6 ranges for internal/reserved addresses (169.254.x.x, 127.x.x.x, ::1, fe80::/10, etc.)
- Validate not just the initial URL but also any HTTP redirects to ensure they don't target internal resources
- Use a robust IP validation library that handles all address formats correctly rather than regex-based solutions
- Maintain a whitelist of allowed domains/IPs rather than a blacklist approach for webhook destinations
- Disable HTTP redirects in server-side requests or validate all redirect targets against the same allowlist
- Regularly audit and test SSRF protections with diverse IP representations and encoding techniques

## Variant hunting
Test other IPv6 representations: compressed form (::ffff:a9fe:a9fe), expanded form (0000:0000:0000:0000:0000:ffff:a9fe:a9fe)
Try IPv6 localhost (::1) and link-local addresses (fe80::) if filters only block specific ranges
Combine IPv6 bypass with URL encoding, case variation, or obfuscation techniques
Test mixed IPv4/IPv6 notation in different webhook URL formats (hostname resolution, DNS rebinding)
Probe for similar bypass in other server-side request features: webhooks, integrations, API callbacks, image upload URLs
Check if internal hostname resolution bypasses exist alongside IP-based filtering
Test double redirect chains to evade redirect validation

## MITRE ATT&CK
- T1190
- T1133
- T1552

## Notes
This report demonstrates a sophisticated bypass of network-level security controls through protocol-aware exploitation. The vulnerability is particularly impactful because it grants access to AWS metadata endpoints, which typically contain sensitive credentials and configuration data. The attack requires relatively low privilege (ability to create webhooks) but yields high-value internal information. The fix requires understanding that IPv6 and IPv4 address spaces overlap and that validation logic must account for all representations of the same logical address.

## Full report
<details><summary>Expand</summary>

**Summary:**

- SSRF stands for "Server-Side Request Forgery" in English. It refers to a security vulnerability where an attacker can manipulate a web application to make HTTP requests from the server side instead of the client side. This can allow the attacker to access internal and sensitive resources that are not normally accessible.
- In an SSRF attack, the attacker can manipulate the requests made by an application to target internal resources such as local files, internal services, or even systems on the internal network. This can lead to the disclosure of sensitive information or unauthorized actions being performed on the server.
- In this case I was able to bypass the anti ssrf rules in the implemented webhook functionality, I noticed that there is no filter enabled for IPV6 IP addresses with IPv6 address mapped to IPv4.

**Description:**

### Steps To Reproduce
- To play this account you need to have an organizational account.
- Additionally, it is necessary to have a public server that interprets php, you can use 000webhost.com
1. Create a public PHP server and upload the following file h1.php:
```
<?php
// Obtén los datos de la solicitud
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE");
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
header("Content-Type: application/json");
header("Location: http://[::ffff:a9fe:a9fe]"); //IPV6 Compressed
?>
```
2. Save the public url where the php script is located
3. Log in to your hackerone account
4. Enter your organization's program settings
5. Look for the **webhooks** option.
6. Create a webhook with the previously copied url.
7. Once the webhook is created, edit it and click on the **Test request** button
9. You can see in the webhook logs that in response it launches the header  **server: EC2ws**  which corresponds to the Amazon metada instance.

## Impact

- "Server-Side Request Forgery" (SSRF) is a security vulnerability that can have various negative impacts. It occurs when an attacker tricks a server into making requests on their behalf. This can lead to unauthorized access to internal resources, such as databases or internal services, that are typically not accessible from the outside. Additionally, SSRF can be exploited for port scanning, potentially revealing vulnerable services. Attackers may use SSRF to force servers to perform unwanted actions on internal services, leading to data breaches or malicious activities. The vulnerability also poses a risk of bypassing network restrictions, allowing attackers to circumvent security measures. To mitigate SSRF, it is crucial to implement secure development practices, validate and filter user inputs effectively, and ensure that servers do not make unauthorized requests to internal resources. Utilizing whitelists for permitted addresses and disabling unnecessary DNS resolution are recommended measures to enhance security.

</details>

---
*Analysed by Claude on 2026-05-11*
