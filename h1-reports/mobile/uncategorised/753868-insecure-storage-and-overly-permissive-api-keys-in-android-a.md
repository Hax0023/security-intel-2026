# Insecure Storage and Overly Permissive API Keys in Android App

## Metadata
- **Source:** HackerOne
- **Report:** 753868 | https://hackerone.com/reports/753868
- **Submitted:** 2019-12-08
- **Reporter:** ticzox
- **Program:** HackerOne (unspecified program)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Insecure Storage, Hardcoded Credentials, Exposure of Sensitive Information, Insufficient Access Controls
- **CVEs:** None
- **Category:** uncategorised

## Summary
API keys and authentication tokens were hardcoded as string literals in the Android application source code, exposing them to extraction via APK decompilation. An attacker could extract these credentials and use them to make unauthorized API requests on behalf of the application, potentially leading to data theft, manipulation, and service abuse.

## Attack scenario
1. Attacker downloads the legitimate APK from Google Play Store or alternative sources
2. Attacker uses a decompiler (e.g., jadx, apktool) to extract and analyze the application source code
3. Attacker searches for hardcoded strings, constants, and configuration data in the decompiled code
4. Attacker identifies exposed API keys, tokens, and authentication credentials in plaintext
5. Attacker uses extracted credentials to craft malicious API requests impersonating the legitimate application
6. Attacker exploits the compromised credentials to access backend services, exfiltrate data, or manipulate user information

## Root cause
Developers stored sensitive API keys and authentication tokens as hardcoded string literals directly in the application source code for convenience, without implementing proper secure storage mechanisms or key management practices.

## Attacker mindset
An attacker with basic reverse engineering skills can easily decompile public APKs to extract hardcoded credentials. While the writeup suggests data pollution may be unprofitable, motivated attackers can monetize compromised API keys through data exfiltration, service abuse, credential resale, or launching attacks against backend infrastructure.

## Defensive takeaways
- Never hardcode API keys, tokens, or sensitive credentials in application source code
- Use secure storage mechanisms: Android Keystore, EncryptedSharedPreferences, or encrypted file-based storage
- Implement key rotation and expiration policies for API credentials
- Use certificate pinning to prevent MITM attacks even if credentials are compromised
- Deploy server-side rate limiting and usage monitoring to detect anomalous API activity
- Implement API key scoping to limit permissions and restrict credential usage to necessary endpoints
- Use environment-specific keys and avoid deploying production credentials in debug/test builds
- Regularly scan codebase and binaries for hardcoded secrets using automated tools
- Implement certificate-based authentication or OAuth 2.0 instead of static API keys where possible

## Variant hunting
Search Android applications for patterns: hardcoded strings matching API key formats (AWS, Google Cloud, Firebase, Stripe, etc.), base64-encoded credentials in manifest/dex files, environment variables leaked in logcat, credentials in WebView JavaScript objects, API endpoints with embedded authentication parameters, unencrypted SharedPreferences containing tokens

## MITRE ATT&CK
- T1552.001 - Unsecured Credentials: Credentials In Files
- T1552.007 - Unsecured Credentials: Hardcoded Secrets
- T1647 - Exfiltration Over C2 Channel
- T1589.001 - Gather Victim Identity Information: Credentials
- T1190 - Exploit Public-Facing Application

## Notes
The writeup lacks detail on specific affected endpoints, the scope of API key permissions, and potential business impact. The assertion that data pollution is 'rarely profitable' underestimates risks including competitive intelligence gathering, backend resource exhaustion, and lateral movement into connected systems. Server-side filtering alone is insufficient mitigation; credentials must be protected at the application level through secure storage and key management.

## Full report
<details><summary>Expand</summary>

#Description:
Most often Developers for their ease of use,leave API keys and some sensitive keys ,Tokens as hardcoded strings,which isn't really a good ideas as it can result in Leaks of sensitive information getting in Wrong Hands which indeed can results in Data theft and Tampering with how the application deals with the data, and API requests the application Makes.

==I found a bunch of API keys,Tokens.==

#To Check API keys leaks Sensitive Information or not
https://github.com/streaak/keyhacks

#Steps to reproduce.
1.Decomiple the app.
2.Look for sensitive information


#Proof of Concept:
Screenshots has been attached as a proof of concept.

## Impact

If an attacker decompiles your apk, and extracts your token, they can indeed maliciously send traffic on your behalf.
This is the case with pretty much every single one of the web  companies out there (google included).
The main thing to know however, is that it is rarely useful for people to do this. Polluting someone else's data  while possible, isn't exactly a profitable thing to do. You can also create server-side filters to help prevent this thing from happening.

</details>

---
*Analysed by Claude on 2026-05-24*
