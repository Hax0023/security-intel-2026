# User DMs Persist in Unencrypted Application State After Logout - Twitter iOS

## Metadata
- **Source:** HackerOne
- **Report:** 23913 | https://hackerone.com/reports/23913
- **Submitted:** 2014-08-12
- **Reporter:** abcdefghijklmnopqrstuvwxyzabc
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Sensitive Data Exposure, Improper Data Deletion, Insecure Data Storage, Local Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
User direct messages and usernames remain stored in plaintext within the iOS application state directory (com.atebits.xxx.application-state) even after user logout and device reboot. While the primary twitter.db is cleared from Cache, sensitive DM content persists in application state files that are accessible to potential attackers with device access.

## Attack scenario
1. Attacker gains physical or logical access to an unlocked iOS device or its backup
2. Attacker navigates to Applications > Documents > com.atebits.xxx.application-state directory using file exploration tools
3. Attacker locates files matching pattern 'app.acct.username-[random].detail.10'
4. Attacker extracts and reads plaintext DM content and communication partner usernames
5. Attacker obtains sensitive conversation history despite target user having logged out
6. Attacker can correlate DMs with usernames to identify relationships and gather intelligence

## Root cause
The Twitter iOS application performs incomplete data sanitization on logout. While the main database (twitter.db) in Cache is properly deleted, application state persistence files in the Documents directory are not cleared. These files maintain plaintext copies of DM content and metadata that should be wiped upon authentication termination.

## Attacker mindset
An attacker with physical device access or backup access seeks to extract sensitive communications from a logged-out account. They exploit the common assumption that logout completely removes user data. By targeting the less obvious application state directories rather than primary databases, they bypass initial security measures.

## Defensive takeaways
- Implement comprehensive data deletion routines that cover all application storage locations, not just primary databases
- Encrypt all sensitive data at rest, including DM content stored in application state files
- Establish a centralized secure deletion mechanism that wipes data from multiple locations during logout
- Regularly audit all application directories (Documents, Library, Caches, tmp) to identify data persistence
- Use secure deletion APIs that overwrite data multiple times before removal
- Implement automatic session timeout with complete cache clearance
- Create security tests that verify no sensitive data remains post-logout across all storage locations

## Variant hunting
Check for DM persistence in Library/Preferences or plist files
Audit other social messaging apps (Facebook Messenger, WhatsApp) for similar state file leakage
Inspect application state files for other sensitive data (authentication tokens, API keys, location history)
Test whether backup/restore cycles preserve these state files, allowing cross-device data leakage
Verify if uninstall/reinstall of app leaves state files accessible
Check for similar patterns in other com.atebits.* applications

## MITRE ATT&CK
- T1565 - Data Manipulation
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel
- T1557 - Man-in-the-Middle
- T1115 - Clipboard Data

## Notes
This is a follow-up report to a previous disclosure about encrypted storage. The researcher identified that while primary databases are cleared, application state files persist indefinitely. The report demonstrates the importance of holistic secure deletion across all application storage domains. The vulnerability affects any user with physical device access, including device owners with malware, attackers with device access, or backup file access. The use of specific file naming patterns (app.acct.username-*.detail.10) suggests this is a known application state serialization format used by Twitter's iOS implementation.

## Full report
<details><summary>Expand</summary>

I would like to add an additional information regarding my previous report about "Unencrypted User's DM and Statuses on twitter.db at Twitter for iOS". I have already tried to logout from my Twitter apps (including from built-in twitter apps for iOS), and then, I already reboot the iDevice too. (tested on iPhone 5 with the same version of Twitter Apps).

In this situation, the twitter.db that located on Cache isn't appear anymore. But, Attacker could still access the User's DM including username and their chat partner from "app.acct.username-some.random.number.detail.10" that could be found on: "Applications > Documents > com.atebits.xxx.application-state".

For support my explanation, I attached the screenshot in this post too.

nb: I'm sorry for opening another ticket. Because, I see that the status is already closed on previous ticket.


Best Regard,

YoKo

</details>

---
*Analysed by Claude on 2026-05-24*
