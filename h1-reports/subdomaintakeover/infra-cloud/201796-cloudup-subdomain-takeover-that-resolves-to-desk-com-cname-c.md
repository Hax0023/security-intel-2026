# Subdomain Takeover via Expired Desk.com Account - help.cloudup.com

## Metadata
- **Source:** HackerOne
- **Report:** 201796 | https://hackerone.com/reports/201796
- **Submitted:** 2017-01-28
- **Reporter:** khizer47
- **Program:** Cloudup
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling CNAME, Account Expiration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A subdomain (help.cloudup.com) was configured with a CNAME pointing to cloudup.desk.com, but Cloudup's Desk account had expired or been canceled. An attacker was able to create a new account on Desk.com with the same subdomain name and gain full control over the CNAME target, effectively taking over the subdomain.

## Attack scenario
1. Attacker identifies that help.cloudup.com resolves to CNAME cloudup.desk.com
2. Attacker determines that the Cloudup account on Desk.com has expired or been canceled
3. Attacker creates a new account on Desk.com using the subdomain identifier 'cloudup'
4. Attacker successfully provisions the CNAME target and gains control over help.cloudup.com via the Desk.com service
5. Attacker can now serve malicious content, host phishing pages, or redirect traffic from help.cloudup.com
6. Users accessing help.cloudup.com receive content controlled by the attacker instead of Cloudup

## Root cause
Cloudup failed to actively monitor and manage DNS records pointing to third-party services. When the upstream Desk.com account expired, the CNAME became dangling and available for registration by an attacker. No remediation was performed to remove or update the DNS record.

## Attacker mindset
Opportunistic reconnaissance-driven approach. The attacker performed basic DNS enumeration (CNAME lookups) and identified a stale third-party service integration. They recognized the business logic weakness that allows new account creation on the third-party service with the same identifier, enabling subdomain takeover without technical exploitation.

## Defensive takeaways
- Implement DNS monitoring to detect dangling CNAMEs and subdomains pointing to unused third-party services
- Maintain an inventory of all DNS records and their associated third-party service accounts
- Establish a process to retire DNS records when associated service accounts are canceled or expired
- Regularly audit subdomains to ensure they resolve to active, authorized services
- Configure DNS validation and ownership checks when using third-party services
- Implement CNAME cloaking or verification mechanisms to prevent unauthorized service binding
- Monitor for subdomain takeover attempts by checking for newly created accounts on integrated services
- Use DNSSEC or other DNS security mechanisms to prevent unauthorized modifications

## Variant hunting
Scan for other expired Desk.com integrations across Cloudup's other subdomains
Identify other Cloudup subdomains pointing to third-party services (Zendesk, Intercom, etc.) that may have expired
Check if other subdomains use similar patterns where account expiration creates takeover opportunities
Enumerate all Cloudup DNS records for dangling CNAMEs pointing to any service provider
Search for subdomains pointing to GitHub pages, Heroku, AWS, or other platforms with available namespace collision

## MITRE ATT&CK
- T1190
- T1657

## Notes
The reporter noted an SSL certificate error on the main domain, suggesting certificate validation may also be lacking. The vulnerability is straightforward - stale third-party service integrations represent a common but overlooked attack surface. The reporter demonstrated responsible disclosure by documenting the finding with screenshots.

## Full report
<details><summary>Expand</summary>

Hi,

While Looking On The CloudUp Website I found That One of The Subdomain of CloudUp [HELP](help.cloudup.com) was Hosted on [Desk](Desk.com) and I think tHe Desk Account of Cloudup was Expired or Canceled by any cause So I have Checked The Site for its CNAME and The CNAME was Resolving to 
###CNAME	http://cloudup.desk.com
So I Tried to Make an Account on [Desk](desk.com) With the same as The CNAME Cloud.desk.com And I was Successful in this Coz Of The Account of cloudup was Expired or cancelled, Now I have setup my page on the site.


But Due to some Problem The Main Domain ***help.cloudup.com (See Screenshot Below 0.png) is Showing SSL Error Maybe due to expired Certificate I'm Not sure as I'm just a Started still have to learn many things! 
So Due to the Error I'm unable to Show my Message on The Main Domain But Still I have Full Control over The CNAME ( See Screenshots) 

Hope This Will Be Resolved

Thanks,
Muhammad Khizer Javed


</details>

---
*Analysed by Claude on 2026-05-24*
