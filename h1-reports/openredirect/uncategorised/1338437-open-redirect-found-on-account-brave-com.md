# Open Redirect Vulnerability on account.brave.com

## Metadata
- **Source:** HackerOne
- **Report:** 1338437 | https://hackerone.com/reports/1338437
- **Submitted:** 2021-09-13
- **Reporter:** tabaahi
- **Program:** Brave Software
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, Unvalidated Redirects and Forwards, CWE-601
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists on account.brave.com that allows attackers to redirect users to arbitrary external domains by manipulating URL parameters. The vulnerability can be exploited via path traversal sequences to bypass basic redirect validation, making phishing attacks appear more legitimate.

## Attack scenario
1. Attacker crafts a malicious URL: https://account.brave.com//example.com/%2F.. containing path traversal sequences
2. Attacker embeds this link in a phishing email appearing to come from Brave
3. Victim clicks the link, trusting the account.brave.com domain
4. Server processes the URL and redirects victim to attacker's malicious site (example.com)
5. Victim arrives at attacker's fake Brave login page due to legitimate domain in URL bar history
6. Attacker captures victim's credentials or delivers malware

## Root cause
The application fails to properly validate and sanitize redirect URLs before performing HTTP redirects. The validation logic likely only checks for basic URL patterns without accounting for path traversal sequences (//) that can obfuscate the actual redirect destination.

## Attacker mindset
Exploit trust in legitimate domain names to conduct credential harvesting phishing campaigns. By leveraging the legitimate account.brave.com domain in the initial URL, the attacker increases click-through rates and reduces victim suspicion compared to direct links to malicious domains.

## Defensive takeaways
- Implement whitelist-based redirect validation using absolute URL comparison, not pattern matching
- Reject any URLs containing //, encoded sequences (%2F), or protocol specifications (http://, https://)
- Enforce relative-only redirects where possible (single / prefix)
- If external redirects are necessary, maintain a strict allowlist of permitted domains
- Use URL parsing libraries to normalize and decode URLs before validation to prevent bypass attempts
- Implement Content Security Policy headers to restrict redirect destinations at the browser level
- Log and monitor redirect attempts to identify abuse patterns

## Variant hunting
Test other redirect parameters: ?return=, ?next=, ?goto=, ?url=, ?redirect_uri=
Try double encoding: %252F, %25252F
Test protocol-relative URLs: //attacker.com, \\attacker.com
Attempt backslash variations: \attacker.com
Test data URIs and javascript protocols: javascript:, data:
Check for redirect chains that compound the vulnerability
Test on other Brave subdomains (.sync.brave.com, .api.brave.com, etc.)

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1566.000

## Notes
The vulnerability is straightforward but effective for phishing. The use of path traversal (//) to bypass validation suggests the original validation was likely a simple string prefix check. No bounty amount is disclosed in the public report. This is a common OWASP Top 10 vulnerability that should be caught during basic security code review.

## Full report
<details><summary>Expand</summary>

## What is open redirect
A web application accepts a user-controlled input that specifies a link to an external site, and uses that link in a Redirect. This simplifies phishing attacks.
An http parameter may contain a URL value and could cause the web application to redirect the request to the specified URL. By modifying the URL value to a malicious site, an attacker may successfully launch a phishing scam and steal user credentials. Because the server name in the modified link is identical to the original site, phishing attempts have a more trustworthy appearance.

## Step to reproduce
visit https://account.brave.com//example.com/%2F.. you will redirect to example.com

## POC
{F1446362}

## Fix / prevention
You can prevent redirects to other domains by checking the URL being passed to the redirect function. Make sure all redirect URLs are relative paths – i.e. they start with a single / character. (Note that URLs starting with // will be interpreted by the browser as a protocol agnostic, absolute URL – so they should be rejected too.)

If you do need to perform external redirects, consider whitelisting the individual sites that you permit redirects to.

## Impact

One of the main uses for this vulnerability is to make phishing attacks more credible and effective. When an Open Redirect is used in a phishing attack, the victim receives an email that looks legitimate with a link that points to a correct and expected domain.

Let me know if you have any questions.

thanks & best regards

</details>

---
*Analysed by Claude on 2026-05-24*
