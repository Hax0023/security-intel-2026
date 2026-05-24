# Clickjacking on https://download.nextcloud.com/

## Metadata
- **Source:** HackerOne
- **Report:** 662155 | https://hackerone.com/reports/662155
- **Submitted:** 2019-07-28
- **Reporter:** j4tayu
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, UI Redressing, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The download.nextcloud.com domain is vulnerable to clickjacking attacks due to missing X-Frame-Options HTTP header, allowing the page to be embedded in an attacker-controlled iframe. An attacker can overlay transparent or opaque iframes to trick users into performing unintended actions such as downloading malware, approving changes, or performing account operations.

## Attack scenario
1. Attacker creates malicious HTML page with embedded iframe pointing to https://download.nextcloud.com
2. Attacker overlays transparent or visually deceptive content on top of the iframe to trick user perception
3. Victim visits attacker's malicious site, unaware the page contains embedded Nextcloud content
4. Attacker manipulates victim's clicks using visual tricks (e.g., fake download buttons, consent prompts) that actually click elements within the Nextcloud iframe
5. Victim unknowingly triggers unintended actions on download.nextcloud.com within their authenticated session
6. Attacker could facilitate malware distribution, credential harvesting, or unauthorized file operations

## Root cause
The download.nextcloud.com server fails to implement the X-Frame-Options HTTP response header (or Content-Security-Policy frame-ancestors directive), allowing the page to be embedded in frames from any origin without restriction.

## Attacker mindset
An attacker seeks to exploit trust in the Nextcloud brand and service to perform social engineering at scale, redirecting user intent toward malicious outcomes while maintaining plausible deniability through third-party framing.

## Defensive takeaways
- Implement X-Frame-Options: DENY or SAMEORIGIN header on all HTTP responses
- Deploy Content-Security-Policy with frame-ancestors 'none' or 'self' directive as defense-in-depth
- Regularly audit security headers using automated scanning tools
- Implement frame-busting JavaScript as supplementary mitigation
- Apply security headers consistently across all subdomains (download., www., etc.)
- Consider SameSite cookie flags to mitigate session hijacking via clickjacking

## Variant hunting
Search for other Nextcloud subdomains (account.nextcloud.com, talk.nextcloud.com, etc.) lacking frame protection; test third-party services integrated with Nextcloud that may expose similar framing vulnerabilities; examine any user-facing endpoints accepting sensitive actions without frame protection.

## MITRE ATT&CK
- T1189 Service Exploitation
- T1190 Exploit Public-Facing Application
- T1055 Process Injection
- T1598 Phishing - Spearphishing Link

## Notes
This is a straightforward clickjacking report demonstrating the vulnerability clearly. The reporter's English limitations do not diminish the validity of the finding. Nextcloud should prioritize remediation given the reputational and security risks associated with a development/download platform being vulnerable to clickjacking attacks that could facilitate malware distribution.

## Full report
<details><summary>Expand</summary>

the vulnerability is Clickjacking

Steps for Reproduce:

1. Create a script like this
<title> Clickjacking! </ title>
<p> The Site is Vulnerability Clickjacking </ p>
<iframe src = "https://www.download.nextcloud.com" height = "700px" width = "700px"> </ iframe>

2. Enter a file name after saving it in the .html format
Then the web is Vuln Clickjacking

Sorry bad english (im indonesian)

## Impact

By using Clickjacking technique, an attacker hijack's click's
meant for one page and route them to another page, most likely
for another application, domain, or both.

</details>

---
*Analysed by Claude on 2026-05-24*
