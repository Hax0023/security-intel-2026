# Subdomain Takeover of Brave.com via Unclaimed Fastly CDN CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 175397 | https://hackerone.com/reports/175397
- **Submitted:** 2016-10-12
- **Reporter:** sahiltikoo
- **Program:** Brave Software
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME Records
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Brave.com had dangling CNAME records pointing to unclaimed Fastly CDN domains (prod.p.ssl.global.fastly.net and prod.p.ssl.global.fastlylb.net). An attacker could register these unclaimed Fastly services and claim the subdomains, potentially serving malicious content under Brave's domain. The misconfiguration left these CDN endpoints unverified and available for takeover.

## Attack scenario
1. Attacker performs DNS enumeration on brave.com and identifies CNAME records pointing to Fastly CDN
2. Attacker discovers that prod.p.ssl.global.fastly.net returns 'unknown domain' error from Fastly, indicating it is unclaimed
3. Attacker creates a Fastly account and adds the unclaimed domain to their own Fastly service
4. Attacker configures the claimed Fastly service to serve malicious content (phishing pages, malware, etc.)
5. Victims accessing the subdomain through Brave's DNS records are redirected to attacker's malicious content with Brave's domain in the URL
6. Attacker can conduct credential harvesting, malware distribution, or defacement attacks under Brave's trusted domain

## Root cause
Brave maintained CNAME DNS records pointing to Fastly CDN endpoints that were no longer claimed or actively used by Brave. The CNAME records were not removed after the Fastly service was decommissioned or transferred, leaving dangling pointers that could be claimed by an attacker with a Fastly account.

## Attacker mindset
An attacker recognized that DNS misconfigurations create trust exploitation opportunities. By identifying unclaimed CDN endpoints referenced in DNS records, they could claim the service and inherit the trusted domain association, bypassing normal domain reputation checks and certificate validation issues that would arise from direct domain registration.

## Defensive takeaways
- Regularly audit all DNS records (A, CNAME, MX, NS) and remove dangling/unused entries immediately after service decommissioning
- Implement DNS monitoring to alert on unclaimed CNAME targets that return 'unknown domain' or similar errors
- Maintain an inventory of all CDN, hosting, and third-party service endpoints and their lifecycle status
- Use CNAME flattening or ALIAS records where possible to reduce subdomain takeover surface area
- Implement subdomain takeover scanning as part of continuous security monitoring
- Verify domain ownership in CDN and third-party services using CNAME validation before pointing DNS records to them
- Establish processes to clean up DNS records as part of service decommissioning checklists

## Variant hunting
Search for other subdomains with CNAME records pointing to: unclaimed CDN endpoints (Cloudflare, Akamai, AWS CloudFront), abandoned hosting providers, discontinued third-party services, or services with generic error messages indicating unclaimed domains. Check for similar patterns across Brave's parent company and related domains.

## MITRE ATT&CK
- T1190
- T1557
- T1589

## Notes
This is a classic subdomain takeover vulnerability. The reporter provided clear DNS enumeration evidence and reproduction steps. The vulnerability is particularly dangerous because it affects www.brave.com infrastructure. Fastly's error message explicitly revealed the domain was unclaimed, making exploitation straightforward. No actual exploitation was demonstrated in the report, only the vulnerability disclosure. The fix likely involved either removing the dangling CNAME records or properly claiming/validating them in Fastly.

## Full report
<details><summary>Expand</summary>

## Summary:

Hey!

I want to inform you about sub domain takeover issue i.e. when I did your DNS enumeration i came across :-

Ip Address        Target Name
----------        -----------
151.101.9.7       www.brave.com
151.101.9.7       prod.p.ssl.global.fastly.net
151.101.9.7       prod.p.ssl.global.fastlylb.net

Except the first domain name , the rest two CName point to an unclaimed domain on fastly.com(CDN) that when opened show :-

Fastly error: unknown domain: prod.p.ssl.global.fastly.net. Please check that this domain has been added to a service

the above error indicates that the above address is not in use and can be claimed by an attacker by making an account on fastly.com . 



## Products affected: 

 *  Brave's sub domain 

## Steps To Reproduce:

 * Steps:- Open the above CName ( prod.p.ssl.global.fastly.net.) , as the error is thrown , it indicates the above address can be claimed by creating an account on fastly and giving this as the Cname for your own domain.

## Supporting Material/References:

  * I have added POC image for the DNS enumeration i did. just have a look .


</details>

---
*Analysed by Claude on 2026-05-24*
