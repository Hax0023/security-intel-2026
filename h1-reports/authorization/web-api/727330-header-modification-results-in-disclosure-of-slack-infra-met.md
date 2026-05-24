# Header Injection via X-Forwarded-Host Bypass Enables Blind SSRF and Intranet Port Scanning on files.slack.com

## Metadata
- **Source:** HackerOne
- **Report:** 727330 | https://hackerone.com/reports/727330
- **Submitted:** 2019-11-01
- **Reporter:** showuon
- **Program:** Slack
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Host Header Injection, Header Validation Bypass, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
The files.slack.com domain improperly trusts the X-Forwarded-Host header over the Host header, allowing attackers to bypass host validation through a simple @ character injection. This enables blind SSRF attacks from backend AWS infrastructure, permitting attackers to perform port scanning and reconnaissance on internal networks including the AWS metadata service endpoint.

## Attack scenario
1. Attacker uploads a file to Slack and obtains the original file URL (files.slack.com/files-pri/...)
2. Attacker intercepts the request and adds X-Forwarded-Host: files.slack.com@attacker.com header to bypass host validation
3. Server processes the @ character as a URL component, validates against files.slack.com portion, but routes request to attacker.com
4. Backend AWS server (not CloudFront) forwards request to attacker-controlled domain, confirming SSRF from internal infrastructure
5. Attacker replaces domain with internal IP (169.254.169.254) and varies port numbers to identify open ports
6. Attacker measures response times to map internal network topology and identify services running on metadata endpoints

## Root cause
Improper trust hierarchy: the server prioritizes X-Forwarded-Host header validation over the canonical Host header. Host validation logic fails to correctly parse URLs with @ character, allowing the validation to check only the left-side portion while routing uses the right-side portion. Backend server inherits this misconfiguration and makes outbound requests from internal AWS infrastructure.

## Attacker mindset
Reconnaissance and lateral movement oriented. The attacker seeks to map internal infrastructure and identify accessible services by leveraging a common proxy header misinterpretation. The blind SSRF approach allows enumeration without direct response content analysis, using timing/response patterns instead.

## Defensive takeaways
- Never trust proxy headers (X-Forwarded-Host, X-Forwarded-For) for security-critical decisions without explicit configuration and validation
- Implement strict URL parsing that rejects malformed input (@ in hostname) rather than partial matching
- Use allowlist-based host validation that validates the entire hostname, not just a substring
- Enforce Host header over X-Forwarded-Host unless explicitly configured for trusted proxies only
- Implement network segmentation to restrict backend servers' egress to internal networks
- Monitor and alert on unusual outbound connections from backend infrastructure
- Apply defense-in-depth with WAF rules blocking X-Forwarded-Host abuse patterns
- Regular security testing of header injection vectors, especially in file serving endpoints

## Variant hunting
Test other proxy headers: X-Forwarded-Proto, X-Original-Host, X-Host, CF-Connecting-IP
Test URL encoding bypass: %40 for @ character
Test semicolon usage: files.slack.com;attacker.com
Test double-encoding or nested injection patterns
Test against other Slack domains and endpoints that may honor proxy headers
Check if CloudFront explicitly strips malicious X-Forwarded-Host headers (why backend received it)
Test SSRF to internal service ports: 80, 443, 8080, metadata service endpoints

## MITRE ATT&CK
- T1190
- T1040
- T1046
- T1552
- T1557

## Notes
The vulnerability is particularly severe because: (1) it originates from backend AWS infrastructure, suggesting internal trust relationships were exploited; (2) blind SSRF allows port scanning without response content; (3) access to 169.254.169.254 metadata endpoint could leak AWS credentials and IAM roles; (4) the bypass technique (@ character) is simple and likely affected multiple endpoints. The writeup lacks discussion of AWS metadata service enumeration impact, which could escalate this to critical severity.

## Full report
<details><summary>Expand</summary>

I found *files.slack.com* domain will honor the **X-Forwarded-Host** header, instead of host header. Although file.slack.com has host validation to return 500 Internal server error when host is not files.slack.com, I can bypass the validation by appending @ at the end of host name. Also, the server will send request to the host in X-Forwarded-Host. And, we can see the server sent request is not the front end server (not from cloudfront.net), it is from the back end server(from amazonaws.com). So, with the blind SSRF vulnerability, the attackers can send arbitrary requests to the intranet, ex: port scanning by identifying the response delay time, to know 169.265.169.254:443 is closed, 169.265.169.254:80 is opened...and so on.

**Reproduce steps:**

1. upload a file onto the slack, find the original image path via Open original. Intercept this original path (i.e. https://files.slack.com/files-pri/TNXC4JD70-FPSL307RB/test.png) on burp suite
2. Send to repeater, make sure it works fine by clicking send directly
3. Add a header X-Forwarded-Host: xxx.com, make sure server returned 500 error
{F623016}

4. Update header to X-Forwarded-Host: files.slack.com@YOUR_DOMAIN, make sure server response with 302, and the location is YOUR_DOMAIN/files-pri/....
{F623017}

5. Make sure the request did sent to your domain, and the server is from xxx.amazonaws.com
6. change *YOUR_DOMAIN* into intranet ip, ex: 169.254.169.254:PORT, change the port to check the response delay time.

Here's the demo video: https://youtu.be/j5_WicLwwC4

## Impact

With the blind SSRF vulnerability, the attackers can send arbitrary requests to the intranet, ex: port scanning by identifying the response delay time. To mitigate it, the server should always honor the **Host** header, not others. Thank you.

</details>

---
*Analysed by Claude on 2026-05-24*
