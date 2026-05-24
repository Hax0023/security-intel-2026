# Coinbase Android Multiple Critical Security Vulnerabilities

## Metadata
- **Source:** HackerOne
- **Report:** 5786 | https://hackerone.com/reports/5786
- **Submitted:** 2014-03-11
- **Reporter:** bryanstern
- **Program:** Coinbase
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Improper Certificate Validation, Man-in-the-Middle (MITM) Attack, Hardcoded Credentials, Lack of Request Signing, Request Replay Vulnerability, Missing Code Obfuscation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Coinbase Android application fails to perform SSL certificate verification, allowing attackers to intercept and modify API communications through MITM attacks. Combined with hardcoded OAuth credentials in the public GitHub repository and unsigned API requests, attackers can hijack user accounts, manipulate financial transactions, and impersonate the legitimate application to the API backend.

## Attack scenario
1. Attacker sets up a proxy server (e.g., Charles Proxy) and configures the target Android device to route traffic through it
2. Attacker installs a self-signed SSL certificate on the device, which the app accepts due to missing certificate validation
3. Attacker intercepts API requests between the app and Coinbase servers, viewing sensitive data including access tokens
4. Attacker extracts the hardcoded OAuth consumer ID and secret from intercepted requests or the public GitHub repository
5. Attacker replays or modifies financial transaction requests (buy/sell/transfer Bitcoin) by tampering with request parameters in transit
6. Attacker uses the stolen access token and public credentials to make unauthorized API calls, bypassing the compromised app entirely

## Root cause
The application was developed without implementing proper transport security validation (SSL pinning or certificate verification), API request authentication (request signing with nonces), secure credential management (hardcoding secrets in source code), and code protection mechanisms (ProGuard obfuscation). These represent fundamental security misconfigurations in the initial design and deployment.

## Attacker mindset
A moderately skilled attacker with network interception capabilities can completely compromise user financial accounts. The low barrier to entry (freely available proxy tools) combined with publicly disclosed credentials makes this highly exploitable. The attacker gains both passive surveillance and active manipulation capabilities without requiring sophisticated exploitation techniques.

## Defensive takeaways
- Implement SSL certificate pinning or strict certificate validation using Android Security Library to prevent MITM attacks
- Sign all API requests using OAuth 1.0a or similar protocol with nonces and timestamps to prevent replay and tampering attacks
- Never hardcode credentials in application source code; use secure credential management systems and rotate exposed secrets immediately
- Implement ProGuard or similar code obfuscation to increase reverse engineering difficulty and protect logic
- Conduct regular security audits of public repositories for accidentally committed secrets and credentials
- Use Android Network Security Configuration to enforce certificate pinning at the framework level
- Implement request-level message authentication codes (HMAC) independent of SSL for defense-in-depth
- Establish a secure secret management pipeline separate from application code distribution

## Variant hunting
Search for similar patterns in other mobile banking/financial applications: hardcoded OAuth credentials in GitHub, missing SSL validation in Android apps, unsigned API request implementations, and lack of certificate pinning. Examine other Coinbase products (web, other mobile platforms) for identical credential exposure. Review GitHub for other projects with similar LoginManager.java implementations that expose consumer secrets.

## MITRE ATT&CK
- T1557.002 - Adversary-in-the-Middle: SSL Stripping
- T1187 - Man in the Browser
- T1555.005 - Credentials from Password Managers: Local
- T1539 - Steal Web Session Cookie
- T1111 - Multi-Factor Authentication Interception
- T1621 - Multi-Factor Authentication Failure
- T1598 - Phishing: Spearphishing Link
- T1040 - Traffic Signaling

## Notes
This report demonstrates a complete failure of foundational mobile security principles. The combination of three critical vulnerabilities creates a cascading failure where each individually severe issue compounds the others. The public availability of credentials in GitHub suggests this was deployed to production without security code review. The 3-week disclosure timeline indicates this was a serious production vulnerability affecting real financial accounts. This case became a seminal example of mobile security anti-patterns in the industry.

## Full report
<details><summary>Expand</summary>

My name is Bryan Stern and I am Android Software Engineer. Last night I took another look at your Android application and found some disturbing vulnerabilities that could allow for a user's account to be hijacked. Fortunately, they are very easy to resolve. Below I have outlined the issue, gave some recommendations, and attached some screenshots.

**Coinbase for Android Security Flaws:**

1. The application does not perform any SSL certificate verification.
2. The API design does not prevent request tampering or replays.
3. The consumer id and secret of the app is widely available.

**Potential for damage:**

1. Without implementing your own SSL certificate validation in the Coinbase app, a "man in the middle" can sniff and alter communication between the application and Coinbase API. A malicious hacker could then use this to violate user privacy as well as take advantage of the other two flaws listed. Worse, an attacker could steal the access token provided in network responses and have full API access to the user's Coinbase account using the widely available Coinbase Android consumer id and secret.
2. Because requests are neither adequately protected by SSL, nor are they signed, an attacker could repeat or tamper with requests. For example, an attacker could repeat requests to buy bitcoin, sell bitcoin, or send bitcoin requests from the app to either empty their associated bank account, sell bitcoins needed by the user, or repeat a transfer bitcoins to another account. Not only can transactions be repeated, they can be modified in transit. So, for example, an attacker could change the recipient (and/or amount) of a transaction request.
3. The consumer id and secret exposure means that their is no trusted secret between the Coinbase Android app and the Coinbase API. This means any program could make requests to the Coinbase API pretending to be the Coinbase Android app. You would not be able to block the abuser of the Coinbase API without disabling the Coinbase Android app until a new build with a new consumer id and secret was distributed.

**How to establish the man in the middle attack on Android**

1. Set up a proxy server that the Android device will route traffic through. I use www.charlesproxy.com for this.
2. Install the SSL certificate on the device that the proxy will present as Coinbase's SSL certificate to it's clients. (www.charlesproxy.com/charles.crt)
3. Configure your device to point it's traffic through Charles.
4. Enable SSL 
5. View, repeat, and modify requests in Charles Proxy.

**Availability of the Consumer Id and Secret**

1. It is publicly available in the GitHub repository. (https://github.com/coinbase/coinbase-android/blob/bc6a03229416736acc2ea6bc2fb13f55f7029751/coinbase-android/src/com/coinbase/api/LoginManager.java#L49)
2. It is visible in many requests made by the device when monitoring requests during the man in the middle attack.

**Recommendations:**

1. Read the Android Documentation on SSL. 
2. Sign OAuth requests and use nonces. See Twitter's documentation for an example. https://dev.twitter.com/docs/auth/creating-signature
3. Change your consumer id and secret and keep them confidential. There is no need to ever send the consumer secret if requests are signed using it.
4. Based on the [available source code](https://github.com/coinbase/coinbase-android), I see that ProGuard is not being used. I highly recommend it both to obfuscate your compiled code and for some of the optimizations available.

----

Please let me know how much time you may need to resolve these issue as I would like to publish this on my own blog soon (~3 weeks). If you have any questions, I would be more than happy to answer any questions and walk your developers through the issues.

Best Regards,
Bryan Stern

</details>

---
*Analysed by Claude on 2026-05-24*
