# Subdomain Takeover via Unclaimed Amazon S3 Bucket (a2.bime.io)

## Metadata
- **Source:** HackerOne
- **Report:** 121461 | https://hackerone.com/reports/121461
- **Submitted:** 2016-03-08
- **Reporter:** michiel
- **Program:** BIME (Zendesk)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Unrelaimed Cloud Resource
- **CVEs:** None
- **Category:** web-api

## Summary
The subdomain a2.bime.io contained a DNS CNAME record pointing to an unclaimed Amazon S3 bucket (bimeio.s3-website-us-east-1.amazonaws.com) that no longer existed. An attacker was able to create an S3 bucket with the same name and host malicious content, including a fake login page to harvest user credentials. This classic subdomain takeover vulnerability exploited the gap between DNS configuration and actual cloud resource ownership.

## Attack scenario
1. Attacker enumerates DNS records for bime.io subdomains and identifies a2.bime.io pointing to an S3 bucket endpoint
2. Attacker verifies the S3 bucket no longer exists by visiting the URL and receiving a 404 error
3. Attacker creates a new S3 bucket with the same name (bimeio) in the same AWS region (us-east-1)
4. Attacker enables static website hosting on the bucket and uploads a cloned BIME login page as index.html
5. Attacker makes the bucket publicly accessible and the fake login page becomes live at http://a2.bime.io
6. Attacker distributes the link to BIME users via social engineering, credential harvesting occurs when users authenticate on the fake login page

## Root cause
BIME failed to clean up DNS records pointing to S3 buckets that were deleted or abandoned. The organization did not implement a process to verify that all DNS CNAME entries for S3 endpoints correspond to actual owned and controlled S3 buckets. Additionally, no monitoring was in place to detect when S3 buckets referenced in DNS became unclaimed or accessible to external parties.

## Attacker mindset
The attacker demonstrated methodical reconnaissance by systematically probing DNS entries for cloud resource misconfigurations. They recognized the high-value target of a subdomain under a trusted domain (bime.io) and the effectiveness of phishing via a legitimate-looking subdomain. The attacker understood AWS S3 bucket naming conventions and regional endpoints, allowing them to quickly claim the abandoned resource and deploy a credential harvesting page.

## Defensive takeaways
- Implement DNS hygiene practices: regularly audit all DNS records and remove entries pointing to non-existent or decommissioned resources
- Establish cloud resource inventory management: maintain a canonical list of all S3 buckets, CloudFront distributions, and other cloud resources in use
- Implement automated monitoring: use tools to periodically verify that all DNS CNAME entries point to valid, owned resources
- Use S3 bucket naming strategies: consider using unique prefixes or GUIDs that are difficult for attackers to guess when creating buckets
- Enable S3 block public access: configure default settings to prevent accidental public exposure of buckets
- Implement DNSSEC: provide cryptographic validation of DNS records to prevent DNS hijacking
- Conduct regular security assessments: include subdomain takeover scanning in vulnerability assessment programs
- Set up alerts: monitor for creation of S3 buckets matching your organization's naming patterns to detect takeover attempts

## Variant hunting
Similar vulnerabilities likely exist across other subdomains if DNS cleanup was not comprehensive. Search for other *.bime.io subdomains pointing to decommissioned resources (Azure Storage, Google Cloud Storage, GitHub Pages, Heroku, etc.). Examine other organizations using Amazon S3 for potential unclaimed buckets. Look for CNAME records pointing to other cloud CDNs or hosting providers that may have been abandoned.

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1040

## Notes
This is a classic and well-documented subdomain takeover vulnerability class. The researcher responsibly disclosed the issue and offered to release the bucket after initial testing. The attack is particularly effective because users trust subdomains under legitimate domains. The vulnerability required minimal technical skill to exploit once the misconfiguration was discovered. This incident highlights the importance of cloud resource deprovisioning procedures and DNS record cleanup during infrastructure changes or service deprecation.

## Full report
<details><summary>Expand</summary>

I noticed BIME is primarily built on Amazon AWS, which spawned my interest. I started looking for DNS entries that were still pointing to S3 buckets that however no longer exist. It appears this was the case for `a2.bime.io`, which points to an Amazon S3 website bucket in the US East region. 

# Steps to Reproduce
- Resolve `a2.bime.io` and see what is behind it:

```
michiel@msp ~ $ dig A a2.bime.io @8.8.8.8                                                                                                [2.1.8]

; <<>> DiG 9.9.5-11ubuntu1.2-Ubuntu <<>> A a2.bime.io @8.8.8.8
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 730
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;a2.bime.io.			IN	A

;; ANSWER SECTION:
a2.bime.io.		59	IN	CNAME	bimeio.s3-website-us-east-1.amazonaws.com.
bimeio.s3-website-us-east-1.amazonaws.com. 59 IN CNAME s3-website-us-east-1.amazonaws.com.
s3-website-us-east-1.amazonaws.com. 4 IN A	54.231.11.130

;; Query time: 210 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Tue Mar 08 15:33:45 EST 2016
;; MSG SIZE  rcvd: 124
```

- It points to an Amazon S3 bucket in the S3 US East 1 region. Visiting http://a2.bime.io revealed that the bucket did not exist (a 404 error was shown). Obviously this is not the case any longer, as the bucket is now claimed and serving a fake login page (see "Attack Scenario").
- I created a bucket with name "a2.bime.io" on my S3 account in the US East 1 region.
- I enabled static website hosting and pointed "index.html" as the index document.
- Then I uploaded `index.html` (attached to this report) and clicked "Make public" to make sure it can be served. 
- Now go to http://a2.bime.io and you will see a BIME login page. Click the Sign In button and you will notice it is a fake login form. 

# Attack Scenario 
I created a false login page and posted it on http://a2.bime.io. The login page looks just like the normal BIME sign in page, but it is 100% controlled by the attacker. The attacker could harvest logins by convincing their victims to visit the fake login page. Since it is a subdomain of `bime.io`, which BIME customers will recognize, it is likely they will fall for the attack. 

I have attached the fake login page here as `index.html`.

# Remediation
Remove the `a2.bime.io` DNS entry so it no longer points to an S3 bucket Zendesk Ops doesn't control. If you need me to release `a2.bime.io` as an S3 bucket, let me know and I'll delete the bucket.



</details>

---
*Analysed by Claude on 2026-05-24*
