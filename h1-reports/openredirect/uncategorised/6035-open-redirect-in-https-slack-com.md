# Open Redirect in slack.com/link endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 6035 | https://hackerone.com/reports/6035
- **Submitted:** 2014-04-06
- **Reporter:** ipk1
- **Program:** Slack
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
The /link endpoint on slack.com fails to validate redirect URLs, allowing attackers to redirect users to arbitrary external websites. An attacker can craft a malicious link using the vulnerable endpoint to redirect Slack users to phishing or malicious sites without validation or user notification.

## Attack scenario
1. Attacker identifies the /link endpoint accepts an unvalidated url parameter
2. Attacker crafts a malicious URL: https://slack.com/link?url=http://attacker-phishing-site.com
3. Attacker distributes the link via email, messages, or social engineering targeting Slack users
4. Victim clicks the link, trusting it originates from slack.com
5. Victim is silently redirected to the attacker's phishing or malware site
6. Attacker harvests credentials or delivers malware via the trusted-looking Slack domain

## Root cause
The /link endpoint implements insufficient URL validation, failing to whitelist safe domains or verify that redirects point to trusted locations. No warning or confirmation dialog is presented to users before redirect execution.

## Attacker mindset
An attacker would exploit this to create convincing phishing attacks leveraging Slack's trusted domain reputation. The silent redirect enhances deception, as users see the slack.com domain in their browser before being redirected without explicit notification.

## Defensive takeaways
- Implement strict URL whitelist validation for all redirect parameters
- Require explicit user confirmation before redirecting to external domains
- Display warning message indicating user is leaving Slack domain
- Use safe redirect patterns that validate domain ownership
- Implement Content Security Policy to restrict redirect destinations
- Log all redirect attempts for security monitoring and anomaly detection
- Disable HTTP in favor of HTTPS-only redirects to prevent downgrade attacks

## Variant hunting
Check other endpoints using url, redirect, return, next, goto parameters
Test for double encoding bypass: url=http%3A%2F%2Fattacker.com
Test protocol handlers: javascript:, data:, vbscript: protocols
Test same-site redirects: //slack.com.attacker.com (scheme-relative)
Check for whitelist bypasses using subdomains or path manipulation
Test POST method redirects if GET is protected
Analyze API endpoints for redirect vulnerabilities

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1566.001 - Phishing: Spearphishing Attachment
- T1192 - Spearphishing Link

## Notes
Open redirects are commonly underestimated but highly effective for phishing attacks due to domain spoofing. The combination of a trusted source (Slack) with silent redirection significantly increases attack success rates. This vulnerability is particularly dangerous for enterprise users who may be targeted in spear-phishing campaigns.

## Full report
<details><summary>Expand</summary>

Navigate to Https://slack.com
append "/link?url=url=http://bing.com" or enter any website of your choice with http://
vulnerable link https://slack.com/link?url=http://bing.com
notice that user is redirected to bing.com without being validated or notified

</details>

---
*Analysed by Claude on 2026-05-24*
