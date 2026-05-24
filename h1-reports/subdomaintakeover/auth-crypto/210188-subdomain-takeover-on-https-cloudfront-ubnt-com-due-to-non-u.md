# Subdomain Takeover on cloudfront.ubnt.com via Unclaimed CloudFront CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 210188 | https://hackerone.com/reports/210188
- **Submitted:** 2017-03-02
- **Reporter:** linkks
- **Program:** Ubiquiti Networks
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record, Improper Access Control
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A CloudFront DNS entry for cloudfront.ubnt.com pointed to an orphaned CloudFront distribution (du6drkqe7qw4g.cloudfront.net) that had no configured CNAME ownership validation. An attacker could register the CloudFront distribution as their own and serve arbitrary content, including phishing pages and stealing httpOnly cookies via SSL certificate acquisition.

## Attack scenario
1. Attacker discovers cloudfront.ubnt.com resolves to du6drkqe7qw4g.cloudfront.net via DNS enumeration
2. Attacker verifies the CloudFront distribution has no active CNAME bindings through CloudFront console or API
3. Attacker creates a CloudFront distribution and claims the orphaned domain by configuring it as a Custom CNAME
4. Attacker obtains valid SSL certificate for cloudfront.ubnt.com via Let's Encrypt or AlphaSSL using DNS/file verification
5. Attacker hosts phishing pages or malicious content on the subdomain with valid HTTPS
6. Users visit cloudfront.ubnt.com believing it is legitimate UBNT infrastructure, exposing credentials and httpOnly cookies

## Root cause
Ubiquiti failed to remove the DNS CNAME record for cloudfront.ubnt.com after decommissioning or ceasing to use the associated CloudFront distribution. AWS CloudFront does not validate ownership of CNAME domains by the requesting account, allowing any attacker to claim an unused CNAME endpoint. Additionally, no continuous monitoring or cleanup process existed for deprecated DNS records.

## Attacker mindset
An opportunistic attacker scanning for dangling DNS records pointing to cloud services. The attacker recognized the business value of compromising a legitimate company subdomain to conduct targeted phishing and credential harvesting against UBNT users and customers who inherently trust the ubnt.com domain.

## Defensive takeaways
- Implement mandatory DNS record cleanup procedures when decommissioning cloud services
- Maintain an authoritative inventory of all DNS records and their associated services with lifecycle tracking
- Deploy continuous DNS monitoring to detect dangling or orphaned records pointing to cloud providers
- Establish alerts for CNAME records pointing to cloud services that are no longer in use
- Implement CNAME validation at the DNS provider or service provider level to prevent unauthorized claims
- Use AWS Certificate Manager (ACM) or equivalent to manage certificates and restrict domain validation
- Conduct regular subdomain enumeration and validation to identify unclaimed or misconfigured entries
- Implement CAA (Certification Authority Authorization) DNS records to restrict certificate issuance
- Establish ownership verification requirements before allowing CNAME binding to CloudFront distributions

## Variant hunting
Search for other UBNT subdomains pointing to CloudFront, AWS S3, Azure, or other CDN/hosting services. Enumerate organizational subdomains across all cloud providers and CDNs. Check for patterns of abandoned services (old product lines, deprecated APIs, archived documentation sites). Review companies with high acquisition activity for dangling records from acquired entities.

## MITRE ATT&CK
- T1584.001 - Compromise Infrastructure: Domains
- T1583.001 - Acquire Infrastructure: Domains
- T1590.003 - Gather Victim Network Information: Server Information
- T1598.003 - Phishing for Information: Spearphishing Link
- T1566.002 - Phishing: Spearphishing Link
- T1187 - Forced Authentication

## Notes
This vulnerability exemplifies the broader class of 'subdomain takeover' attacks. The impact is amplified by the legitimate appearance of the UBNT domain and potential to obtain valid SSL certificates. The researcher correctly noted that visitors have no mechanism to detect content is not served by legitimate UBNT infrastructure. The root cause is organizational neglect rather than a platform vulnerability in CloudFront itself. Similar vulnerabilities are widespread due to improper cloud service lifecycle management across enterprises.

## Full report
<details><summary>Expand</summary>

So lately I have discovered that CloudFront is not validating which user that connects a CNAME:d domain to a CloudFront Origin. This means that if I could find a domain that is still pointing to CloudFront, without being connected to any Origin as a Custom CNAME, I can actually claim the domain myself and point it to whatever I want.

dig cloudfront.ubnt.com

; <<>> DiG 9.10.3-P4-Debian <<>> cloudfront.ubnt.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52550
;; flags: qr rd ra; QUERY: 1, ANSWER: 9, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;cloudfront.ubnt.com. IN A

;; ANSWER SECTION:
cloudfront.ubnt.com. 268 IN CNAME du6drkqe7qw4g.cloudfront.net.
du6drkqe7qw4g.cloudfront.net. 29 IN A 52.222.171.58
du6drkqe7qw4g.cloudfront.net. 29 IN A 52.222.171.143
du6drkqe7qw4g.cloudfront.net. 29 IN A 52.222.171.238
du6drkqe7qw4g.cloudfront.net. 29 IN A 52.222.171.216
du6drkqe7qw4g.cloudfront.net. 29 IN A 52.222.171.144
du6drkqe7qw4g.cloudfront.net. 29 IN A 52.222.171.190
du6drkqe7qw4g.cloudfront.net. 29 IN A 52.222.171.55
du6drkqe7qw4g.cloudfront.net. 29 IN A 52.222.171.71

;; Query time: 7 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Wed Feb 22 03:26:49 MSK 2017
;; MSG SIZE rcvd: 218

;; ANSWER SECTION:
cloudfront.ubnt.com. 268 IN CNAME du6drkqe7qw4g.cloudfront.net.

You should most likely just remove the DNS-entry for this domain, and also make sure you constantly remove DNS records pointing to CloudFront (and other services as well of course) when you stop using them.

As you might understand, the consequences of this are pretty bad. I now can serve whatever I like on this domain, even fetching httpOnly cookies. I would also be able to issue an SSL for this domain through AlphaSSL or Let's Encrypt (that only needs meta/file verification to issue the certificate) That would end up with the ability to read secure cookies as well.

Also, there's no way at all for a visitor of this page to validate that the content on this domain is not served by UBNT, making it extremely easy to utilize this for targeting the organization by fake login forms / spear phishing using your own domain to plant the attack.

You can read about this sort of attacks here : http://labs.detectify.com/post/109964122636/hostile-subdomain-takeover-using

</details>

---
*Analysed by Claude on 2026-05-24*
