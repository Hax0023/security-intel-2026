# Missing Input Validation on User Name Length Enables Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 1018037 | https://hackerone.com/reports/1018037
- **Submitted:** 2020-10-24
- **Reporter:** tw4v3sx
- **Program:** Hey.com
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Improper Input Validation, Denial of Service (DoS), Resource Exhaustion, Client-Side Crash
- **CVEs:** None
- **Category:** memory-binary

## Summary
Hey.com fails to validate the length of user name fields, allowing attackers to set excessively long names that cause both server-side (500 errors) and client-side (Android app crashes) denial of service. An attacker can either crash their own Android app or send messages with a long-named account to slow down or crash recipient accounts.

## Attack scenario
1. Attacker navigates to the account settings page at app.hey.com/contacts/{user_id}/user/edit
2. Attacker submits an extremely long string (thousands of characters) as their account name with no validation enforcement
3. Server accepts the oversized input and stores it in the database without length restrictions
4. When attacker logs in via Android app, the UI fails to render the excessively long name, causing the app to crash or hang indefinitely
5. If attacker sends emails/messages with the long-named account, recipient's application slows dramatically when rendering the sender's name in contact lists, message headers, or inbox views
6. Recipient experiences 40+ minute loading times or complete app unavailability, achieving denial of service against victim account

## Root cause
Absence of input validation on the name field - no maximum length constraints enforced at the application or database layer, allowing arbitrary-length strings to be stored and processed by both web and mobile clients

## Attacker mindset
Opportunistic - discovered the vulnerability through basic fuzzing (changing name to long value), then recognized dual impact potential: self-DoS capability and griefing vector against other users. Low effort, high impact abuse case.

## Defensive takeaways
- Implement strict input validation with reasonable max length limits on all user-modifiable fields (e.g., names, profiles)
- Enforce validation at multiple layers: client-side (UX feedback), server-side (security boundary), and database schema (constraints)
- Add server-side request size limits and timeouts to prevent resource exhaustion from processing oversized payloads
- Implement UI rendering safeguards in mobile apps to gracefully handle unexpectedly long strings (truncation, ellipsis)
- Consider field-specific constraints: names typically 50-255 characters, enforce at API level with 400 Bad Request for violations
- Add monitoring for unusual input patterns or repeated name change requests indicating potential abuse
- Test with extreme input sizes during security QA (strings >1MB, millions of characters)

## Variant hunting
Check other user profile fields (bio, title, company) for similar validation gaps
Test name fields in team/organization settings and group chats
Attempt to inject other resource-intensive payloads (Unicode, special characters, binary data) in name fields
Verify if profile picture, avatar, or media uploads have similar size/validation issues
Check if the vulnerability affects API endpoints beyond the web UI (REST API, GraphQL)
Test batch operations (bulk user imports, name changes via admin API) for amplified DoS potential
Investigate if long names in contact lists or shared folders have different impact vectors

## MITRE ATT&CK
- T1190
- T1498

## Notes
This is a straightforward input validation vulnerability with clear business impact. The dual nature (self-DoS + griefing) makes it particularly dangerous. The 500 error response suggests backend buffer issues or database column limits being exceeded. The 40-minute hang indicates synchronous rendering without async/pagination in the mobile app. Severity should be High due to user account accessibility impact; not Critical only because it requires active exploitation per victim.

## Full report
<details><summary>Expand</summary>

Summary :
=========
after trying to change my initial name to something long i found out that their are no limits to how long it can be , so i directly changed it to something very long {F1050497} which caused my account to really slow down when accessing it and in **the android app , it just keeps crashing** whenever i open it ( no way to access my account at all ) + if i make it longer i get a **500 Internal Server Error response** which highly suggests that this can cause a **server side denial of service .**

Description:
==========
due to not checking the length of the name one can change it to a very long one causing both a server side denial of service  and a client side one

server side : 
------------

one can send multiple requests to change the name of the account and each of them containing a very long name which will cause a 500 internal server error leading to an extensive Resource Consumption.

client side : 
-----------
- if one is able to change the name another account he will also have the ability to crash his android app therefore preventing him from accessing his account.
- if one with a long name sends a message to any email he will slowwwwww down everything where the message appears including folders (inbox , trash ..) and prevent him from accessing his contacts where the email's name also appears , because the app will hang on a loading screen for about 40min each time , and this can be more if for example he sends multiple messages or use multiple accounts ( each on with a long name ) to send a message to the victim mail.

Proof of Concept:
==============

1. open `https://app.hey.com/contacts/%user_id_number%/user/edit`and change the name to the one attached {F1050497} and submit.
1. now u can't open the android app and u can slow down anyone's account just by sending them a message (or multiple ones).

## Impact

- **Attacker can perform a DoS Attack against the server**
- **slow down anyone's account**
- **crash the android app**

</details>

---
*Analysed by Claude on 2026-05-24*
