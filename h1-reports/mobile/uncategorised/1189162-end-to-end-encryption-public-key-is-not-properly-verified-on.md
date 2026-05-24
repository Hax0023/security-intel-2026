# End-to-End Encryption Public Key Not Properly Verified on Desktop and Android

## Metadata
- **Source:** HackerOne
- **Report:** 1189162 | https://hackerone.com/reports/1189162
- **Submitted:** 2021-05-08
- **Reporter:** rtod
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cryptographic Failure, Insufficient Cryptographic Validation, Man-in-the-Middle (MITM), Key Substitution Attack
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Nextcloud E2EE implementation fails to verify that the private key on newly registered devices matches the public key stored on the server, allowing an attacker with server access to substitute the user's public key with their own. This breaks the fundamental security guarantee of end-to-end encryption, enabling the attacker to decrypt all data encrypted by the victim.

## Attack scenario
1. Attacker gains administrative access to the Nextcloud server hosting the victim's account
2. Attacker identifies the victim's public key in the E2EE system and replaces it with a public key for which the attacker holds the corresponding private key
3. Victim sets up a new device and attempts to enable E2EE, entering the previously stored nonce
4. The client fails to verify that the new private key generated during setup matches the public key now stored on the server (which has been substituted)
5. Victim uploads data using the new device, which encrypts the data using the attacker's public key
6. Attacker decrypts all subsequently uploaded data using their private key, completely compromising the confidentiality of the victim's communications

## Root cause
The client-side implementation does not perform the verification step defined in the Nextcloud E2EE RFC, which explicitly requires clients to verify that the private key belongs to the previously downloaded public certificate. The absence of this critical binding check allows key substitution attacks when a device is re-enrolled or a new device is added to an account.

## Attacker mindset
An attacker with server-level access (evil admin scenario) seeks to conduct persistent, targeted surveillance of specific users by silently substituting their encryption keys. This provides perfect access to all encrypted data without detection, as the victim believes their data is encrypted with their own key.

## Defensive takeaways
- Implement mandatory verification that the private key generated/used on the client matches the public key retrieved from the server before any encryption operations
- Throw an explicit, high-severity error if key mismatch is detected rather than silently proceeding or exhibiting 'weird behavior'
- Bind the keypair through a test encryption/decryption cycle (as iOS implementation does) on all platforms for consistency
- Add logging and alerts for key verification failures to help users detect compromises
- Consider implementing key pinning or out-of-band verification mechanisms for initial key establishment
- Ensure RFC compliance across all client implementations (Desktop, Android, iOS) with feature parity
- Implement server-side checks to detect and alert on public key modifications
- Provide user-facing notifications when E2EE keys change or new devices are added

## Variant hunting
Check if key verification is missing on first-device setup vs. subsequent device setup scenarios
Investigate whether the vulnerability affects key rotation mechanisms or certificate renewal processes
Test whether an attacker can perform selective key replacement targeting only specific devices or users
Examine if the nonce mechanism provides any protection against key substitution attacks
Analyze whether the vulnerability exists in other E2EE implementations (Jitsi, Matrix, etc.) with similar architectures
Test if metadata or other unencrypted fields could leak information about the substitution
Investigate whether the attacker can trigger the 'weird behavior' bugs mentioned to cause denial of service

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1550 - Use Alternate Authentication Material
- T1021 - Remote Services (for initial server compromise)
- T1040 - Network Sniffing (MITM capability post-compromise)

## Notes
This vulnerability directly violates the Nextcloud E2EE RFC specification, making it a compliance issue in addition to a security flaw. The fact that iOS appears to implement the correct verification (through test encryption/decryption) suggests this is a platform-specific implementation gap rather than a design issue. The reporter correctly identifies that absence of error handling for key mismatches is dangerous, as it masks a potentially catastrophic security event. The attack requires high privilege (admin access) but the impact is absolute compromise of user data confidentiality. The report lacks specific bounty information and details on which Nextcloud versions are affected.

## Full report
<details><summary>Expand</summary>

Since last time when I reported something on multiple platforms you seems to prefer handling it in 1 spot. I now just do one. Let me know if You want me to fill separate for android as well. This issue does not seem to happen on iOS as there a test string is encrypted and decrypted, in short binding the keypair.

So the attack vector results in weird behavior but that seems to be due to random bugs in the end to end encryption implementations (because I also ran into those when just messing around with the end to end encryption). In any case there should be a big error if this happens. 

1. userA has an account on serverA
2. End2End encryption is enabled on serverA
3. userA setups device1 and enabled end to end encryption. Stores the nonce. Uploads some data. All is good.
4. Now an attacker obtains access to the server, for sake of argument assume there is an evil Admin.
5. They replace the public key of userA with their own
6. userA now setups device2
7, userA enters the nonce
8. userA uploads more data
9. the evil admin now has access to the uploaded data

## Impact

In short it breaks the whole premise of your end to end encryption. An evil admin is able to make the device encrypt to their key.

It is even in the RFC: https://github.com/nextcloud/end_to_end_encryption_rfc/blob/master/RFC.md#further-devices
"Client checks if private key belongs to previously downloaded public certificate."

Recommendations:
1. the clients should verify that the private key matches with the public key and if not  throw a big error

This is especially important because somebody is clearly doing something they are not supposed to if this happens.

</details>

---
*Analysed by Claude on 2026-05-24*
