# Android App Fails to Clear End-to-End Encryption Keys on Account Removal

## Metadata
- **Source:** HackerOne
- **Report:** 1189168 | https://hackerone.com/reports/1189168
- **Submitted:** 2021-05-08
- **Reporter:** rtod
- **Program:** HackerOne (specific program not named in report)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Improper Cryptographic Key Management, Insufficient Data Sanitization, Privilege Escalation, Information Disclosure
- **CVEs:** CVE-2021-32658
- **Category:** uncategorised

## Summary
An Android application fails to properly delete end-to-end encryption keys and mnemonic phrases when a user removes their account from the device. An attacker with physical access to the device can retrieve the abandoned keys, then log in as the victim and decrypt all previously encrypted data without requiring the mnemonic phrase.

## Attack scenario
1. Victim (userA) sets up end-to-end encryption on Android device and stores encrypted data on serverA
2. Victim removes their account from the Android device for any reason, expecting all sensitive data to be cleaned
3. Attacker gains physical access to the victim's device (theft, temporary seizure, or supplied device)
4. Attacker discovers encryption keys and mnemonic still stored unencrypted in device storage
5. Attacker resets victim's password on serverA or gains login credentials through other means
6. Attacker logs in as victim using their credentials and accesses decrypted sensitive data using the recovered keys

## Root cause
The application's account removal function does not implement secure deletion of cryptographic keys, mnemonics, and other sensitive authentication material from local storage. Keys persist on the device after account removal, violating secure deletion principles and assuming device-level security will protect abandoned credentials.

## Attacker mindset
An insider threat (malicious admin) or someone with temporary physical access exploits the assumption that account removal equals data removal. The attacker recognizes that mobile devices often store sensitive data in accessible locations and that recovering abandoned encryption keys provides complete access to previously encrypted information without knowledge of recovery phrases.

## Defensive takeaways
- Implement secure deletion (cryptographic wiping) for all encryption keys, mnemonics, and sensitive cryptographic material on account removal
- Use Android Keystore or equivalent TEE-backed storage for sensitive keys rather than application-accessible storage
- Require mnemonic phrase re-entry when re-authenticating or restoring accounts, even if keys exist locally
- Clear all account-related data including encrypted metadata, key derivation parameters, and authentication tokens on logout/removal
- Implement cryptographic binding of keys to specific accounts or device identifiers to prevent reuse
- Add security logging for sensitive key operations and account removal events
- Consider requiring device-level passcode before accessing stored encryption keys

## Variant hunting
Check if other account types or authentication methods have similar key retention issues
Audit backup/restore functionality to ensure keys aren't backed up unencrypted
Review multi-account scenarios where keys from one account might be accessible to another logged-in account
Test key retention across app updates, reinstallation, or app migration
Verify whether application cache, shared preferences, or temporary files contain key material
Check if biometric/PIN authentication keys are similarly abandoned after account removal
Test account switching to see if previous account keys remain accessible

## MITRE ATT&CK
- T1190
- T1056
- T1555
- T1005
- T1187
- T1040

## Notes
This vulnerability bridges local security and remote security by showing how poor key hygiene on client devices enables account compromise. The reporter correctly notes minimal practical impact due to physical access requirement, but the vulnerability is still critical from a security architecture perspective. The fix requires minimal code changes but fundamental design review of the account lifecycle management. Consider this as a regression test case for any future encryption implementation.

## Full report
<details><summary>Expand</summary>

1. userA on serverA sets up end to end encryption on their android device
2. userA has some end to end encrypted data
3. userA removes their account on serverA from their android device (for whatever reason)
4. attacker (evil admin) obtains the device of userA
5. attacker (evil admin) logs in on the account of userA  (reset the pw and just log in)
6. attacker (evil admin) can see and access all encrypted files

## Impact

While I believe the impact is minimal since you need to obtain the device of the victim.
Once you remove your account all information regarding that account should be removed.

* the keys
* the mnemonic

And certainly when you re-add an account you should be asked to enter your mnemonic!

</details>

---
*Analysed by Claude on 2026-05-24*
