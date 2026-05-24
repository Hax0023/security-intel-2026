# Denial of Service via Password Reset Request Flooding

## Metadata
- **Source:** HackerOne
- **Report:** 812754 | https://hackerone.com/reports/812754
- **Submitted:** 2020-03-07
- **Reporter:** makerlab
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Insufficient Rate Limiting
- **CVEs:** CVE-2020-8295
- **Category:** memory-binary

## Summary
A password reset endpoint in Nextcloud lacks proper rate limiting, allowing attackers to exhaust PHP worker processes by sending rapid reset requests. Each request takes ~30 seconds due to brute-force protection, and sending just 1000 requests can render the entire server unresponsive for extended periods.

## Attack scenario
1. Attacker navigates to Nextcloud login page and clicks 'Forgot password?' button
2. Attacker enters any value in the email/username field
3. Attacker opens browser developer tools and identifies the password reset endpoint
4. Attacker sends rapid successive requests to the reset endpoint (via automated script or holding Enter key)
5. Each request blocks a PHP worker for ~30 seconds due to brute-force protection logic
6. With sufficient concurrent requests (e.g., 1000), all available PHP workers become exhausted, causing DoS for legitimate users

## Root cause
The password reset endpoint implements brute-force protection that artificially delays responses (30 seconds per request), but fails to implement per-IP or per-user rate limiting. This allows attackers to overwhelm the limited PHP worker pool without authentication, as there is no mechanism to throttle or block rapid sequential requests from the same source.

## Attacker mindset
An attacker with minimal technical skill can execute this attack unauthenticated from a single machine or distributed sources. The low barrier to entry (simple form submission automation) combined with high impact (complete service disruption) makes this an attractive DoS vector. The attacker seeks to maximize resource consumption relative to the effort required.

## Defensive takeaways
- Implement strict per-IP rate limiting on password reset endpoints (e.g., 3-5 requests per hour per IP)
- Use token-based or challenge-response mechanisms instead of arbitrary delays for brute-force protection
- Implement request queuing or circuit breakers to prevent worker pool exhaustion
- Add CAPTCHA or other anti-automation measures to unauthenticated sensitive endpoints
- Monitor and alert on unusual spike in password reset requests from single IPs
- Consider blocking or rate-limiting reset requests for non-existent accounts
- Implement adaptive rate limiting that tightens restrictions during attack patterns
- Use reverse proxy (nginx/HAProxy) to enforce rate limits before reaching PHP workers

## Variant hunting
Check other unauthenticated endpoints (2FA reset, account recovery, contact forms) for similar rate-limiting gaps
Test if the 30-second delay is synchronous blocking or async - async might use different resource exhaustion vectors
Verify if the brute-force protection is cumulative per account or per IP, and if attackers can target multiple accounts simultaneously
Test password reset with valid vs invalid email addresses to identify if response times differ
Check if email verification is required - if not, attackers can also spam arbitrary email addresses
Look for similar patterns in other Nextcloud modules (share links, API endpoints, WebDAV)
Test if request cancellation or connection resets release PHP workers or keep them blocked

## MITRE ATT&CK
- T1499.4
- T1498.1
- T1190
- T1526

## Notes
This is a classic resource exhaustion vulnerability combining weak rate limiting with resource-intensive operations. The 30-second delay per request is the core issue - it was intended as brute-force protection but becomes a DoS amplification mechanism without horizontal request limiting. The report demonstrates real-world impact on demo2.nextcloud.com, showing the attack reliably extends downtime to 1 hour with just 1000 requests.

## Full report
<details><summary>Expand</summary>

## Description:
I believe that this is posible due to the brute force protection that makes all request last for 30 seconds which in this case is using all the PHP workers avalible in the pool, so the only way to defend yourself is setting up a limit or having a lot of resources.

### How to reproduce:
* In the Nextcloud login screen click the "Forgot password?" button and then type something in the textbox (can be anything)
* Then open the developers tools and go to the network tab
* Hold the "enter" key after pressing the reset password button and in the network tab you will see a lot of request being made
* With just 1000 request I managed to make the demo server "https://demo2.nextcloud.com/" not respond for 1 hour

## Impact

The attacker could make an entire nextcloud installation or even the entire server where it is hosted not respond for a very long time
Also, this attack can be made by almost anyone

</details>

---
*Analysed by Claude on 2026-05-24*
