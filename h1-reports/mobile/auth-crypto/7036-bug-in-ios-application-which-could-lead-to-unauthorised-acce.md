# Unprotected Session Identifier in iOS Application Preferences File

## Metadata
- **Source:** HackerOne
- **Report:** 7036 | https://hackerone.com/reports/7036
- **Submitted:** 2014-04-11
- **Reporter:** uname
- **Program:** IRCCloud
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure Data Storage, Inadequate Cryptographic Protection, Missing File Protection, Session Hijacking
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The iOS application stores authenticated session identifiers in a plist file (com.irccloud.IRCCloud.plist) within the Preferences folder without proper data protection classes. This file remains accessible even when the device is locked with a passcode, allowing attackers with physical access to extract session credentials and gain unauthorized account access.

## Attack scenario
1. Attacker gains physical access to a locked iOS device running the IRCCloud application with an active user session
2. Attacker uses tools like ios-dataprotection or iExplorer to dump the contents of the application's Preferences folder
3. Attacker extracts the com.irccloud.IRCCloud.plist file containing the user's authenticated session identifier
4. Attacker transfers the extracted plist file to their own device or analyzes it to obtain the session token
5. Attacker uses the stolen session identifier to authenticate to IRCCloud services, bypassing password requirements
6. Attacker gains full unauthorized access to the victim's account, messages, and connected IRC channels

## Root cause
The application fails to implement iOS Data Protection by not setting sensitive files to NSFileProtectionComplete. The plist file is stored with a lower protection class (likely NSFileProtectionNone or NSFileProtectionUntilFirstUserAuthentication), making it accessible without device unlock.

## Attacker mindset
A opportunistic attacker with brief physical access to a locked device can compromise user accounts without requiring jailbreak, passcode bypass, or technical exploitation. The low barrier to entry makes this a practical attack for theft or espionage scenarios.

## Defensive takeaways
- Always use NSFileProtectionComplete for files containing authentication tokens, session identifiers, or other sensitive credentials
- Implement proper file protection classes for all sensitive data stored in the application's sandbox
- Review all files in the Preferences, Documents, and Caches folders to identify unprotected sensitive data
- Use the ios-dataprotection tool or similar utilities during security testing to verify proper data protection implementation
- Consider encrypting sensitive data at the application level in addition to OS-level file protection
- Implement session timeout mechanisms to limit the window of exposure if credentials are compromised
- Educate users about the risks of leaving devices unattended, particularly when logged into sensitive applications

## Variant hunting
Search for similar unprotected plist files storing authentication data, API keys, tokens, or personal information. Check for other apps using NSFileProtectionNone or NSFileProtectionUntilFirstUserAuthentication for sensitive data. Examine backup-related files, cache files, and temporary files that might contain session information.

## MITRE ATT&CK
- T1111
- T1005
- T1040
- T1552.001

## Notes
This report demonstrates a critical gap between iOS security best practices and implementation. The vulnerability is particularly severe because it requires only physical access and a locked device, not a jailbreak or exploit. The reporter provided clear remediation guidance referencing Apple's official documentation, making this an actionable security issue.

## Full report
<details><summary>Expand</summary>

Hi,

The file under the Preferences folder within the iOS application stores sensitive information: com.irccloud.IRCCloud.plist. This file stores the user's authenticated session identifier. Stealing this information would allow unauthorised access to a user's account.

The content of the file can be seen in the file attached to this report.

This file is accessible from the phone even while the phone is locked with a passcode suggesting that the application does not secure the file using the appropriate data protection class.

This can also be verified by using the tool available at the following link:

https://github.com/ciso/ios-dataprotection/

If a user is logged into the application, all that an attacker needs to do is surreptitiously take the phone and dump the file within the folder. This would work while the phone is locked and does not require the phone to be jailbroken.

I should also mention that I haven't looked through all the files, but any sensitive file with the Protection class set to anything other than NSFileProtectionComplete would be extractable from the iPhone without requiring the passcode.

If you would like to test this, you can use the ios-data protection tool mentioned above or extract the data with iExplorer (Demo version) while the phone is locked and the user logged in.

More information regarding data protection is available here:

https://developer.apple.com/library/ios/documentation/iPhone/Conceptual/iPhoneOSProgrammingGuide/AdvancedAppTricks/AdvancedAppTricks.html#//apple_ref/doc/uid/TP40007072-CH7-SW24

</details>

---
*Analysed by Claude on 2026-05-24*
