# Moderator Can Remotely Enable Camera/Microphone if Previously Activated

## Metadata
- **Source:** HackerOne
- **Report:** 1520685 | https://hackerone.com/reports/1520685
- **Submitted:** 2022-03-24
- **Reporter:** michag86
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Improper Access Control, Privacy Violation, State Management Flaw
- **CVEs:** CVE-2022-24890
- **Category:** uncategorised

## Summary
A moderator in Nextcloud Spreed can remotely re-enable a participant's camera and microphone by revoking and then re-granting permissions, if those devices were previously activated. This occurs because the application retains the enabled state of media devices even after permissions are revoked, allowing a moderator to restore access without the user's explicit consent.

## Attack scenario
1. Moderator creates a video call and invites a target participant (victim user)
2. Victim user joins the call and explicitly enables their camera and microphone
3. Moderator revokes all media permissions for the victim user, disabling camera and microphone access
4. Victim user believes their devices are now fully disabled and controlled locally
5. Moderator re-grants camera and microphone permissions to the victim user
6. Camera and microphone are automatically re-enabled without victim's interaction, broadcasting audio/video without consent

## Root cause
The application fails to properly reset the device activation state when permissions are revoked. The internal state tracking retains whether devices were 'enabled' as a separate attribute from 'permission granted', allowing permission re-grant to restore enabled devices without requiring explicit user activation.

## Attacker mindset
A malicious moderator exploits trust relationships in collaborative video conferencing to covertly surveil participants by manipulating permission states as a proxy for device activation control, targeting privacy-conscious users who believe disabling devices provides protection.

## Defensive takeaways
- Implement state reset logic: when permissions are revoked, reset device enabled/disabled state to false regardless of prior state
- Separate permission model from activation state: treat permissions and user-initiated activation as independent controls
- Require explicit user action to re-enable devices after permission changes: don't auto-restore prior states
- Log all permission changes with moderator identity for audit trails
- Provide user-visible indicators of device state changes triggered by moderators
- Implement device lockdown mode where users can prevent moderators from affecting device state
- Add consent prompts when permissions are restored, requiring user acknowledgment before devices activate

## Variant hunting
Screen sharing permission re-grant without explicit user re-activation
Recording state persistence across permission changes
Audio-only mode state restoration when full A/V permissions re-granted
Virtual background activation state recovery
Similar permission-state desync in other WebRTC-based communication platforms
Participant settings restore in group video calls when moderator role is reassigned

## MITRE ATT&CK
- T1123 - Audio Capture
- T1113 - Screen Capture
- T1557 - Man-in-the-Middle
- T1562 - Impair Defenses

## Notes
This vulnerability is particularly dangerous in workplace and educational settings where moderators have administrative roles. The attack is difficult for users to detect as the device state change occurs silently without notification. The affected versions are Nextcloud 23.0.3, Spreed 13.0.4, and Nextcloud Spreed Signaling 0.4.0. This represents a fundamental flaw in the state machine logic for media device management.

## Full report
<details><summary>Expand</summary>

## Summary:
[add summary of the vulnerability]

## Steps To Reproduce:

  1. Create a Call as User A (Moderator)
  2. Add User B to the call
  3. Start the call as User A
  4. User B joins the call and enables the camera
  5. User A removes all permissions for User B, cam and mic are now disabled
  6. User A grants all permissions to User B

--> now mic and cam are enabled remotely, if User B didn't disable it before removing permissions by User B

## Used Software Versions:
Nextcloud 23.0.3
spreed-App 13.0.4
nextcloud-spreed-signaling 0.4.0

## Impact

A call moderator can remotely enable user webcams, if there were enabled before removing the permissions. This is a big privacy issue.

</details>

---
*Analysed by Claude on 2026-05-24*
