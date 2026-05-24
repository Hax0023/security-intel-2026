# Passcode Protection Bypass in Nextcloud Android Client via Direct Activity Launch

## Metadata
- **Source:** HackerOne
- **Report:** 631206 | https://hackerone.com/reports/631206
- **Submitted:** 2019-06-28
- **Reporter:** ctulhu
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Improper Access Control, Authentication Bypass, Insecure Activity Exposure, Missing Intent Filter Protection
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Nextcloud Android client's passcode protection mechanism can be bypassed by directly launching the FileDisplayActivity component using Drozer without triggering authentication checks. An attacker with physical device access can circumvent the app's security layer and gain unauthorized access to user files and account information.

## Attack scenario
1. Attacker gains physical access to an unlocked or minimally secured Android device with Nextcloud client installed and configured with a passcode
2. Attacker installs Drozer and Drozer Agent on the target device to enable remote component launching capabilities
3. Attacker closes the Nextcloud application to trigger the passcode prompt on next launch
4. Attacker uses Drozer console to directly invoke FileDisplayActivity (com.owncloud.android.ui.activity.FileDisplayActivity) bypassing the passcode verification
5. Application launches directly to the main UI, skipping authentication checks entirely
6. Attacker gains full access to user files, account details, and all stored data within the application

## Root cause
The FileDisplayActivity component is exported or accessible without proper protection mechanisms (missing android:exported='false' or insufficient permission checks). The authentication/passcode verification logic is implemented at the application entry point but not enforced at the Activity level, allowing direct component invocation to circumvent security controls.

## Attacker mindset
An opportunistic attacker with physical device access seeks quick unauthorized access to sensitive cloud storage and account information. The attack requires minimal technical sophistication once Drozer is installed, making it practical for device theft or insider threats.

## Defensive takeaways
- Implement authentication checks within individual Activities, not just at application entry point
- Explicitly set android:exported='false' for Activities not intended for external access
- Use custom permissions to restrict Activity access and validate caller identity
- Implement passcode/authentication state verification in Activity lifecycle (onCreate/onResume)
- Consider using FLAG_SECURE to prevent app content from appearing in recent apps or screenshots
- Validate Intent origin and add additional security layers before displaying protected UI
- Regularly audit exported components and their access control implementations
- Use Android Security Testing framework to identify exposed Activities during development

## Variant hunting
Check other exported Activities in Nextcloud client for similar authentication bypass patterns
Test other cloud sync applications (Sync.com, pCloud, Tresorit) for equivalent vulnerabilities
Investigate if other authentication mechanisms (biometric, 2FA) are similarly bypassable
Search for similar Activity export vulnerabilities in other file management apps
Test whether Service or BroadcastReceiver components have similar protection gaps
Examine if the vulnerability affects backup/restore or migration Activities

## MITRE ATT&CK
- T1190
- T1621
- T1556
- T1111

## Notes
This vulnerability requires physical device access and Drozer installation, limiting real-world exploitation scope. However, it represents a critical design flaw in authentication architecture. The report lacks specific version information and bounty details. Video PoC (poc.mp4) was provided but content redacted. Android 9 non-rooted device used in testing. Drozer is a well-known penetration testing framework for Android application assessment, making this a realistic attack vector for physical device theft scenarios.

## Full report
<details><summary>Expand</summary>

###What is The Vulnerability?

The Passcode can be bypassed by calling a MainLoginActivity which is com.owncloud.android.ui.activity.FileDisplayActivity , We have successfully bypassed the passcode and are redirected to the App's User Interface.
of the user’s credentials:

Android Version: 9
Non Rooted Device.

##How to Reproduce:
1.) Setup a Emulated Device Via Android Studio AVD Using the Same Setup.
{F518191}

2.) Install NextCloud Client and Login Your NextCloud Account.

{F518192}

3.) Setup the PassCode

{F518193}

4.) Install Drozer and Drozer Agent

* https://labs.mwrinfosecurity.com/tools/drozer/

5.) Start the Drozer Embedded Server

{F518195}

6.) Open your CMD/Console and type ```drozer console connect```

█████████

7.) Close the NextCloud Client and Open it Again

{F518197}

8.) Go Back to Drozer Console and run this code
```run app.activity.start --component com.nextcloud.client com.owncloud.android.ui.activity.FileDisplayActivity```

9.) Voila, Passcode Bypassed

{F518198}

##Supporting Materials

* Attached as poc.mp4

█████

## Impact

Successful exploitation of this vulnerability allows an attacker to bypass the android application's authentication mechanisms and gain unauthorized access to the user files and infos.

</details>

---
*Analysed by Claude on 2026-05-24*
