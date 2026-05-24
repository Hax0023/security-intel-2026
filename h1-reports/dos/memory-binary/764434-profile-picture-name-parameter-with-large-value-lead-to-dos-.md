# Unrestricted Profile Picture Filename Length Causes DoS via GraphQL Response Bloat

## Metadata
- **Source:** HackerOne
- **Report:** 764434 | https://hackerone.com/reports/764434
- **Submitted:** 2019-12-25
- **Reporter:** d3f4u17
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Input Validation Flaw, GraphQL Response Bloat
- **CVEs:** None
- **Category:** memory-binary

## Summary
The HackerOne profile picture upload feature lacks filename length validation, allowing attackers to submit multi-megabyte filenames. Since GraphQL queries return complete filenames in responses across multiple pages (reports, profiles, leaderboards), this causes severe client-side DoS by bloating response payloads and crashing browsers or timing out page loads.

## Attack scenario
1. Attacker navigates to profile picture upload at hackerone.com/settings/profile/edit
2. Attacker intercepts the upload request and replaces the filename with a 3MB+ junk string (e.g., repeating characters) while maintaining a valid image extension
3. System accepts the oversized filename without validation and stores it in the database
4. When any GraphQL query fetches user data (profile page, report participants, leaderboard), the response includes the massive filename string
5. Client browser receives multi-megabyte JSON payloads, causing severe lag, memory exhaustion, and crashes
6. If multiple attacker accounts use this technique on shared pages (report participants, program leaderboards), the cumulative payload causes platform-wide DoS

## Root cause
Missing input validation on profile picture filename length during upload. The application fails to enforce reasonable filename size constraints and blindly includes the full filename in all downstream GraphQL responses without truncation or sanitization.

## Attacker mindset
An attacker with a HackerOne account exploits the lack of input validation to craft a low-effort, high-impact DoS attack affecting multiple users viewing shared resources. The attack is particularly effective on pages displaying multiple profiles (leaderboards, report participants) where aggregate payload sizes become catastrophic. This represents a griefing/disruption attack rather than data theft.

## Defensive takeaways
- Implement strict filename length limits (e.g., 255 characters) at upload time with server-side validation
- Truncate or hash filenames in GraphQL responses rather than returning raw user input
- Add response size monitoring and alerts for unusually large payloads
- Implement rate limiting on profile picture uploads per user/time period
- Sanitize and validate all user-supplied filename inputs server-side before storage
- Consider storing filenames separately from display URLs and generating clean references
- Add client-side response size limits and graceful degradation for oversized payloads

## Variant hunting
Check other file upload features (cover photos, report attachments) for similar filename validation bypasses
Test other user-controlled fields included in GraphQL responses (bios, descriptions) for similar bloat attacks
Examine API endpoints returning user data in bulk (search, filters, exports) for response amplification
Review other platforms' leaderboard/listing pages that display many user profiles for identical vulnerabilities
Test SVG or HTML filenames to determine if XSS is possible alongside DoS

## MITRE ATT&CK
- T1190
- T1498
- T1499

## Notes
The writeup demonstrates clear proof-of-concept with multiple impact scenarios. The attacker responsibly did not fully execute the DDoS scenario (Scenario #2) on production. HackerOne's use of GraphQL without response size limits created a perfect storm for this vulnerability. The issue affects not just direct victims but all users viewing pages containing the attacker's profile, making it a high-impact griefing vector on a platform with thousands of concurrent researchers.

## Full report
<details><summary>Expand</summary>

# Summary:

The issue persists as there are no text limitations for profile-picture name while uploading the profile-picture, these heavy text names can cause denial of service on different pages of hackerone.

# Description:

I was checking the profile picture upload feature of  hackerone and found out that there is no text limitation for image name, You can provide as much long image name as you want.
{F668357}

At first it didn’t look like a serious issue so I played with it a little and tried to add some special characters to make it throw a 500 response but didn’t work out.

The next thing I noticed that there are many places where a graphql query is getting executed to fetch the info of the user and the json response is also containing the Image url along with the filename which was provided at the time of upload.

So the first thought that came into my mind is to provide a humongous long string at the place of the image name so I created the payload(attached with the report **payload.txt**) and paste the entire payload in front of the filename, the size of the payload is approx 3MB and it took a little bit of time to execute the request. Account used - @d3f4ul7_m4n

{F668360}

{F668358}

Then I created a dummy report #654270 using my main account(@red_assassin) and invited @d3f4ul7_m4n into that report and found out that a request has been made to the endpoint `/reports/<report-id>/participants/` and as the response contains a humongous text payload it took a long amount of time to load, enough for a timeout and to crash the browser, to create more impact I did the same trick with my another account @fossnow27 and invited it to the same report so that when the endpoint `/reports/<report-id>/participants/` starts loading huge amount of junk gets returned inside the response to crash the report.
> I can also invite you to the dummy report for POC.

{F668359}

As you can see the amount of data loaded is so huge that even burp can't handle it.

Next thing I did was to load all the pages which were displaying my profile pictures in it e.g. profile page, reports page, invited reports page and I noticed that all the pages are taking significantly much more amount of time to load as they were taking before and some were even failing to load and crashing my browser.

{F668371}

# Steps To Reproduce

* Go to https://hackerone.com/settings/profile/edit
* Upload new profile picture and Intercept the request using Burp
{F668357}
* Add the payload text (attached with report payload.txt) at the starting of the filename in the above request e.g `<payload>abcd.png` 


# Security Impact/How an attacker can exploit such behavior

## Scenario - #1

Few months back I reported an issue on hackerone as it was a duplicate issue I got invited as a participant in the original report by the program. Report link - https://hackerone.com/reports/442522
Now suppose if I act as an attacker I can restrict the access to that report for all the participants by doing the above mentioned trick.

An attacker can restrict access of the report if the attacker is an external participant to the report.

## Scenario - #2

> I didn't tried this scenario as I didn't want to affect anything in Production/Live environment.

**Program Pages**
As you can see program pages have top hacker images and the thank you page has hundreds of hacker images. GraphQL queries are used to load the image URLs of the hacker profiles.

{F668378}

{F668379}

In this scenario, a **DDoS** attack is possible if more than one hacker tries to do the same trick as discussed previously, the amount of data needed to load will be huge which can easily crash the web page and the browser of the victim because of this lot of hackerone pages including Program pages can get affected.

## Impact

*  Blocking or Slowing Down of Hackerone pages containing the Payload Image
*  Crashing of Web browser.

</details>

---
*Analysed by Claude on 2026-05-24*
