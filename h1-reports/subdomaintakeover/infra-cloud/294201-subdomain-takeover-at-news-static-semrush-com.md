# Subdomain Takeover at news-static.semrush.com via Unclaimed S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 294201 | https://hackerone.com/reports/294201
- **Submitted:** 2017-12-01
- **Reporter:** 0ways
- **Program:** Semrush
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Cloud Resource Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The subdomain news-static.semrush.com was pointed via CNAME to an unclaimed Amazon S3 bucket, allowing attackers to create the bucket and serve arbitrary content from the subdomain. This enables phishing, malware distribution, and cross-origin XSS attacks against Semrush users.

## Attack scenario
1. Attacker discovers news-static.semrush.com resolves to s3.amazonaws.com via CNAME chain
2. Attacker creates AWS account and registers S3 bucket named 'news-static.semrush.com'
3. Attacker uploads malicious content (phishing page, malware, XSS payload) to the S3 bucket
4. Legitimate Semrush users visit or are redirected to http://news-static.semrush.com/malicious-content
5. Browser trusts content as it comes from Semrush domain, bypassing same-origin policy for *.semrush.com
6. Attacker steals credentials, deploys malware, or executes JavaScript in Semrush context

## Root cause
Semrush created DNS CNAME record pointing to S3 bucket but failed to either (1) create the S3 bucket to claim ownership or (2) remove the DNS record when the bucket was no longer in use. No TTL/timeout mechanism existed to reclaim dangling resources.

## Attacker mindset
Opportunistic recon identifying low-hanging fruit through DNS enumeration. Attacker recognized that unclaimed cloud resources are common misconfigurations and systematically tested S3 bucket availability. The fact the researcher proactively claimed the bucket demonstrates awareness that such vulnerabilities are frequently exploited before responsible disclosure.

## Defensive takeaways
- Implement inventory and monitoring of all DNS records, especially CNAME entries pointing to cloud resources
- Automatically validate that cloud resources (S3 buckets, CloudFront distributions, etc.) referenced in DNS exist and are owned by the organization
- Use CloudFormation or Infrastructure-as-Code to manage DNS alongside cloud resources to prevent orphaned records
- Implement alerting for DNS changes and periodic audits of CNAME records
- When decommissioning cloud resources, immediately remove associated DNS records
- Use DNS CAA records and S3 bucket naming policies to prevent resource hijacking
- Apply principle of least privilege: restrict S3 bucket creation permissions and implement organizational naming conventions

## Variant hunting
Scan other Semrush subdomains for dangling CNAME records pointing to AWS, GCP, Azure resources
Check for CNAME records pointing to CloudFront distributions, Route53, API Gateway endpoints that may be unclaimed
Test vanity subdomains and third-party service integrations (CDNs, analytics, email providers) for takeover
Look for CNAME records with typos or pointing to deprecated service endpoints
Enumerate acquired company subdomains that may reference deleted infrastructure
Test for dangling MX, TXT records that could enable email spoofing or domain verification bypasses

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains
- T1589.001 - Gather Victim Identity Information: Credentials
- T1598.003 - Phishing for Information: Spearphishing Link
- T1195.001 - Supply Chain Compromise: Compromise Software Dependencies

## Notes
This is a classic subdomain takeover vulnerability with straightforward exploitability (CVSS ~7.5). The researcher's responsible disclosure included securing the bucket to prevent exploitation before vendor fix, which is commendable but indicates the vulnerability was easily exploitable. The cross-origin implications are particularly severe as content served from *.semrush.com subdomains may bypass CORS restrictions for semrush.com resources. The researcher reference to 'claiming the bucket' before disclosure suggests AWS S3 bucket naming uses first-come-first-served model without ownership verification per domain WHOIS.

## Full report
<details><summary>Expand</summary>

**Summary:** The subdomain news-static.semrush.com can be taken over by attackers and abuse it for further attacks (Phishing, XSS Cross origin, malware, etc..).

**Description:** The subdomain news-static.semrush.com was pointed using CNAME to Amazon S3, but no bucket with that name was registered. This meant that anyone could sign up for Amazon S3, claim the bucket as their own and then serve content on news-static.semrush.com

**Browsers Verified In:**
  * Google Chrome v62.0.3202.94 
  * FireFox ESR v52.5.0

**Steps To Reproduce:** 
  1. Open AWS account
  2. Create s3 bucket and claim the subdomain news-static.semrush.com
  3. upload poc.html file to the bucket

**Supporting Material/References:**

```
$ dig A news-static.semrush.com @8.8.8.8

; <<>> DiG 9.8.3-P1 <<>> A news-static.semrush.com @8.8.8.8
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 35678
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;news-static.semrush.com.	IN	A

;; ANSWER SECTION:
news-static.semrush.com. 59	IN	CNAME	s3.amazonaws.com.
s3.amazonaws.com.	3459	IN	CNAME	s3-1.amazonaws.com.
s3-1.amazonaws.com.	4	IN	A	52.216.21.165
```

**POC**
http://news-static.semrush.com/POC_2313521212.html

This means that nobody else can claim the bucket and add content.

**Mitigation/Fix** 
I have claimed the bucket on my account so no one can claimed it before I release it.
Remove the news-static.semrush.com DNS entry. Alternatively, if you wish to use news-static.semrush.com with S3, tell me in a comment and I will remove the bucket from my Amazon account.

## Impact

The attacker will own the subdomain and can do whatever he want with it, such as Phishing, XSS that can affect all *.semrush.com to bypass cross origin policy and upload malwares. etc..

</details>

---
*Analysed by Claude on 2026-05-24*
