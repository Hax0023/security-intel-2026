# Talk Android Broadcast Receiver Not Protected by Broadcast Permission

## Metadata
- **Source:** HackerOne
- **Report:** 1596459 | https://hackerone.com/reports/1596459
- **Submitted:** 2022-06-10
- **Reporter:** andyscherzinger
- **Program:** Talk (Android application)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Insecure Inter-Process Communication, Missing Permission Enforcement, Broadcast Receiver Exposure
- **CVEs:** CVE-2022-4192
- **Category:** uncategorised

## Summary
The Talk Android application registers a broadcast receiver without specifying the broadcastPermission parameter, allowing any malicious application on the device to send broadcasts to it. This enables unprivileged applications to potentially interfere with call initiation and audio/Bluetooth setup functionality.

## Attack scenario
1. Attacker creates a malicious Android application with minimal permissions
2. Malicious app identifies the broadcast receiver registered by Talk via reverse engineering or Android package analysis
3. Attacker sends crafted broadcast intents to the unprotected receiver
4. Talk processes the broadcasts without verifying the sender's permissions
5. Attacker manipulates call flows, audio routing, or Bluetooth connectivity
6. User experiences unexpected behavior during calls or audio configuration

## Root cause
The registerReceiver() call omits the broadcastPermission parameter, defaulting to no permission checks. Without this parameter, Android allows any application to send broadcasts to the receiver, bypassing the intended permission-based security model.

## Attacker mindset
An attacker would exploit this to disrupt VoIP functionality, perform denial-of-service attacks on call initiation, hijack audio routing decisions, or manipulate Bluetooth connections during sensitive calls. This could be chained with other vulnerabilities for account takeover or social engineering attacks.

## Defensive takeaways
- Always specify broadcastPermission parameter when registering broadcast receivers that handle sensitive operations
- Define custom permissions in AndroidManifest.xml and enforce them at broadcast registration time
- Use LocalBroadcastManager for internal application communication instead of global broadcasts
- Validate the source and content of all received broadcasts before processing
- Conduct security code review of all IPC mechanisms during development
- Use static analysis tools (Lint, Snyk) to detect missing broadcast permissions

## Variant hunting
Search for other registerReceiver() calls in the codebase lacking broadcastPermission parameter. Check for BroadcastReceiver implementations handling call control, audio, Bluetooth, network, or authentication-related intents. Review all dynamically registered receivers for permission enforcement.

## MITRE ATT&CK
- T1418 - Software Discovery
- T1516 - Input Injection
- T1571 - Non-Standard Port

## Notes
This is a common vulnerability pattern in Android applications. The fix involves adding a custom permission declaration and passing it to registerReceiver(). Similar issues have been identified and fixed in buseta, Android Messenger++, and IRCCloud projects as referenced. The impact on call audio setup could escalate to denial-of-service or more severe manipulation depending on how the receiver processes broadcasts.

## Full report
<details><summary>Expand</summary>

## Summary:
Call to registerReceiver misses the broadcastPermission argument - no permissions will be checked for the broadcaster, which allows a malicious application to communicate with the broadcast receiver.

## Supporting Material/References:

  * Screenshot Snyk report
 * references to fixes in other repos

https://github.com/alvinhkh/buseta/commit/6b791de8e3622ef157b065f9c82fcfd5a0e2302a?diff=split#diff-a75527f97c6732197964c1dbf30fd385L66

https://github.com/serso/android-messengerpp/commit/1528fdc2d3561bab192dfde9a84a737a26a19fce?diff=split#diff-7ff52f2abe79bd0a68d54916fe71aef2L92

https://github.com/irccloud/android/commit/857287d6d9da443b0ff667505d5bf4a383922784?diff=split#diff-f06bf5e27b9130d322139330f7f31997L40

## Impact

Unsure, potentially interfere with call starts and audio/bluetooth setup

</details>

---
*Analysed by Claude on 2026-05-24*
