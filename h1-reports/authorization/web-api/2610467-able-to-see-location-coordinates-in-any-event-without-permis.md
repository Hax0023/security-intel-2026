# Location Coordinates Exposed in Event API Response Despite Privacy Settings

## Metadata
- **Source:** HackerOne
- **Report:** 2610467 | https://hackerone.com/reports/2610467
- **Submitted:** 2024-07-18
- **Reporter:** ezzra
- **Program:** Fetlife
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Information Disclosure, Broken Access Control, Insufficient Authorization
- **CVEs:** None
- **Category:** web-api

## Summary
FetLife's event API endpoint leaks precise geographic coordinates in HTTP responses even when the event host has enabled privacy settings to hide the exact address from non-RSVP attendees. An unauthenticated or unauthorized attacker can extract latitude/longitude coordinates from the API response and reverse-engineer the event's physical location on Google Maps.

## Attack scenario
1. Attacker creates two accounts on FetLife
2. Victim account creates a private event and enables the 'Address & Name of Location' privacy setting to hide the address from non-attendees
3. Attacker proxies HTTP traffic and navigates to the event page with their account
4. Attacker intercepts the GET /events/{event-id} API request and examines the response body
5. Attacker locates and extracts the location coordinates (latitude/longitude) embedded in the API response
6. Attacker reverses the coordinate order and inputs them into Google Maps to pinpoint the exact physical location of the event

## Root cause
The API endpoint returns the complete location object containing geographic coordinates in the JSON response without checking whether the requesting user has proper authorization to view location details. The privacy setting is enforced only on the frontend/UI layer but not validated server-side before returning sensitive location data in the API response.

## Attacker mindset
An attacker with malicious intent could use this vulnerability to dox event attendees, conduct physical surveillance, harassment, or stalking by determining exact event locations despite host privacy protections. This is particularly dangerous on adult/social platforms where privacy and security are critical.

## Defensive takeaways
- Implement server-side authorization checks before including sensitive data (coordinates, addresses) in API responses
- Apply the principle of least privilege: only return location data to users with explicit permission
- Validate privacy settings on the backend, not just the frontend
- Consider omitting or masking coordinates entirely from API responses when privacy settings restrict location visibility
- Audit all API endpoints for similar authorization bypasses where sensitive user/event data is exposed
- Implement field-level access control in API serializers to conditionally exclude restricted data

## Variant hunting
Check other event endpoints (event list, search, calendar) for similar coordinate leakage
Test if other sensitive event fields (attendee lists, private notes) are also leaked via API despite privacy settings
Examine user profile endpoints for location coordinate exposure
Test older API versions or deprecated endpoints that might lack authorization checks
Check cached or archived API responses from CDNs that might bypass fresh authorization validation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Gather Victim Identity Information
- T1598 - Phishing for Information

## Notes
The vulnerability is particularly impactful because FetLife is an adult social network where location privacy is critical for user safety and security. The attacker does not need special privileges beyond creating a basic account. The coordinates are intentionally reversed in the response, suggesting possible obfuscation attempts that failed to provide actual security. This is a classic case of security through obscurity rather than proper access control.

## Full report
<details><summary>Expand</summary>

Hi Fetlife team!

You can see the **location coordinates** in endpoint ``https://fetlife.com/events/{event-id}`` **response** even though the host event has blocked non-RSVP users (users don't attend the event) from seeing the exact address.

If the event host does not hide the address via privacy setting or the attacker has already attended the event, there's a Google Map link on the right event detail tab.

{F3448703}

If you check the coordinates from Google Map link, you will see that it is approximately the same as the coordinates you see in the response.

The coordinates in the response are reversed, so when entering them on Google Map you need to reverse them. 

``131.04425, -12.496252 -> -12.496252, 131.04425``

{F3448636}

Attack condition/Limitation:
=====================
Attackers are not being banned from the event.

Step to Reproduce:
=====================
1. Open Burp and proxy all HTTP requests.
2. Prepare 2 accounts. In this case, I use my 2 accounts: Ezzra1 (attacker), Ezzra2 (victim).
3. Victim creates event and goes to the privacy setting, ticks the box ``Address & Name of Location`` and clicks ``Update Event Privacy`` to hide the exact address.
4. Attacker goes to the event ``https://fetlife.com/events/{event-id}`` 
5. Check HTTP history. You will see the **Request** ``GET /events/{event-id}``
6. In **Response** tab, type in the search box **location** and now you can see the location coordinates.

## Impact

Attackers can see/guess the exact location of the event.

</details>

---
*Analysed by Claude on 2026-05-24*
