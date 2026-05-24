# Unauthorized Access to GitLab's Google Cloud Storage Bucket - Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 1669176 | https://hackerone.com/reports/1669176
- **Submitted:** 2022-08-14
- **Reporter:** hacker1_agent
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Improper Access Control, Information Disclosure, Cloud Storage Misconfiguration, Sensitive Data Exposure
- **CVEs:** CVE-2022-2185
- **Category:** uncategorised

## Summary
The about.gitlab.com Google Cloud Storage bucket was publicly accessible without authentication, exposing sensitive information including undisclosed security vulnerability details from HackerOne reports, internal staff directories, security release documentation, and tokens. Attackers could enumerate bucket contents, access XML files containing critical CVE information and researcher identities, and retrieve configuration files with phone numbers and API tokens.

## Attack scenario
1. Attacker discovers the GCS bucket is publicly accessible via gsutil or direct HTTPS access
2. Attacker lists bucket contents using 'gsutil ls gs://about.gitlab.com/' to enumerate all available files
3. Attacker accesses all-releases.xml and security-releases.xml files containing undisclosed HackerOne vulnerability reports with CVE details and researcher credits
4. Attacker retrieves mindmap.txt file and discovers links to internal Google Docs with editing permissions, potentially modifying internal documentation
5. Attacker accesses roulette.json to extract full names of all GitLab staff members for targeted social engineering
6. Attacker retrieves JavaScript files and JSON configuration files (db-0881eaf3.json) containing phone numbers, API tokens, and 1000+ internal URLs for further exploitation

## Root cause
Google Cloud Storage bucket permissions were misconfigured to allow public read access (allUsers or allAuthenticatedUsers) instead of restricting access to authorized GitLab systems only. No access control lists (ACLs) or bucket policies were properly enforced to limit exposure of the about.gitlab.com bucket.

## Attacker mindset
An attacker with reconnaissance objectives would systematically enumerate cloud storage buckets associated with a target organization. Upon discovering public access, they would comprehensively extract all available data including security disclosures, staff information, and credentials for use in multi-stage attacks including social engineering, insider threat development, and exploitation of known vulnerabilities.

## Defensive takeaways
- Implement principle of least privilege on all cloud storage buckets - default to private with explicit whitelist of authorized users
- Regularly audit GCS bucket permissions using 'gsutil iam ch' and enforce uniform bucket-level access control over object-level ACLs
- Never store sensitive information (tokens, API keys, phone numbers) in publicly accessible storage; use secret management services instead
- Implement bucket versioning and retention policies to prevent deletion of audit logs and ensure compliance tracking
- Use GCS signed URLs with time-limited access for legitimate file sharing instead of making entire buckets public
- Separate public content (about.gitlab.com website) into a dedicated bucket with restricted permissions, keeping release notes and security data in private buckets
- Implement bucket encryption and regularly scan buckets for sensitive data patterns using Cloud DLP API
- Monitor all GCS access logs and set up alerts for unauthorized listing or access attempts
- Implement security headers (X-Robots-Tag: noindex) on sensitive XML/JSON files to prevent indexing
- Conduct regular cloud security audits and penetration testing of cloud infrastructure

## Variant hunting
Scan other GitLab-owned GCS buckets (cdn.gitlab.com, downloads.gitlab.com, etc.) for similar misconfigurations
Check for publicly accessible AWS S3 buckets with similar naming patterns using tools like S3Scanner or CloudMapper
Enumerate Azure Blob Storage containers owned by GitLab for exposed sensitive data
Search for other exposed Google Docs links in publicly accessible JSON/XML files across GitLab infrastructure
Investigate whether other company internal tools (Slack, Jira, Confluence) have linked to the exposed Google Docs
Check Git repositories for hardcoded GCS URLs or credential references that may access other sensitive buckets

## MITRE ATT&CK
- T1526 - Cloud Service Discovery (enumeration of GCS bucket)
- T1619 - Cloud Storage Object Discovery (listing bucket contents)
- T1657 - Financial Information Discovery (accessing configuration files)
- T1526.001 - Cloud Infrastructure Discovery (identifying exposed storage)
- T1040 - Traffic Interception (accessing unencrypted or publicly available data)
- T1087.004 - Gather Victim Identity Information - Credentials (extracting tokens and API keys)
- T1589.001 - Gather Victim Identity Information - Credentials (phone numbers and staff names)

## Notes
This is a textbook cloud misconfiguration vulnerability with severe business impact. The exposure of undisclosed HackerOne reports represents a critical breach of responsible disclosure practices and could undermine the security research community's trust in GitLab. The presence of editable Google Docs with potential for unauthorized modification adds a second-order impact. The report demonstrates excellent reconnaissance methodology and clear documentation of the exploitation chain. This vulnerability likely affected the production environment at about.gitlab.com for an unknown duration before remediation.

## Full report
<details><summary>Expand</summary>

Hello Gents,
I would like to report an issue where attackers are able to:
1. List `about.gitlab.com` GS bucket.
2. Access all resales through https://about.gitlab.com/all-releases.xml & https://about.gitlab.com/security-releases.xml, which contains undisclosed HackerOne reports.
> For Example:
```
<p>This vulnerability has been discovered internally by the GitLab team.</p> <h2 id="pipeline-subscriptions-trigger-new-pipelines-with-the-wrong-author">Pipeline subscriptions trigger new pipelines with the wrong author</h2> <!-- https://gitlab.com/gitlab-org/security/gitlab/-/issues/642 -->
 <p>A critical issue has been discovered in GitLab affecting all versions starting from 14.0 prior to 14.10.5, 15.0 prior to 15.0.4, and 15.1 prior to 15.1.1 where an authenticated user authorized to import projects could import a maliciously crafted project leading to remote code execution. This is a critical severity issue (<code>CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H</code>, 9.9). It is now mitigated in the latest release and is assigned <a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2185">CVE-2022-2185</a>.</p> <p>Thanks <a href="https://hackerone.com/vakzz">vakzz</a>
```
3. Access https://about.gitlab.com/mindmap.txt which contains this internal Google Documents link:
https://docs.google.com/document/d/e/2PACX-1vSNzTLkZMqILVYoey4dnSLYdk0Jmsd8pFu7ygLJ57RQ1c8XlZDbzaG45rQMOrDbHRWCQa5LN7DZid8s/pub
> I didn't dig in so much , but I was able to edit a document like this one: 
> [GitLab_MessageGuide](https://docs.google.com/document/d/14APaSKwYpwutujISnkbLOnjdQ5RG-hIQXulasZT7h6s/edit)
4. list All Gitlab Staff full names through https://about.gitlab.com/roulette.json
5. All JavaScript files using `gsutil ls gs://about.gitlab.com/javascripts/`, there are many other files too.
> Also please take a look at this json file: https://storage.googleapis.com/about.gitlab.com/_nuxt/content/db-0881eaf3.json, it contains phone numbers, tokens, and more than 1000 URLs could be useful for attackers.

### Steps to reproduce:
+ Please visit https://storage.googleapis.com/about.gitlab.com, or you can install [gsutil](https://cloud.google.com/storage/docs/gsutil_install). then list the bucket using the following command: 
+ `gsutil ls gs://about.gitlab.com/`.

### Proof of concept
+ {F1867120}
+ {F1867121}
+ {F1867122}
+ {F1867125}

## Impact

Unauthorized access & Information disclosure.

Thanks and have a nice day!

</details>

---
*Analysed by Claude on 2026-05-24*
