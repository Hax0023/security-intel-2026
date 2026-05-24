# Hard-coded API Keys in NordVPN Android App Resources

## Metadata
- **Source:** HackerOne
- **Report:** 792850 | https://hackerone.com/reports/792850
- **Submitted:** 2020-02-11
- **Reporter:** dantt
- **Program:** NordVPN
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cleartext Storage of Sensitive Information, Exposed Credentials, Insecure Configuration Management
- **CVEs:** None
- **Category:** uncategorised

## Summary
Hard-coded API keys (Google API key and Stripe publishable key) were found in plain text within the Android app's strings.xml resource file. These sensitive credentials were discoverable through APK decompilation, exposing them to potential abuse.

## Attack scenario
1. Attacker downloads NordVPN Android app APK from Play Store
2. Attacker decompiles APK using tools like apktool or JADX
3. Attacker extracts res/values/strings.xml resource file
4. Attacker identifies hard-coded Google and Stripe API keys in plain text
5. Attacker can abuse Google API key for quota theft or unauthorized service access
6. Attacker can use Stripe publishable key to gather customer payment information or manipulate transactions

## Root cause
Development credentials embedded directly in app source code without abstraction layer or secure configuration management; improper release builds that fail to strip sensitive data during compilation

## Attacker mindset
An attacker performing reconnaissance on mobile apps can quickly decompile APKs to extract hardcoded secrets for API abuse, payment fraud, or further lateral movement into backend services

## Defensive takeaways
- Never store API keys or secrets in application source code or resources
- Use secure configuration management systems or environment variables for sensitive credentials
- Implement API key rotation policies and monitor usage patterns for anomalies
- Use build-time obfuscation and code stripping for production releases
- Separate publishable and secret keys; use only publishable keys client-side with proper restrictions
- Regularly audit decompiled APKs during development to detect exposed secrets
- Implement certificate pinning to prevent man-in-the-middle attacks on API communications
- Monitor for unauthorized API usage and revoke compromised keys immediately

## Variant hunting
Search for other hard-coded credentials in AndroidManifest.xml, build.gradle, or other resource files
Check for AWS access keys, Firebase database URLs, or OAuth tokens in app resources
Inspect native libraries (.so files) for embedded credentials using string extraction tools
Review shared preferences and cached data storage for leaked secrets
Examine decompiled Java code for credentials passed as string literals in method calls
Check for secrets in app signing certificates or release notes

## MITRE ATT&CK
- T1552.001
- T1513
- T1555.005

## Notes
Publishable Stripe keys are designed for client-side use but should still be protected and monitored for abuse. Google API keys without proper restrictions can be throttled or hijacked. The vulnerability demonstrates why APK security analysis should be part of secure SDLC. Report lacks specific bounty amount but represents significant credential exposure risk.

## Full report
<details><summary>Expand</summary>

Hello NordVpn,

**APK Version : 4.6.2**
**API'S at res/values/strings.xml**

>**Google**
>google_api_key = ███
**Stripe**
>stripe_publishable_api_key = ██████████

**Referance;** 
>https://stripe.com/docs/keys

## Impact

Cleartext Storage of Sensitive Information

</details>

---
*Analysed by Claude on 2026-05-24*
