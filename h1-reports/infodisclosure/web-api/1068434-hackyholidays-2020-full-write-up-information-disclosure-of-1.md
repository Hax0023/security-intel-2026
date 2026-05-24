# HackyHolidays 2020 CTF - Information Disclosure of 12 Flags

## Metadata
- **Source:** HackerOne
- **Report:** 1068434 | https://hackerone.com/reports/1068434
- **Submitted:** 2020-12-29
- **Reporter:** liamg
- **Program:** HackerOne Hacky Holidays 2020 CTF
- **Bounty:** CTF competition (non-monetary)
- **Severity:** high
- **Vuln:** Information Disclosure, Insecure Direct Object Reference (IDOR), Sensitive Data in robots.txt, Improper Access Control, Path Traversal/Enumeration, Weak Encoding (Base64), API Enumeration
- **CVEs:** None
- **Category:** web-api

## Summary
A comprehensive CTF writeup demonstrating multiple information disclosure vulnerabilities across a deliberately vulnerable web application. The researcher identified 12 flags through various techniques including robots.txt inspection, DOM analysis, base64 decoding, API fuzzing, and direct object reference exploitation.

## Attack scenario
1. Attacker begins reconnaissance by checking standard files like robots.txt, discovering sensitive paths and embedded flags
2. Attacker inspects page source and DOM elements, finding hidden flags in comments or HTML attributes
3. Attacker identifies non-standard library versions through source code review and diffs them against known versions to find anomalies
4. Attacker discovers API endpoints through fuzzing and parameter discovery techniques
5. Attacker recognizes weak encoding schemes (base64) protecting object IDs and manipulates them to access unauthorized records
6. Attacker leverages IDOR vulnerabilities by modifying sequential IDs to access missing or hidden records containing flags

## Root cause
Multiple security misconfigurations and design flaws: (1) Sensitive information exposed in robots.txt, (2) Flags embedded in HTML comments/DOM, (3) Modified library versions with embedded secrets, (4) Insufficient access controls on API endpoints, (5) Base64-encoded parameters treated as security measure rather than encoding, (6) No authentication/authorization on data retrieval endpoints, (7) Sequential/predictable object IDs without access controls

## Attacker mindset
Methodical reconnaissance and enumeration mindset. The attacker demonstrates persistence by trying multiple approaches (unintended solutions), comfort with decoding/encoding schemes, API fuzzing capabilities, and understanding that weak access controls create IDOR vulnerabilities. Shows capability to identify patterns (missing ID 1) and test hypotheses systematically.

## Defensive takeaways
- Never expose sensitive information in robots.txt, comments, or HTML DOM elements
- Implement proper authentication and authorization on all API endpoints
- Use strong, non-sequential object identifiers (UUIDs) instead of predictable integers
- Apply cryptographic controls rather than encoding for sensitive data protection
- Validate all API parameters server-side with strict type and range checking
- Implement rate limiting and anomaly detection on API endpoints to prevent fuzzing
- Remove or whitelist base64-encoded parameters; do not rely on encoding for security
- Conduct regular code reviews to prevent embedded secrets, flags, or sensitive data in source
- Use version control and file integrity monitoring to detect unauthorized library modifications
- Implement proper access control checks for each data record, not relying on client-side validation
- Employ automated security scanning to identify exposed API endpoints and information disclosure

## Variant hunting
Similar vulnerabilities exist in production applications: (1) Check /robots.txt, /.git, /.env for exposed paths and secrets, (2) Inspect DOM and page source for hidden flags/credentials in comments, (3) Fuzz API endpoints with scout/ffuf to find undocumented endpoints, (4) Test for IDOR by modifying sequential IDs across all record-based endpoints, (5) Decode base64 values in requests/responses to identify weak encoding, (6) Test API authentication bypass by removing/modifying auth headers, (7) Search for backup files (.bak, .old, .sql) containing sensitive data, (8) Check for information disclosure in error messages and stack traces

## MITRE ATT&CK
- T1190
- T1526
- T1592
- T1589
- T1598
- T1591
- T1201
- T1120
- T1040
- T1041

## Notes
This is a CTF writeup demonstrating intentionally vulnerable application design. Key insights: (1) The researcher found an 'unintended solution' for Flag 2 by diffing jQuery versions, showing creative problem-solving, (2) Base64 is encoding, not encryption - a common misconception, (3) Sequential IDs are highly exploitable when combined with missing access controls, (4) API discovery through fuzzing is highly effective against undocumented endpoints, (5) The vulnerability chain demonstrates that multiple low-severity issues (information disclosure) compound into high-impact vulnerabilities. The writeup lacks details on flags 5-12 but demonstrates solid methodology for flag discovery.

