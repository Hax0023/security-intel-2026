# Subdomain Takeover on partners.ubnt.com via Unclaimed CloudFront DNS Entry

## Metadata
- **Source:** HackerOne
- **Report:** 145224 | https://hackerone.com/reports/145224
- **Submitted:** 2016-06-16
- **Reporter:** fransrosen
- **Program:** Ubiquiti Networks
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Improper Resource Cleanup, Domain Hijacking
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The domain partners.ubnt.com had a DNS CNAME record pointing to CloudFront that was no longer claimed by any CloudFront distribution, allowing an attacker to claim the domain and serve arbitrary content. This enabled credential theft via fake login pages, phishing attacks, and potential SSL certificate issuance under the trusted domain.

## Attack scenario
1. Attacker discovers partners.ubnt.com resolves to a CloudFront distribution DNS endpoint
2. Attacker verifies no active CloudFront distribution claims this domain as a CNAME
3. Attacker creates their own CloudFront distribution and adds partners.ubnt.com as a custom CNAME
4. Attacker serves malicious content (fake login form, phishing page) on partners.ubnt.com
5. Attacker can obtain valid SSL certificate via ACME verification (Let's Encrypt, AlphaSSL)
6. Victims are fully deceived due to legitimate domain and HTTPS, allowing credential harvesting and malware distribution

## Root cause
Ubiquiti failed to remove DNS records (CNAME entries) pointing to CloudFront when discontinuing use of the partners.ubnt.com subdomain. CloudFront does not validate domain ownership at the DNS level, allowing any attacker to claim an orphaned CNAME record by creating their own distribution.

## Attacker mindset
Opportunistic reconnaissance followed by systematic domain enumeration to identify dangling DNS records. Once discovered, the attacker exploits CloudFront's lack of ownership validation to claim the subdomain and immediately leverage the trusted domain for credential theft and phishing at scale.

## Defensive takeaways
- Implement DNS record lifecycle management: audit and remove all CNAME/alias records when services are decommissioned
- Maintain an inventory of all DNS records pointing to third-party services (CloudFront, Azure CDN, GitHub Pages, etc.)
- Implement automated monitoring to detect DNS changes and alert on unused records
- Establish a process for verifying that all DNS entries actively resolve to claimed resources
- Consider using CAA records to restrict certificate issuance and prevent unauthorized SSL certificates
- Periodically scan subdomains for dangling DNS records and subdomain takeover risks
- Communicate security requirements to CDN providers regarding CNAME ownership verification

## Variant hunting
Search for other UBNT subdomains pointing to CloudFront, Azure CDN, GitHub Pages, Heroku, AWS S3, Fastly, or other services. Check common subdomains (api, dev, staging, cdn, mail, blog, shop, support, auth, login). Monitor TLSH/domain similarity patterns for other organizations with similar cleanup failures.

## MITRE ATT&CK
- T1190
- T1199
- T1566
- T1598
- T1621

## Notes
This vulnerability demonstrates a critical gap between infrastructure management and security. The attacker leveraged legitimate trust in the domain combined with valid HTTPS to conduct sophisticated phishing. The writeup is from Detectify (a security researcher collective) with proper responsible disclosure. No evidence of actual exploitation beyond PoC is claimed. The ability to serve content and obtain valid SSL certificates under a trusted domain makes this a severe credential theft vector.

## Full report
<details><summary>Expand</summary>

Hi,

So lately I have discovered that CloudFront is not validating which user that connects a CNAME:d domain to a CloudFront Origin. This means that if I could find a domain that is still pointing to CloudFront, without being connected to any Origin as a Custom CNAME, I can actually claim the domain myself and point it to whatever I want. A vulnerable domain looks like this:
{F99783}

I noticed that this was indeed the result I got on partners.ubnt.com. This domain is currently still pointing to CloudFront, but there is no CF Origin with the domain set as a CNAME.

I have claimed the domain now for PoC using the following setup:
{F99779}

And I have placed a file located under /login for validation and to show what could be a possible variant of an attack:

http://partners.ubnt.com/login

PoC-image:
{F99780}

You should most likely just remove the DNS-entry for this domain, and also make sure you constantly remove DNS records pointing to CloudFront (and other services as well of course) when you stop using them.

As you might understand, the consequences of this are pretty bad. I now can serve whatever I like on this domain, even fetching httpOnly cookies. I would also be able to issue an SSL for this domain through AlphaSSL or Let's Encrypt (that only needs meta/file verification to issue the certificate) That would end up with the ability to read secure cookies as well.

Also, there's no way at all for a visitor of this page to validate that the content on this domain is not served by UBNT, making it extremely easy to utilize this for targeting the organization by fake login forms / spear phishing using your own domain to plant the attack.

We at Detectify have written about this before a few years ago, but we were now able to actually exploit this using CloudFront as well, something that was not known before.

Regards,
Frans

</details>

---
*Analysed by Claude on 2026-05-24*
