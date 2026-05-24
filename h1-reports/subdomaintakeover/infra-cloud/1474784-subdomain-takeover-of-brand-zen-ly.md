# Subdomain Takeover of brand.zen.ly

## Metadata
- **Source:** HackerOne
- **Report:** 1474784 | https://hackerone.com/reports/1474784
- **Submitted:** 2022-02-08
- **Reporter:** hacker1_agent
- **Program:** Datadog
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The subdomain brand.zen.ly is configured with a CNAME record pointing to brandpad.io, a third-party service that no longer hosts content for this domain. An attacker can register an account on Brandpad and claim the subdomain, enabling phishing, malware distribution, and other malicious activities under the guise of the legitimate domain.

## Attack scenario
1. Attacker discovers brand.zen.ly resolves to CNAME brandpad.io via DNS enumeration
2. Attacker verifies the subdomain shows 'Not Found' error, indicating no active service
3. Attacker registers an account on Brandpad service platform
4. Attacker configures their Brandpad account to serve content for brand.zen.ly
5. Attacker hosts phishing pages, malware, or malicious content accessible via https://brand.zen.ly
6. Users accessing brand.zen.ly are redirected to attacker-controlled content with legitimate domain appearance

## Root cause
Dangling CNAME record: DNS configuration points to an external service (Brandpad) that is no longer actively hosting content for this subdomain. The organization failed to remove or update the DNS record when the Brandpad service was discontinued or deprovisioned, leaving the subdomain unclaimed and available for takeover.

## Attacker mindset
An attacker with reconnaissance skills performs DNS enumeration to identify subdomains pointing to third-party services. Upon finding an unclaimed service endpoint, they register an account on that service to claim the subdomain, leveraging the legitimate domain for social engineering attacks, credential theft, or malware distribution.

## Defensive takeaways
- Maintain an inventory of all subdomains and their target services
- Regularly audit DNS records to identify dangling CNAMEs pointing to deleted or unused services
- Implement automated monitoring to detect DNS misconfigurations and unused external service pointers
- Remove or redirect DNS records when deprovisioning external services
- Use DNS CAA records to restrict certificate issuance
- Monitor third-party services for unauthorized claims on organizational subdomains
- Implement domain monitoring tools that specifically check for subdomain takeover vulnerabilities
- Document service dependencies and establish decommissioning procedures that include DNS cleanup

## Variant hunting
Search for other zen.ly subdomains with dangling CNAME records pointing to various SaaS platforms (GitHub Pages, Heroku, Shopify, AWS S3, Azure, Netlify, Firebase). Check for wildcard DNS entries that may mask unclaimed subdomains. Identify any subdomains pointing to deprecated or discontinued services.

## MITRE ATT&CK
- T1583.001 - Acquire Infrastructure: Domains
- T1583.005 - Acquire Infrastructure: Botnet
- T1190 - Exploit Public-Facing Application
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Spearphishing Attachment

## Notes
This is a classic subdomain takeover vulnerability with high exploitability. The reporter demonstrated actual takeover capability by registering on Brandpad. The impact is severe as it enables phishing, malware distribution, and brand impersonation. The fix requires immediate DNS record audit and removal of unused CNAME records. Similar vulnerabilities likely exist on other Datadog subdomains and competitors' infrastructure.

## Full report
<details><summary>Expand</summary>

Hello Gents,

### Background:
> + Subdomain takeover vulnerabilities occur when a subdomain (subdomain.example.com) is pointing to a service (e.g. GitHub pages, Heroku, etc.) that has been removed or deleted. This allows an attacker to set up a page on the service that was being used and point their page to that subdomain. For example, if subdomain.example.com was pointing to a GitHub page and the user decided to delete their GitHub page, an attacker can now create a GitHub page, add a CNAME file containing subdomain.example.com, and claim subdomain.example.com.

### Summary:
+ I just went to `brand.zen.ly` and it shows an error "Not Found", also I've checked the CNAME is pointing to `brandpad.io`, which means it can be added to any account.
+ This is pretty serious security issue in some context, so please act as fast as possible.
+ I was able to takeover `brand.zen.ly` by registering at **Brandpad**.

### Vulnerable URL:
+ https://brand.zen.ly

### Proof of Concept:
```
└─$ dig brand.zen.ly
brand.zen.ly.		255	IN	CNAME	brandpad.io.
```
+ Please visit: https://brand.zen.ly.

+ {F1610891}

### Recommended Fix:
+ Check your DNS-configuration for subdomains pointing to services not in use.
+ Set up your external service so it fully listens to your wildcard DNS.

## Impact

+ Subdomain takeover is abused for several purposes:
1. Malware distribution.
2. Phishing / Spear phishing.
3. XSS and steal cookies.
4. Bypass domain security.
5. Legitimate mail sending and receiving on behalf of Datadog subdomain.

Thanks and have a nice day!

</details>

---
*Analysed by Claude on 2026-05-24*
