# Open Redirect and XSS in supporthiring.shopify.com via Double Slash Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 158434 | https://hackerone.com/reports/158434
- **Submitted:** 2016-08-11
- **Reporter:** jamesclyde
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Open Redirect, XSS (Reflected), Authorization Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A path parameter validation bypass vulnerability exists in supporthiring.shopify.com that allows attackers to redirect users to arbitrary domains. By encoding a double slash as %2F%2F, attackers bypass the existing redirect protection mechanism and redirect victims to attacker-controlled sites after a 2-second delay.

## Attack scenario
1. Attacker identifies the path= parameter in supporthiring.shopify.com as having redirect protection
2. Attacker discovers that double slashes (%2F%2F) bypass the validation filter
3. Attacker crafts a malicious URL: http://supporthiring.shopify.com/apps/locksmith/resource/pages/gauntlet-challenge?&path=%2F%2Fevil.com
4. Attacker sends this URL to victims via phishing email or social engineering
5. Victim clicks the link and sees a legitimate 404 error page from Shopify domain
6. After 2 seconds, victim is silently redirected to attacker's malicious domain (evil.com) where credential theft or malware distribution occurs

## Root cause
The redirect validation logic fails to properly decode URL-encoded characters before checking if the path is external. The filter likely checks for '//' or similar patterns in decoded form but applies validation to encoded input, allowing %2F%2F to bypass the check.

## Attacker mindset
An attacker would leverage the trusted Shopify domain as a stepping stone for phishing. The 404 page lends legitimacy to the redirect, reducing victim suspicion. This enables credential harvesting, malware distribution, or further social engineering attacks.

## Defensive takeaways
- Always decode user input before validation, not after
- Use allowlist-based redirect validation (only allow internal paths or whitelisted domains)
- Implement multiple encoding/decoding passes to catch double-encoded bypasses
- Avoid relying on blacklists of dangerous characters; use positive validation instead
- Validate that redirects point to same-origin or explicitly trusted domains
- Implement redirect destination logging and monitoring for anomalies
- Use HTML5 rel='noreferrer noopener' on external links to limit attack surface

## Variant hunting
Test other encoding schemes: ..%252F..%252F, Unicode encoding (\u002f), HTML entities
Check for protocol bypass: javascript:%2F%2F, data:%2F%2F, vbscript:%2F%2F
Attempt bypass with backslashes or mixed separators: %5C%5C, %2F%5C
Try null byte injection: %00, %2500 before the path
Test redirect parameter variations: redirect=, url=, return=, goto=, next=
Check other Shopify subdomains for similar vulnerabilities
Attempt XSS payload injection in path parameter: path=%2F%2F<img src=x onerror=alert(1)>

## MITRE ATT&CK
- T1598 - Phishing: Spearphishing Link (using open redirect for initial compromise)
- T1566 - Phishing (delivery mechanism)
- T1190 - Exploit Public-Facing Application
- T1608.005 - Stage Capabilities: Link Target (crafting malicious redirect URL)
- T1656 - Impersonation (leveraging trusted Shopify domain)

## Notes
The report indicates this affects all browsers, suggesting the vulnerability exists server-side. The 2-second delay before redirect may be a client-side meta refresh or JavaScript redirect, which could provide a window for user awareness but is unreliable. The XSS component mentioned in the title suggests the path parameter may also be reflected in the 404 page HTML, creating a secondary XSS vector. This is a critical finding as it chains redirect + phishing with Shopify's trusted domain reputation.

## Full report
<details><summary>Expand</summary>

Hello,

The users can be redirected to some other site which is in control of the attacker from 

Vulnerable parameter: path=

You have a protection here at path= but it bypass the parameter if you add a double slash, like %2F%2F.

Let's say user is attacker asked victim to came to this page: :
http://supporthiring.shopify.com/apps/locksmith/resource/pages/gauntlet-challenge?&path=%2F%2Fevil.com

Victim will be see a 404 error page and after 2 seconds he will be redirected to: https://evil.com

These can be controlled by the attacker and used in other attacks

Works in all browsers!!




</details>

---
*Analysed by Claude on 2026-05-24*
