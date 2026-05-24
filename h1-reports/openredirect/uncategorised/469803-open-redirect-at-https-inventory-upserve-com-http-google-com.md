# Open Redirect in inventory.upserve.com

## Metadata
- **Source:** HackerOne
- **Report:** 469803 | https://hackerone.com/reports/469803
- **Submitted:** 2018-12-18
- **Reporter:** stankoja
- **Program:** Upserve
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
The inventory.upserve.com application accepts arbitrary URLs in its path and redirects users to them without proper validation. An attacker can craft a URL that redirects legitimate users to a malicious domain by embedding the target URL directly in the path component.

## Attack scenario
1. Attacker identifies the open redirect vulnerability in inventory.upserve.com path handling
2. Attacker crafts a malicious URL: https://inventory.upserve.com/http://attacker.com/phishing
3. Attacker distributes the link via email, social media, or other channels to target users
4. User clicks the link trusting the inventory.upserve.com domain
5. Application redirects user to attacker.com without validation
6. Attacker's site can perform credential harvesting, malware distribution, or social engineering

## Root cause
The application improperly parses and validates URL paths without sanitizing or validating redirect destinations. The path component is treated as a redirect target without checking against a whitelist or ensuring it belongs to a trusted domain.

## Attacker mindset
Leverage the trusted Upserve brand to bypass user skepticism of links. Use in phishing campaigns where users are more likely to click links from known business domains. Combine with spear phishing for credential theft or malware delivery.

## Defensive takeaways
- Implement strict URL validation using a whitelist of allowed redirect destinations
- Validate that redirect URLs are relative paths or belong to explicitly allowed domains
- Use URL parsing libraries correctly to avoid bypasses from malformed URLs
- Implement HTTP security headers like Referrer-Policy to limit information leakage
- Log and alert on suspicious redirect attempts for security monitoring
- Educate users to verify URLs in the address bar before entering credentials

## Variant hunting
Search for similar path-based redirect patterns in other URL paths on the domain
Test parameter-based redirects (redirect=, return_to=, next=, url=)
Check for double URL encoding bypasses (http%3A%2F%2F)
Test protocol handling (javascript:, data:, file://)
Look for redirect logic in API endpoints that might accept URLs
Test for redirect chains that bypass single-level validation

## MITRE ATT&CK
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing for Information: Spearphishing Link
- T1187 - Forced Phishing

## Notes
This is a classic open redirect vulnerability with low technical complexity but significant social engineering impact. The vulnerability is particularly dangerous because it leverages trust in the legitimate domain. The report lacks specific timeline information and bounty amount, suggesting it may have been resolved without explicit reward disclosure.

## Full report
<details><summary>Expand</summary>

The following URL is vulnerable to an open redirect (it will redirect to stanko.sh):

https://inventory.upserve.com/http://stanko.sh/

## Impact

Users could get redirected to malicious domain.

</details>

---
*Analysed by Claude on 2026-05-24*
