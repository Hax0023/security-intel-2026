# Broken Access Control on Private Assets via JSON Response Format

## Metadata
- **Source:** HackerOne
- **Report:** 1424291 | https://hackerone.com/reports/1424291
- **Submitted:** 2021-12-12
- **Reporter:** trieulieuf9
- **Program:** FetLife
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Broken Access Control, Authorization Bypass, Inconsistent Security Implementation
- **CVEs:** None
- **Category:** web-api

## Summary
The endpoint serving user pictures, videos, and posts implements authorization checks only for HTML responses but fails to validate permissions when the same endpoint returns JSON format. An authenticated attacker can bypass authorization by sending Accept: application/json header to access any private media they shouldn't have access to.

## Attack scenario
1. Attacker obtains valid session cookies for a FetLife account through legitimate login
2. Attacker enumerates or discovers user IDs and asset IDs of target private content (through social engineering, information disclosure, or systematic enumeration)
3. Attacker crafts HTTP request to resource endpoint with Accept: application/json header and valid session cookie
4. Server processes request and recognizes JSON format response is requested
5. Authorization check is skipped for JSON responses, and private asset data is returned in JSON format
6. Attacker extracts sensitive private pictures, videos, or posts from JSON response payload

## Root cause
The application implements content negotiation based on Accept header but has inconsistent authorization logic across different response formats. The authorization check is likely performed at the view/template rendering layer rather than at the resource access layer, allowing it to be bypassed when alternative content types are requested.

## Attacker mindset
An authenticated user with curiosity about other users' private content could systematically request JSON responses to bypass frontend authorization checks. The attacker needs prior knowledge of asset IDs but can obtain these through various reconnaissance methods. This represents a low-effort, high-reward attack if asset IDs can be enumerated.

## Defensive takeaways
- Implement authorization checks at the resource/data layer before content negotiation, not at the presentation layer
- Ensure all response formats (HTML, JSON, XML, etc.) go through identical authorization validation
- Use consistent security controls regardless of Accept header values
- Implement server-side validation of user permissions before retrieving or serializing sensitive data
- Add logging and alerting for access to private resources across all content types
- Use allowlisting for Accept header values if only specific formats are supported
- Test authorization logic across all supported response formats during security testing

## Variant hunting
Check other endpoints for similar content-negotiation-based authorization bypass (API endpoints, export functions)
Test if XML/CSV/PDF responses have same authorization bypass
Look for other endpoints that differentiate between HTML and JSON but may have inconsistent checks
Check if authenticated users can access deleted/archived content via JSON
Test if authorization bypass works for other user roles (admin, moderator)
Examine if other private resources (messages, profile data, location) have similar bypass
Check if rate limiting differs between HTML and JSON responses

## MITRE ATT&CK
- T1190
- T1566
- T1592
- T1526

## Notes
This is a classic case of inconsistent security implementation across different code paths. The fact that the attacker still needed a valid session cookie means this requires authentication, reducing severity slightly from Critical. However, the ability to access private content without explicit permission justifies High severity. The writeup notes asset IDs are required, which limits practical exploitation unless enumeration is possible.

## Full report
<details><summary>Expand</summary>

# Description
Endpoint `https://fetlife.com/users/{user-id}/pictures/{pic-id}` has 2 types of responses, HTML and JSON. The type of response depends on `Accept`  header of request it get. If request contains `Accept: application/json`, then it will return JSON response. Other than that, it returns HTML response.

When this endpoint returns JSON response, it does not check if requester is authorized to access requested resource. Therefore, attacker can access any private picture by requesting them in JSON response.

# PoC
User `trieulieuf9` has the following private assets
**Picture**: https://fetlife.com/users/14104003/pictures/120041856
**Video**: https://fetlife.com/users/14104003/videos/3102890
**Post**: https://fetlife.com/users/14104003/posts/7673012

We can access them with the following `curl` commands
**Picture**: 
```
curl https://fetlife.com/users/14104003/pictures/120041856 -H "Cookie: _fl_sessionid={your-session}" -H "Accept: application/json" --user-agent "not cur1"
```
**Video**:
```
curl https://fetlife.com/users/14104003/videos/3102890 -H "Cookie: _fl_sessionid={your-session}" -H "Accept: application/json" --user-agent "not cur1"
```
**Post**:
```
curl https://fetlife.com/users/14104003/posts/7673012 -H "Cookie: _fl_sessionid={your-session}" -H "Accept: application/json" --user-agent "not cur1"
```

# Limitation
Attacker needs to know asset IDs before the attack.

## Impact

Attacker can access any private picture/video/post if he can somehow get their ID.

</details>

---
*Analysed by Claude on 2026-05-24*
