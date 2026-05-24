# Brave Shield for iOS Vulnerable to IDN Homograph Attacks

## Metadata
- **Source:** HackerOne
- **Report:** 1819329 | https://hackerone.com/reports/1819329
- **Submitted:** 2022-12-31
- **Reporter:** nishimunea
- **Program:** Brave Software
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** IDN Homograph Attack, Unicode Spoofing, Information Disclosure, UI Spoofing
- **CVEs:** None
- **Category:** uncategorised

## Summary
Brave Shield on iOS fails to implement IDN homograph attack protections when displaying domain information in the security panel, while other parts of the browser have these protections. An attacker can register an IDN domain (e.g., xn--80ak6aa92e.com which displays as apple.com) and the Shield panel will show the spoofed domain name, deceiving users into trusting malicious sites.

## Attack scenario
1. Attacker registers an IDN domain that converts to a legitimate brand name (e.g., xn--80ak6aa92e.com → apple.com)
2. Attacker hosts phishing content on this IDN domain
3. User visits the malicious IDN URL, either through malicious link or typosquatting
4. User opens Brave Shield panel to verify the site's legitimacy
5. Shield panel displays the spoofed domain name (apple.com) instead of the actual punycode domain
6. User is deceived into trusting the site and entering credentials or sensitive information

## Root cause
Inconsistent implementation of IDN homograph protections across Brave iOS browser components. The Shield panel uses raw domain display without converting punycode to unicode for security analysis, creating a discrepancy where other UI elements properly handle IDN detection.

## Attacker mindset
Exploit inconsistent security implementations to bypass browser protections. Attacker recognizes that users trust the official security indicator (Shield panel) and leverages the false sense of security from seeing a familiar brand name to conduct phishing attacks.

## Defensive takeaways
- Apply consistent IDN homograph protections across all user-facing domains in the browser UI
- Display punycode representation in security-critical UI elements (Shield panel, address bar) to make spoofing attempts visible
- Implement visual warnings when users navigate to IDN domains that homograph legitimate brands
- Regularly audit all domain display locations for consistent security policy enforcement
- Consider disallowing registration of certain high-risk IDN domains that spoof popular brands
- Add integration testing to verify IDN handling across all browser components

## Variant hunting
Check other Brave browsers (Android, Desktop) for similar Shield panel IDN vulnerabilities
Test other security indicator panels or popups for IDN homograph handling
Verify if SSL certificate information panels properly display punycode vs unicode
Check site permission panels and other security-related UI for IDN inconsistencies
Test mixed-script attacks combining Latin and non-Latin characters in IDN domains
Verify if bookmark names and history display properly handle IDN domains

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link (IDN domain in links)
- T1566.002 - Phishing: Phishing - Email (IDN domain in email)
- T1594 - Search Open Websites/Domains
- T1583.001 - Acquire Infrastructure: Domains (IDN domain registration)

## Notes
This is a UI trust boundary violation where a security component (Shield panel) provides false assurance by displaying homographed domain names. The vulnerability's impact is amplified because users explicitly trust Shield as a security feature. The inconsistency across browser components suggests insufficient security code review during feature implementation.

## Full report
<details><summary>Expand</summary>

## Summary:

In most parts of Brave for iOS, including the address bar, protection against IDN attacks are implemented.
However, Brave Shield has no countermeasures.
For example, when you visit https://www.xn--80ak6aa92e.com , Brave Shield panel in the address bar shows the domain of this site is "apple.com".
This may lead users to be deceived into believing that the site is legitimate.

## Products affected: 

 * Brave for iOS (Version 1.45.2)

## Steps To Reproduce:

 * Visit https://www.xn--80ak6aa92e.com
 * Open Brave Shield panel from the address bar
 * "apple.com" is shown in the panel

## Supporting Material/References:

  * See the screenshot I attached.

## Impact

This may lead users to be deceived into believing that the site is legitimate.

</details>

---
*Analysed by Claude on 2026-05-24*
