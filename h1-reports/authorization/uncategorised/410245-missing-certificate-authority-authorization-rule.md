# Missing Certificate Authority Authorization (CAA) Rule

## Metadata
- **Source:** HackerOne
- **Report:** 410245 | https://hackerone.com/reports/410245
- **Submitted:** 2018-09-16
- **Reporter:** theendisnear
- **Program:** Hacker101
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Missing Security Controls, Insufficient PKI Configuration, DNS Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
The organization failed to implement CAA DNS records for its domains, allowing any CAA-compliant Certificate Authority to potentially issue certificates. This misconfiguration enables attackers to obtain fraudulent SSL/TLS certificates for the target domain, facilitating man-in-the-middle attacks and domain impersonation.

## Attack scenario
1. Attacker identifies that target domain lacks CAA DNS records (type 257)
2. Attacker contacts a less-strict or compromised Certificate Authority requesting a certificate for the target domain
3. CA issues certificate without verifying domain authorization since no CAA record restricts issuance
4. Attacker uses fraudulent certificate to intercept HTTPS traffic or perform phishing attacks
5. Users connecting to attacker-controlled server see valid certificate warning indicators
6. Sensitive data or credentials are harvested from unsuspecting users

## Root cause
Organization did not implement DNS CAA resource records (type 257) to explicitly authorize which Certificate Authorities are permitted to issue certificates for their domains. This represents a missing security control rather than a coding vulnerability.

## Attacker mindset
An attacker seeks to obtain valid SSL/TLS certificates for the target domain to conduct sophisticated attacks including MITM interception, phishing with valid certificate indicators, and impersonation. The absence of CAA records significantly reduces the effort and cost required to obtain fraudulent certificates.

## Defensive takeaways
- Implement CAA DNS records specifying authorized Certificate Authorities (e.g., Let's Encrypt, internal CA)
- Use CAA records with appropriate flags to restrict certificate issuance and wildcard generation
- Monitor CAA record compliance across all owned domains including subdomains
- Implement DNSSEC to prevent CAA record tampering
- Establish certificate transparency monitoring to detect unauthorized certificate issuance
- Regularly audit DNS records for security controls and misconfigurations
- Include CAA record implementation in domain hardening security baselines

## Variant hunting
Check for missing CAA records on: organization's main domain, all subdomains, acquired/subsidiary domains, brand-associated domains, customer-facing domains. Verify CAA records on competitor domains to identify implementation patterns.

## MITRE ATT&CK
- T1190
- T1557
- T1040

## Notes
This is a configuration oversight rather than a code vulnerability. CAA records are optional but highly recommended as a defense-in-depth measure against certificate misissuance. The attack requires either a compromised CA or a CA with weak validation processes, making this a medium-severity issue that amplifies the impact of other CA-level attacks.

## Full report
<details><summary>Expand</summary>

Certificate Authority Authorization (supported by LetsEncrypt and other CAs) allows a domain owner to specify which Certificate Authorities should be allowed to issue certificates for the domain. All CAA-compliant certificate authorities should refuse to issue a certificate unless they are the CA of record for the target site. This helps reduce the threat of a bad guy tricking a Certificate Authority into issuing a phony certificate for your site.

The CAA rule is stored as a DNS resource record of type 257. You can view a domain’s CAA rule using a DNS lookup service:

https://dns.google.com/query?name=hacker101.com&type=257&dnssec=true

https://dns.google.com/query?name=ctf.hacker101.com&type=257&dnssec=true

hacker101 should set a CAA record to help prevent misissuance of a certificate for its domains.

Reference Report :  https://hackerone.com/reports/129992

## Impact

Misissuance of a certificate

</details>

---
*Analysed by Claude on 2026-05-24*
