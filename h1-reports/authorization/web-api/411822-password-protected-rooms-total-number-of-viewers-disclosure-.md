# Password Protected Room Viewer Count Disclosure via Contest Log Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 411822 | https://hackerone.com/reports/411822
- **Submitted:** 2018-09-20
- **Reporter:** batee5a
- **Program:** Chaturbate
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Information Disclosure, Improper Access Control, Authorization Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
An unauthenticated attacker can enumerate the total number of active viewers in password-protected rooms by accessing the /contest/log/{username}/ endpoint, which should be completely private. This information disclosure bypasses the intended access controls that prevent any data exposure about password-protected rooms to unauthorized users.

## Attack scenario
1. Attacker identifies a target Chaturbate user who operates a password-protected room
2. Attacker constructs the endpoint URL: https://chaturbate.com/contest/log/{target_username}/
3. Attacker accesses the endpoint without authentication or the room password
4. Endpoint responds with current viewer count and historical viewer data
5. Attacker can monitor viewer count changes over time to infer activity patterns
6. Attacker uses this information for social engineering, blackmail, or competitive intelligence

## Root cause
The contest/log endpoint lacks proper authorization checks to verify if the requester has permission to view password-protected room statistics. The endpoint returns viewer count data without validating that the caller either owns the room or has the room password, treating it as public data.

## Attacker mindset
An attacker seeking to gather intelligence about private room activity for purposes of harassment, blackmail, competitive disadvantage, or social engineering. The low barrier to exploitation (simple URL enumeration) makes this attractive for widespread reconnaissance.

## Defensive takeaways
- Implement authorization checks on all endpoints that return sensitive data about password-protected resources
- Verify user authentication and authorization before exposing any statistics or metadata about private rooms
- Return HTTP 401/403 errors or zero values for unauthorized access attempts rather than actual data
- Audit all endpoints that handle contest/viewer data to ensure consistent authorization policies
- Apply principle of least privilege: only room owners or authenticated authorized users should access room statistics
- Consider that password-protected content requires authentication before ANY associated data is exposed

## Variant hunting
Check other /contest/ endpoints for similar authorization bypass patterns
Test historical data endpoints that might expose viewer trends for protected rooms
Examine any analytics or reporting endpoints that could leak aggregate room data
Verify /viewers/, /stats/, /logs/ endpoints for password-protected rooms
Test with variations like /contest/log/{username}/history, /archive, /replay endpoints
Check API endpoints that might expose room metadata in JSON format

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate Information via API
- T1555 - Credentials from Password Stores
- T1589 - Gather Victim Identity Information

## Notes
This is a straightforward authorization bypass on an information disclosure endpoint. The vulnerability demonstrates inadequate access control on sensitive data endpoints. The reporter provides clear proof-of-concept steps and demonstrates that the endpoint should either return zero values or an authorization error. The impact is somewhat limited as it only reveals viewer counts rather than sensitive personal data, but combined with other information could facilitate harassment or blackmail of cam performers.

## Full report
<details><summary>Expand</summary>

##Summary##
Password protected rooms are supposed to be completely private, no information should be exposed if you do not have the room's password, and the UI looks like this.

{F348826}

However, through the following endpoint, It is possible to know the total number of viewers of the room even if it is password protected.
https://chaturbate.com/contest/log/{Username}/

## Steps To Reproduce:

  1.  Create a profile and add a Password to the room, lets say for testing purposes the username is "batee5a123" which is my test username.
  2. Go to users and refresh the user list (Just to make sure your are synced) and see yourself there

{F348830}

  3. Open an Incognito instance in your web browser and visit the following endpoint:
https://chaturbate.com/contest/log/batee5a123/ Or whatever your username is instead of "batee5a123", You'll find the total number of viewers there.

{F348824}

  4. For further testing, I made a second account and gave it the password and logged in, then from another browser instance I visited the same endpoint to see it is enumerating the total views and that it increased to 2 after joining with my other test account.

{F348825}

## Impact

Password protected rooms are supposed to be completely private with no exposure of any information what so ever, If even the least information exposed could be used in social engineering or blackmailing any chaturbate user.

The correct response for this matter should be like this (always give zero):

{F348823}

Or show Unauthorized message.

</details>

---
*Analysed by Claude on 2026-05-24*
