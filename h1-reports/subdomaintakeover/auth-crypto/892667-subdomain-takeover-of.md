# Subdomain Takeover via Dangling CNAME Record

## Metadata
- **Source:** HackerOne
- **Report:** 892667 | https://hackerone.com/reports/892667
- **Submitted:** 2020-06-06
- **Reporter:** simplyrishabh
- **Program:** Unknown (redacted)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, CNAME Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A subdomain had a CNAME record pointing to an unclaimed third-party service, allowing an attacker to register the service and claim ownership of the subdomain. This grants complete control over content served on the affected subdomain, enabling malware distribution, phishing, and XSS attacks.

## Attack scenario
1. Attacker discovers a dangling CNAME record pointing to an unclaimed service endpoint
2. Attacker registers an account on the third-party service (e.g., webservice platform)
3. Attacker navigates to custom domain settings within the third-party service
4. Attacker adds the target subdomain as a custom domain in the third-party service
5. Attacker uploads malicious content (PoC, phishing page, malware) to the registered service
6. Malicious content becomes accessible via the victim's subdomain through DNS resolution

## Root cause
Organization failed to maintain DNS records after a service migration or decommission, leaving a CNAME pointing to an unclaimed resource on a third-party platform. No verification mechanism existed to ensure claimed domains matched active service ownership.

## Attacker mindset
Systematic subdomain enumeration and DNS record analysis to identify stale or dangling references. Opportunistic registration of unclaimed services to obtain legitimate-looking domains for trust exploitation and phishing campaigns.

## Defensive takeaways
- Implement DNS audits to identify and remove dangling CNAME, NS, and MX records
- Establish ownership verification for all DNS records pointing to third-party services
- Monitor DNS changes and maintain an inventory of all active subdomains
- Use DNSSEC and DNS monitoring tools to detect unauthorized changes
- Implement CAA records to restrict certificate issuance for subdomains
- Establish processes to claim/verify domains on third-party platforms when migrating services
- Perform regular subdomain takeover scanning in CI/CD or security automation
- Use wildcard CNAME records cautiously and document their purpose

## Variant hunting
Scan for all dangling DNS records (CNAME, NS, A, MX, TXT) across domain portfolios
Check for CNAME records pointing to GitHub Pages, Azure, AWS, Heroku, and other PaaS endpoints
Identify subdomains with NXDOMAIN or SERVFAIL responses that previously resolved
Look for expired SSL certificates on subdomains as indicators of abandoned services
Enumerate subdomains using OSINT and check each for takeover potential

## MITRE ATT&CK
- T1584.001
- T1583.001
- T1566.002
- T1589.001

## Notes
Researcher responsibly held the subdomain after takeover to prevent malicious use. The vulnerability class (subdomain takeover) is well-documented but remains prevalent due to DNS record management gaps during infrastructure changes. Organizations should treat DNS cleanup as mandatory during decommissioning workflows.

## Full report
<details><summary>Expand</summary>

#Summary:
The subdomain ██████ had an CNAME record pointing to an unclaimed ███████ webservice. This is a high severity security issue because an attacker can register the subdomain on ███ and therefore can own the subdomain  █████████.



#Description:
The dangling CNAME record of █████████  is pointing to █████.███████ which was not claimed by you. I registered a service with this name and therefore was able to takeover the subdomain. Every attacker doing this has afterwards full control over the contents served on this subdomain.



#Subdomain Affected: 
██████████




#Proof Of Concept:
I have uploaded a simple subdomain takeover PoC on http://███████/████████





# Step-by-step Reproduction Instructions
1. Open ██████ and register for web app which is under market place. I have used ██████  (See: ████)

2. After registering, go to Custom Domains which will be available under settings. (See: ████)

3. In here, add custom domain i have used █████████ (See: █████)

4. After that upload any PoC you want to upload. I have used ████ which has my PoC. (See: ███████)





#Suggested Mitigation/Remediation Actions
1. Remove the dangling CNAME record for █████

2. Claim it back in ███████ portal after I release it

#Reference
Some hackerone reports #661751 #325336

#NOTE:
I have claimed the subdomain http://█████████ at the current moment to keep it safe from malicious users. Whenever you want i will release ██████.███. Afterwards you can claim it back.

## Impact

Subdomain takeover is abused for several purposes:

1.	Malware distribution
2.	Phishing / Spear phishing
3.	XSS

</details>

---
*Analysed by Claude on 2026-05-24*
