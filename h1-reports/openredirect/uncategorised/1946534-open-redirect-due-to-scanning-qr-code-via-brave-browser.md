# Open Redirect via Brave Browser QR Code Scanner Auto-Navigation

## Metadata
- **Source:** HackerOne
- **Report:** 1946534 | https://hackerone.com/reports/1946534
- **Submitted:** 2023-04-14
- **Reporter:** roland_hack
- **Program:** Brave Browser
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, Insufficient Input Validation, Missing User Consent Mechanism
- **CVEs:** CVE-2023-28364
- **Category:** uncategorised

## Summary
Brave's QR code scanner automatically navigates to URLs encoded in QR codes without displaying the target link or requiring user confirmation, enabling attackers to redirect users to malicious sites. This differs from safer QR code scanner implementations that preview the URL before navigation, allowing users to make informed decisions about whether to proceed.

## Attack scenario
1. Attacker generates a QR code containing a malicious URL (e.g., www.evil.com) using a QR code generator service
2. Attacker distributes the QR code through physical media (posters, stickers) or digital channels where Brave users may encounter it
3. Victim opens Brave browser and accesses the QR code scanner feature via the camera/scan option
4. Victim scans the malicious QR code without examining its contents
5. Brave automatically decodes and navigates to the embedded malicious URL without displaying it or requesting confirmation
6. Victim is redirected to attacker's phishing site, malware distribution server, or credential harvesting page before they can assess the target

## Root cause
Brave's QR code scanner implementation automatically parses QR codes and initiates navigation to the decoded URL without implementing a preview step or user confirmation dialog. The scanner lacks validation of the target domain against blocklists and does not provide visibility into the decoded URL before redirection occurs.

## Attacker mindset
Attackers exploit user trust in browser-integrated features and the assumption that native scanners are safe. By embedding malicious URLs in QR codes distributed through high-traffic areas or social engineering, they can achieve high redirect rates without requiring phishing emails or suspicious links, lowering detection and increasing success rates for credential theft and malware distribution.

## Defensive takeaways
- Implement URL preview dialogs showing the decoded target before any navigation occurs
- Require explicit user confirmation before navigating to QR-code-sourced URLs
- Validate decoded URLs against malware/phishing blocklists (Safe Browsing API) before preview
- Display visual indicators of domain/protocol to prevent homograph attacks
- Consider disabling auto-navigation for non-https URLs or URLs with suspicious characteristics
- Add URL sanitization to detect and warn on open redirect parameters
- Implement origin context display (e.g., 'where was this QR code scanned from')
- Provide user preference settings to require confirmation for all QR-based navigation
- Log and monitor QR code scan events for security analysis

## Variant hunting
Test QR scanners in other Chromium-based browsers (Edge, Opera) for identical behavior
Examine whether NFC tag scanning exhibits the same auto-navigation vulnerability
Investigate if custom URL schemes (intent://, about:) can be embedded in QR codes for privilege escalation
Test encoding open redirect parameters in QR URLs to chain vulnerabilities
Scan QR codes with unicode/punycode domain names to assess homograph attack feasibility
Test data: URLs or javascript: protocol handlers in QR code encoding
Verify behavior with file:// protocol URLs pointing to local system resources

## MITRE ATT&CK
- T1566.002
- T1598.003
- T1589.001
- T1201
- T1187
- T1566.004

## Notes
This vulnerability represents a UX security flaw rather than a code injection or cryptographic weakness. The severity is Medium rather than High because exploitation requires user action (scanning a QR code), limiting attack surface compared to passive vulnerabilities. However, the combination with social engineering (distributing malicious QR codes in public spaces) significantly increases real-world risk. The report references legitimate security concerns but lacks proof of concept code or bounty documentation. The vulnerability was fixed in later Brave versions by implementing URL preview before navigation. Similar issues have affected other QR scanner implementations (Google Lens, WeChat), indicating a systemic UX security pattern in mobile scanning features.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please fill all sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to verify and then potentially issue a bounty.

## Summary:
This vulnerability was discovered in Brave's QR code scanner, which allows users to read QR codes and open corresponding links. Exploitation of this vulnerability allows attackers to direct users to malicious sites without their consent or knowledge. This vulnerability can put the security of Brave users at risk and allow them to be exposed to phishing, phishing and malware attacks. In this report, we'll describe the vulnerability in more detail, assess its severity, and provide recommendations to address it.



## Products affected: 

Brave 1.50.114, Chromium 112.0.5615.49 on Android 11; Build/RP1A.200720.011

## Steps To Reproduce:

{F2291837}

The QR code above is the one I generated to replicate the attack.
To create my QR code, I used the site https://app.qr-code-generator.com.
 I included a malicious link in this QR code. As an example link, I used www.evil.com

#  Steps To Reproduce

 -  Open the browser 
- Then in your browser you can click on the "scan a QR code" option and scan the QR code in which I have included my malicious link. 
This will automatically redirect you to the malicious site I inserted in the QR code, without even asking your opinion.
- However, some QR code scanners do not automatically redirect the user to the malicious site, but rather display the link with the "Go to site" option. Other scanners don't even show this option. 
- However, in the case of Brave, the browser automatically redirects the user to the malicious site without their consent, which poses a significant security risk to users.


## Supporting Material/References:

https://resources.infosecinstitute.com/topic/security-attacks-via-malicious-qr-codes/
https://shahjerry33.medium.com/open-redirection-qr-code-magic-18ace1a0170f

## Impact

Here are some potential business impacts that this security vulnerability could have in Brave 1.50.114, Chromium 112.0.5615.49 on Android 11; Build/RP1A.200720.011:

The fact that Brave's QR code scanner opens the link without the user's notice has a big impact on user security. This vulnerability allows an attacker to redirect a Brave user to a malicious site without the user being able to see the link and make an informed decision. This can lead to exposure to malware or phishing attacks that can compromise user data.

The actual impact depends on the nature of the malicious link to which the user is redirected. In the worst case, the link may be designed to steal sensitive information, such as credit card information, credentials, or other personal information. This can lead to loss of privacy and financial damage to the user.

Moreover, if the user is redirected to a malicious site that contains malware, then it can compromise the security of the user's device and lead to loss of important data. Overall, the fact that Brave's QR code scanner automatically opens malicious links without user's notice poses a significant risk to user security and should be fixed as soon as possible.

    Increased Risk of Phishing: Exploiting this vulnerability could allow attackers to direct Brave users to malicious sites that can be used to steal sensitive information such as usernames, passwords, banking and other personal information.

    Exposure to malware: Malicious sites that users are redirected to may also contain malware that can infect Brave users' devices with malicious programs such as viruses, Trojans or ransomware.

    Privacy loss: Brave users may also be at risk of privacy loss if sensitive information is stolen as a result of the exploitation of this vulnerability.

    Loss of user trust: If Brave users fall victim to attacks as a result of exploiting this vulnerability, they may lose trust in the application and seek out more secure alternatives, which could impact reputation of the application and the company.

    Financial costs: If users fall victim to attacks as a result of this vulnerability, they may suffer financial losses, which may lead to legal action and financial costs to the company responsible for the application.

</details>

---
*Analysed by Claude on 2026-05-24*
