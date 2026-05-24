# SAML Response Reuse Attack on HackerOne SAML Authentication

## Metadata
- **Source:** HackerOne
- **Report:** 888930 | https://hackerone.com/reports/888930
- **Submitted:** 2020-06-01
- **Reporter:** samtink
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** SAML Response Replay Attack, Missing SAML Assertion ID Tracking, Insufficient Token Validation, Session Management Weakness
- **CVEs:** None
- **Category:** auth-crypto

## Summary
HackerOne's SAML authentication endpoint (/users/saml/auth) fails to prevent replay attacks by not tracking previously-used SAML assertions. An attacker who captures a valid SAML response can replay it multiple times to generate new authenticated sessions until the assertion expires. This allows unauthorized account access with the privileges of the compromised user.

## Attack scenario
1. Attacker intercepts SAML response via MITM, phishing, or XSS attack during legitimate user login
2. Attacker extracts the SAML assertion from the POST request body sent to /users/saml/auth
3. Attacker replays the captured SAML response by resending the POST request to HackerOne
4. HackerOne validates the SAML response (signature, expiration) and issues a new session cookie without checking if assertion was previously used
5. Attacker obtains authenticated session as the victim user and can repeat steps 3-4 multiple times
6. Attacker gains access to victim's HackerOne account, potentially viewing confidential vulnerabilities, modifying program settings, or impersonating the organization

## Root cause
HackerOne does not implement SAML assertion replay detection by tracking used assertion IDs. The application validates SAML response signature and expiration time but lacks stateful verification of whether an assertion has already been consumed. This is a critical oversight in SAML protocol implementation as per OASIS specifications which recommend tracking consumed assertions.

## Attacker mindset
An attacker would be motivated to capture a SAML response if they can intercept network traffic (MITM on unencrypted connection, rogue WiFi, network compromise), trick a user into revealing credentials or clicking malicious links (phishing/XSS), or compromise an organization's network. The long TTL of SAML responses (potentially weeks) creates an extended attack window. Once obtained, replaying is trivial and the attacker gains full account access with inherited permissions.

## Defensive takeaways
- Implement SAML assertion ID (NotOnOrAfter) tracking using a database or cache to record consumed assertion IDs and their expiration times
- Reject any SAML response where the assertion ID has already been processed, even if cryptographically valid
- Implement automatic cleanup of expired assertion IDs from the tracking store to prevent unbounded growth
- Consider implementing additional SAML security measures: SubjectConfirmation validation with OneTimeUse restrictions if supported by IdP
- Log all SAML authentication attempts and flag multiple logins from the same assertion ID for security monitoring
- Educate users on SAML security and encourage shorter assertion expiration times (5-15 minutes vs weeks)
- Enforce HTTPS for all SAML flows to prevent MITM interception
- Implement session anomaly detection (multiple simultaneous sessions, geographic impossibilities) as compensating control

## Variant hunting
Check other SSO endpoints for similar replay vulnerabilities (OAuth token reuse, OpenID Connect replay)
Test if assertion binding information (recipient, audience) is properly validated or if they can be modified
Investigate whether multiple SAML assertions from same IdP session can be reused simultaneously
Check if assertion ID tracking is per-user or global (potential for cross-user assertion reuse)
Test encrypted SAML responses - verify assertion ID tracking works for both signed and encrypted assertions
Look for timing windows where assertions consumed in one session can affect tracking in concurrent sessions
Examine if assertion replay protection exists in other authentication flows (OIDC, API token endpoints)

## MITRE ATT&CK
- T1190
- T1556
- T1556.003
- T1550.001
- T1187
- T1598

## Notes
This is a classic SAML replay vulnerability stemming from incomplete protocol implementation. The reporter provided clear reproduction steps and appropriate remediation guidance. The vulnerability's impact is significant given HackerOne's role in vulnerability disclosure and the potential access to undisclosed security issues. The barrier to exploitation is moderate - requiring network access or social engineering to capture a SAML response. The long validity period of SAML responses (potentially weeks) significantly increases practical exploitability. Report ID 888930 demonstrates the importance of tracking assertion consumption state rather than relying solely on cryptographic validation and expiration times.

## Full report
<details><summary>Expand</summary>

**Summary:**
When logging in with SAML, the user's IDP authenticates the user and generates a SAML response. The IDP then redirects the user's browser back to HackerOne to submit the SAML response. Upon receiving the SAML response, HackerOne validates it, sets a session cookie in the user's browser, and logs the user in. The SAML response can be captured and resubmitted to H1 repeatedly until it expires. Every time H1 receives the captured SAML response it sets a new session cookie and logs the user in.

**Description:**

### Steps To Reproduce

1. Make sure your email address is set to use your organization's SSO provider. Make sure you can capture and replay traffic using Burp suite or some other proxy.
2. Go to the H1 login screen and enter your email. Press the login button to be sent to your organization's SAML provider (IDP).
3. Log into your org's IDP and capture the SAML response from the IDP. The request that needs to be captured is the POST request to hackerone.come/users/saml/auth. In the message body you can find the SAML response. The easiest way to capture and replay is to send it to the repeater tab in Burp. 
4. Resend the POST request with the SAML response to H1 and observe the successful response with a new session identifier. Send 4-5 more times and observe the successful responses and new session id's. 

### Your Environment (Browser version, Device, etc)

 * Burp Version: ████████
 * Browser: █████████
 * SSO Provider: █████████
 * SAML Response TTL: ██████████.

### Remediation:

After a SAML response is used store the assertion ID and it's expiration in a list. When a SAML response has been received and validated, check the assertion ID against the previously mentioned list. If the ID is in the list, throw an error and do not log the user in. Once an ID in the list is past it's expiration then remove it from the list (since it will fail anyway for being expired).

## Impact

Likelihood:
There is a fairly high barrier of entry to be able to use this flaw. An attacker would have to obtain a valid SAML response. This could be done via MITM, phishing, XSS, etc. None of which are super easy but none are impossible. The likelihood of an attacker being able to obtain a SAML response varies greatly between different organizations and their respective security postures. The likelihood increases the longer the SAML response is valid for. It can be set to as little as a few minutes or up to several weeks. The organization's IDP is responsible for setting how long a SAML response is valid. 

Impact:
If an attacker would successfully capture and use a SAML response they would log into H1 as the user who generated the SAML response. Depending on which user they log in as they could have full control over an organizations H1 program or they could have only read only permissions. This could allow the attacker to see undisclosed vulnerabilities and full instructions on how to exploit them. The attacker could also pose as a member of the organization and tarnish relations with security researchers. The attacker could lock members of the organization out by removing permissions. So ultimately, the attacker would inherit whatever permissions from the user they stole the SAML response from.

</details>

---
*Analysed by Claude on 2026-05-24*
