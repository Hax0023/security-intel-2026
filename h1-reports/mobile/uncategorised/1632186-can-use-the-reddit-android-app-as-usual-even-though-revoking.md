# Reddit Android App Maintains Access After Token Revocation Due to Insufficient Cache Invalidation

## Metadata
- **Source:** HackerOne
- **Report:** 1632186 | https://hackerone.com/reports/1632186
- **Submitted:** 2022-07-09
- **Reporter:** sateeshn
- **Program:** Reddit
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insufficient Session Invalidation, Token Revocation Bypass, Improper Cache Management, Authentication Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
After revoking Reddit Android app access via reddit.com, the app initially denies access but regains full functionality after approximately 20+ hours without re-authentication. The vulnerability allows previously logged-in accounts to be reused despite explicit revocation, indicating improper cache invalidation and token lifecycle management on the client side.

## Attack scenario
1. Attacker logs into Reddit Android app with their account
2. Attacker logs into reddit.com/old.reddit.com with same account
3. Attacker navigates to Account Activity > Apps you have authorized and revokes Android app access
4. Initially, the Android app shows errors and denies access as expected
5. Attacker waits 20+ hours or receives push notifications (chat invites, post notifications) from the app
6. Attacker clicks notification or reopens app to find full account access restored without re-authentication

## Root cause
The Android app caches authentication tokens/session data locally with insufficient invalidation mechanisms. While the server-side revocation works initially, the client-side cache persists and refreshes or revalidates after a time threshold (20+ hours) or following specific user interactions (push notification clicks), allowing continued use of revoked credentials without checking server-side revocation status.

## Attacker mindset
An attacker with access to a compromised or shared Android device could exploit this window to maintain persistent account access even after the legitimate owner revokes app permissions, enabling account takeover, data theft, or malicious actions attributed to the original account.

## Defensive takeaways
- Implement immediate token invalidation on client-side when revocation occurs server-side; use push notifications to force cache clearing
- Enforce mandatory server-side token validation on every API request rather than relying solely on client-side caching
- Add short expiration times (minutes, not hours) for authentication tokens with refresh token rotation
- Implement certificate pinning and token binding to prevent replay attacks
- Add server-side revocation checks on critical operations and periodic background validation
- Ensure push notifications and app wake-ups trigger authentication re-validation rather than resuming with cached credentials
- Implement cryptographic signing of cached tokens with server-side verification capabilities
- Add user-facing notifications when app access is revoked to alert of active sessions

## Variant hunting
Test iOS Reddit app for similar token cache invalidation issues
Examine third-party Reddit clients for equivalent authentication bypass vulnerabilities
Investigate if other OAuth-integrated apps show similar revocation bypass behavior
Check if background app refresh or sync operations bypass revocation checks
Test if direct API calls with cached tokens continue to work after revocation
Examine if network-offline conditions allow cached token usage post-revocation
Check for similar issues in other Reddit API scopes (read, write, moderation)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (OAuth token handling)
- T1550.001 - Use Alternate Authentication Material (cached tokens)
- T1556 - Modify Authentication Process (bypass revocation)
- T1110 - Brute Force (token reuse attempts)
- T1539 - Steal Web Session Cookie (session cache exploitation)

## Notes
Reporter demonstrates good methodology with reproduction steps and version tracking. However, inconsistent reproduction (chat invite feature failed to trigger vulnerability consistently) suggests timing-dependent or state-dependent behavior. The 20+ hour window suggests either: (1) token refresh cycle, (2) cache expiration override, or (3) server sync delay. Push notification interaction appears to be a significant trigger. Recommend Reddit investigate client-side caching implementation, token refresh logic, and push notification handler authentication state management.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi Team,

For the last 4 days, I kept testing reddit web. That time, I revoked app access from the old.reddit.com and i checked my app and as expected i was not able to use the account in my app. 

After 2 days I was checking the chat invites feature on the web and after some time I turned on the internet on my mobile and got a Reddit "invitation accept"  notification. I clicked on that and I was surprised that I was able to use the previously revoked user account again in the Reddit app.

After I tried to reproduce the scenario again. I  thought the revoked account get access again after clicking on the app "chat invite" notification. 
- I again revoked the app access from the old.reddit.com
- I sent a chat invitation link to another test account and replied with the test account so that I get a "chat accept" notification in the mobile
- After several tries from several test accounts, Finally, I received the "chat accept" invitation, only one time on the mobile (Note: this is also an issue)
- I clicked on the notification and I was not able to access anything in the app (it was showing some error)
- I tried to reproduce the issue again, I don't know the reason But this time I was not able to view the chat invite links from any accounts. (it was showing some error)
- It took my whole day and I stopped testing.

The next day again I got a post notification on my mobile. I clicked on that and again I see that the app was working as usual with a previous logged-in user!!!

Finally, I came to the conclusion that whenever we revoke the app access, it works fine. But if you check the app approximately after 20+ hours you can reuse the previously logged-in account again.

## Steps To Reproduce:
  1. log in to your account from both the android mobile app and from the web(reddit.com or old.reddit.com)
  2. On the Reddit web go to https://www.reddit.com/account-activity 
  3. Navigate to the "Apps you have authorized" section
  4. Find "Reddit on Android" click the revoke access and confirm
  5. Now open the Reddit app where you have logged in step 1
  6. You are no more able to access any info about the user and it will show errors like "Let's try that again" or "uh oh something went wrong but we're not     sure what"
  7. Open the app approximately after 20+ hours and see that you can reuse the previously logged-in account without any issue.

## Supporting Material/References:
I see that I got the latest app update and trying to reproduce the issue again on the latest version i.e 2022.25.1 I will update you on it again. I assume previously my Reddit app version was 2022.25.0 or 2022.24.1
Device and version info{F1814768}
The account/username used for testing is: sateeshn_1

## Impact

Unauthorized access to account even though revoking the access.

</details>

---
*Analysed by Claude on 2026-05-24*
