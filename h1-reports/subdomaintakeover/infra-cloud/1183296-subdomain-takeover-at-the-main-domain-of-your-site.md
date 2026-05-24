# Subdomain Takeover at Main Domain (sifchain.finance pointing to unclaimed Wix CNAME)

## Metadata
- **Source:** HackerOne
- **Report:** 1183296 | https://hackerone.com/reports/1183296
- **Submitted:** 2021-05-03
- **Reporter:** ahmedelmalky
- **Program:** Sifchain (HackerOne Report #1183296)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME Record
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The main domain sifchain.finance contains a CNAME record pointing to an unclaimed Wix.com subdomain, allowing any Wix premium account holder to claim ownership and take over the domain. This critical misconfiguration affects the primary domain rather than a subdomain, exposing the organization to complete account takeover, phishing, malware distribution, and authentication bypass attacks.

## Attack scenario
1. Attacker identifies that sifchain.finance resolves to a Wix.com CNAME record via DNS enumeration
2. Attacker verifies the Wix subdomain is unclaimed by visiting the domain and observing Wix error page
3. Attacker creates or uses existing Wix premium account to claim the orphaned subdomain
4. Attacker gains full control of sifchain.finance, serving malicious content from their Wix account
5. Attacker redirects visitors to phishing page impersonating Sifchain to harvest credentials
6. Users unknowingly interact with attacker-controlled domain believing it is legitimate Sifchain

## Root cause
DNS CNAME record for sifchain.finance points to Wix.com infrastructure without ensuring the Wix account maintains active subscription or ownership. The organization either abandoned the Wix hosting relationship without cleaning up DNS records or failed to renew the subscription, leaving the CNAME dangling and claimable by third parties.

## Attacker mindset
An attacker with Wix premium access could perform high-impact attacks by claiming the unclaimed CNAME, gaining instant control of the main domain for phishing campaigns, credential harvesting, malware distribution, or impersonation attacks without needing to compromise actual Sifchain infrastructure.

## Defensive takeaways
- Regularly audit all DNS records (A, AAAA, CNAME, MX, TXT) for dangling or orphaned entries pointing to third-party services
- Implement DNS cleanup procedures when decommissioning services or letting subscriptions expire
- Maintain inventory of all hosting providers and third-party services with associated DNS records
- Use DNS monitoring tools to detect changes and alert on suspicious modifications
- Document the purpose and ownership of each DNS record for periodic review
- Prefer direct A/AAAA records over CNAME when possible to reduce third-party dependencies
- Implement DNSSEC and CAA records to prevent unauthorized domain claims
- Establish service lifecycle management procedures ensuring DNS cleanup before termination

## Variant hunting
Scan for other Sifchain subdomains pointing to abandoned third-party services (GitHub Pages, Heroku, AWS, Azure, Firebase)
Check for MX records pointing to defunct email providers that could enable email takeover
Identify other organizations' main domains with similar dangling CNAME configurations
Search for historical DNS records of sifchain.finance to identify past service providers
Check for NS record delegation to nameservers no longer actively managed by organization
Look for TXT records (DKIM, SPF) pointing to abandoned email service providers

## MITRE ATT&CK
- T1190
- T1566.002
- T1199
- T1589.001
- T1598.003
- T1542.005

## Notes
Reporter notes this falls outside stated scope but represents critical risk to main domain. Reporter exercised responsible disclosure by not attempting manual exploitation due to lack of testing permission and premium Wix account. The vulnerability's impact is amplified by affecting the primary domain rather than a subdomain, making it a direct path to complete domain hijacking. Organization should treat as P0/critical priority.

## Full report
<details><summary>Expand</summary>

Hello,

I Know that isn't in the Scope But this The Only Way I can Report With And This Issue Is Very High It Belongs to the Main Domain 
this is pretty serious security issue in some context, so please act as fast as possible.

##overview 
 the  Main Domain [sifchain.finance] is pointing to wix.com, which has unclaimed CNAME record. ANYONE is able to own http://sifchain.finance domain at the moment.
This vulnerability is called subdomain takeover. You can read more about it here:
https://blog.sweepatic.com/subdomain-takeover-principles/
https://hackerone.com/reports/32825
https://hackerone.com/reports/175070
https://hackerone.com/reports/172137

## Steps To Reproduce:
Visit >> https://sifchain.finance

when you open the above Link you will find wix.com subdomain error if you have an account in wix.com "premium" you can take over this subdomain
I don't try it manually because I haven't permission to test this issue and i haven't the Premuim Account . 

##Mitigation:
 Remove the CNAME record from  sifchain.finance  DNS zone completely.
Or renew the Subscription .  

Regards,

Ahmed Elmalky

## Impact

Very Critical It is In the Main Domain . 
Subdomain takeover is abused for several purposes:
    Authentication bypass
Malware distribution
Phishing / Spear phishing
XSS

</details>

---
*Analysed by Claude on 2026-05-24*
