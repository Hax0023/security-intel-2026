# Secret App Transmitting Sensitive Data Over HTTP

## Metadata
- **Source:** HackerOne
- **Report:** 12977 | https://hackerone.com/reports/12977
- **Submitted:** 2014-05-23
- **Reporter:** told_snider
- **Program:** Secret
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure Transport, Cleartext Transmission of Sensitive Data, Credential Exposure, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Secret messaging app for iOS and Android was transmitting sensitive user data and API credentials over unencrypted HTTP connections to third-party analytics services (Bugsnag and Flurry). This allowed attackers on the same network to intercept device identifiers, user IDs, API keys, and device information via man-in-the-middle attacks.

## Attack scenario
1. Attacker positions themselves on the same network as a Secret app user (public WiFi, compromised router, etc.)
2. Attacker runs a network sniffer or ARP spoofing tool to intercept traffic between the app and backend services
3. App sends POST request to notify.bugsnag.com over HTTP containing device ID, user ID, and API key
4. Attacker captures the HTTP request and extracts the API key (42062feb3044ef86b492c724ffc87691) and device identifiers
5. Attacker uses captured API key to access analytics data or impersonate the user account
6. Similar interception occurs on iOS when app communicates with data.flurry.com, exposing device architecture, OS version, and unique identifiers

## Root cause
The application developers used HTTP instead of HTTPS for sending telemetry and analytics data to third-party services, likely prioritizing performance or not treating analytics transmissions as sensitive. The absence of certificate pinning and lack of end-to-end encryption compounded the issue.

## Attacker mindset
An attacker would recognize that analytics traffic contains valuable metadata about users and could include API keys for service authentication. Network interception is trivial on unencrypted HTTP, making this low-effort, high-reward for targeting messaging app users to extract identifiers and credentials.

## Defensive takeaways
- Always enforce HTTPS/TLS for all network communications, including analytics and telemetry
- Implement certificate pinning to prevent MITM attacks even if CA is compromised
- Never transmit API keys or authentication credentials to client applications; use server-side authentication only
- Implement security testing in CI/CD pipeline to detect HTTP usage and unencrypted data transmission
- Apply data minimization principle—only transmit necessary analytics data and avoid including sensitive identifiers
- Use OWASP Mobile Security Top 10 as baseline for secure mobile development practices
- Conduct regular network traffic analysis during penetration testing of mobile applications

## Variant hunting
Check for HTTP usage in other third-party integrations (crash reporting, push notifications, ads)
Verify if API keys are hardcoded in the application binary and accessible via reverse engineering
Test other endpoints used by the app for similar unencrypted transmission patterns
Analyze if device identifiers can be used to track or identify users across services
Check if cached analytics data is stored unencrypted in application storage
Test for absence of certificate pinning by attempting to intercept with self-signed certificates

## MITRE ATT&CK
- T1557.002
- T1040
- T1041
- T1020
- T1005

## Notes
This vulnerability affected a security-focused messaging application, making it particularly critical since users trusted the app to protect their privacy. The use of third-party analytics services introduced additional attack surface. The report demonstrates the importance of treating all network communications as sensitive in security-critical applications. The presence of unique device identifiers (UUIDs) enables tracking even without API keys.

## Full report
<details><summary>Expand</summary>

POC for android:

POST /metrics HTTP/1.1
Content-Type: application/json
User-Agent: Dalvik/1.6.0 (Linux; U; Android 4.2.2; google_sdk Build/JB_MR1.1)
Host: notify.bugsnag.com
Connection: Keep-Alive
Accept-Encoding: gzip
Content-Length: 468

{"device":{"id":"6a2be12c-db31-4a3b-9684-f4d5a3e7188a","model":"google_sdk","osVersion":"4.2.2","totalMemory":50331648,"apiLevel":17,"jailbroken":true,"manufacturer":"unknown","locale":"en_US","screenResolution":"728x480","screenDensity":1.5,"osName":"android"},"app":{"releaseStage":"production","packageName":"ly.secret.android","id":"ly.secret.android","version":"1"},"user":{"id":"6a2be12c-db31-4a3b-9684-f4d5a3e7188a"},"apiKey":"42062feb3044ef86b492c724ffc87691"}






POC for IOS:


POST /aas.do HTTP/1.1
Host: data.flurry.com
Proxy-Connection: keep-alive
Accept-Encoding: gzip, deflate
Content-Type: application/octet-stream
Accept-Language: en-us
Accept: */*
Pragma: no-cache
Content-Length: 294
Connection: keep-alive
User-Agent: Secret/3 CFNetwork/672.0.8 Darwin/14.0.0

{F+.QQWQYVHGXCQ4JFYX8HXW3$B51F061B-B2B4-4B61-8695-E9CE5D3772CF$DD8B763A-F256-46BB-A102-4F86171F0B9CÁd)6þ>Ø³@·ÇçØqÙF%4hF+.ß
scr.height480device.archarm32device.os.version7.0.4device.model.1	iPhone4,1	scr.width320âxõÑ





i attached POC images

please fix it by using HTTPS ( secure one )

best regards

</details>

---
*Analysed by Claude on 2026-05-24*
