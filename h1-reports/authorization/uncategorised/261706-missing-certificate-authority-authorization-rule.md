# Missing Certificate Authority Authorization (CAA) DNS Record

## Metadata
- **Source:** HackerOne
- **Report:** 261706 | https://hackerone.com/reports/261706
- **Submitted:** 2017-08-20
- **Reporter:** theendisnear
- **Program:** Gratipay
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Missing Security Control, Improper Certificate Management, DNS Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
Gratipay.com lacks a CAA DNS record, which allows any CAA-compliant Certificate Authority to issue certificates for the domain without explicit authorization. This enables potential certificate misissuance attacks where an attacker could obtain a fraudulent SSL/TLS certificate from a compromised or malicious CA.

## Attack scenario
1. Attacker identifies that gratipay.com has no CAA DNS record configured
2. Attacker compromises or socially engineers a CAA-compliant Certificate Authority
3. Attacker requests a certificate for gratipay.com from the compromised CA
4. The CA issues the certificate without verifying authorization since no CAA record restricts issuance
5. Attacker uses the fraudulent certificate to perform MITM attacks or phishing against Gratipay users
6. Legitimate users trust the certificate due to CA signature, exposing credentials and data

## Root cause
Gratipay failed to implement CAA DNS records as a proactive security control to restrict which Certificate Authorities can issue certificates for their domain.

## Attacker mindset
An attacker seeks to obtain valid SSL certificates for target domains without going through legitimate channels. Missing CAA records represent an easy win requiring no technical exploitation—just requesting a certificate from any willing CA.

## Defensive takeaways
- Implement CAA records for all domain names specifying only authorized Certificate Authorities
- Use restrictive CAA policies (e.g., issue="letsencrypt.org" and iodef reporting)
- Monitor CAA records as part of regular security audits
- Establish certificate transparency monitoring to detect unauthorized issuance
- Implement DNSSEC to prevent CAA record tampering
- Use multiple layers of certificate validation including pinning for critical services

## Variant hunting
Check for missing CAA records across all organizational domains and subdomains; verify CAA records on acquisition targets; audit for wildcards or overly permissive CAA policies; search for organizations allowing multiple unvetted CAs unnecessarily

## MITRE ATT&CK
- T1190
- T1556
- T1557

## Notes
This is a configuration weakness rather than a code vulnerability. CAA records are foundational to PKI security and their absence is a common oversight. The impact depends on CA compromise likelihood and attacker capability. This report demonstrates responsible disclosure of missing security hygiene rather than active exploitation.

## Full report
<details><summary>Expand</summary>

Certificate Authority Authorization (supported by LetsEncrypt and other CAs) allows a domain owner to specify which Certificate Authorities should be allowed to issue certificates for the domain. All CAA-compliant certificate authorities should refuse to issue a certificate unless they are the CA of record for the target site. This helps reduce the threat of a bad guy tricking a Certificate Authority into issuing a phony certificate for your site.

The CAA rule is stored as a DNS resource record of type 257. You can view a domain’s CAA rule using a DNS lookup service:

https://dns.google.com/query?name=gratipay.com&type=257&dnssec=true

Gratipay should set a CAA record to help prevent misissuance of a certificate for its domains.

</details>

---
*Analysed by Claude on 2026-05-24*
