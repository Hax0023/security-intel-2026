# Subdomain Takeover on developer.openapi.starbucks.com via Mashery

## Metadata
- **Source:** HackerOne
- **Report:** 275714 | https://hackerone.com/reports/275714
- **Submitted:** 2017-10-09
- **Reporter:** dpgribkov
- **Program:** Starbucks
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, Insecure Third-Party Service Configuration, Dangling DNS
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The subdomain developer.openapi.starbucks.com was vulnerable to takeover through Mashery API proxy service. An attacker could register a Mashery account, add the target domain to their portal settings, and serve arbitrary content under the Starbucks subdomain without any validation. This enabled session hijacking, credential theft, and phishing attacks.

## Attack scenario
1. Attacker performs subdomain enumeration and discovers developer.openapi.starbucks.com returning HTTP 200 with Mashery Proxy server header
2. Attacker registers a trial account on Mashery service
3. Attacker accesses Mashery dashboard and navigates to Portal Settings domain configuration
4. Attacker adds developer.openapi.starbucks.com to their Mashery portal without encountering validation errors
5. Attacker crafts malicious JavaScript (e.g., alert(document.domain)) and confirms execution on the subdomain
6. Attacker hosts phishing content or session-stealing code on the legitimate Starbucks subdomain to conduct further attacks

## Root cause
Starbucks configured a subdomain to use Mashery API proxy service but failed to maintain proper DNS ownership validation or domain control verification. Mashery allowed domain addition without confirming the registrant's authorization or ownership, enabling any user to claim unclaimed subdomains pointing to Mashery infrastructure.

## Attacker mindset
The attacker systematically enumerated Starbucks subdomains, identified an externally-hosted service (Mashery) via HTTP headers, then exploited the lack of domain ownership verification in the third-party service's configuration. The attacker demonstrated controlled content injection with JavaScript to prove arbitrary execution capability.

## Defensive takeaways
- Implement DNS CNAME validation or ownership token verification before allowing third-party services to claim subdomains
- Maintain an inventory of all subdomains and their hosting services; audit for dangling or unverified configurations
- Use DNS CAA records to restrict certificate issuance and prevent unauthorized service claims
- Establish regular subdomain enumeration and health checks to identify orphaned or misconfigured subdomains
- Require explicit authorization tokens or DNS TXT records for third-party service domain registration
- Audit all third-party integrations (CDNs, API platforms, proxies) for proper domain control mechanisms
- Monitor for unauthorized changes to subdomain configurations at third-party service providers

## Variant hunting
Search for other Starbucks subdomains (*.starbucks.com) that may point to Mashery or similar third-party services
Identify other organizations using Mashery without proper domain ownership validation
Look for subdomains on Mashery-hosted services where domain control verification is absent or bypassable
Test other API gateway providers (Kong, Apigee, AWS API Gateway) for similar subdomain takeover vulnerabilities
Enumerate subdomains across partner organizations using shared service providers

## MITRE ATT&CK
- T1190
- T1583.001
- T1589.001
- T1598.003
- T1566.002

## Notes
The reporter noted uncertainty about the complete root cause mechanism. The vulnerability exemplifies the risks of delegating subdomain infrastructure to third parties without proper ownership verification. Mashery's lack of domain control validation was the critical flaw allowing unauthorized claims. This is a classic subdomain takeover scenario compounded by third-party service misconfiguration.

## Full report
<details><summary>Expand</summary>

Hi team,

### Summary: 
Subdomain `developer.openapi.starbucks.com` is vulnerable to subdomain takeover via Mashery service. The reason why it's worked unfortunately not fully clear to me.

### Details:
Doing my recent research on starbucks.com subdomains, I stumbled upon http://developer.openapi.starbucks.com/ The server returned 200 response with the following {F227581} The `Server` header of HTTP responce was `Mashery Proxy` so it gave me an idea, that I should go and try register an trial account at https://www.mashery.com/

After registering an account and confirming it, I got access to the dashboard. Under the `Portal Settings` menu there was an option to add your own domain name. I added developer.openapi.starbucks.com as my domain and I get no error. After I went to the http://developer.openapi.starbucks.com/ and saw welcome page {F227586} which gave me understanding that I can serve my own content under developer.openapi.starbucks.com

### PoC:
I added simple js code to the Welcome page `alert(document.domain)` for this proof-of-concept.
To confirm it just click this link http://developer.openapi.starbucks.com/

### Impact:
As I can serve my own content without any restrictions, with this webpage I can set up a campaign to steal user cookie sessions, or use it to steal credentials, or for phishing purposes. 

Please let me know, if you need more information!

Thanks,
Danil

</details>

---
*Analysed by Claude on 2026-05-24*
