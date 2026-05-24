# Open Redirect in Slack Link Handler

## Metadata
- **Source:** HackerOne
- **Report:** 4549 | https://hackerone.com/reports/4549
- **Submitted:** 2014-03-22
- **Reporter:** prakharprasad
- **Program:** Slack
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Slack link parameter endpoint failed to validate redirect destinations, allowing attackers to craft malicious URLs that redirect users to arbitrary external sites. This was exploitable through the `/link?url=` parameter which accepted unvalidated user-supplied URLs.

## Attack scenario
1. Attacker crafts a malicious Slack URL with an arbitrary external URL in the url parameter
2. Attacker shares this link in Slack messages, channels, or embeds it in phishing content
3. Slack user clicks the link trusting the slack.com domain
4. User is transparently redirected to attacker-controlled site (e.g., phishing page mimicking Slack login)
5. Attacker harvests credentials or deploys malware via fake Slack login page
6. User's Slack credentials or session tokens are compromised

## Root cause
The `/link` endpoint accepted the `url` parameter without validation or allowlisting, directly redirecting to any user-supplied destination without domain verification or safety checks.

## Attacker mindset
Exploiting trust in known domains to bypass user security awareness. Users are conditioned to trust slack.com URLs, making this effective for credential harvesting and phishing campaigns.

## Defensive takeaways
- Implement whitelist-based redirect validation - only allow redirects to known safe domains
- If external redirects are necessary, use an intermediate verification page warning users
- Validate and sanitize all URL parameters against a strict allowlist
- Implement anti-phishing measures like content security policy headers
- Log all redirect attempts for security monitoring
- Educate users about verifying URLs before clicking, especially checking for redirect chains

## Variant hunting
Check other redirect endpoints: `/go?`, `/r?`, `/redirect?`, `/exit?`
Test parameter variations: `return_url`, `next`, `target`, `destination`, `redirect_uri`
Look for authenticated redirect endpoints that may have different validation
Check mobile app redirect handlers and deep linking mechanisms
Test encoded/obfuscated URLs in the parameter
Verify if internal Slack domains can be redirected to (potential information disclosure)

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1187 - Forced Authentication
- T1192 - Spearphishing Link

## Notes
Classic open redirect vulnerability with high phishing potential due to the trusted Slack domain. Particularly dangerous in enterprise environments where Slack is widely used. The simplicity of exploitation makes this a high-impact issue despite medium severity rating. Early HackerOne report (ID 4549) indicating this was discovered during early bug bounty program phases.

## Full report
<details><summary>Expand</summary>

This link shall redirect to google.co.in: http://prakhar.slack.com/link?url=http%3A%2F%2Fgoogle.co.in

Straight, open redirection!

Thanks!


</details>

---
*Analysed by Claude on 2026-05-24*
