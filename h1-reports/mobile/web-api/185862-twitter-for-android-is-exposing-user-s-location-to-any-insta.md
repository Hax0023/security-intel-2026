# Twitter Android App Exposing User Location via Unprotected Broadcast to All Installed Apps

## Metadata
- **Source:** HackerOne
- **Report:** 185862 | https://hackerone.com/reports/185862
- **Submitted:** 2016-11-27
- **Reporter:** mishre
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insecure Broadcast, Unauthorized Information Disclosure, Missing Access Controls, Local Privilege Escalation
- **CVEs:** None
- **Category:** web-api

## Summary
Twitter's Android application broadcasts user location data via an unprotected Intent broadcast that any locally installed application can receive without requiring permissions. A malicious app can intercept these broadcasts and track user location even without declaring location permissions, as long as the user has granted Twitter location access.

## Attack scenario
1. Attacker develops a benign-looking Android application requiring minimal permissions
2. User installs the malicious app from app store or sideload it onto their device
3. User grants Twitter permission to access device location and uses location features
4. Twitter app receives GPS coordinates and broadcasts them via unprotected sendBroadcast() with action 'com.twitter.library.geo.LOCATION_CHANGED'
5. Malicious app's BroadcastReceiver silently listens to and captures all location broadcasts without user knowledge
6. Attacker exfiltrates collected location data to remote server for continuous user tracking

## Root cause
Twitter Android app implements location sharing via implicit broadcast Intents without protecting the broadcast with permissions. The vulnerable code uses `sendBroadcast()` with action string 'com.twitter.library.geo.LOCATION_CHANGED' containing location extras, allowing any app to register a BroadcastReceiver to intercept the location data. The broadcast lacks required permissions via the second parameter of sendBroadcast(permission).

## Attacker mindset
An attacker seeks to track user location without requiring location permissions in their own app manifest. By leveraging Twitter's trusted location access, the attacker can piggyback on user-granted permissions to the Twitter app. The attack is elegant because the malicious app appears benign in permission requests, evading user suspicion while enabling location tracking.

## Defensive takeaways
- Use protected broadcasts with explicit permission requirements: sendBroadcast(intent, 'com.twitter.permission.LOCATION_CHANGED') instead of unprotected sendBroadcast()
- Consider using LocalBroadcastManager or EventBus for internal app communications instead of system-wide broadcasts
- Implement whitelist of trusted receivers if broadcasting sensitive data
- Never broadcast PII (personally identifiable information) like location, contacts, or biometrics via unprotected Intents
- Use explicit Intents with component names instead of implicit broadcasts for sensitive data
- Add permission declarations in AndroidManifest.xml with dangerous protection level for any sensitive broadcasts
- Document location data handling and audit all broadcast operations during security reviews

## Variant hunting
Search Android codebases for patterns: `sendBroadcast(` without permission parameter containing location-related actions, PII extras (email, phone, address), or user identity data. Look for Intent actions with patterns like '*LOCATION*', '*POSITION*', '*GPS*', '*COORDINATES*'. Check for BroadcastReceiver registrations without permission checks. Scan for implicit Intent broadcasts containing 'Extra' suffixes with sensitive data.

## MITRE ATT&CK
- T1418
- T1517
- T1430
- T1619

## Notes
Report includes proof-of-concept video and APK demonstrating exploitation. Vulnerable code pattern is trivial to exploit - any app can intercept without declaring android.permission.ACCESS_FINE_LOCATION or android.permission.ACCESS_COARSE_LOCATION. This is a classic Android inter-process communication (IPC) security flaw. The fix is simple but requires careful implementation to avoid breaking existing functionality. Similar patterns may exist in other Twitter features using broadcasts.

## Full report
<details><summary>Expand</summary>

Hi,

I have noticed that while a user is using the location feature in twitter's android application twitter is sending the user's location to all other locally installed applications without verifying the possible (malicious) receivers (By sending a broadcast). As a poc I have created an application (attached) which asks for no permissions from android and is just listening to location broadcasts sent by twitter. You can see both the application's apk and its code attached.
I have also created a poc video which shows how to use it - I have used an android emulator but it can also be used by a real device. Here is the video: https://vimeo.com/193261287 pass is: twittergps121
It can be seen in the video that the moment twitter asks for(and receives) gps signal - my malicious application is receiving it due to twitter forwarding this location - also my app has no permissions assigned.

Note: I am sending the coordinates to my emulator manually - but on a real device which allows twitter to use  location it is sent automatically.

Vulnerable code
===
This is happening because of the following lines in your app's code: 
```
paramLocation = new Intent("com.twitter.library.geo.LOCATION_CHANGED").putExtra("com.twitter.library.geo.LOCATION_EXTRA", paramLocation);
this.c.sendBroadcast(paramLocation);
```
Some variable names might be wrong due to obfuscation but the idea remains - you should probably add permission to the broadcast.

Implications
===
Any malicious application installed on a user's device can track the user's location without any permissions if the user is allowing twitter to access his location.




</details>

---
*Analysed by Claude on 2026-05-24*
