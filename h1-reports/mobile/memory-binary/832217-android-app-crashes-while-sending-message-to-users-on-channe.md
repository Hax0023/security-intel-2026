# Android App Denial of Service via Crafted Message Content

## Metadata
- **Source:** HackerOne
- **Report:** 832217 | https://hackerone.com/reports/832217
- **Submitted:** 2020-03-26
- **Reporter:** legalizenepal
- **Program:** Rocket.Chat
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Denial of Service, Improper Input Validation, Unhandled Exception
- **CVEs:** None
- **Category:** memory-binary

## Summary
A security vulnerability in Rocket.Chat's Android application allows remote attackers to crash the app by sending specially crafted messages containing malicious code/markup to private messages or public channels. The vulnerability requires the victim to open the message to trigger the crash, affecting Android 6.0 through 10.0+.

## Attack scenario
1. Attacker identifies that Rocket.Chat Android app lacks proper input validation for message content
2. Attacker crafts a malicious message payload (likely containing unescaped markup, special characters, or code) designed to trigger a parsing error or unhandled exception
3. Attacker sends the crafted message to a public channel (e.g., #general) or private message to target user(s)
4. When the victim opens Rocket.Chat and views the message, the Android app attempts to process/render the malicious content
5. The improper handling of the crafted content causes an uncaught exception, crashing the application
6. Victim's app becomes unstable and crashes repeatedly when attempting to view messages in the affected channel/conversation

## Root cause
The Rocket.Chat Android application fails to properly validate, sanitize, or safely handle message content before rendering or processing it. The app likely lacks exception handling for edge cases in message parsing/rendering, allowing malformed or specially crafted input to cause unhandled exceptions. This issue is specific to the Android/React Native implementation and does not affect iOS or web clients.

## Attacker mindset
An opportunistic attacker seeking to disrupt communication and availability. The attacker likely discovered this through fuzzing or testing message rendering edge cases. The goal is to cause immediate denial of service to team communication, potentially for harassment, disruption of operations, or proof-of-concept demonstration of platform vulnerabilities.

## Defensive takeaways
- Implement comprehensive input validation and sanitization for all message content before rendering
- Add exception handling and defensive coding practices around message parsing and rendering logic
- Implement strict limits on message content size, character sets, and markup complexity
- Use a robust, well-tested HTML/markup parser with safe defaults rather than custom parsing logic
- Conduct platform-specific testing (iOS, Android, Web) as rendering behavior may differ significantly
- Implement crash reporting and monitoring to detect widespread DoS attacks via crafted messages
- Apply security patch testing across all client implementations consistently
- Consider sandboxing message rendering or using a separate process to prevent full app crashes

## Variant hunting
Test with various markup languages (HTML, XML, Markdown) to identify which triggers the crash
Attempt message content with excessive nesting, circular references, or recursive structures
Test with oversized messages or messages containing extremely long strings/tokens
Try special Unicode characters, zero-width characters, or RTL/LTR override sequences
Test with file attachment metadata or embedded media URLs with malformed content
Attempt similar payloads against other Rocket.Chat clients (desktop, iOS) to identify platform-specific issues
Test with messages containing control characters or binary sequences
Check if similar parsing issues exist in other features (user profiles, room descriptions, etc.)

## MITRE ATT&CK
- T1561
- T1499
- T1190

## Notes
The researcher responsibly disclosed this vulnerability on GitHub before submitting to HackerOne. The use of postimg.cc and pastebin links for PoC suggests the payload is relatively simple to construct. The fact that iOS and web clients are unaffected indicates this is likely a React Native/Android-specific rendering or parsing issue. No specific bounty amount was disclosed in the report. The vulnerability was reported in March 2020 and had not been fixed at the time of submission according to the reporter.

## Full report
<details><summary>Expand</summary>

## Description
 I found a security vulnerability in Rocket's latest android app by which I was able to remotely crash any  user’s app  instantly just by just sending a simple message in private or in channel. The vulnerability  require the victim open the message. 


## Devices and Versions

Rocket.Chat.Android version: (e.g. 4.5.1)
Mobile device model and OS version: (tested on :+1: -- " **Android 6.0, 8.0, 10.0**"), probably any other android version

## Steps to reproduce

> Create new #test channel
> Send POC Code onto the channel
> Open Mobile App
> App gets crashed

## POC
### Crafted code to crash mobile app
https://i.postimg.cc/zvBWdMzT/Screenshot-20200320-112405.png

### Message Preview
https://i.postimg.cc/fbCJ6KgC/Screenshot-20200320-112541.png

### App Gets Crashed
https://i.postimg.cc/26J8DXdQ/Screenshot-20200320-112711.png

### Code Link
https://pastebin.com/raw/JEDcC5Yr

**There is no such problem in iOS client and rocket web**

## Impact

An attacker could crash the internal chat user's phone, everytime he/she opens the rocket chat , i.e posting crafted code on #general channel

Hi, i even posted the issue on github, before i got to know about rocket chat on H1, but issue still not fixed, so just tryna keep you updated guys.

https://github.com/RocketChat/Rocket.Chat.ReactNative/issues/1907

</details>

---
*Analysed by Claude on 2026-05-24*
