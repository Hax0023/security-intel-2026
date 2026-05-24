# S3 Bucket Misconfiguration - Public Upload/Delete Access on studio.redditinc.com

## Metadata
- **Source:** HackerOne
- **Report:** 1276733 | https://hackerone.com/reports/1276733
- **Submitted:** 2021-07-24
- **Reporter:** dinesh07
- **Program:** Reddit (HackerOne)
- **Bounty:** Undisclosed
- **Severity:** Critical
- **Vuln:** Misconfigured Cloud Storage, Insufficient Access Controls, Insecure S3 Bucket Permissions, Unrestricted File Upload, Unrestricted File Deletion, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
An S3 bucket (s3-r-w.ap-east-1.amazonaws.com) hosting content for studio.redditinc.com was configured with overly permissive bucket policies allowing unauthenticated or insufficiently authenticated users to list, upload, and delete files. The bucket naming convention exposed its read-write capabilities, and DNS enumeration revealed the bucket alias, enabling straightforward exploitation.

## Attack scenario
1. Attacker performs DNS reconnaissance on studio.redditinc.com using 'dig' to discover the CloudFront distribution endpoint (d326d3e45wj426.cloudfront.net)
2. Attacker performs DNS lookups on the CloudFront distribution domain to enumerate the underlying S3 bucket name (s3-r-w.ap-east-1.amazonaws.com)
3. Attacker authenticates to AWS CLI (either with their own credentials or finds credentials that have overly broad permissions) and attempts to list bucket contents using 's3 ls'
4. Attacker successfully lists all files in the bucket, achieving information disclosure of potentially sensitive studio content
5. Attacker uploads malicious files (HTML, executables, media) to the bucket, potentially serving them via the CDN to modify content served to legitimate users
6. Attacker deletes critical files or the entire bucket to disrupt service or perform a ransomware-style extortion attack

## Root cause
The S3 bucket was configured with bucket policies or ACLs that granted overly permissive permissions to authenticated AWS principals (possibly '*' principal or overly broad role/policy). The bucket naming convention 's3-r-w' advertised read-write capabilities. Lack of proper access controls, resource-based policies, and absence of bucket encryption/versioning protections allowed unauthorized file operations.

## Attacker mindset
An attacker with basic cloud infrastructure knowledge can perform reconnaissance via DNS enumeration to identify S3 buckets. Once the bucket is discovered, they exploit misconfigured permissions to enumerate, modify, and destroy content. The attacker may be motivated by data exfiltration, content manipulation, service disruption, extortion, or lateral movement within the AWS environment.

## Defensive takeaways
- Implement strict S3 bucket policies with principle of least privilege - deny all by default, explicitly allow only necessary operations to specific principals
- Use bucket names that do not expose capabilities (avoid 's3-r-w', 's3-public', etc.)
- Enable S3 Block Public Access (all four settings) to prevent accidental public exposure
- Require bucket versioning and enable MFA delete to prevent unauthorized file deletion
- Implement S3 bucket encryption at rest (SSE-S3 or SSE-KMS) and enforce encryption in transit
- Use CloudFront Origin Access Identity (OAI) or Origin Access Control (OAC) to restrict direct S3 access
- Enable S3 access logging and CloudTrail logging for audit trails of bucket operations
- Regularly audit bucket policies and IAM permissions using AWS Config and Access Analyzer
- Implement resource-based policies that explicitly deny dangerous actions (s3:DeleteBucket, s3:DeleteObject) to untrusted principals
- Use temporary credentials with short TTLs and scope permissions by resource ARN
- Monitor DNS records for CNAME/alias changes that expose bucket infrastructure
- Conduct periodic security assessments and bucket enumeration scanning

## Variant hunting
Search for other S3 buckets with similar naming patterns (s3-rw-*, *-r-w-*, *-read-write-*) across all AWS regions
Enumerate CloudFront distributions and trace back to underlying S3 origins to identify other potentially misconfigured buckets
Check for S3 buckets in ap-east-1 region belonging to Reddit that may have similar permission issues
Scan for buckets with public ACLs or bucket policies allowing 's3:*' actions to authenticated or unauthenticated principals
Look for buckets without versioning/MFA delete protection that allow destructive operations
Search for buckets lacking encryption or access logging configurations
Test other Reddit subdomains (*.redditinc.com, *.reddit.com) for similar CloudFront/S3 misconfigurations

## MITRE ATT&CK
- T1190
- T1526
- T1530
- T1537
- T1040
- T1020
- T1561

## Notes
The reporter demonstrated responsible disclosure by uploading test files and reporting findings rather than deleting or exfiltrating sensitive data. The bucket's descriptive name 's3-r-w' (read-write) indicates intentional exposure or misconfiguration. The ability to delete the entire bucket ('rb') poses extreme risk for denial-of-service and potential account takeover via bucket reclamation. This vulnerability likely affected production studio assets served globally via CloudFront. The exploitation required minimal technical skill beyond DNS enumeration and AWS CLI knowledge, making it a high-impact issue.

## Full report
<details><summary>Expand</summary>

Greetings team,

Found a s3 bucket that belongs to studio.redditinc.com and properly not configured.

bucket name:- s3-r-w.ap-east-1.amazonaws.com
Bucket Source:-studio.redditinc.com

Steps To reproduce:-

In terminal , " dig studio.redditinc.com "
will get the CNAME as d326d3e45wj426.cloudfront.net

Then, "host -t ns d326d3e45wj426.s3.ap-east-1.amazonaws.com"
will get 
d326d3e45wj426.s3.ap-east-1.amazonaws.com is an alias for s3-r-w.ap-east-1.amazonaws.com.
s3-r-w.ap-east-1.amazonaws.com name server ns-1885.awsdns-43.co.uk.
s3-r-w.ap-east-1.amazonaws.com name server ns-192.awsdns-24.com.
s3-r-w.ap-east-1.amazonaws.com name server ns-908.awsdns-49.net.
s3-r-w.ap-east-1.amazonaws.com name server ns-1338.awsdns-39.org.

So, I came to know that d326d3e45wj426.s3.ap-east-1.amazonaws.com is an alias for "s3-r-w.ap-east-1.amazonaws.com" 

Got the bucket name. Now I tried to upload by using command in authenticated  AWS CLI Machine
" aws s3 cp <path/filename> s3://s3-r-w

Uploaded was successful! Two files( dinesh.jpg and dinesh.html )

" aws s3 ls s3://<The_bucket_name> "
By this command I can list out  all the files in the bucket

I don't know is it possible or not. Attacker can delete the bucket using this command:-
" aws s3 rb s3://<The_bucket_name> "
and claim the bucket again to takeover the bucket.

Thanks team

## Impact

I can see every files present in the bucket .
I can upload any files . 
I can delete any file .

</details>

---
*Analysed by Claude on 2026-05-24*
