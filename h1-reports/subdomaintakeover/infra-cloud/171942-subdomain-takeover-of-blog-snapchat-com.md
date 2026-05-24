# Subdomain Takeover of blog.snapchat.com via Expired Tumblr CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 171942 | https://hackerone.com/reports/171942
- **Submitted:** 2016-09-25
- **Reporter:** jreynoldsdev
- **Program:** Snapchat
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME
- **CVEs:** None
- **Category:** infra-cloud

## Summary
blog.snapchat.com was configured with a CNAME pointing to Snapchat's Tumblr blog (snapchat-blog.com), but the Tumblr blog had been abandoned or the CNAME claim was removed. An attacker registered the snapchat-blog.com custom domain on Tumblr, gaining full control of the blog.snapchat.com subdomain. This allowed the attacker to serve arbitrary content under Snapchat's domain.

## Attack scenario
1. Attacker discovers blog.snapchat.com resolves to a CNAME pointing to snapchat-blog.com on Tumblr infrastructure
2. Attacker verifies that snapchat-blog.com is no longer claimed/active on Tumblr
3. Attacker creates a Tumblr account and registers snapchat-blog.com as a custom domain through Tumblr's domain settings
4. Attacker's Tumblr blog now receives all traffic intended for blog.snapchat.com
5. Attacker can host arbitrary content (malware, phishing, defacement) on the subdomain
6. Users accessing blog.snapchat.com trust the content due to Snapchat's domain authority

## Root cause
Snapchat failed to maintain ownership of the snapchat-blog.com domain after establishing the CNAME delegation. The upstream Tumblr blog was either abandoned or the CNAME claim was revoked without updating Snapchat's DNS records. No monitoring was in place to detect dangling CNAME records.

## Attacker mindset
An opportunistic security researcher who systematically identified an unclaimed delegated domain. The attacker recognized that platforms like Tumblr allow custom domain registration without additional verification, creating a window for takeover. The researcher responsibly disclosed the vulnerability rather than exploiting it for malicious purposes.

## Defensive takeaways
- Regularly audit all DNS records, especially CNAME entries pointing to third-party services
- Implement monitoring/alerting for dangling DNS records and failed domain resolution
- Establish a process to immediately reclaim or remove CNAME delegations when external services are decommissioned
- Require strong verification/authentication when third-party platforms allow custom domain registration
- Maintain an inventory of all subdomains and their delegation targets with ownership tracking
- Use DNS CAA records and DNSSEC to prevent unauthorized domain claims where possible
- Implement periodic DNS health checks as part of infrastructure monitoring

## Variant hunting
Search for other dangling CNAMEs across Snapchat's DNS space, particularly those pointing to: third-party blog platforms (Medium, Ghost, Hashnode), content delivery services (Fastly, Akamai), email services (Mailchimp, SendGrid), and other SaaS platforms. Check for similar patterns at other organizations with extensive third-party integrations. Examine archived DNS records to identify historical delegations that may no longer be maintained.

## MITRE ATT&CK
- T1190
- T1583.1
- T1565.2

## Notes
This is a classic example of a dangling CNAME subdomain takeover. The vulnerability stems from the asymmetry in DNS delegation: once a CNAME is created, an attacker only needs to claim the target domain on the delegated service. Tumblr's weak verification (or lack thereof) for custom domains exacerbated the issue. The researcher demonstrated responsible disclosure by only taking minimal action (verifying takeover was possible) before reporting. The fix required coordination between Snapchat and Tumblr to properly reclaim the domain.

## Full report
<details><summary>Expand</summary>

#Overview
The ANAME for blog.snapchat.com, which redirects to snapchat-blog.com, was pointing to tumblr for Snapchat's blog.  This blog had been expired or had removed the CNAME claim.  Adding "snapchat-blog.com" to the custom domain setting on tumblr allowed takeover of this subdomain.

#Repro Steps
1) Visit http://blog.snapchat.com
Result: Blog registered by my account "jreynoldsdev" displays title "Hello Snapchat - Jake Reynolds"

#Suggested Fixes
The best fix would be for Snapchat's tumblr blog to reclaim this CNAME.  For resolution contact me and we can coordinate switching the domain name back under your control.

If you have any further questions please feel free to reach out.

Thanks,
Jake

</details>

---
*Analysed by Claude on 2026-05-24*
