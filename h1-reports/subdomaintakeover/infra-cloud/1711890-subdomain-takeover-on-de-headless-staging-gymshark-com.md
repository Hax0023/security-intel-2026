# Subdomain Takeover on de-headless.staging.gymshark.com via Unclaimed Shopify

## Metadata
- **Source:** HackerOne
- **Report:** 1711890 | https://hackerone.com/reports/1711890
- **Submitted:** 2022-09-26
- **Reporter:** a-p0c
- **Program:** Gymshark
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS, Third-party Service Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
An attacker could claim the subdomain de-headless.staging.gymshark.com via an unclaimed Shopify store because the CNAME record pointed to an unowned Shopify resource. This would allow the attacker to serve arbitrary malicious content from a legitimate Gymshark domain, enabling phishing, malware distribution, or defacement attacks.

## Attack scenario
1. Attacker discovers CNAME record for de-headless.staging.gymshark.com pointing to Shopify
2. Attacker identifies that the corresponding Shopify store is unclaimed or abandoned
3. Attacker registers/claims the Shopify store using the unclaimed shop name
4. Attacker gains control over the subdomain and can serve arbitrary content
5. Attacker hosts phishing pages, malware, or defacement content on the Gymshark domain
6. Victims trust the Gymshark domain and are compromised by attacker-controlled content

## Root cause
The CNAME record for de-headless.staging.gymshark.com was not removed after the associated Shopify store was abandoned or deprovisioned, creating a dangling DNS pointer to an unclaimed third-party service.

## Attacker mindset
An attacker would recognize that staging subdomains are often overlooked during security reviews. By identifying dangling DNS records pointing to popular third-party services (Shopify), the attacker can claim ownership and leverage the legitimate domain for credential harvesting, malware distribution, or brand impersonation without raising immediate suspicion.

## Defensive takeaways
- Implement regular DNS audits to identify and remove unused CNAME records pointing to third-party services
- Establish a subdomain lifecycle management process ensuring DNS records are cleaned up when infrastructure is decommissioned
- Monitor for dangling DNS records across all subdomains, including staging and development environments
- Implement automated checks to validate that DNS records point to claimed/active services
- Use DNSSEC and DNS monitoring tools to detect unexpected changes to DNS records
- Include all subdomains (staging, dev, etc.) in vulnerability assessment and security review processes
- Maintain an inventory of all active subdomains and their associated services with regular audits

## Variant hunting
Search for other Gymshark subdomains with CNAME records pointing to unclaimed cloud services (AWS S3, Azure Blob Storage, GitHub Pages, Heroku, Firebase), or similar patterns where staging/abandoned infrastructure retains dangling DNS pointers.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing for Information: Spearphishing Link
- T1583.001 - Acquire Infrastructure: Domains

## Notes
The researcher demonstrated responsible disclosure by temporarily claiming the domain, password-protecting it to minimize impact, and offering to release it upon confirmation. The subdomain appears to be a German (de-) headless commerce variant, indicating potential multi-region deployments with similar vulnerabilities. Staging subdomains are frequently overlooked despite being valid targets for subdomain takeover attacks.

## Full report
<details><summary>Expand</summary>

The Gymshark subdomain https://de-headless.staging.gymshark.com/ was pointing to an unclaimed Shopify site. Because of this an attacker could claim this subdomain, via Shopify, and serve their own content.

This is extremely dangerous as an attacker could serve any malicious content on this domain such as malware, domain defacement, phishing campaigns etc. 

Also, phishing victims wouldn't be able to identify the maliciousness of a potential phishing campaign because it would be from a valid Gymshark subdomain.

**Note:** *I have temporarily claimed this domain for PoC and have password protected the site to reduce unnecessary impact to others. I am happy to remove this protection if you require further takeover evidence*.

## Remediation
- Remove the CNAME record for Shopify on 'de-headless.staging.gymshark.com'.
- I can release 'de-headless.staging.gymshark.com' for reclaim if needed.

## PoC Link
https://de-headless.staging.gymshark.com/

## PoC Evidence
{F1954064}
{F1954066}
{F1954069}
{F1954070}

Thanks, A-p0c

## Impact

If an attacker controlled https://de-headless.staging.gymshark.com/ they could host any malicious content they wanted, such as malware, defacement, a convincing phishing campaign

</details>

---
*Analysed by Claude on 2026-05-24*
