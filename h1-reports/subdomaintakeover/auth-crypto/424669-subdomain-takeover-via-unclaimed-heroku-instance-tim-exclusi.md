# Subdomain Takeover Via Unclaimed Heroku Instance tim-exclusive.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 424669 | https://hackerone.com/reports/424669
- **Submitted:** 2018-10-16
- **Reporter:** todayisnew
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Cloud Service Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A Shopify subdomain (tim-exclusive.shopify.com) was configured with a CNAME record pointing to an unclaimed Heroku instance, allowing an attacker to register the corresponding Heroku app and assume control of the subdomain. This enabled the attacker to serve arbitrary content, potentially facilitating phishing, malware distribution, or credential theft under the trusted Shopify domain.

## Attack scenario
1. Attacker discovers tim-exclusive.shopify.com via DNS enumeration or subdomain scanning tools
2. Attacker identifies the CNAME record pointing to an unclaimed Heroku instance (e.g., tim-exclusive.herokuapp.com)
3. Attacker registers an account on Heroku and claims the unclaimed app name
4. Attacker configures the Heroku app to serve malicious content (phishing page, malware, etc.)
5. Victim visits tim-exclusive.shopify.com and is served attacker-controlled content while believing they are on a legitimate Shopify domain
6. Attacker harvests credentials, distributes malware, or performs other attacks leveraging the trusted domain reputation

## Root cause
The organization created a DNS CNAME record pointing to a Heroku instance that was never registered or has since been deleted/abandoned. No mechanism exists to prevent re-registration of unclaimed cloud services, and the CNAME was not cleaned up when the Heroku app was removed.

## Attacker mindset
Opportunistic reconnaissance-driven attacker who systematically scans for dangling DNS records pointing to popular cloud services. Minimal effort exploitation leveraging weak cloud service claim mechanisms. Motivated by domain hijacking for phishing, credential harvesting, or reputation abuse.

## Defensive takeaways
- Implement DNS record inventory and monitoring to detect and alert on CNAME records pointing to external services
- Establish a process to verify that all external cloud service endpoints are actively claimed and maintained
- Regularly audit DNS records and remove CNAME entries for services no longer in use
- Use DNS CAA records to restrict certificate issuance and prevent SSL/TLS abuse of subdomains
- Implement automated scanning for subdomain takeover vulnerabilities in CI/CD pipelines
- Consider using subdomain verification/validation mechanisms provided by cloud platforms
- Maintain an up-to-date inventory of all subdomains and their purposes with ownership accountability

## Variant hunting
Search for other Shopify subdomains with CNAME records pointing to unclaimed cloud services (AWS, Azure, GitHub Pages, Firebase, etc.). Scan for similar patterns across other organizations using AWS S3 buckets, Azure blobs, or other services with claim-based naming. Check for wildcard DNS configurations that could enable broader takeover.

## MITRE ATT&CK
- T1190
- T1583.1
- T1584.1

## Notes
The report demonstrates good ethical disclosure and provides fix recommendations. The POC is somewhat weak (screenshot link rather than direct demonstration) but sufficient to prove the vulnerability. This is a classic subdomain takeover scenario common in bug bounties. The attacker's polite tone and genuine remediation suggestions suggest this was a legitimate security researcher. The vulnerability has high impact despite ease of exploitation, as it affects brand reputation and enables downstream attacks.

## Full report
<details><summary>Expand</summary>

Good day, I truly hope it treats you great on your side of the screen :)

I have found that your website tim-exclusive.shopify.com is pointed via a cname to an unclaimed Heroku Instance

This was not registered on Heroku.

I was able to take over the domain:

See my POC (Pug of Concept)
http://tim-exclusive.shopify.com/

POC Video:
https://www.dropbox.com/s/0p6dqz3rwbx2wxn/Screenshot%202018-10-16%2011.30.52.png?dl=0

Options How to fix:

1) Remove the Cname record on tim-exclusive.shopify.com to not point to Heroku

2) Ask me to remove my registered tim-exclusive.shopify.com on Heroku, and you can re register yours :)

May you be well on your side of the screen :)

-Eric

## Impact

control over domain :)

</details>

---
*Analysed by Claude on 2026-05-24*
