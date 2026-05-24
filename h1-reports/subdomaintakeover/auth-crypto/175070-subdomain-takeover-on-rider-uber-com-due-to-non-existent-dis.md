# Subdomain Takeover on rider.uber.com via Unclaimed CloudFront Distribution

## Metadata
- **Source:** HackerOne
- **Report:** 175070 | https://hackerone.com/reports/175070
- **Submitted:** 2016-10-11
- **Reporter:** fransrosen
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME, Cloud Resource Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
rider.uber.com contained a CNAME pointing to an unclaimed CloudFront distribution, allowing an attacker to claim the distribution and serve arbitrary content. The subdomain was responding with CloudFront's error message indicating no active distribution was associated with it, creating a window for takeover. An attacker could register the orphaned CloudFront distribution and fully control content served to users accessing rider.uber.com.

## Attack scenario
1. Attacker discovers rider.uber.com returns CloudFront error indicating no active distribution
2. Attacker identifies the CNAME record points to an unclaimed AWS CloudFront distribution
3. Attacker creates a CloudFront distribution with matching alternate domain name configuration
4. Attacker gains control of the subdomain and can serve malicious content
5. Attacker could perform phishing attacks, steal credentials, deliver malware, or conduct session hijacking
6. Users trust the legitimate Uber domain and unknowingly interact with attacker-controlled content

## Root cause
DNS CNAME record for rider.uber.com pointed to a CloudFront distribution that had been deleted or deprovisioned without removing the corresponding DNS entry. AWS CloudFront allows alternate domain names to be claimed by any AWS account, creating a race condition where an attacker can claim the orphaned distribution.

## Attacker mindset
An opportunistic attacker systematically scans for dangling DNS records pointing to cloud resources. Upon discovering an unclaimed CloudFront distribution error, they recognize the takeover opportunity and quickly claim the distribution before the organization remedies the DNS misconfiguration. The attacker demonstrates responsible disclosure by immediately notifying Uber rather than maintaining persistent access.

## Defensive takeaways
- Implement DNS audit processes to identify and remove dangling CNAME records pointing to cloud resources
- Use automated scanning tools to detect CloudFront error responses indicating unclaimed distributions
- Establish lifecycle management policies ensuring DNS records are removed when cloud resources are deprovisioned
- Monitor CloudFront distributions and document all alternate domain names in use
- Implement DNS validation and monitoring as part of infrastructure change management
- Use AWS Config rules or similar tools to detect unclaimed CloudFront distributions
- Maintain inventory of all CNAME records and their associated cloud resources
- Implement rapid response procedures for subdomain takeover reports

## Variant hunting
Scan other Uber subdomains for similar dangling CNAME records pointing to AWS/cloud resources
Identify other companies with CloudFront distributions and scan for unclaimed alternate domain names
Search for CNAME records in DNS zone files pointing to deleted S3 buckets, API Gateway endpoints, or ELB load balancers
Test for GitHub Pages, Heroku, and other PaaS takeover scenarios on similar dangling CNAMEs
Examine acquired companies' infrastructure for forgotten DNS records pointing to deprovisioned resources

## MITRE ATT&CK
- T1190
- T1199
- T1566.002
- T1589.001

## Notes
This is a classic subdomain takeover vulnerability with significant business impact. The reporter demonstrated excellent responsible disclosure practices by creating a proof-of-concept, documenting it clearly, and offering immediate remediation assistance. The vulnerability highlights the importance of DNS hygiene in large organizations managing numerous cloud resources. Uber's reliance on rider.uber.com for user authentication and operations made this a critical security issue. The 3-hour window mentioned suggests this was a recently deprovisioned distribution, emphasizing the need for automated cleanup procedures.

## Full report
<details><summary>Expand</summary>

Hi,

3 hours ago, rider.uber.com was responding like this:
{F127137}

This happened on both HTTP and HTTPS. Now, as our blog post from last week says:
https://labs.detectify.com/2016/10/05/the-story-of-ev-ssl-aws-and-trailing-dot-domains/

This means that there's a high chance this domain does not have any distribution at all, and that anyone can now claim it.

I've done this as a PoC now, I haven't placed anything on the apex level, howevel if you use this URL:
http://rider.uber.com/login-poc

There's a PoC there:
{F127139}

You should immediately remove the DNS RR, or point it elsewhere, or tell me and I'll remove the Alternate CNAME again on my PoC-distribution.

Regards,
Frans


</details>

---
*Analysed by Claude on 2026-05-24*
