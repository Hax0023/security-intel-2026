# Missing Certificate Authority Authorization (CAA) Record

## Metadata
- **Source:** HackerOne
- **Report:** 129992 | https://hackerone.com/reports/129992
- **Submitted:** 2016-04-12
- **Reporter:** ericlaw
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Missing Security Control, Weak Certificate Management, DNS Configuration Weakness
- **CVEs:** None
- **Category:** uncategorised

## Summary
HackerOne's domains lacked CAA DNS records, failing to restrict which Certificate Authorities could issue TLS certificates for the domain. This configuration weakness could allow an attacker to obtain fraudulent certificates from CAA-compliant CAs, enabling man-in-the-middle attacks and domain impersonation.

## Attack scenario
1. Attacker identifies that HackerOne domains lack CAA DNS records
2. Attacker contacts a CAA-compliant Certificate Authority (e.g., Let's Encrypt) requesting a certificate for hackerone.com
3. CA performs domain validation (ACME challenge, email verification, etc.)
4. Without CAA restrictions, the CA issues the fraudulent certificate to the attacker
5. Attacker uses the malicious certificate to intercept HTTPS traffic or perform phishing
6. Users connecting to the attacker's server see a valid certificate, bypassing browser warnings

## Root cause
HackerOne failed to implement CAA DNS records (type 257) to explicitly authorize specific Certificate Authorities for their domains. This is an oversight in DNS security configuration best practices.

## Attacker mindset
Opportunistic attacker seeking to obtain valid SSL/TLS certificates for high-value domains without domain ownership. CAA bypass enables credential harvesting, phishing, and traffic interception without triggering certificate transparency logs as primary detection vector.

## Defensive takeaways
- Implement CAA records for all organizational domains, explicitly listing only authorized CAs
- Use restrictive CAA policies with 'issue' and 'issuewild' tags to prevent certificate misissuance
- Include iodef reporting tag in CAA records to receive notifications of unauthorized issuance attempts
- Monitor Certificate Transparency logs for unexpected certificates issued for your domains
- Regularly audit DNS security records including CAA, DNSSEC, SPF, DKIM, and DMARC
- Establish certificate issuance approval workflows and audit CA-issued certificates monthly

## Variant hunting
Check for CAA records on all organizational subdomains and sister domains
Identify other organizations missing CAA records in similar technology sectors
Search Certificate Transparency logs for fraudulently issued certificates before CAA implementation
Examine wildcard CAA policies that may have broader scope than intended
Test CAA enforcement across different CA providers (some may be non-compliant)

## MITRE ATT&CK
- T1190
- T1556
- T1557
- T1589

## Notes
This is a configuration/defensive control weakness rather than a traditional vulnerability. The impact is significant for high-profile targets as fraudulent certificates enable sophisticated attacks. Report demonstrates good security research methodology by explaining the technical context and remediation. CAA adoption remains surprisingly low despite being available since 2013.

## Full report
<details><summary>Expand</summary>

Certificate Authority Authorization (supported by LetsEncrypt and other CAs) allows a domain owner to specify which Certificate Authorities should be allowed to issue certificates for the domain. All CAA-compliant certificate authorities should refuse to issue a certificate unless they are the CA of record for the target site. This helps reduce the threat of a bad guy tricking a Certificate Authority into issuing a phony certificate for your site.

The CAA rule is stored as a DNS resource record of type 257. You can view a domain’s CAA rule using a DNS lookup service:

https://dns.google.com/query?name=hackerone.com&type=257&dnssec=true

Hackerone should set a CAA record to help prevent misissuance of a certificate for its domains.

</details>

---
*Analysed by Claude on 2026-05-24*
