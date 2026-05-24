# Open Redirect Vulnerability via redirect_url Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2265413 | https://hackerone.com/reports/2265413
- **Submitted:** 2023-11-27
- **Reporter:** hasn0x
- **Program:** Undisclosed
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Open Redirect, URL Redirection to Untrusted Site
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the application where the 'redirect_url' parameter is not properly validated, allowing attackers to redirect users to arbitrary malicious websites. This vulnerability can be exploited to conduct phishing attacks or distribute malware by disguising malicious URLs as legitimate redirects.

## Attack scenario
1. Attacker identifies the vulnerable parameter 'redirect_url' on the target application
2. Attacker crafts a legitimate-looking URL containing the vulnerable endpoint with a malicious redirect_url parameter pointing to attacker-controlled phishing site
3. Attacker shares the crafted URL via email, social media, or other channels to potential victims
4. Unsuspecting users click the link, trusting the legitimate domain origin
5. User is automatically redirected to the attacker's phishing site which mimics the legitimate application
6. Attacker harvests credentials, credit card information, or other sensitive data from compromised users

## Root cause
The application fails to implement proper URL validation and whitelisting for the 'redirect_url' parameter. The redirect functionality does not verify that the destination URL belongs to an authorized/trusted domain before performing the redirect.

## Attacker mindset
An attacker would leverage this vulnerability as an effective social engineering vector since users trust the initial legitimate domain. The vulnerability enables low-effort phishing campaigns with higher success rates due to the legitimate origin masking malicious intent.

## Defensive takeaways
- Implement strict URL validation using whitelist approach - only allow redirects to pre-approved internal URLs or domains
- Parse and validate redirect URLs against a list of allowed hosts/domains before execution
- Use relative URLs instead of absolute URLs when possible to prevent external redirects
- Implement URL scheme validation to prevent javascript: and data: protocol redirects
- Log all redirect attempts for monitoring and security auditing
- Add security headers like Referrer-Policy to limit information leakage
- Educate users about URL verification before clicking links

## Variant hunting
Search for similar redirect parameters: 'return_url', 'next', 'goto', 'continue', 'back_url', 'return_to', 'url', 'redirect', 'target' across application endpoints. Test both GET and POST parameters. Check for URL encoding bypasses, protocol relativization (//), and domain confusion techniques.

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1601
- T1189

## Notes
The writeup references redacted URLs and endpoints (███), limiting full vulnerability assessment. Report appears preliminary with proof-of-concept video referenced but not fully detailed. Open redirects are often underestimated but are effective for credential harvesting and malware distribution when combined with social engineering.

## Full report
<details><summary>Expand</summary>

Vulnerability Details:

User can be Redirect to malicious site POC:  █████████

Steps To Reproduce:
Use a browser to navigate to ███

  1.Navigate to the vulnerable page on the website/application
  2.Modify the “redirect_url” parameter by adding a malicious URL as its value.
  3.Submit the request and observe that the page is redirected to the malicious URL.


  screenrecord

## Impact

Open redirect vulnerabilities can have various impacts on both users and organizations. Here are some potential consequences:

Phishing Attacks: Attackers can exploit open redirect vulnerabilities to craft convincing phishing attacks. They can redirect users to malicious websites that mimic legitimate ones, tricking them into divulging sensitive information such as usernames, passwords, or credit card details.

Malware Infections: Redirecting users to malicious websites through open redirect vulnerabilities can lead to the inadvertent download and installation of malware. This can result in the compromise of user devices, theft of personal information, or unauthorized access to sensitive data.

</details>

---
*Analysed by Claude on 2026-05-24*
