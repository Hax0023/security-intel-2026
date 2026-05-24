# code.wordpress.net Subdomain Takeover via Dangling DNS Record

## Metadata
- **Source:** HackerOne
- **Report:** 295330 | https://hackerone.com/reports/295330
- **Submitted:** 2017-12-05
- **Reporter:** sniperpex
- **Program:** WordPress
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Domain Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The subdomain code.wordpress.net contains a dangling DNS CNAME record pointing to wpprojects.wordpress.com, which appears to be unclaimed or improperly configured. An attacker can claim the intermediate domain and serve content under code.wordpress.net, potentially enabling phishing, malware distribution, or credential theft from WordPress users.

## Attack scenario
1. Attacker identifies code.wordpress.net resolves via CNAME chain to wpprojects.wordpress.com and ultimately lb.wordpress.com
2. Attacker determines wpprojects.wordpress.com is unclaimed or not properly configured by WordPress
3. Attacker registers or claims wpprojects.wordpress.com (or exploits misconfiguration at the intermediate point)
4. Attacker configures DNS records to point wpprojects.wordpress.com to attacker-controlled infrastructure
5. code.wordpress.net now resolves to attacker's server due to CNAME chain
6. Attacker hosts malicious content (phishing page, malware) under the trusted WordPress domain

## Root cause
WordPress failed to properly decommission the code.wordpress.net subdomain by either removing the DNS record or ensuring the target domain in the CNAME chain remains under their control. The CNAME points to wpprojects.wordpress.com which appears to be either abandoned or not properly claimed, creating a window for takeover.

## Attacker mindset
An attacker recognizes that legitimate WordPress infrastructure (code.wordpress.net) would be highly trusted by users and developers. By taking over the subdomain through DNS hijacking, they can impersonate WordPress services, harvest credentials, or distribute malware with significantly higher success rates than a completely spoofed domain.

## Defensive takeaways
- Regularly audit all subdomains and their DNS configurations for dangling records
- Implement DNS security monitoring to detect unauthorized changes to CNAME/A records
- Avoid CNAME chains; use direct A records or ensure all intermediate domains remain under your control
- Decommission unused subdomains completely rather than leaving orphaned DNS entries
- Use subdomain takeover prevention by registering potential intermediate domains or using DNS validation
- Implement DNSSEC to prevent DNS hijacking attacks
- Monitor for unclaimed domains in CNAME chains and reclaim them immediately

## Variant hunting
Search for other wordpress.* subdomains with similar CNAME chains; investigate other Automattic properties for dangling records; look for subdomains pointing to 'wpprojects' or similar intermediate service names; scan for domains with broken domain mapping configurations

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1187

## Notes
This is a classic subdomain takeover vulnerability. The error message 'Domain mapping upgrade for this domain not found' suggests WordPress once had infrastructure to handle custom domain mappings but this particular subdomain was not properly cleaned up. The CNAME chain indicates infrastructure debt and suggests other similar misconfigurations may exist. No bounty amount was specified in the report, suggesting it may have been resolved quickly or the researcher did not disclose the amount.

## Full report
<details><summary>Expand</summary>

Hy Wordpress sec i found as it is posible to takeover this domain http://code.wordpress.net when you navigate it you will get this error msg:

Warning! Domain mapping upgrade for this domain not found. Please log in and go to the Domains Upgrades page of your blog to use this domain. 

$ host code.wordpress.net
code.wordpress.net is an alias for wpprojects.wordpress.com.
wpprojects.wordpress.com is an alias for lb.wordpress.com.
lb.wordpress.com has address 192.0.78.13
lb.wordpress.com has address 192.0.78.12

## Impact

The attacker can takeover this subdomain

</details>

---
*Analysed by Claude on 2026-05-24*
