# Subdomain Takeover in help.tictail.com via Unclaimed Zendesk CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 869605 | https://hackerone.com/reports/869605
- **Submitted:** 2020-05-09
- **Reporter:** meow-hacker-meow
- **Program:** Shopify (via Tictail acquisition)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME Record
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain help.tictail.com contains a dangling CNAME record pointing to an unclaimed tictail.zendesk.com instance, allowing an attacker to register the Zendesk subdomain and claim the DNS-configured domain. This enables phishing attacks impersonating the legitimate support website and social engineering of users who trust the Tictail brand.

## Attack scenario
1. Attacker discovers help.tictail.com via DNS reconnaissance or search results
2. Attacker performs dig/nslookup to identify CNAME record pointing to tictail.zendesk.com
3. Attacker verifies tictail.zendesk.com is unclaimed by attempting Zendesk signup with that subdomain name
4. Attacker registers free Zendesk trial account and claims tictail.zendesk.com as their subdomain
5. Attacker configures host mapping in Zendesk Settings to map help.tictail.com to their Zendesk instance with SSL enabled
6. Attacker creates phishing content mimicking legitimate support pages and harvests credentials from users visiting the now-hijacked subdomain

## Root cause
Tictail/Shopify provisioned a Zendesk integration and created a CNAME DNS record (help.tictail.com -> tictail.zendesk.com) but failed to claim/secure the Zendesk subdomain or clean up the DNS record after discontinuing the service. The Zendesk instance was left in an orphaned state, allowing registration by anyone.

## Attacker mindset
An attacker recognizes that abandoned infrastructure creates trust-abuse opportunities. By hijacking a subdomain under a trusted brand (Tictail/Shopify), they bypass user skepticism and can execute high-success-rate phishing campaigns. The attacker understands DNS mechanics, Zendesk's signup process, and the value of brand impersonation for credential harvesting.

## Defensive takeaways
- Maintain a comprehensive DNS inventory and regularly audit CNAME records for dangling pointers
- When deprovisioning third-party services, either delete DNS records immediately or claim/secure the target subdomain in the third-party system
- Implement preventive controls: use DNS record validation that prevents CNAME creation to non-verified domains
- Monitor for subdomain registration attempts matching your organization's subdomains across major platforms (Zendesk, Heroku, GitHub, etc.)
- Establish incident response procedures for subdomain takeover (DNSSEC, CNAME flattening, or redirect to canonical support domain)
- Periodically scan for dangling DNS records using automated tools and security scanning platforms

## Variant hunting
Search for other Tictail/Shopify subdomains with CNAME records pointing to unclaimed third-party services (e.g., S3, GitHub Pages, Heroku, Netlify, Vercel, Firebase). Check for abandoned subdomains pointing to: mail.*, api.*, dev.*, staging.*, cdn.*, or other common prefixes that may use external services. Examine acquisition-related infrastructure where parent company (Shopify) may not have properly claimed all assets.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (phishing via trusted domain)
- T1598 - Phishing for Information (credential harvesting through hijacked support domain)
- T1583 - Acquire Infrastructure (registering the unclaimed Zendesk subdomain)
- T1589 - Gather Victim Identity Information (leveraging trust in Tictail brand)

## Notes
The researcher provided excellent proof-of-concept documentation including video evidence. The vulnerability chain is clear: DNS misconfiguration + unverified third-party integration + service discontinuation without cleanup = complete domain takeover. This is a teaching example of why infrastructure deprovisioning checklists must include both removal of DNS records AND claiming/securing external service accounts. The potential for high-impact phishing against support-seeking users makes this High severity despite the straightforward remediation.

## Full report
<details><summary>Expand</summary>

Hello,

Description:
---------------------

The subdomain at https://help.tictail.com  has an unclaimed CNAME record ( tictail.zendesk.com ) . I checked the username availability in the signup process at zendesk, it was observed that the subdomain is vulnerable to a subdomain takeover which allows an attacker could exploit such a situation by registering the expired subdomain and setting up a phishing page that mimics the company’s main support website.

This vulnerability is called subdomain takeover. You can read more about it here:

https://blog.sweepatic.com/subdomain-takeover-principles/
https://hackerone.com/reports/32825
https://hackerone.com/reports/175070
https://hackerone.com/reports/172137

Steps to Reproduce & Proof of Concepts:
---------------------

1. Using dig and and username availability check at zendesk, I was able to determine that the subdomain https://help.tictail.com was vulnerable to takeover. 

Screenshots : 
F821713
F821710

2. I went to zendesk.com and registered for a free trial. When I was asked what name I want the zendesk domain to have, i chose the name (tictail.zendesk.com). and it was available for takeover. (showed green mark)

Screenshot : F821718

3.After registering, I went to Settings > Account > Host mapping. Filled in the domain the vulnerable subdomain. ( https://help.tictail.com  )

Screenshot : F821717

4.I did enable SSL (under security)  on the domain to stop the redirect when browsing to the target's domain.

Screenshot : F821716

5.I created a guide Help Center (not published )

Screenshot : F821712

6.Added a test article called “POC”. (Not published)

Screenshot :  F821714

Supporting Material/References:
---------------------

Video of the full takeover process : F821719


Mitigation and How to fix :
---------------------

Remove the DNS record from the DNS zone if it is no longer needed.
Claim the domain name in a permanent DNS record so it cannot be used elsewhere.

## Impact

Subdomain takeover is abused for several purposes:
---------------------


1- As mentioned above, an attacker could exploit such a situation by registering the expired domain and setting up a phishing page that mimics the company’s main support website. 

### Example scenarios : 

### Scenario 1 : 

 An attacker would create the same helpdesk page (design, texts etc… ) as in https://help.shopify.com/ 
Redirect users to custom urls (phishing pages) to collect login details : 
(eg; This page contains custom urls (store owner) to other parts of the helpdesk website, an attacker can create the exact same page and add  a custom url to lead shopify  users to phishing pages that mimics all the company’s pages that requires logins. 
https://help.shopify.com/en/manual/your-account/manage-account#update-your-billing-information

Screenshots :
 https://prntscr.com/sdqkpr

###Scenario 2 : 

More than that, since the brand name “Tictail”is famous and trusted, an attacker can use that and  register domain name “ticctail.com” (available),  and create the same exact home page as the original tictail.com homepage, and this time the button will lead to a phishing pages (logins, password reset etc…), and of course with the help of some advanced SEO techniques, the phishing page and subdomain could be found easily.

This is how I found the vulnerable subdomain in question, it was the first result. Imagine what people will find when they will search for “tictail” (If SEO is applied well)

Screenshot : F821715 

2- Share malicious files using the sharing files option in zendesk
       etc...

Here's a write up of the vulnerabilities : https://0xpatrik.com/subdomain-takeover/

Regards, 

Mohmaed Ali Moujehed

</details>

---
*Analysed by Claude on 2026-05-24*
