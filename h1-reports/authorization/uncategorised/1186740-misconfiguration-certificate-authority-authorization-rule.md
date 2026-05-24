# Missing Certificate Authority Authorization (CAA) DNS Record

## Metadata
- **Source:** HackerOne
- **Report:** 1186740 | https://hackerone.com/reports/1186740
- **Submitted:** 2021-05-06
- **Reporter:** d4rk_r0s3
- **Program:** Sifchain
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Missing Security Configuration, Inadequate Access Controls, DNS Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
Sifchain.finance domain lacks CAA DNS records, failing to restrict which Certificate Authorities can issue SSL/TLS certificates for the domain. This misconfiguration allows any CAA-compliant CA to issue certificates for the domain, enabling potential certificate misissuance attacks and domain takeover scenarios.

## Attack scenario
1. Attacker identifies that sifchain.finance has no CAA DNS record set
2. Attacker compromises or socially engineers a Certificate Authority (e.g., through account takeover or by exploiting CA processes)
3. Attacker requests a certificate for sifchain.finance from the compromised/cooperative CA
4. Without CAA enforcement, the CA issues the malicious certificate without checking domain ownership restrictions
5. Attacker uses the fraudulent certificate for SSL interception, phishing, or MITM attacks on Sifchain traffic
6. Users connecting to attacker's server receive the malicious certificate, believing it's legitimate

## Root cause
Sifchain failed to implement CAA DNS records (type 257) that would instruct Certificate Authorities which CAs are authorized to issue certificates for their domain. This is a configuration oversight in DNS security controls.

## Attacker mindset
An attacker would recognize that missing CAA records represent low-hanging fruit for certificate misissuance attacks. The absence of CAA eliminates a critical DNS-level control, making it easier to obtain fraudulent certificates through CA compromise or social engineering rather than solving ACME challenges.

## Defensive takeaways
- Implement CAA DNS records explicitly authorizing only legitimate CAs (e.g., Let's Encrypt, DigiCert) to issue certificates
- Set restrictive CAA records using DNS configuration: e.g., 'CAA 0 issue "letsencrypt.org"'
- Include wildcard CAA records for subdomains to prevent issuance of certificates for unexpected subdomains
- Regularly audit CAA records using tools like caatest.co.uk or DNS lookup services
- Monitor Certificate Transparency (CT) logs for unauthorized certificate issuances
- Implement certificate pinning for critical infrastructure as an additional control layer
- Establish monitoring for suspicious certificate requests through CA-provided alerting services

## Variant hunting
Search for other Sifchain domains (subdomains, partner domains) lacking CAA records. Check if competitors or similar DeFi platforms have implemented CAA. Investigate whether other DNS security controls (DNSSEC, SPF, DKIM, DMARC) are also missing.

## MITRE ATT&CK
- T1190
- T1589
- T1583
- T1556

## Notes
While technically a configuration issue rather than a code vulnerability, CAA misconfiguration poses significant risk in the context of financial platforms like Sifchain where SSL certificate trust is critical. The lack of specificity regarding 'Domain Authority Takeover' impact suggests the reporter may have been referencing broader domain security implications. CAA implementation is a low-effort, high-value security control that should be standard practice for all internet-facing organizations.

## Full report
<details><summary>Expand</summary>

Hello,Sifchain Security Team,
I found a bug called Missing CAA. Certificate Authority Authorization (supported by LetsEncrypt and other CAs) allows a domain owner to specify which Certificate Authorities should be allowed to issue certificates for the domain. All CAA-compliant certificate authorities should refuse to issue a certificate unless they are the CA of record for the target site. This helps reduce the threat of a bad guy tricking a Certificate Authority into issuing a phony certificate for your site. The CAA rule is stored as a DNS resource record of type 257. You can view a domain’s CAA rule using a DNS lookup service:
https://caatest.co.uk/sifchain.finance
Sifchain should set a CAA record to help prevent misissuance of a certificate for its domains.

## Impact

Impact:-
Domain Authority Can Be Takeover. If you need further information let me know

</details>

---
*Analysed by Claude on 2026-05-24*
