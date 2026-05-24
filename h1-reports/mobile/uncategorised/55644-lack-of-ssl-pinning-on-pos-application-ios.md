# Lack of SSL Pinning on POS Application (iOS)

## Metadata
- **Source:** HackerOne
- **Report:** 55644 | https://hackerone.com/reports/55644
- **Submitted:** 2015-04-10
- **Reporter:** ishikawa
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Improper Certificate Validation, Man-in-the-Middle (MiTM) Vulnerability, Insufficient Transport Layer Protection, Missing SSL/TLS Pinning
- **CVEs:** None
- **Category:** uncategorised

## Summary
The iOS POS application performs SSL certificate validation through the OS keychain but fails to implement certificate pinning, making it vulnerable to man-in-the-middle attacks. An attacker can intercept sensitive cardholder data (CHD) by installing a malicious certificate on the device that the application will trust. This is particularly critical for a payment application handling sensitive financial information.

## Attack scenario
1. Attacker creates or obtains a self-signed or rogue CA certificate
2. Attacker tricks user into installing the certificate on iOS device (via social engineering, malicious profile, or compromised app)
3. User trusts the certificate at OS level in iOS settings
4. Attacker positions themselves on network path (public WiFi, ARP spoofing, DNS hijacking) and intercepts HTTPS traffic
5. Application validates certificate chain against OS keychain and accepts the attacker's certificate as valid
6. Attacker successfully decrypts and captures sensitive cardholder data, credentials, or transaction details

## Root cause
The application relies solely on the OS-level certificate validation using the keychain without implementing additional certificate pinning checks. This assumes the OS certificate store is trustworthy and uncompromised, which is not guaranteed in security-sensitive applications. The application does not verify that the certificate belongs specifically to Shopify or pin to known good certificates.

## Attacker mindset
An attacker targets this POS application because it processes payment card holder data (CHD), making the breach highly valuable. They exploit the trust chain vulnerability to position themselves as a trusted intermediary without needing to compromise the legitimate certificate authority, which is easier than breaking cryptography. The attacker recognizes that mobile users often connect to untrusted networks (public WiFi) where MiTM attacks are feasible.

## Defensive takeaways
- Implement SSL/TLS certificate pinning on all mobile applications, especially those handling sensitive financial data
- Pin to multiple certificates or public keys to allow for certificate rotation without breaking the app
- Do not rely solely on OS-level certificate validation; add application-level validation
- For POS and payment applications, pinning is a baseline security requirement, not optional
- Consider pinning to intermediate CAs or root certificates for flexibility in certificate management
- Regularly review and update pinned certificates before expiration to prevent service disruption
- Implement certificate transparency monitoring to detect unauthorized certificates issued for your domain
- Educate users about certificate warnings and risks of installing untrusted profiles

## Variant hunting
Check for SSL pinning implementation in Android version of the same application
Review other Shopify mobile apps (merchant dashboard, analytics, inventory) for similar pinning vulnerabilities
Test backend API endpoints for lack of mutual TLS or certificate validation
Examine if web application version has HPKP (HTTP Public Key Pinning) headers implemented
Verify if third-party payment SDKs used by Shopify implement their own pinning
Check for hardcoded certificate validation logic that may have bypass vulnerabilities
Test if app uses vulnerable networking libraries with known TLS validation issues

## MITRE ATT&CK
- T1557.002
- T1071.001
- T1040
- T1187
- T1566.002

## Notes
This report was submitted to Shopify in 2015 (HackerOne report #55644). At the time, certificate pinning was becoming industry standard for sensitive applications. The vulnerability is particularly concerning because: (1) It directly impacts CHD security under PCI-DSS compliance, (2) iOS allows users to install custom CAs system-wide without restrictions, (3) The threat model includes both sophisticated attackers and compromised applications on the same device. The researcher correctly notes that competitors like Square and Amazon POS had already implemented pinning, establishing industry precedent. The proof of concept using Burp Suite/mitmproxy is practical and demonstrates the vulnerability is not theoretical but immediately exploitable by standard pentesting tools.

## Full report
<details><summary>Expand</summary>

#### Description

Given that this is a POS application and handle CHD, cryptographic security is of most importance. Applications such as Square, Amazons POS, etc. have already implemented this. The iOS application is correctly checking for SSL certs using the os keychain, but due to the lack of checking for wether or not the certificate actually belongs to Sopify, the mobile app is vulnerable to MiTM attacks in which an attacker is able to install or force the user to install a certificate on the device. Given today's known issues with CAs and the lack of trust they are generating lately, Pinning on mobile devices is a technique that is becoming a standard practice. SSL Pinning is a technique for which you pin your applications or clients to one or more SSL Certificates, keys or CAs. This technique allows you to perform the normal SSL chain of trust exchange during SSL transmissions, but also checks that the SSL certificate or key within that cert is actually the one you know and trust.

#### Vulnerable platform

iOS - entire application.

#### Proof of Concept

A simple way of testing this will be to use a tool like Burp Proxy and/or mitmproxy.
Step 1) install the "malicious" cert on device and trust it. An attacker can easily trick a user to install a profile, and/or malicious applications could potentially do it as part of installation.  Step 2) Proxy all the communication through them.  Step 3) You will confirm that your application is no longer using the Certificate it should trust.

#### Recommendation

Even though this is not a high risk vulnerability, lack of SSL Pinning certainly creates an unnecessary risk for applications on mobile devices. It is our recommendation that Shopify implements SSL Pinning on iOS, and do not trust the os-level certificate store since other applications might have control over it and there is no guarantees they won't be maliciously altered. Additionally, you might have other types of attacks in which CA issue wild-card certificates to random entities, as it was recently seen with Google and a Chinese CA.
For more information please refer to 
https://www.owasp.org/index.php/Certificate_and_Public_Key_Pinning

</details>

---
*Analysed by Claude on 2026-05-24*
