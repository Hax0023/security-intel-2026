# Subdomain Takeover via Unclaimed Amazon S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 918946 | https://hackerone.com/reports/918946
- **Submitted:** 2020-07-08
- **Reporter:** ph0cu5
- **Program:** Department of Defense
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Cloud Misconfiguration
- **CVEs:** None
- **Category:** web-api

## Summary
A subdomain pointed to a non-existent Amazon S3 bucket, allowing an attacker to claim the bucket and take over the subdomain. The attacker demonstrated the vulnerability by creating an S3 bucket matching the subdomain name, uploading malicious content including XSS payloads, and successfully serving them from the trusted domain.

## Attack scenario
1. Attacker performs DNS enumeration and discovers subdomain pointing to S3 bucket endpoint via CNAME record
2. Attacker verifies the S3 bucket no longer exists by visiting the subdomain (receives S3 bucket does not exist error)
3. Attacker creates a new S3 bucket with the same name in the same AWS region (us-east-1)
4. Attacker configures bucket for website hosting and uploads malicious content (XSS payloads, phishing pages, etc.)
5. Attacker accesses subdomain which now serves the malicious content under the trusted domain name
6. Victims interact with the content, believing it is from the legitimate organization, leading to credential theft or XSS exploitation

## Root cause
Organization failed to maintain DNS hygiene by leaving a CNAME record pointing to a non-existent S3 bucket. The S3 bucket was deleted or abandoned without removing the corresponding DNS entry, creating a dangling DNS record that could be claimed by any AWS account holder.

## Attacker mindset
Opportunistic attacker performs systematic reconnaissance of DNS records for target domains, identifies orphaned cloud resources, and exploits the trust relationship between the domain and subdomain to host malicious content without needing to compromise the actual domain or web servers.

## Defensive takeaways
- Implement DNS hygiene checks to identify and remove dangling DNS records pointing to non-existent resources
- Maintain an inventory of all DNS records and their corresponding cloud resources
- Use DNS monitoring tools to detect changes in DNS resolution and alert on suspicious patterns
- Implement verification mechanisms in cloud platforms to prevent bucket/resource claims by unauthorized accounts
- Regularly audit and clean up unused cloud resources (S3 buckets, CloudFront distributions, etc.)
- Configure AWS S3 bucket naming policies and implement account-level restrictions if possible
- Consider using subdomain takeover detection services
- Implement CAA records and DNSSEC where applicable to add additional validation layers

## Variant hunting
Search for other dangling DNS records pointing to S3 buckets, CloudFront distributions, Azure Blobs, or Heroku apps
Identify subdomains with CNAME records pointing to defunct third-party services
Look for DNS records with long TTLs that may have been forgotten
Check for wildcard DNS entries that might cover unclaimed subdomains
Investigate expired SSL certificates that may indicate abandoned subdomains
Scan for GitHub Pages takeovers (CNAME pointing to username.github.io)
Look for Heroku, Netlify, or other PaaS platform takeovers

## MITRE ATT&CK
- T1190
- T1195
- T1583.003
- T1589.001

## Notes
The report was submitted to DoD indicating the subdomain was related to DoD infrastructure. The researcher followed responsible disclosure by offering to remove the test bucket immediately upon remediation. DNS resolution clearly showed CNAME chain pointing to S3 website endpoint. This is a critical vulnerability class affecting many organizations due to poor DNS maintenance practices.

## Full report
<details><summary>Expand</summary>

**Summary:**
An unclaimed Amazon S3 bucket on █████████ gives an attacker the possibility to gain full control over this subdomain.

**Description:**
`███████` pointed to an S3 bucket that did no longer exists. The bucket points to an Amazon S3 website bucket in the US East region. I claimed this bucket and successfully took over this subdomain. 

Note:
I am reporting this issue to DoD since: "████████ ██████" The ████████ is linked to ███, so I believe this belongs here. I discovered this domain initially from the DoD websites list. Please excuse if this is a misconception. 

## Impact
This is extremely vulnerable to attacks as a malicious user could create any web page with any content and host it on the ██████████ domain. This would allow them to post malicious content which would be mistaken for a valid site. They could:
 * XSS
 * Phishing
 * Bypass domain security 
 * Steal sensitive user data, cookies, etc. 

## Step-by-step Reproduction Instructions
`dig ███` results in: 

```
; <<>> DiG 9.11.3-1ubuntu1.12-Ubuntu <<>> ███
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 53839
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;███████.    IN  A

;; ANSWER SECTION:
██████████. 1022 IN CNAME   ████-website-us-east-1.amazonaws.com.
██████████-website-us-east-1.amazonaws.com. 1022 IN CNAME s3-website-us-east-1.amazonaws.com.
s3-website-us-east-1.amazonaws.com. 2542 IN A   █████

;; Query time: 304 msec
;; SERVER: 10.68.0.1#53(10.68.0.1)
;; WHEN: Wed Jul 08 22:01:20 KST 2020
;; MSG SIZE  rcvd: 154
```

1. █████████ points to an Amazon S3 bucket in the S3 US East 1 region. Visiting http://███████ revealed that the bucket did not exist (refer to `before.png`). 
2. I created an S3 bucket with the name `████████` on my S3 account in the US East 1 region and uploaded an `index.html` and  an XSS POC (`xss_poc_998877665544332211.html`).
3. Visiting http://███ shows the successful subdomain takeover. View the page source to see the following comment: ` <!-- Demonstrated subdomain takeover by chron0x -->`
4. Visiting http://████████/xss_poc_998877665544332211.html you can see the simple XSS payload in action. 

## Suggested Mitigation/Remediation Actions
Remove the █████ DNS entry and I will remove the bucket from my Amazon account as soon as this issue is resolved. If you want to reclaim the domain instead, please let me know in the comments and I free the bucket before.

## Impact

High. An attacker can use the domain for various malicious activities ranging from XSS, over phishing to cookie stealing, etc. All of this while using a trusted domain name (██████).

</details>

---
*Analysed by Claude on 2026-05-24*
