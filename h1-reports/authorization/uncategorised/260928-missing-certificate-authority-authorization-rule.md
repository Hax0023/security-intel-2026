# Missing Certificate Authority Authorization (CAA) DNS Record

## Metadata
- **Source:** HackerOne
- **Report:** 260928 | https://hackerone.com/reports/260928
- **Submitted:** 2017-08-17
- **Reporter:** gujjuboy10x00
- **Program:** Gratipay
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Missing Security Control, Improper Certificate Management, DNS Configuration Issue
- **CVEs:** None
- **Category:** uncategorised

## Summary
Gratipay's domain lacks a Certificate Authority Authorization (CAA) DNS record, which is a security mechanism that allows domain owners to specify which Certificate Authorities can issue certificates for their domain. Without this control, any CAA-compliant CA could potentially be tricked into issuing unauthorized certificates for the domain. This increases the attack surface for certificate misissuance and domain takeover scenarios.

## Attack scenario
1. Attacker identifies that Gratipay's domain has no CAA record configured
2. Attacker contacts a CA that issues certificates (such as LetsEncrypt or other providers)
3. Attacker requests a certificate for gratipay.com using social engineering or account compromise tactics
4. Without CAA restrictions, the CA may issue the certificate to the attacker
5. Attacker uses the fraudulent certificate to perform MITM attacks, phishing, or impersonation of Gratipay services
6. Legitimate users connecting to attacker-controlled servers believe they are communicating with authentic Gratipay infrastructure

## Root cause
Gratipay failed to implement CAA DNS records as a preventive security control. This is an oversight in domain security configuration where the organization did not establish explicit authorization rules to restrict certificate issuance to legitimate CAs only.

## Attacker mindset
An attacker would recognize that without CAA records, the path to obtaining a fraudulent certificate is significantly easier. They would view this missing control as a low-hanging fruit for obtaining valid-looking credentials to facilitate phishing, MITM attacks, or service impersonation with reduced likelihood of detection.

## Defensive takeaways
- Implement CAA records for all organizational domains to explicitly authorize only trusted Certificate Authorities
- Use CAA records with multiple issuers for redundancy and backup CAs
- Regularly audit DNS records and CAA configurations as part of security hygiene
- Consider implementing DNSSEC to prevent DNS spoofing and CAA record tampering
- Monitor certificate issuance through Certificate Transparency logs to detect unauthorized certificates
- Establish a process to revoke and reissue certificates if misissuance is detected

## Variant hunting
Look for other domains owned by Gratipay or related services without CAA records. Check subdomains and apex domains separately. Scan competitor organizations and industry peers for similar missing CAA controls. Investigate organizations with high-value targets (financial services, healthcare, government) that lack this control.

## MITRE ATT&CK
- T1190
- T1556
- T1571
- T1021

## Notes
CAA is a preventive control specified in RFC 6844. This vulnerability represents a configuration gap rather than a code vulnerability. The reporter helpfully referenced a similar finding (report #129992) indicating this was a known issue class. CAA implementation is a best practice that provides defense-in-depth against certificate-based attacks and should be considered mandatory for any organization with security-conscious infrastructure.

## Full report
<details><summary>Expand</summary>

Hi Team,

# Summary

Certificate Authority Authorization (supported by LetsEncrypt and other CAs) allows a domain owner to specify which Certificate Authorities should be allowed to issue certificates for the domain. All CAA-compliant certificate authorities should refuse to issue a certificate unless they are the CA of record for the target site. This helps reduce the threat of a bad guy tricking a Certificate Authority into issuing a phony certificate for your site.

The CAA rule is stored as a DNS resource record of type 257. You can view a domain’s CAA rule using a DNS lookup service:

https://caatest.co.uk/gratipay.com

gratipay should set a CAA record to help prevent misissuance of a certificate for its domains.

https://hackerone.com/reports/129992

Thanks,
Vishal

</details>

---
*Analysed by Claude on 2026-05-24*
