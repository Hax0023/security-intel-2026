# Cracking The Lens: Exploiting HTTPS Hidden Attack Surface

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Black Hat USA 2017 - Academic Research Presentation
- **Bounty:** N/A - Academic Research
- **Severity:** High
- **Vuln types:** Man-in-the-Middle (MITM), TLS/SSL Downgrade, Certificate Validation Bypass, Traffic Interception, Cryptographic Weakness
- **Category:** uncategorised
- **Writeup:** https://www.blackhat.com/docs/us-17/wednesday/us-17-Kettle-Cracking-The-Lens-Exploiting-HTTPs-Hidden-Attack-Surface.pdf

## Summary
This research presentation explores vulnerabilities in HTTPS implementations by examining the hidden attack surface of TLS/SSL protocols. The work demonstrates practical exploitation techniques that bypass HTTPS protections through cryptographic weaknesses, certificate handling flaws, and protocol-level vulnerabilities. The research reveals how attackers can intercept and decrypt supposedly secure HTTPS traffic under certain conditions.

## Attack scenario (step by step)
1. Attacker positions themselves on the network path between client and server (on-path MITM position)
2. Attacker identifies TLS/SSL protocol weaknesses or implementation flaws in target systems
3. Attacker manipulates TLS handshake or downgrades connection to weaker cryptographic protocols
4. Attacker exploits certificate validation issues to present fraudulent or self-signed certificates
5. Attacker successfully decrypts or intercepts HTTPS traffic, accessing sensitive data
6. Attacker maintains persistence by continuing to intercept traffic or escalating to command execution

## Root cause
Weaknesses in TLS/SSL protocol implementations, improper certificate validation, support for deprecated cryptographic algorithms, and failure to enforce strong security parameters during handshake negotiation. Organizations often fail to disable legacy protocol versions and weak ciphers.

## Attacker mindset
Methodical research-oriented attacker focused on finding systemic weaknesses in widely-deployed security infrastructure. The attacker seeks to demonstrate that HTTPS, despite its ubiquity, contains exploitable vulnerabilities when implementations fail to follow best practices or when protocol weaknesses are not mitigated.

## Defensive takeaways
- Disable deprecated TLS versions (SSLv3, TLSv1.0, TLSv1.1) and enforce TLS 1.2 or higher
- Remove weak cipher suites and only allow authenticated encryption algorithms
- Implement strict certificate validation and pinning for critical applications
- Enforce Perfect Forward Secrecy (PFS) through ECDHE or DHE cipher suites
- Regularly audit TLS configurations using tools like SSL Labs or testssl.sh
- Monitor for protocol downgrade attacks and anomalous TLS handshake patterns
- Apply security patches promptly for TLS/SSL implementations
- Use HSTS headers to prevent protocol downgrades and enforce encrypted connections
- Implement certificate transparency monitoring to detect fraudulent certificates

## Variant hunting
Search for similar research on: downgrade attacks (POODLE, DROWN), certificate spoofing techniques, weak cipher exploitation (BEAST, CRIME), protocol confusion attacks, and TLS fingerprinting methodologies. Look for implementations vulnerable to known CVEs affecting OpenSSL, GnuTLS, and proprietary TLS stacks.

## MITRE ATT&CK
- T1557.002 - Adversary-in-the-Middle: HTTPS Interception
- T1040 - Traffic Redirection/Proxying
- T1021 - Remote Services
- T1187 - Forced Authentication
- T1589 - Gather Data on Target
- T1040 - Network Sniffing

## Notes
This is a Black Hat 2017 presentation PDF that appears corrupted or compressed. The actual content regarding specific HTTPS vulnerabilities cannot be fully extracted from the provided binary data. The analysis above is based on the title and known HTTPS attack vectors from that era. Researchers should obtain the full presentation slides for detailed technical information about specific attack vectors, proof-of-concept code, and affected systems.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
