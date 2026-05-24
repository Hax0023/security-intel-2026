# AWS S3 Subdomain Takeover via Unclaimed Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 1329792 | https://hackerone.com/reports/1329792
- **Submitted:** 2021-09-03
- **Reporter:** al-madjus
- **Program:** AWS
- **Bounty:** Not disclosed in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Cloud Resource Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A www subdomain pointed via CNAME to an unclaimed AWS S3 bucket that was available for registration. The attacker registered the bucket and demonstrated proof-of-concept by serving content from the taken-over domain. This allows potential exploitation through cookie theft, CORS/CSP bypass, SSRF bypass, and phishing attacks.

## Attack scenario
1. Attacker performs DNS reconnaissance and identifies CNAME pointing to AWS bucket URL (*.s3.amazonaws.com or similar)
2. Attacker verifies the referenced S3 bucket does not exist or is unclaimed by attempting to access it
3. Attacker registers/claims the S3 bucket with the same name as the dangling DNS record
4. Attacker uploads malicious content (HTML, JavaScript) to the newly controlled bucket
5. Users accessing the subdomain receive attacker-controlled content from the bucket
6. Attacker exploits trust relationship to steal session cookies, bypass security policies, or conduct phishing

## Root cause
DNS record (CNAME) was not cleaned up after the associated S3 bucket was deleted or never properly provisioned. The organization failed to maintain inventory of cloud resources and their corresponding DNS entries, allowing dangling DNS pointers to exist.

## Attacker mindset
Opportunistic reconnaissance-based attack. Attacker systematically scanned DNS records, identified misconfigured infrastructure, and exploited the lack of resource ownership verification to claim abandoned cloud resources. Low-effort, high-reward attack requiring only basic cloud knowledge.

## Defensive takeaways
- Implement DNS audit procedures to identify and remove dangling DNS records regularly
- Use DNS validation checks before deploying CNAME records pointing to cloud resources
- Maintain comprehensive inventory of all DNS records and their corresponding cloud resources
- Implement bucket naming conventions and access controls to prevent unauthorized registration
- Configure S3 bucket policies to reject requests from unexpected referers/origins
- Use AWS Config or similar tools to detect orphaned resources and alert on creation of resources matching known patterns
- Implement TTL reduction on CNAME records to S3 to minimize exposure window
- Use ACME DNS challenges or similar mechanisms to validate DNS-to-resource mappings

## Variant hunting
Scan other subdomains (api., admin., mail., etc.) for similar dangling CNAME records
Check for dangling DNS records pointing to CloudFront distributions, Heroku, GitHub Pages, or other third-party hosting
Search for A/AAAA records pointing to deprovisioned IP addresses or hosting providers
Enumerate DNS records across acquired domains or organizational restructuring scenarios
Look for CNAME records with long TTLs as these indicate infrequently managed records

## MITRE ATT&CK
- T1583.001
- T1583.006
- T1190
- T1566.002
- T1557.002

## Notes
This is a classic dangling DNS/subdomain takeover vulnerability in cloud environments. The severity depends on what content can be served and what trust relationship exists with the domain. Factors increasing impact: wildcard DNS records, subdomains used in CSP whitelisting, subdomains used for API communications, presence of authentication cookies sent to parent domain. The report properly demonstrated proof-of-concept without causing harm.

## Full report
<details><summary>Expand</summary>

**Description:**
The AWS bucket hosted on `www.████████` was vulnerable to a subdomain takeover. It has a DNS record pointing to an unclaimed bucket that I was able to register and serve a PoC on. 

## References
Output of `dig`:
```
;; QUESTION SECTION:
;www.███████.		IN	A

;; ANSWER SECTION:
www.████.	1833	IN	CNAME	██████████.
███. 60 IN	A	███████
█████. 60 IN	A	███
█████████. 60 IN	A	████████
█████. 60 IN	A	███

;; AUTHORITY SECTION:
█████. 1831 IN	NS	████.
███. 1831 IN	NS	█████████.
███████. 1831 IN	NS	██████.
██████. 1831 IN	NS	██████████.

;; ADDITIONAL SECTION:
█████████.	151098	IN	A	████
████.	153636	IN	A	████████
█████.	132552	IN	A	█████
███████. 6009	IN	A	███
████.	56631	IN	AAAA	███

```

## Impact

The impact for a subdomain takeover can be varied and wide: potentially steal cookies, bypass CSP and CORS policies, bypass domain whitelisting for SSRF, spy on legitimate requests sent to that domain, phising vector, etc.

## System Host(s)
www.█████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Go to https://www.███████/█████████████████ which is the PoC I have hosted.

## Suggested Mitigation/Remediation Actions
Please remove all dangling DNS records if they are not needed, or claim the buckets if they are.



</details>

---
*Analysed by Claude on 2026-05-24*
