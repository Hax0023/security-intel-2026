# Sensitive Password Hash Exposure via Admin User Search Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1489892 | https://hackerone.com/reports/1489892
- **Submitted:** 2022-02-23
- **Reporter:** dark_haxor
- **Program:** upchieve.org
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Information Disclosure, Sensitive Data Exposure, Improper Access Control, API Data Leakage
- **CVEs:** None
- **Category:** uncategorised

## Summary
The /api/users endpoint accessible from the admin panel returned password hashes for all users in search results, exposing sensitive authentication credentials. This vulnerability allowed authenticated administrators to retrieve plaintext-searchable password hashes without legitimate business purpose, enabling offline brute-force attacks against user accounts.

## Attack scenario
1. Attacker gains valid admin credentials through social engineering, credential stuffing, or insider access
2. Attacker navigates to Admin → Search Users panel in the application
3. Attacker sends GET request to /api/users endpoint with minimal filter parameters (firstName=test)
4. Backend API returns user records including password_hash field in JSON response without filtering
5. Attacker extracts all password hashes from response and downloads complete user credential database
6. Attacker performs offline dictionary/brute-force attacks on weak password hashes to gain additional user accounts

## Root cause
Backend API endpoint failed to implement output filtering/sanitization of sensitive fields. The /api/users endpoint returned raw user objects including password_hash fields to authenticated admin users without field-level access controls. No distinction between frontend-displayable fields and sensitive backend-only data.

## Attacker mindset
Opportunistic insider or low-privilege admin seeking to escalate access by harvesting credential hashes. Alternatively, external attacker who compromised single admin account leveraging overprivileged API response to compromise entire user database. Attacker anticipates weak password entropy and password reuse across services.

## Defensive takeaways
- Implement strict output filtering in API responses - never include password hashes, salts, or authentication material in any API response
- Apply principle of least privilege - admin APIs should only return fields necessary for specified admin function
- Implement field-level access controls using allowlists rather than blocklists for sensitive endpoints
- Audit all API endpoints returning user data to ensure no sensitive fields are exposed
- Add logging/alerting for bulk user data exports and password hash access patterns
- Consider using separate DTOs (Data Transfer Objects) for API responses that explicitly exclude sensitive fields
- Implement role-based response filtering - admin role should not receive password hashes even if data exists
- Add rate limiting to user search endpoints to detect bulk data harvesting attempts

## Variant hunting
Search for similar patterns: (1) Other endpoints accepting filter parameters that return user objects - /api/admin/users, /api/users/export, /api/search/users, /api/bulk-operations; (2) Any endpoint with user data that includes 'password', 'hash', 'pwd', 'secret' fields; (3) Admin panels with bulk user operations (import/export) that may expose hashes; (4) API endpoints that support wildcard or empty filters that return full datasets; (5) Reporting/analytics endpoints that may include raw user field data

## MITRE ATT&CK
- T1190
- T1526
- T1087
- T1040
- T1005
- T1530
- T1557

## Notes
Hash exposure severity elevated due to: (1) low entropy user passwords likely crackable with commodity hardware, (2) password reuse across services enables lateral account takeover, (3) broad exposure to all users not filtered subset, (4) accessible via admin role without additional auth factor. Fixed by removing password_hash from API response entirely regardless of authentication level.

## Full report
<details><summary>Expand</summary>

# Summary:
During my primary research I found that `api/users?page=1&userId=&firstName=test&lastName=&email=&partnerOrg=&highSchool=` this endpoint gives hashed password of all users.

# Steps To Reproduce:
+ Login to Admin and go to Admin--> Search Users.
+ We see a request like this was send and in response we get the hashed password of all the users.

{F1630381}

##HTTP Request:

```
GET /api/users?page=1&userId=&firstName=test&lastName=&email=&partnerOrg=&highSchool= HTTP/2
Host: hackers.upchieve.org
Cookie: connect.sid=s%3AaF9AzSGty6cZOHNTyahImdIzUoSDCWuB.ofJzU1Tr25W2Kd2unMFlpS66K4VsPtK3YE0xmHvUZGU; _gcl_au=1.1.2044852401.1644683211; _ga=GA1.2.1811282066.1644683221; _csrf=whFQZop0bR6xQh6KtmNQLBfS; __cf_bm=2KDOr5.OqRrhRkG3HhcUs0vp57z5O6ajxpDfiZBVfGA-1645624338-0-AU9Yc7GzGOeS+GILwGKIEWzbToj/4SEhBw5wog9uHW0rWkomQxhuC756xXzHVx5vQZWpm8qGUUNBPxFB6cvtTQ9BfzCJWA5Zq9jDYP3Z9p+Olw+qCSjBa/rjulVDF51Kjg==; io=zIQg9SCEJ_ZblHVdAAAy; _gid=GA1.2.1980510602.1645624337; ph_bogus_posthog=%7B%22distinct_id%22%3A%22619ea2c8488636001138121f%22%2C%22%24device_id%22%3A%2217eeec24dba290-06a553129ffb21-4c3e227d-1fa400-17eeec24dbb903%22%2C%22%24user_id%22%3A%22619ea2c8488636001138121f%22%2C%22%24initial_referrer%22%3A%22%24direct%22%2C%22%24initial_referring_domain%22%3A%22%24direct%22%2C%22%24referrer%22%3A%22%24direct%22%2C%22%24referring_domain%22%3A%22%24direct%22%2C%22%24session_recording_enabled%22%3Afalse%7D
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Newrelic: eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjI2NzQ5NzQiLCJhcCI6IjQyOTE2Mzc1MCIsImlkIjoiNzFhMzgxOGNjZDQ2OGNkYyIsInRyIjoiYjBiM2Q0YTI3N2NjZDZmODBmOWU2NWIwODBlY2U1NDAiLCJ0aSI6MTY0NTYyNTExMDY0N319
Traceparent: 00-b0b3d4a277ccd6f80f9e65b080ece540-71a3818ccd468cdc-01
Tracestate: 2674974@nr=0-1-2674974-429163750-71a3818ccd468cdc----1645625110647
X-Csrf-Token: KeypPQND-ch0LQMIPkTckMoZdYHTBgA4Mha0
X-Requested-With: XMLHttpRequest
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Te: trailers
```

## Impact

Chances that weak passwords can be cracked and people might have same passwords for email and other places.

</details>

---
*Analysed by Claude on 2026-05-24*
