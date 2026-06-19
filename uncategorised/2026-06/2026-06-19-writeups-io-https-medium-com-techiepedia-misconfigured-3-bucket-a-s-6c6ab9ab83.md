# Misconfigured S3 Bucket - Semi-Open Environment (RedBull)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** RedBull Bug Bounty Program
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Cloud Storage Misconfiguration, Improper Access Control, Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://medium.com/techiepedia/misconfigured-3-bucket-a-semi-opened-environment-9cfb9dee782d

## Summary
A misconfigured AWS S3 bucket associated with RedBull was discovered through systematic subdomain and acquisition enumeration, revealing sensitive data exposure. The bucket was accessible via AWS CLI despite returning 403 errors in browser access, indicating improper bucket policy and access control configuration.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of target domain (redbull.com) using automated scripts
2. Attacker identifies acquisitions/subsidiaries using reverse WHOIS lookup tools and extends enumeration scope
3. Attacker uses httpx to probe for alive hosts and filters for S3-related infrastructure
4. Attacker derives potential S3 bucket names from subdomain first and second-level domains
5. Attacker probes derived bucket names against S3 endpoints and identifies 403 responses
6. Attacker uses AWS CLI to enumerate bucket contents, bypassing browser-based access restrictions

## Root cause
S3 bucket policy was misconfigured to block public browser access (returning 403) but failed to properly restrict AWS API access, allowing enumeration and potential data access via AWS CLI. Lack of proper bucket ACLs and bucket policies that would deny all unauthenticated API requests.

## Attacker mindset
Persistence and methodological thinking - when initial approaches failed (200/404 responses), the attacker pivoted to extract first/second-level domains and tested those. Rather than accepting browser 403 errors as complete denial, the attacker recognized that S3 buckets can be accessed via AWS CLI without credentials and continued investigation.

## Defensive takeaways
- Implement strict S3 bucket policies that explicitly deny all unauthenticated access, not just browser access
- Block PutObject and DeleteObject permissions for unauthenticated principals
- Use S3 Block Public Access settings at both account and bucket levels
- Monitor and audit S3 bucket enumeration attempts via CloudTrail logging
- Implement proper CORS and bucket policies that align with actual access requirements
- Avoid predictable bucket naming patterns based on domain names or acquisitions
- Regularly audit bucket policies and permissions, especially for sensitive data buckets
- Use bucket versioning and MFA delete for critical data protection
- Implement IP-based restrictions where applicable to limit access to known networks

## Variant hunting
['Check for S3 buckets named after company acquisitions not yet publicly integrated', 'Look for buckets with predictable naming: [company]-[service], [acquisition]-backup, [subsidiary]-files', 'Enumerate buckets using variations of discovered domain names (hyphens, underscores, numbers)', 'Test bucket access with different AWS credential contexts (public, cross-account, role-based)', 'Probe for bucket ACLs that allow authenticated AWS users from other accounts to ListBucket', 'Check for buckets with overly permissive bucket policies allowing s3:GetObject to Principal:*', 'Look for historical bucket versions or snapshots with relaxed permissions', 'Test S3 bucket endpoints with HEAD requests to bypass full enumeration detection']

## MITRE ATT&CK
- T1526 - Cloud Service Discovery (S3 bucket enumeration)
- T1526.001 - Cloud Service Discovery (domain/subdomain enumeration)
- T1592 - Gather Victim Identity Information (WHOIS reverse lookup)
- T4013 - Unsecured Credentials (AWS API access without auth requirements)
- T1580 - Cloud Infrastructure Discovery (identifying cloud storage)
- T2110 - Gather Victim Organization Information (acquisition discovery)

## Notes
The writeup is incomplete (content cuts off mid-article) and does not reveal the final impact or sensitive data discovered. The methodology demonstrates excellent reconnaissance tradecraft including subdomain enumeration, acquisition research, and tool chaining. The attacker correctly identified that browser-level access denial (403) does not equate to API-level denial. This represents a common misconfiguration where organizations apply browser-friendly redirects or access denied pages without properly implementing underlying API authentication controls.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
