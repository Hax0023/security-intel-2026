# iOS App Crash via Malformed Direct Message Reactions

## Metadata
- **Source:** HackerOne
- **Report:** 784676 | https://hackerone.com/reports/784676
- **Submitted:** 2020-01-28
- **Reporter:** alexiaya
- **Program:** Twitter
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Improper Input Validation, Denial of Service (DoS), Insufficient Input Sanitization, Buffer Handling Error
- **CVEs:** None
- **Category:** memory-binary

## Summary
Twitter's iOS app fails to properly sanitize direct message reaction text, allowing attackers to inject special characters including NUL bytes that crash the application. An attacker with the ability to send direct messages to a victim can render the iOS app completely unusable, forcing victims to delete conversations via the web interface.

## Attack scenario
1. Attacker initiates or identifies a direct message conversation with target victim
2. Attacker crafts malicious API request to /dm/reaction/new.json endpoint with reaction_key parameter containing a NUL byte (\0)
3. Victim receives the malicious reaction notification in their direct message list
4. iOS app attempts to parse and render the reaction text in the message preview
5. Application crashes due to unhandled NUL byte during string processing
6. Victim cannot use the iOS app; subsequent launch attempts also crash until conversation is deleted via web

## Root cause
The iOS application does not implement proper input validation and sanitization for direct message reaction payloads received from the backend API. Specifically, control characters (\0, \r, \n) are not stripped or escaped before being processed by string rendering components, causing memory corruption or buffer overread when the NUL terminator is encountered prematurely.

## Attacker mindset
An attacker with direct messaging capability seeks to degrade user experience and platform availability by exploiting a trivial input validation flaw. The low barrier to entry (standard API call with modified parameters) combined with high impact (complete app crash) makes this an attractive griefing vector. The attacker may be motivated by harassment, denial of service, or demonstrating platform fragility.

## Defensive takeaways
- Implement strict input validation on all user-supplied data received from APIs, especially control characters and non-printable characters
- Sanitize reaction text by filtering or escaping special characters (\0, \r, \n, etc.) at the API boundary before persistence
- Use safe string handling libraries that explicitly check for and handle NUL terminators and other control characters
- Implement application-level crash handlers that gracefully degrade rather than crashing on malformed input
- Conduct security review of all user-generated content rendering paths, particularly those involving direct messages and real-time notifications
- Add input validation tests covering edge cases like control characters, zero-length strings, and maximum length boundaries
- Consider server-side validation and rejection of invalid reaction payloads rather than relying on client-side parsing

## Variant hunting
Search for similar input validation bypasses in: (1) Other message attachment types (emojis, stickers, quoted messages) lacking sanitization, (2) Status/tweet reactions using the same /reaction/new.json endpoint, (3) Comment reactions on other Twitter products, (4) Any feature accepting user-controlled text rendered in UI lists, (5) Web and Android implementations of reaction handling for parity issues, (6) Historical reaction formats that may not properly validate backward compatibility

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1561 - Disk Wipe
- T1499 - Endpoint Denial of Service

## Notes
This vulnerability demonstrates the classic mistake of assuming backend API responses are safe for direct use in UI rendering without validation. The fact that attackers need only the ability to send DMs (not authentication as the victim) significantly lowers the attack barrier. The persistent nature of the crash (app crashes on every launch until conversation deleted) suggests the reaction data is cached or persisted unsafely. The writeup lacks specific bounty amount, which may indicate report status or coordinated disclosure details not disclosed.

## Full report
<details><summary>Expand</summary>

**Summary:** iOS app crashed by specially crafted direct message reactions

**Description:**
Twitter does not properly sanitize direct message reactions, making it possible for arbitrary reaction text to be shown to the user via the message preview in the direct message list. Special characters such as `\r` and `\n` are not stripped, and it is even possible to crash the app by inserting a `\0` character into the reaction text.

## Steps To Reproduce:

(Add details for how we can reproduce the issue)

  1. Start a direct message conversation with the victim (this can also be yourself).
  1. Make a request to https://api.twitter.com/1.1/dm/reaction/new.json with an appropriate `conversation_id` and `dm_id` parameter, and `reaction_key` set to `\0` (an actual NUL byte).
  1. Notice that the iOS app crashes, even on any subsequent attempts to reopen it.

## Impact

This makes it trivial for an attacker to make the Twitter iOS app unusable for any user they can send a direct message to. The only recourse for the victim is to log in via twitter.com and delete the affected message or conversation.

</details>

---
*Analysed by Claude on 2026-05-24*
