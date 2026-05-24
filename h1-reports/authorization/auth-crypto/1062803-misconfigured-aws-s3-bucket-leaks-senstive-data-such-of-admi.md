# Misconfigured AWS S3 Bucket Exposing Sensitive DoD Data

## Metadata
- **Source:** HackerOne
- **Report:** 1062803 | https://hackerone.com/reports/1062803
- **Submitted:** 2020-12-20
- **Reporter:** i_am_no__one
- **Program:** Department of Defense (DoD)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Improper Access Control, Information Disclosure, Cloud Misconfiguration, Insecure Direct Object References
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An AWS S3 bucket belonging to the DoD was publicly accessible without authentication, allowing unauthenticated users to list and download sensitive files including production data, admin documents, and configuration files from directories labeled as prod, admin, beta, and localhost. The bucket's misconfiguration exposed directories and files that should have been restricted to authorized personnel only.

## Attack scenario
1. Attacker discovers the S3 bucket URL through reconnaissance (DNS enumeration, GitHub leaks, etc.)
2. Attacker directly accesses the bucket URL in a browser and observes directory listing enabled
3. Attacker identifies sensitive directory names (prod, admin, beta, localhost) indicating production/sensitive environments
4. Attacker uses AWS CLI commands to recursively enumerate all directories and files within the bucket
5. Attacker downloads sensitive files containing production data, credentials, configuration details, and operational documents
6. Attacker gains intelligence on DoD systems, infrastructure, and potentially exploits additional vulnerabilities discovered in downloaded files

## Root cause
S3 bucket policy or ACL was configured to allow public read access (s3:ListBucket and s3:GetObject permissions for anonymous principals) without proper access controls, combined with unrestricted directory listing enabled on the bucket.

## Attacker mindset
Opportunistic reconnaissance targeting cloud storage misconfigurations; attackers assume that sensitive data leaks are common and worth scanning for; once found, comprehensive enumeration and exfiltration of all accessible data for intelligence gathering or sale.

## Defensive takeaways
- Implement principle of least privilege: disable public access for all S3 buckets by default using Block Public Access settings
- Enforce bucket policies that explicitly deny s3:* actions to unauthenticated principals (Principal: '*')
- Disable bucket listing (s3:ListBucket) for public or unnecessary principals
- Enable versioning and MFA Delete on sensitive buckets to prevent data destruction
- Use S3 encryption at rest (SSE-S3 or SSE-KMS) and enforce encryption in transit (SSL/TLS)
- Enable S3 access logging and CloudTrail logging to detect unauthorized access attempts
- Implement automated scanning for S3 misconfigurations using tools like AWS Config, Prowler, or Scout Suite
- Regularly audit S3 bucket policies, ACLs, and permissions using AWS IAM Access Analyzer
- Apply organizational policies to prevent public access at the account level
- Never expose sensitive environment identifiers (prod, admin, beta, localhost) in directory names; use obscured naming
- Conduct periodic security assessments specifically targeting cloud storage configurations
- Implement network segmentation and VPC endpoints for sensitive S3 buckets

## Variant hunting
Check other DoD-related AWS accounts for similarly misconfigured buckets
Scan for CloudFront distributions pointing to private S3 buckets with misconfigured origin access
Hunt for S3 buckets with public ACLs combined with disabled Block Public Access settings
Identify buckets containing environment-specific keywords (prod, admin, test, staging, beta, localhost, dev) that are publicly accessible
Search for S3 buckets with overly permissive bucket policies using wildcards in Principal or Action
Enumerate subdomain patterns (*.s3.amazonaws.com) for other potentially exposed buckets
Audit buckets with public ListBucket permissions but private GetObject to identify partial exposure scenarios

## MITRE ATT&CK
- T1526 - Reconnaissance: Cloud Storage Object Enumeration
- T1619 - Gather Victim Identity Information: Credentials
- T1526 - Reconnaissance
- T1040 - Network Sniffing
- T1078 - Valid Accounts: Cloud Accounts (if credentials found in files)
- T1530 - Data from Cloud Storage

## Notes
This is a classic cloud misconfiguration vulnerability common in organizations transitioning to cloud infrastructure. The exposure of environment-specific directory names (prod, admin, localhost, beta) suggests this bucket may have been created during development and migrated to production without properly securing access controls. The sensitivity of DoD data makes this a critical finding with potential national security implications. The fact that AWS CLI enumeration was possible indicates both ListBucket and GetObject permissions were overly permissive. This type of vulnerability is frequently discovered through automated scanning of known cloud storage patterns and is often exploited in the wild for data exfiltration.

## Full report
<details><summary>Expand</summary>

**Description:**
It has been observed that the amazon s3 bucket which i believe belongs to DoD as it contains data related to Dod prod,admin,localhost documents and all is misconfigured as a result any unauthenticated users can access it without any restrictions

## Step-by-step Reproduction Instructions

1.Access following URL
https://██████.s3.amazonaws.com/
so the bucket name is "█████████"
2.And we can see that we are successfully able to see all the contents present on it.Which confirms s3 bucket is misconfigured.
3.And to access contents of different directories we can use following cmd in terminal

aws s3 ls s3://███/
aws s3 ls s3://████/██████/
aws s3 ls s3://███████/███████████████/
aws s3 ls s3://██████████/███████/
aws s3 ls s3://██████████/████/

and in a similar way ,we can access content of root or any directory which contains sensitive manuals , document and media files 

## Suggested Mitigation/Remediation Actions
configure s3 bucket properly to disable listing of such a sensitive files

## Impact

Any unauthenticated user can access and download sensitive files present on DoD s3 storage.

</details>

---
*Analysed by Claude on 2026-05-24*
