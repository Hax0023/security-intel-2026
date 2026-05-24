# Widespread SSL Certificate Validation Failures in 75+ Android Applications

## Metadata
- **Source:** HackerOne
- **Report:** 2293 | https://hackerone.com/reports/2293
- **Submitted:** 2014-02-25
- **Reporter:** secbro
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Improper Certificate Validation, Missing Hostname Verification, Broken TLS/SSL Implementation, Man-in-the-Middle (MITM) Vulnerability
- **CVEs:** None
- **Category:** uncategorised

## Summary
A widespread vulnerability affecting approximately 75 Android and iPad applications that fail to properly validate SSL certificates, either ignoring certificate authority validation, hostname verification, or both. The vulnerability could allow attackers to intercept sensitive communications including credit card data and passwords through man-in-the-middle attacks on unencrypted or improperly validated HTTPS connections.

## Attack scenario
1. Attacker positions themselves on the same network as the target user (café WiFi, compromised router, etc.)
2. Attacker intercepts HTTPS traffic from vulnerable app using network sniffing tools
3. Attacker presents their own certificate or a forged certificate authority certificate
4. Due to missing certificate validation, vulnerable app accepts the attacker's certificate without verification
5. App establishes encrypted tunnel with attacker instead of legitimate server
6. Attacker decrypts and harvests sensitive data (credentials, payment info, authentication tokens)

## Root cause
Applications failing to implement proper TLS/SSL certificate validation by: (1) not verifying certificate authority chains, (2) not validating hostname matches certificate CN/SAN fields, (3) disabling certificate verification for debugging and not re-enabling in production, or (4) using outdated or improperly configured HTTP client libraries with insecure defaults

## Attacker mindset
An attacker would target high-value applications handling financial data or authentication (banking apps, payment processors, e-commerce) to intercept credentials and payment information. The widespread nature of this vulnerability across major brands indicates relatively easy exploitation requiring only network-level access, making it attractive for targeted attacks on public WiFi or compromised networks.

## Defensive takeaways
- Implement certificate pinning for critical applications to prevent certificate substitution attacks
- Enforce strict hostname verification matching certificate Subject Alternative Names (SAN)
- Never disable certificate validation in production code; segregate debug configurations
- Use modern TLS libraries (minimum TLS 1.2) and keep them updated
- Perform security code review of all network communication and SSL/TLS implementations
- Test certificate validation with tools like mitmproxy to verify proper validation behavior
- Implement Certificate Transparency (CT) log validation for additional assurance
- Include certificate validation testing in automated security testing pipelines
- Monitor for deprecated HTTP clients and replace with secure alternatives
- Educate developers on secure defaults and common TLS misconfigurations

## Variant hunting
Search for: (1) custom SSL socket factories with overridden verification methods, (2) use of 'accept all certificates' patterns in WebView configurations, (3) disabled hostname verification in HTTP clients (HttpClient, OkHttp, Retrofit), (4) WebView with setWebContentsDebuggingEnabled in production builds, (5) applications using older Android HTTP libraries known to have insecure defaults, (6) network traffic analysis showing HTTPS connections accepting invalid certificates

## MITRE ATT&CK
- T1557.001
- T1557.002
- T1071.001
- T1040

## Notes
This 2014 report represents a critical industry-wide problem that likely persists today. The sheer volume of affected applications (75+) across major brands suggests systematic misunderstanding of TLS implementation among developers. Multiple high-sensitivity applications handling financial data (Capital One, US Bank, American Express) were affected. The researcher's responsible disclosure effort across so many vendors was substantial. Some apps were subsequently fixed (Authy, Uber, Serve), but many others remained vulnerable at time of disclosure. This vulnerability class remains relevant and commonly found in modern app security assessments.

## Full report
<details><summary>Expand</summary>

I have identified approximately 75 Android applications (and some iPad) that fail to validate SSL certificates, either failing to validate valid certificate authorities, correct hostnames or both.

I have made attempts to responsibly disclose all of these vulns to the responsible parties. A few have been omitted from this list for various reasons.

Almost all of these could have lead to credit card and/or password disclosure.

Capital One Spark Pay 0.9.50
Authy 16.3 - fixed
Uber 2.7.13 - fixed
Outlook.com 7.8.2.12.49.2176
Kindle 4.3.0.67
US Bank 1.14.19
ADP Mobile 1.68
Piwik Mobile 1.9.6
Piwik Mobile 2 2.0.1
ClubLocal 1.4
SafeNetMobile Pass 8.3.4.5
TWC TV 3.4.4 #78
BestBuy 7.3.1
Bing 4.2.1.20140123
Walgreens 4.2
SouthWest 2.1.0
CNNMoney 1.01
StumbleUpon 3.2.4
SplashID 7.08 bld 734
Pocket 5.12
Kayako (unsure of version)
Hootsuite 2.5.4.34
Sylphone 5.3.3
Citizen's Bank Champaign Bank
Honeywell TC 2.0 2.2.0
OfficeDepot 2.3.1
Sears 6.1.8
NewEgg 3.2.3
OfficeDepot for Business "BSD" 1.4
Macy's 1.4.1
CostCo 1.5.2
Kmart 6.1.7
SonicWall Mobile Connect 2.0.11
Staples Advantage 1.1
Cisco Technical Support 3.5
Zappos ( iPad)
iTunes Connect (iPad)
Cisco WebEx 4.5.0 (current version)
Oracle Now app v.1.5.1
Lync 2010 4.0.6509.3001
Lync 2013 (v?)
Cisco OnPlus Mobile app 1.1.1001
CA DMV (current version)
Ask.com app v. 2.2.5
WordPress (current version)
GoDaddy v.3.3.2
WD My Cloud v. 3.1.1
Weibo 4.2.6
Huntington Mobile v. 1.6.21
Medscape 3.0.1
My Bluebird v. 2.1.0.0
Dominos
Pizza Hut
Citrix Receiver v. 3.4.13
Orbitz
Kayak Android v. 5.8
Solarwinds Mobile Admin v. 8.1.319643 
Western Union v. 4.2.5
Groupon v. 2.10.3166
Serve (American Express - Fixed)





</details>

---
*Analysed by Claude on 2026-05-24*
