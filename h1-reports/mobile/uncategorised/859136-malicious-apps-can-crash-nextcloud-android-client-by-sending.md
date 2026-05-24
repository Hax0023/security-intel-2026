# Malicious apps can crash Nextcloud Android client by sending malformed intents

## Metadata
- **Source:** HackerOne
- **Report:** 859136 | https://hackerone.com/reports/859136
- **Submitted:** 2020-04-25
- **Reporter:** bigbug
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service, Unhandled Exception, Intent Hijacking, Crash via Malformed Input
- **CVEs:** CVE-2021-32694
- **Category:** uncategorised

## Summary
The Nextcloud Android client registers a deeplink handler (nc://login) in ModifiedAuthenticatorActivity that fails to properly handle malformed intent data, allowing malicious applications to crash the client. The parseLoginDataUrl method throws an unhandled exception when processing incomplete or malformed login URIs, causing a denial of service.

## Attack scenario
1. Attacker develops a malicious Android application with access to send intents
2. Attacker crafts a malformed intent with URI nc://login lacking required parameters
3. Attacker sends intent to Nextcloud client via am start command or Intent.startActivity()
4. ModifiedAuthenticatorActivity receives the intent and invokes parseLoginDataUrl
5. parseLoginDataUrl throws an unhandled exception due to missing data parsing
6. Nextcloud application crashes, denying service to legitimate user

## Root cause
The parseLoginDataUrl method in ModifiedAuthenticatorActivity does not implement proper input validation or exception handling for malformed login URIs. The method likely attempts to parse URI components (scheme, host, parameters) without null checks or try-catch blocks, causing NullPointerException or similar runtime exceptions when expected data is missing.

## Attacker mindset
An attacker could abuse this vulnerability to repeatedly crash the Nextcloud client, degrading user experience and preventing legitimate access to cloud storage features. This could be used as a harassment vector or combined with other attacks to prevent users from accessing time-sensitive files.

## Defensive takeaways
- Implement comprehensive input validation for all intent deeplink handlers before parsing URI components
- Wrap URI parsing logic in try-catch blocks to gracefully handle malformed or incomplete data
- Use null safety checks and optional parsing methods that return default values instead of throwing exceptions
- Validate that all required parameters exist in the intent URI before attempting to access them
- Implement unit tests covering malformed input scenarios (missing scheme, empty path, null components)
- Use intent-filter verification to ensure only expected data formats are processed
- Log malformed intent attempts for security monitoring and debugging

## Variant hunting
Test other deeplink handlers registered in AndroidManifest.xml for similar unhandled exceptions
Fuzz all intent-receiving activities with malformed URIs containing special characters, missing parameters, and invalid formats
Check for other URI parsing methods that may lack exception handling (file:// schemes, content:// schemes)
Examine broadcast receiver implementations for similar intent handling vulnerabilities
Test intent extras (Bundle data) in addition to URI data for unhandled exceptions
Search for other deeplinks like nc://open, nc://file for similar parsing issues

## MITRE ATT&CK
- T1406
- T1499.004

## Notes
This vulnerability is specific to Android's intent system and deeplink handling. The attack requires the malicious app to have basic permissions to send intents, which are available to all installed applications. The impact is primarily Denial of Service rather than data exfiltration. The fix is straightforward: add proper exception handling and input validation to the parseLoginDataUrl method. Similar issues are common in Android applications that expose deeplinks without proper input sanitization.

## Full report
<details><summary>Expand</summary>

Not sure if this can be tracked as a security issue, but this definitely calls for a code change. This can be classified into Denial of Service category attack and can seriously hamper user experience. 

Asset: Nexcloud Android Client (com.nextcloud.client)
Version: 3.11.1 (latest)

###_Details_ 

The Nextcloud android app registers a deeplink `nc://login` that is handled by the `com.owncloud.android.authentication.ModifiedAuthenticatorActivity` class as seen in AndroidManifest file.

The above mentioned class implements `AuthenticatorActivity` class in order to handle incoming deeplinks.

It is seen that the method `parseLoginDataUrl` does not handle exception correctly crashing the Nextcloud app.  

malicious apps can thus crash the nextcloud client by sending following data in intent : `nc://login`. 

ADB payload:

```
adb shell am start -a "android.intent.action.VIEW" -c "android.intent.category.DEFAULT" -n "com.nextcloud.client/com.owncloud.android.authentication.ModifiedAuthenticatorActivity" -d "nc://login"
```

Attaching video PoC
{F803256}

## Impact

1. Malicious apps can crash the nextcloud android client to cause a denial of service attack.

</details>

---
*Analysed by Claude on 2026-05-24*