## Full report
<details><summary>Expand</summary>

## Intro

This is my report for the 2020 Hacky Holidays HackerOne CTF. I managed to find all 12 flags with the assistance of my little helper, Jake. He specialises in brute-forcing via a unique keyboard mashing technique:

{F1134543}

Anywho, let's get started...

## Flag 1: Robots

The first one was a nice easy find as a result of some basic enumeration.

Looking in [/robots.txt](https://hackyholidays.h1ctf.com/robots.txt), I immediately spotted the flag:

```
User-agent: *
Disallow: /s3cr3t-ar3a
Flag: flag{48104912-28b0-494a-9995-a203d1e261e7}
```

Flag: `flag{48104912-28b0-494a-9995-a203d1e261e7}`

## Flag 2: Moved

The content of the `robots.txt` file also contained a clue about the second flag:

```
Disallow: /s3cr3t-ar3a
```

There was a [/s3cr3t-ar3a](https://hackyholidays.h1ctf.com/s3cr3t-ar3a) page which the server requested spiders to avoid. Very suspect!

The secret area consisted of a message telling me the page had moved.

If I had hit "inspect element" and browsed the DOM I could have quite quickly spotted the flag.

{F1134542}

However...

### Unintended Solution

I'm ashamed to say I went the much longer way around. I initially viewed the static source code of the page, and noticed that the jQuery library wasn't loaded from a CDN like everything else on the site.

Viewing the file showed the version of jQuery:

```
/*! jQuery v3.5.1 ...
```

I downloaded the file and then grabbed the "real" jQuery v3.5.1. Diffing them showed an interesting anomaly in the CTF version of the file:

{F1134541}

Interesting! Piecing it together revealed the flag. At this point I realised I could have just inspected element and seen the flag. Whoops.

Flag: `flag{b7ebcb75-9100-4f91-8454-cfb9574459f7}`

## Flag 3: People Rater

The last challenge hinted at the existence of the `/apps` page. On this page I found another link, this time to the People Rater application at [/people-rater](https://hackyholidays.h1ctf.com/people-rater).

I was presented with a list of buttons, each with the name of a person. Clicking a button resulted in an alert box with a description of the person.

Digging a little deeper with dev tools, I could see that when I clicked a button, an HTTP request was made in the background. One such example is `https://hackyholidays.h1ctf.com/people-rater/entry?id=eyJpZCI6Mn0=`, which responded with:

```json
{"id":"eyJpZCI6Mn0=","name":"Tea Avery","rating":"Awful"}
```

It looked like that `id` was base64 encoded. Decoding it resulted in:

```json
{"id":2}
```

Going through the rest of the list and decoding the `id` field for each revealed that there was no record with an `id` of `1` in the list. Perhaps there was something interesting in the missing record?

I base64 encoded some JSON with an `id` of `1`:

```bash
$ echo '{"id":1}' | base64 
eyJpZCI6MX0K
```

...and supplied the resultant value to the `entry` endpoint: [/people-rater/entry?id=eyJpZCI6MX0K](https://hackyholidays.h1ctf.com/people-rater/entry?id=eyJpZCI6MX0K), and got a nice response:

```json
{"id":"eyJpZCI6MX0=","name":"The Grinch","rating":"Amazing in every possible way!","flag":"flag{b705fb11-fb55-442f-847f-0931be82ed9a}"}
```

There was the flag!

Flag: `flag{b705fb11-fb55-442f-847f-0931be82ed9a}`

## Flag 4: Swag Shop

A quick browse of the swag shop source code revealed the existence of an API:

{F1134539}

I decided to try a bit of fuzzing to reveal any other API endpoints that might help me to progress.

Fuzzing with:

```bash
scout url -s https://hackyholidays.h1ctf.com/swag-shop/api
```

...revealed:

```
/swag-shop/api/user
/swag-shop/api/sessions
```

Hitting the `user` endpoint gave a 400 status and told me I was missing required parameters. I put that to one side for a moment and started to look at `sessions` instead.

The `sessions` endpoint returned a list of sessions!

```json
{"sessions":["eyJ1c2VyIjpudWxsLCJjb29raWUiOiJZelZtTlRKaVlUTmtPV0ZsWVRZMllqQTFaVFkxTkRCbE5tSTBZbVpqTW1ObVpHWXpNemcxTVdKa1pEY3lNelkwWlRGbFlqZG1ORFkzTkRrek56SXdNR05pWmpOaE1qUTNZMlJtWTJFMk4yRm1NemRqTTJJMFpXTmxaVFZrTTJWa056VTNNVFV3WWpka1l6a3lOV0k0WTJJM1pXWmlOamsyTjJOak9UazBNalU9In0=","eyJ1c2VyIjpudWxsLCJjb29raWUiOiJaak0yTXpOak0ySmtaR1V5TXpWbU1tWTJaamN4TmpkbE5ETm1aalF3WlRsbVkyUmhOall4TldNNVkyWTFaalkyT0RVM05qa3hNVFEyTnprMFptSXhPV1poTjJaaFpqZzBZMkU1TnprMU5UUTJNek16WlRjME1XSmxNelZoWkRBME1EVXdZbVEzTkRsbVpURTRNbU5rTWpNeE16VTBNV1JsTVRKaE5XWXpPR1E9In0=","eyJ1c2VyIjoiQzdEQ0NFLTBFMERBQi1CMjAyMjYtRkM5MkVBLTFCOTA0MyIsImNvb2tpZSI6Ik5EVTBPREk1TW1ZM1pEWTJNalJpTVdFME1tWTNOR1F4TVdFME9ETXhNemcyTUdFMVlXUmhNVGMwWWpoa1lXRTNNelUxTWpaak5EZzVNRFEyWTJKaFlqWTNZVEZoWTJRM1lqQm1ZVGs0TjJRNVpXUTVNV1E1T1dGa05XRTJNakl5Wm1aak16WmpNRFEzT0RrNVptSTRaalpqT1dVME9HSmhNakl3Tm1Wa01UWT0ifQ==","eyJ1c2VyIjpudWxsLCJjb29raWUiOiJNRFJtWVRCaE4yRmlOalk1TUdGbE9XRm1ZVEU0WmpFMk4ySmpabVl6WldKa09UUmxPR1l3TWpJMU9HSXlOak0xT0RVME5qYzJZVGRsWlRNNE16RmlNMkkxTVRVek16VmlNakZoWXpWa01UYzRPREUzT0dNNFkySmxPVGs0TWpKbE1ESTJZalF6WkRReE1HTm1OVGcxT0RReFpqQm1PREJtWldReFptRTFZbUU9In0=","eyJ1c2VyIjpudWxsLCJjb29raWUiOiJNMlEyTURJek5EZzVNV0UwTjJNM05ESm1OVEl5TkdNM05XVXhZV1EwTkRSbFpXSTNNVGc0TWpJM1pHUmtNVGxsWlRNMlpEa3hNR1ZsTldFd05tWmlaV0ZrWmpaaE9EZzRNRFkzT0RsbVpHUmhZVE0xWTJJeU1HVmhNakExTmpkaU5ERmpZekJoTVdRNE5EVTFNRGM0TkRFMVltSTVZVEpqT0RCa01qRm1OMlk9In0=","eyJ1c2VyIjpudWxsLCJjb29raWUiOiJNV1kzTVRBek1UQmpaR1k0WkdNd1lqSTNaamsyWm1Zek1XSmxNV0V5WlRnMVl6RTBNbVpsWmpNd1ltSmpabVE0WlRVMFkyWXhZelZtWlRNMU4yUTFPRFkyWWpGa1ptRmlObUk1WmpJMU0yTTJNRFZpTmpBMFpqRmpORFZrTlRRNE4yVTJPRGRpTlRKbE1tRmlNVEV4T0RBNE1qVTJNemt4WldOaE5qRmtObVU9In0=","eyJ1c2VyIjpudWxsLCJjb29raWUiOiJNRE00WXpoaU4yUTNNbVkwWWpVMk0yRmtabUZsTkRNd01USTVNakV5T0RobE5HRmtNbUk1T1RjeU1EbGtOVEpoWlRjNFlqVXhaakl6TjJRNE5tUmpOamcyTm1VMU16VmxPV0V6T1RFNU5XWXlPVGN3Tm1KbFpESXlORGd5TVRBNVpEQTFPVGxpTVRZeU5EY3pOakZrWm1VME1UZ3hZV0V3TURVMVpXTmhOelE9In0=","eyJ1c2VyIjpudWxsLCJjb29raWUiOiJPR0kzTjJFeE9HVmpOek0xWldWbU5UazJaak5rWmpJd00yWmpZemRqTVdOaE9EZzRORGhoT0RSbU5qSTBORFJqWlRkbFpUZzBaVFV3TnpabVpEZGtZVEpqTjJJeU9EWTVZamN4Wm1JNVpHUmlZVGd6WmpoaVpEVmlPV1pqTVRWbFpEZ3pNVEJrTnpObU9ESTBPVE01WkRNM1kySmpabVk0TnpFeU9HRTNOVE09In0="]}
```

These looked like base64, so I decoded them:

```bash
$ curl https://hackyholidays.h1ctf.com/swag-shop/api/sessions | jq -r '.sessions[]' | base64 -d | jq

{
  "user": null,
  "cookie": "YzVmNTJiYTNkOWFlYTY2YjA1ZTY1NDBlNmI0YmZjMmNmZGYzMzg1MWJkZDcyMzY0ZTFlYjdmNDY3NDkzNzIwMGNiZjNhMjQ3Y2RmY2E2N2FmMzdjM2I0ZWNlZTVkM2VkNzU3MTUwYjdkYzkyNWI4Y2I3ZWZiNjk2N2NjOTk0MjU="
}
{
  "user": null,
  "cookie": "ZjM2MzNjM2JkZGUyMzVmMmY2ZjcxNjdlNDNmZjQwZTlmY2RhNjYxNWM5Y2Y1ZjY2ODU3NjkxMTQ2Nzk0ZmIxOWZhN2ZhZjg0Y2E5Nzk1NTQ2MzMzZTc0MWJlMzVhZDA0MDUwYmQ3NDlmZTE4MmNkMjMxMzU0MWRlMTJhNWYzOGQ="
}
{
  "user": "C7DCCE-0E0DAB-B20226-FC92EA-1B9043",
  "cookie": "NDU0ODI5MmY3ZDY2MjRiMWE0MmY3NGQxMWE0ODMxMzg2MGE1YWRhMTc0YjhkYWE3MzU1MjZjNDg5MDQ2Y2JhYjY3YTFhY2Q3YjBmYTk4N2Q5ZWQ5MWQ5OWFkNWE2MjIyZmZjMzZjMDQ3ODk5ZmI4ZjZjOWU0OGJhMjIwNmVkMTY="
}
{
  "user": null,
  "cookie": "MDRmYTBhN2FiNjY5MGFlOWFmYTE4ZjE2N2JjZmYzZWJkOTRlOGYwMjI1OGIyNjM1ODU0Njc2YTdlZTM4MzFiM2I1MTUzMzViMjFhYzVkMTc4ODE3OGM4Y2JlOTk4MjJlMDI2YjQzZDQxMGNmNTg1ODQxZjBmODBmZWQxZmE1YmE="
}
{
  "user": null,
  "cookie": "M2Q2MDIzNDg5MWE0N2M3NDJmNTIyNGM3NWUxYWQ0NDRlZWI3MTg4MjI3ZGRkMTllZTM2ZDkxMGVlNWEwNmZiZWFkZjZhODg4MDY3ODlmZGRhYTM1Y2IyMGVhMjA1NjdiNDFjYzBhMWQ4NDU1MDc4NDE1YmI5YTJjODBkMjFmN2Y="
}
{
  "user": null,
  "cookie": "MWY3MTAzMTBjZGY4ZGMwYjI3Zjk2ZmYzMWJlMWEyZTg1YzE0MmZlZjMwYmJjZmQ4ZTU0Y2YxYzVmZTM1N2Q1ODY2YjFkZmFiNmI5ZjI1M2M2MDViNjA0ZjFjNDVkNTQ4N2U2ODdiNTJlMmFiMTExODA4MjU2MzkxZWNhNjFkNmU="
}
{
  "user": null,
  "cookie": "MDM4YzhiN2Q3MmY0YjU2M2FkZmFlNDMwMTI5MjEyODhlNGFkMmI5OTcyMDlkNTJhZTc4YjUxZjIzN2Q4NmRjNjg2NmU1MzVlOWEzOTE5NWYyOTcwNmJlZDIyNDgyMTA5ZDA1OTliMTYyNDczNjFkZmU0MTgxYWEwMDU1ZWNhNzQ="
}
{
  "user": null,
  "cookie": "OGI3N2ExOGVjNzM1ZWVmNTk2ZjNkZjIwM2ZjYzdjMWNhODg4NDhhODRmNjI0NDRjZTdlZTg0ZTUwNzZmZDdkYTJjN2IyODY5YjcxZmI5ZGRiYTgzZjhiZDViOWZjMTVlZDgzMTBkNzNmODI0OTM5ZDM3Y2JjZmY4NzEyOGE3NTM="
}
```

I now had a session associated with an authenticated user (the third one down in the list). Using the cookie didn'

</details>

---
*Analysed by Claude on 2026-05-24*
