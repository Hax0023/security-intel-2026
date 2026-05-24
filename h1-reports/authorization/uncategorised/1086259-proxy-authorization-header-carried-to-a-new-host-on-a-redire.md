# Proxy-Authorization Header Leaked to Redirect Hosts in cURL

## Metadata
- **Source:** HackerOne
- **Report:** 1086259 | https://hackerone.com/reports/1086259
- **Submitted:** 2021-01-25
- **Reporter:** dftrace
- **Program:** cURL
- **Bounty:** Not specified in report
- **Severity:** HIGH
- **Vuln:** Information Disclosure, Credential Exposure, Insecure Redirect Handling, Header Leakage
- **CVEs:** CVE-2018-1000007
- **Category:** uncategorised

## Summary
cURL fails to strip the Proxy-Authorization header when following HTTP redirects (with -L flag) to a different host or port, exposing proxy credentials to unintended servers. While regular Authorization headers are properly stripped on redirect, the Proxy-Authorization header is incorrectly forwarded, creating a credential disclosure vulnerability.

## Attack scenario
1. Attacker controls or compromises a web server that receives initial requests with Proxy-Authorization headers (e.g., Server1:8080)
2. Attacker configures Server1 to respond with an HTTP 3xx redirect to a server they fully control (Server2:8081)
3. Victim's cURL client follows the redirect with -L flag, sending the GET request to the attacker's Server2
4. Server2 receives the Proxy-Authorization header containing the base64-encoded proxy credentials
5. Attacker decodes the credentials and gains unauthorized access to the proxy infrastructure
6. If original connection was HTTPS but redirect points to HTTP, credentials are transmitted over plaintext

## Root cause
cURL's redirect handling logic treats Proxy-Authorization headers differently from Authorization headers, failing to apply the same cross-origin security checks. The Proxy-Authorization header is incorrectly assumed to be safe for forwarding across host/port boundaries due to its proxy-specific nature, overlooking that the proxy credentials should not be shared with arbitrary redirect targets.

## Attacker mindset
An attacker would set up a malicious server to receive redirects from legitimate services, banking on the fact that Proxy-Authorization headers carry authentication material for infrastructure-level access. By controlling the redirect target, they can harvest proxy credentials with minimal effort, potentially gaining access to internal networks or other protected services routing through that proxy.

## Defensive takeaways
- Strip all authentication-related headers (Authorization, Proxy-Authorization, etc.) when redirecting to different hosts
- Apply the same cross-origin header security policies to Proxy-Authorization as to Authorization headers
- Implement explicit whitelist-based redirect handling for authentication-protected requests
- Enforce HTTPS-to-HTTP downgrade prevention in redirect scenarios with sensitive headers
- Log and alert on credential-carrying redirects to different hosts for security monitoring
- Consider requiring explicit user consent before following redirects that involve authentication headers

## Variant hunting
Check other HTTP clients (libcurl bindings in Python requests, Go http, Ruby) for similar Proxy-Authorization leakage
Test custom header forwarding behavior in redirect chains (X-Custom-Auth, X-API-Key, etc.)
Examine redirect handling for other proxy-related headers (Proxy-Connection, Proxy-Authenticate response headers)
Verify behavior on cross-protocol redirects (HTTPS→HTTP, HTTP→HTTPS) with proxy credentials
Test redirect chains with multiple hops to different hosts to ensure no re-exposure
Check for similar issues with other infrastructure-level credentials (SSL client certificates, mTLS headers)

## MITRE ATT&CK
- T1187 - Forced Authentication (credential capture via redirect)
- T1598 - Phishing for Information (credential harvesting)
- T1528 - Steal Application Access Token (proxy credential theft)
- T1550 - Use Alternate Authentication Material (leveraging stolen proxy creds)
- T1041 - Exfiltration Over C2 Channel (credential transmission to attacker server)

## Notes
Report references CVE-2018-1000007, a similar vulnerability affecting Authorization headers from 3 years prior, indicating this is a systemic issue with redirect handling in cURL. The reporter demonstrates good security awareness by noting the HTTPS→HTTP downgrade scenario amplifies the risk. This affects cURL 7.64.1 and potentially many later versions, making it a widely-distributed vulnerability in infrastructure tooling.

## Full report
<details><summary>Expand</summary>

hi cURL team

I am not entirely sure this is an issue, please feel free to close of it isn't.

I noticed that when making an HTTP GET request with Proxy-Authorization header, together with the "-L" flag to follow redirects

 curl -H "Authorization-Proxy: Basic xxx==" http://host:8000 -L

If the remote web server redirects to an alternate host/port, cURL  will carry over the Proxy-Authorization header to the redirected new host along with the secret.

If Authorization header is used (vs Proxy-Authentication) then the header gets stripped as it should.

Client  sends GET request with Proxy-Authorization header to Server 1:8080
Server1 Redirects cURL to Server2:8081
Server2:8081 Receives the Proxy-Authorization header
This was reproducible in the following version:

curl 7.64.1 (x86_64-apple-darwin20.0) libcurl/7.64.1 (SecureTransport) LibreSSL/2.8.3 zlib/1.2.11 nghttp2/1.41.0
Release-Date: 2019-03-27

I believe the expected behaviour is that Proxy-Authorization header should be stripped upon a server redirection, since its not within the same domain origin.

I also noticed a similar issue was opened 3 years ago regarding Authorization header: https://curl.se/docs/CVE-2018-1000007.html

## Impact

If the password is sent via HTTPS, the server may redirect it to over unencrypted protocols if sent to an HTTP web server, making the Interception of the password possible.

</details>

---
*Analysed by Claude on 2026-05-24*
