# Subdomain Takeover at Landing.udemy.com via Unclaimed Unbounce Service

## Metadata
- **Source:** HackerOne
- **Report:** 208719 | https://hackerone.com/reports/208719
- **Submitted:** 2017-02-24
- **Reporter:** computer-engineer
- **Program:** Udemy
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME Record
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain landing.udemy.com contains a CNAME record pointing to unbouncepages.com, an unclaimed service on Unbounce. An attacker could register this subdomain on Unbounce and host malicious content (phishing pages, XSS payloads) on a legitimate Udemy domain. This allows large-scale phishing and XSS attacks while appearing to originate from Udemy's trusted domain.

## Attack scenario
1. Attacker discovers landing.udemy.com resolves via CNAME to unbouncepages.com
2. Attacker verifies the Unbounce service is unclaimed and available for registration
3. Attacker creates an Unbounce account and claims the unbouncepages.com subdomain
4. Attacker uploads malicious HTML/JavaScript content (phishing form, credential stealer, etc.) to Unbounce
5. Users visiting landing.udemy.com are served attacker-controlled content from trusted Udemy domain
6. Phishing/XSS attack succeeds due to domain legitimacy and user trust in Udemy

## Root cause
Udemy configured a CNAME record pointing to an external Unbounce service without claiming or properly maintaining ownership of the endpoint. When the service was abandoned or never claimed, the dangling CNAME created a takeover vector.

## Attacker mindset
An opportunistic attacker recognizes that subdomain takeovers on popular services provide high-trust attack vectors. Targeting a landing page subdomain specifically maximizes phishing effectiveness since users expect legitimate-looking pages from Udemy. The attacker leverages Unbounce's 404-page hosting to make content appear authentically hosted.

## Defensive takeaways
- Regularly audit all DNS records (especially CNAME, A, MX) for dangling or unclaimed endpoints
- Claim or explicitly decommission all third-party service integrations
- Implement monitoring to detect when external services become unclaimed or unregistered
- Use DNS CAA records to restrict certificate issuance for critical domains
- Maintain an inventory of all subdomains and their purposes
- Remove CNAME records for abandoned services immediately
- Consider using subdomain monitoring tools to detect takeover opportunities before attackers
- Implement DNSSEC to prevent DNS hijacking attacks

## Variant hunting
Hunt for other dangling CNAME records pointing to: GitHub Pages (*.github.io), Heroku apps (*.herokuapp.com), Azure services (*.azurewebsites.net), Shopify stores (*.myshopify.com), other page builders, CDNs, and hosting services. Check for abandoned subdomains across the organization's domain portfolio.

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1189
- T1190

## Notes
The researcher demonstrated responsible disclosure by not completing the takeover and instead contacting Udemy support. The report is well-structured with clear technical evidence (CNAME record details) and remediation steps. Subdomain takeovers are particularly dangerous when targeting landing pages or customer-facing infrastructure.

## Full report
<details><summary>Expand</summary>

**Target:**  `Landing.udemy.com`

###Details: 

The target subdomain points to _unbounce.com_ service, via a _DNS CNAME_ record. As a result of this, an attacker could potentially initiate a subdomain takeover by registering the subdomain on unbounce.com.

Additionally, 

Unbounce is a custom 404-page hosting service, therefore leveraging its functionality an attacker can host custom HTML/Javascript webpage on the domain which will look very legitimate to the end-user and can be used to conduct large-scale phishing/XSS attacks.

###Proof of Concept:

CNAME Record:
>**Cname:**	unbouncepages.com
>**Name:**	landing.udemy.com
>**Type:**  CNAME
>**Class:**	IN
>**TTL:**	300

I did not proceed with the takeover, Contacting the support and confirming from them was more sensible.

{F163493}

###Remediation:

Remove the CNAME entry or claim the domain by signing up on unbounce.com

~Regards



</details>

---
*Analysed by Claude on 2026-05-24*
