# Subdomain Takeover in gratipay.com via Heroku DNS

## Metadata
- **Source:** HackerOne
- **Report:** 257331 | https://hackerone.com/reports/257331
- **Submitted:** 2017-08-07
- **Reporter:** anshad
- **Program:** Gratipay
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** uncategorised

## Summary
A dangling DNS record pointing to 'www.gratipay.com.herokudns.com' was discovered that is not registered in Heroku, allowing an attacker to register this subdomain and take control of it. An attacker could leverage this to perform phishing attacks, serve malicious content, or steal credentials by impersonating Gratipay services.

## Attack scenario
1. Attacker discovers dangling DNS record 'www.gratipay.com.herokudns.com' pointing to unregistered Heroku instance
2. Attacker registers the subdomain with Heroku, gaining full control of the DNS resolution
3. Attacker deploys malicious application or content on the compromised subdomain
4. Users or automated systems trust the subdomain due to Gratipay domain origin, visiting the attacker's site
5. Attacker harvests credentials, injects malware, or performs further attacks leveraging the trusted domain
6. Potential lateral movement or privilege escalation within Gratipay infrastructure or user accounts

## Root cause
Gratipay created a DNS record pointing to Heroku infrastructure but failed to maintain the corresponding Heroku application or properly clean up the dangling DNS record when the application was removed or abandoned. No verification was performed to ensure the subdomain remained under organizational control.

## Attacker mindset
Opportunistic subdomain hijacking to impersonate a legitimate service, establish trust with users, and conduct downstream attacks such as phishing, credential harvesting, or malware distribution under the guise of a trusted domain.

## Defensive takeaways
- Implement DNS monitoring to regularly audit all DNS records and identify dangling or orphaned entries
- Establish a lifecycle management process for DNS records that ensures cleanup when infrastructure is decommissioned
- Regularly scan organizational domains for subdomain takeover vulnerabilities using automated tools
- Configure DNS CAA records to restrict certificate issuance for critical subdomains
- Maintain an authoritative inventory of all subdomains and their corresponding infrastructure
- Implement DNSSEC to prevent unauthorized DNS modifications
- Use subdomain takeover detection services that actively monitor for unregistered subdomains pointing to popular platforms

## Variant hunting
Scan all subdomains of target organization for DNS records pointing to unclaimed cloud services (AWS, Azure, Netlify, Vercel, etc.)
Check for CNAME records pointing to non-existent or unregistered instances across major hosting providers
Look for MX records, A records, or other DNS entries pointing to decommissioned services
Enumerate subdomains using passive DNS databases and cross-reference against active infrastructure
Test subdomains systematically across all major PaaS platforms (GitHub Pages, Firebase, Shopify, etc.)
Monitor for historical DNS records that may no longer be actively managed

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1583.1

## Notes
This vulnerability represents a common but often overlooked security issue. The reporter used knockpy tool for enumeration and identified the issue through browser testing. The bug demonstrates the importance of DNS hygiene and the risk of partial infrastructure migration or cleanup. Heroku's error message actually revealed the misconfiguration, making this easily exploitable. The vulnerability requires relatively low technical skill to exploit once discovered but can have significant impact on user trust and security.

## Full report
<details><summary>Expand</summary>

# Summary

Sub domain take over in gratipay.com

# Description

I scanned gratipay.com using knockpy to find the sub domains. I found one subdomain
'www.gratipay.com.herokudns.com'. But this sub domain is not registered in heroku. An attacker can buy this sub domain from heroku. 

# Browsers Verified In

  * Firefox
  * Chrome

# Steps To Reproduce

  1. use the 'knockpy gratipay.com' command in  knockpy to find sub domains
       .
       You will get one domain like 'www.gratipay.com.herokudns.com'.
  1. Test this domain in browser. Then you will get error message from heroku. Please refer attached screen shot for more clarity.
  

</details>

---
*Analysed by Claude on 2026-05-24*
