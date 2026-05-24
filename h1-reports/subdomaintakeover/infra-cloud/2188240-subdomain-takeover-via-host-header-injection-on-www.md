# Subdomain Takeover via Host Header Injection on www.█████

## Metadata
- **Source:** HackerOne
- **Report:** 2188240 | https://hackerone.com/reports/2188240
- **Submitted:** 2023-10-01
- **Reporter:** ezequielpuig
- **Program:** U.S. Department Of Defense
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, Host Header Injection, DNS CNAME Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A subdomain takeover vulnerability exists where www.██████ contains a CNAME record pointing to an unclaimed ██████.netlify.app endpoint. An attacker can manipulate the Host header in HTTP requests to redirect traffic to malicious content hosted on the unclaimed Netlify domain, enabling phishing, malware distribution, and XSS attacks.

## Attack scenario
1. Attacker discovers that www.██████ has a CNAME record pointing to an unclaimed Netlify subdomain
2. Attacker registers or claims the unclaimed ██████.netlify.app domain on Netlify
3. Attacker hosts malicious content (phishing page, malware, XSS payload) on the claimed Netlify domain
4. Attacker crafts HTTP requests to www.██████ with Host header set to the Netlify domain using curl, Burp Suite, or browser extensions
5. Server responds with content from the attacker-controlled Netlify domain due to Host header processing
6. Victims are served malicious content appearing to come from the legitimate DoD domain, increasing attack credibility

## Root cause
The organization created a CNAME DNS record pointing to a third-party Netlify domain but failed to claim/register that domain on the Netlify platform. Additionally, the web server processes untrusted Host headers without validation, allowing attackers to manipulate which backend content is served. The combination of dangling DNS records and Host header reliance creates the vulnerability.

## Attacker mindset
An attacker recognizes the value of targeting government infrastructure for credibility in phishing campaigns. By discovering an unclaimed Netlify endpoint, they can register it and serve convincing phishing pages or malware that appears to originate from a trusted DoD domain. The Host header injection technique requires minimal resources and allows content manipulation without compromising the actual DoD infrastructure.

## Defensive takeaways
- Regularly audit all DNS records (especially CNAME, A, MX) to identify and remove dangling or unclaimed entries
- Immediately register or claim all third-party service endpoints referenced in DNS to prevent unauthorized registration
- Implement strict Host header validation - only allow whitelisted hostnames and reject or normalize unexpected values
- Use HTTP Strict-Transport-Security (HSTS) and X-Frame-Options headers to limit exploitation vectors
- Implement DNS monitoring and alerting for changes to DNS records
- Establish a subdomain enumeration program to identify all subdomains in scope
- Use security headers like Content-Security-Policy to limit XSS and phishing damage even if Host header injection succeeds
- Ensure CNAME records are only used for actively managed external services with proper access controls

## Variant hunting
Search for other CNAME records in the organization's DNS that may point to unclaimed third-party services (Heroku, GitHub Pages, AWS, Azure, etc.)
Test other subdomains for Host header injection vulnerabilities using different backend services
Identify subdomains pointing to cloud hosting providers (AWS S3, Azure Blob Storage, Google Cloud Storage) and verify bucket ownership
Check for MX, NS, and other record types that reference external services that may be unclaimed
Review historical DNS records using tools like DNSHistory to identify patterns of abandoned services

## MITRE ATT&CK
- T1190
- T1566
- T1566.002
- T1598
- T1608.005
- T1583.001

## Notes
This is a classic dangling DNS record vulnerability combined with Host header injection. The DoD's rapid resolution timeline (accepted on 01/October/2023) demonstrates the severity recognized by government security teams. The vulnerability is particularly dangerous for government targets due to the trust users place in official domains. The reporter's clear documentation and multiple PoC methods increased the report's credibility. This type of vulnerability is increasingly common as organizations migrate services to third-party providers without proper lifecycle management.

## Full report
<details><summary>Expand</summary>

## Vulnerability Overview

**_Reported By_**: Ezequiel \[@ezequielpuig\]
**_Reported Date_**: 01/October/2023
**_Reported To_**: U.S. Department Of Defense
**_Vulnerability Type_**: Subdomain Takeover
**_Affected URL_**: www\.███████

Hello U.S. Department Of Defense Security Team, I hope this report finds you well. 

I want to bring to your attention a serious security issue that poses a significant risk to www\.████████. This is related to a subdomain takeover vulnerability, which could allow malicious individuals to gain control over the subdomain and potentially misuse it for malicious purposes.

_Overview:
The affected subdomain is www\.███, which currently points to an unclaimed CNAME record on the ████████.netlify.app. This situation allows anyone to potentially take ownership of the subdomain and manipulate its content. Since www\.█████████ has a CNAME record pointing to ██████████.netlify.app, by changing the Host header to www\.██████████, it is possible to visualize the malicious content hosted on █████████.netlify.app.

Here are a few scenarios where the Host header can be modified:

Proxy Servers: If you control a proxy server, you can intercept incoming requests and modify the Host header before forwarding the request to the intended destination. This is often done for load balancing, content caching, or security purposes.

DNS Spoofing: In a malicious context, an attacker might attempt DNS spoofing to redirect requests to a different server with a modified Host header.

Server-Side Scripting: If you have control over the server-side code that processes incoming requests, you can modify the Host header as part of your application logic.

Browser Extensions: Malicious browser extensions installed can modify the Host header for all outgoing requests.

_Proof of Concept (PoC):
This vulnerability materializes when an HTTP request is sent to www\.██████████ with a manipulated Host header.

PoC via curl:
`curl -skS https://www.███████ --header "Host: ███.netlify.app"`

PoC via Burp Suite:
█████████

_Impact:
Subdomain takeover can be exploited for various malicious purposes, including:

Malware distribution
Phishing / Spear phishing attacks
Cross-Site Scripting (XSS) attacks
Authentication bypass
And more.

_Mitigation:
To address this issue and prevent potential abuse, I recommend taking the following steps:

Remove the CNAME record from the DNS zone for www\.█████████.
Reclaim and register the affected subdomain (███.netlify.app) in the Netlify portal to prevent takeover by unauthorized entities.
I urge you to take swift action to remediate this vulnerability to safeguard the security and reputation of U.S. Department Of Defense.

//

Please feel free to reach out to me if you need any further information or assistance in resolving this matter.

Best regards,
Ezequiel Puig

HackerOne: https://hackerone.com/ezequielpuig
LinkedIn: https://linkedin.com/in/ezequielpuig
Mail: puigezequiel@gmail.com

## Impact

Impact detailed above.

## System Host(s)
www.██████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Steps to reproduce detailed above.

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
