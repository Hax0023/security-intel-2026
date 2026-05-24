# PII Leak of Approximately 1000 DoD Personnel via Publicly Accessible PDF

## Metadata
- **Source:** HackerOne
- **Report:** 1050196 | https://hackerone.com/reports/1050196
- **Submitted:** 2020-12-03
- **Reporter:** nagli
- **Program:** DoD (Department of Defense)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Information Disclosure, Improper Access Control, Sensitive Data Exposure, Directory Traversal/Path Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
A PDF file containing personally identifiable information (PII) of approximately 1000 DoD personnel was publicly accessible on the organization's website. The exposed data included personal phone numbers and private email addresses of individuals in contact with the DoD. The vulnerability allowed unauthenticated access to sensitive contact information through a direct URL.

## Attack scenario
1. Attacker discovers or is informed of a publicly accessible PDF URL on the DoD website
2. Attacker navigates to the specified URL without requiring authentication or authorization
3. PDF document is retrieved containing a list with PII of approximately 1000 personnel
4. Attacker extracts personal phone numbers and email addresses from the PDF
5. Attacker can use harvested contact information for phishing, social engineering, or targeted attacks
6. Sensitive data is potentially further distributed or sold on dark markets

## Root cause
Improper access controls on web resources combined with insecure file upload/storage practices. The organization failed to implement authentication/authorization checks on sensitive documents and did not restrict public access to PDFs containing PII. Files were likely uploaded without proper access control configuration or were placed in a publicly accessible directory without restriction.

## Attacker mindset
Opportunistic reconnaissance attacker seeking to harvest contact information for follow-on attacks. The attacker may have discovered this through automated scanning, directory enumeration, or prior knowledge of the upload location. The disclosure suggests civic responsibility, though the data could easily have been exploited for social engineering, phishing campaigns targeting DoD personnel, or sold to threat actors.

## Defensive takeaways
- Implement mandatory authentication and authorization checks on all file uploads and downloads
- Conduct regular audits of publicly accessible web resources to identify unintended data exposure
- Classify all files containing PII and apply appropriate access controls based on sensitivity level
- Use file upload restrictions to prevent PII-containing documents from reaching web-accessible directories
- Implement data loss prevention (DLP) tools to detect and prevent unauthorized exposure of sensitive information
- Establish secure file storage practices separate from public-facing web directories
- Require encryption for files containing PII, both in transit and at rest
- Implement logging and monitoring to detect unauthorized access attempts to sensitive files
- Use security headers and Content-Disposition headers to prevent accidental downloads

## Variant hunting
Search for similar patterns: (1) Other PDF or document files with direct URL access on domain; (2) Backup files (.bak, .old, .tmp) containing PII; (3) Spreadsheets or archives in public directories; (4) Cached versions in web archives (Wayback Machine); (5) Similar endpoints or URL patterns suggesting systematic upload vulnerabilities; (6) Historical git commits or version control exposures; (7) Misconfigured S3 buckets or cloud storage with similar naming patterns

## MITRE ATT&CK
- T1526 - Reconnaissance: Enumerate cloud resources
- T1589 - Reconnaissance: Gather victim identity information
- T1590 - Reconnaissance: Gather victim network information
- T1199 - Trusted Relationship
- T1566 - Phishing (secondary impact)
- T1598 - Phishing for information (secondary impact)

## Notes
This writeup lacks technical detail and appears to have significant redactions. The report quality is low with minimal reproduction steps provided. Critical concern: exposing 1000 DoD personnel contact information represents national security risk. The reporter redacted the actual URL, preventing verification. The report was filed on HackerOne but DoD vulnerabilities are typically handled through DoD-specific programs (DoDCIO, DCSA). The October 7th upload date and quick discovery suggests either lucky timing or targeted scanning. No timeline for remediation provided in the report.

## Full report
<details><summary>Expand</summary>

##Hello DoD Team,

##Summary:
PII Leakage of approx 1000 personal is being disclosed through the pdf at https://www.████████which had been uploaded at the 7th of October, this includes Personal phone number and email address.

##Description:
The list presented at the "████████" contains personal info such as phone numbers and private emails of personal in contact with the DoD.

##Step-by-step Reproduction Instructions

Navigating to https://www.█████

##Suggested Mitigation/Remediation Actions
Provoking the public access to the specified PDF

##Best Regards,
nagli.

## Impact

PII Disclosure of DoD personal, this include email addresses and phone numbers.

</details>

---
*Analysed by Claude on 2026-05-24*
