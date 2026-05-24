# Subdomain Takeover - 8ybhy85kld9zp9xf84x6.imgur.com

## Metadata
- **Source:** HackerOne
- **Report:** 1527405 | https://hackerone.com/reports/1527405
- **Submitted:** 2022-03-31
- **Reporter:** mr_baka
- **Program:** Imgur
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Unclaimed Subdomain
- **CVEs:** None
- **Category:** infra-cloud

## Summary
An unclaimed subdomain (8ybhy85kld9zp9xf84x6.imgur.com) pointing to Squarespace was left unregistered, allowing an attacker to claim it via Squarespace and gain control over the subdomain. This enables hosting arbitrary content under the Imgur domain, facilitating phishing, malware distribution, and other attacks.

## Attack scenario
1. Attacker discovers unclaimed subdomain 8ybhy85kld9zp9xf84x6.imgur.com through DNS enumeration or OSINT
2. Attacker identifies that the subdomain points to Squarespace infrastructure (dangling DNS record)
3. Attacker creates a Squarespace account and claims the unclaimed custom domain
4. Attacker gains control over the subdomain and can host malicious content at https://8ybhy85kld9zp9xf84x6.imgur.com
5. Attacker leverages the trusted Imgur domain for phishing emails, malware distribution, or XSS attacks
6. Users trust the Imgur domain and fall victim to attacks hosted on the attacker-controlled subdomain

## Root cause
Imgur created a DNS record pointing to Squarespace infrastructure but failed to complete the domain verification/registration process on Squarespace, leaving the subdomain unclaimed and vulnerable to takeover.

## Attacker mindset
An attacker with subdomain enumeration skills recognized that an unclaimed subdomain could be hijacked by registering it on the third-party service (Squarespace) it pointed to. This is a classic subdomain takeover technique exploiting abandoned infrastructure setup.

## Defensive takeaways
- Implement continuous monitoring of all DNS records and subdomains to identify dangling records
- Complete domain verification processes promptly after creating DNS entries
- Regularly audit subdomains and remove or properly claim those no longer in use
- Use DNS monitoring tools to detect when subdomains point to services where the domain is not claimed
- Implement CNAME flattening or use DNS providers with subdomain takeover prevention features
- Maintain an inventory of all subdomains and their associated services/owners
- Consider using wildcard DNS or ACME DNS challenges to prevent unauthorized third-party claims

## Variant hunting
Scan for other Imgur subdomains pointing to unclaimed Squarespace domains
Check other Imgur subdomains for similar dangling DNS records pointing to other third-party services (Heroku, GitHub Pages, AWS, etc.)
Look for patterns in subdomain naming (8ybhy85kld9zp9xf84x6 appears to be a hash/ID) that might indicate abandoned setup attempts
Enumerate all *.imgur.com subdomains and test for takeover on common platforms (Azure, Netlify, Firebase, etc.)

## MITRE ATT&CK
- T1583.001
- T1583.002
- T1190
- T1598.003
- T1566.002

## Notes
The reporter demonstrated proof-of-concept by successfully claiming the domain on Squarespace without hosting malicious content. The vulnerability is complete - an attacker could immediately begin hosting phishing pages or malware. The fact that account upgrade is needed for certain features does not mitigate the core risk of domain takeover and hosting arbitrary content.

## Full report
<details><summary>Expand</summary>

Hello Gents,
+ While testing ** Imgur ** I found an unclaimed subdomain which is; “8ybhy85kld9zp9xf84x6.imgur.com”, and I was able to claim it!
+ But actually I didn't upload or host a simple file like `mr_baka.html`, because I need to upgrade the account to be able to use this custom domain!
+ Anyway, you can verify that I was able to claim this subdomain by visiting https://8ybhy85kld9zp9xf84x6.imgur.com and clicking [Manage domain settings here.](https://mrbaka.squarespace.com/config#/settings/domains), which should lead you to my account; https://mrbaka.squarespace.com" .

### Before claiming:
+ {F1675230}

### After:
+ {F1675231}

## Impact

Subdomain Takeover may lead to below consequences:

- Phishing / Spear Phishing
- Malware distribution
- XSS
- Authentication bypass and more
- Credential stealing

</details>

---
*Analysed by Claude on 2026-05-24*
