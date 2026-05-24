# Coinbase Android Application - Bitcoin Wallet Leaks OAuth Response Code via Logcat

## Metadata
- **Source:** HackerOne
- **Report:** 5314 | https://hackerone.com/reports/5314
- **Submitted:** 2014-03-31
- **Reporter:** prakharprasad
- **Program:** Coinbase
- **Bounty:** Not specified in report
- **Severity:** HIGH
- **Vuln:** Information Disclosure, Insecure Logging, OAuth Implementation Flaw, Hardcoded Credentials, Insufficient Access Controls
- **CVEs:** None
- **Category:** web-api

## Summary
The Coinbase Android application logs sensitive OAuth response codes to system logcat, which can be read by any application on the device or via adb commands. Combined with a hardcoded client secret in the application, an attacker can exchange this response code for an access token, leading to account compromise.

## Attack scenario
1. Attacker installs malicious application on victim's device with READ_LOGS permission (or uses adb with physical access)
2. Victim opens Coinbase app and authenticates via OAuth flow
3. Coinbase app logs the OAuth response code to logcat in plaintext
4. Attacker's malicious app reads logcat output or attacker uses adb logcat command to extract response code
5. Attacker extracts hardcoded client_secret from Coinbase APK via reverse engineering
6. Attacker sends token exchange request to Coinbase OAuth endpoint with stolen response code and client_secret to obtain access_token
7. Attacker gains unauthorized access to victim's Coinbase account and cryptocurrency assets

## Root cause
The application logs OAuth sensitive values (response codes) to system logcat without redaction, and relies on client_secret as a security boundary despite it being embedded in the APK where it can be reverse engineered. OAuth response codes should never be logged, and implicit trust in client_secret in client-side applications is inherently insecure.

## Attacker mindset
An attacker with local device access or ability to install applications seeks to escalate privileges and obtain financial access by harvesting OAuth credentials. The combination of two weaknesses (logging + hardcoded secret) creates a critical attack chain. This is attractive for financially motivated attackers targeting cryptocurrency holders.

## Defensive takeaways
- Never log OAuth tokens, response codes, or other sensitive authentication material to any logging system (logcat, file logs, crash logs)
- Never hardcode secrets (client_secret, API keys) in client-side mobile applications; use server-side OAuth token exchange instead
- Implement token rotation and expiration policies for OAuth flows
- Use PKCE (Proof Key for Code Exchange) for OAuth on mobile clients to eliminate reliance on client_secret
- Sanitize and redact sensitive values before logging any debugging information
- Use Android Security Logging APIs that respect LogCat permission boundaries
- Implement certificate pinning and additional runtime integrity checks
- Request minimal permissions (avoid unnecessary READ_LOGS-like capabilities)
- Conduct regular security code reviews focused on credential handling in authentication flows

## Variant hunting
Check for other sensitive tokens logged to logcat: refresh tokens, access tokens, session IDs, API keys
Search for other hardcoded secrets in Coinbase APK: database passwords, encryption keys, API credentials
Test other Coinbase applications (web, desktop) for similar OAuth implementation flaws
Review other OAuth implementations in popular crypto/finance apps for identical vulnerabilities
Check if response codes are logged in crash reports, analytics, or error reporting services
Test for sensitive data in app backup files and bundle caches
Verify if SharedPreferences or SQLite databases store unencrypted OAuth tokens

## MITRE ATT&CK
- T1557 - Adversary-in-the-Middle
- T1555 - Credentials from Password Stores
- T1187 - Forced Authentication
- T1621 - Multi-Stage Channels
- T1111 - Multi-Factor Authentication Interception
- T1056.004 - Keylogging
- T1052 - Exfiltration Over Physical Medium

## Notes
This report highlights a critical vulnerability chain in mobile OAuth implementations. The severity is amplified by the financial nature of the application (cryptocurrency access). The vulnerability requires local access or a malicious application but impacts confidentiality and integrity significantly. Similar patterns were previously disclosed in Facebook OAuth implementation (referenced report). The POC video demonstration confirms practical exploitability. Modern best practices (PKCE, server-side token exchange) would completely mitigate this vulnerability class.

## Full report
<details><summary>Expand</summary>

Hi,

There's a simple bug here, the Coinbase Android App. "BitCoin Wallet" leaks the **OAuth** Response Code which can be obtained using `adb logcat -s Coinbase` command line for testing, and any Android application on the same phone can read the response code for the user by reading the logs. As of now nothing can be harmed with OAuth Response code, but along with the hardcoded `client secret` we can obtain the `access_token`.

This bug is similar to this - http://attack-secure.com/all-your-facebook-access-tokens-are-belong-to-us/

So using the stolen response code and `client secret` we can derive the `access_token`

POC: https://www.dropbox.com/s/zionksi1pt7lot5/Coinbase-Android.mov

</details>

---
*Analysed by Claude on 2026-05-24*
