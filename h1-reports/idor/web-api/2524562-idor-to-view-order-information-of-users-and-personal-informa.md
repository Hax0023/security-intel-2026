# IDOR to View Order Information and Personal User Data on WakaTime API

## Metadata
- **Source:** HackerOne
- **Report:** 2524562 | https://hackerone.com/reports/2524562
- **Submitted:** 2024-05-29
- **Reporter:** hasn0x
- **Program:** WakaTime
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Object Level Authorization, Unauthorized Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
An IDOR vulnerability exists in the WakaTime API endpoint `/api/v1/users/` that allows authenticated attackers to view detailed personal information and profile data of arbitrary users by modifying the user identifier parameter. By replacing the `current` endpoint with a target username or user ID, attackers can enumerate and access sensitive user information including profile details, social media usernames, location data, and account settings.

## Attack scenario
1. Attacker authenticates to WakaTime and intercepts a request to `/api/v1/users/current?`
2. Attacker identifies that the endpoint returns detailed user profile information including personal data
3. Attacker replaces 'current' with a target username (e.g., `@hasn0xxxx`) to create request `/api/v1/users/@hasn0xxxx`
4. API processes the request without proper authorization checks and returns full user profile data
5. Attacker iterates through known or enumerated usernames to harvest personal information at scale
6. Attacker collects sensitive data including email status, social media handles, location, and profile URLs for malicious purposes

## Root cause
The API endpoint implements insufficient authorization controls that fail to verify if the requesting user has permission to access another user's profile data. The endpoint uses user-supplied identifiers (username/user ID) without proper access control validation, allowing any authenticated user to retrieve any other user's information.

## Attacker mindset
An attacker with basic API knowledge can easily enumerate user profiles and collect personal information for identity theft, social engineering, targeted harassment, or data aggregation. The low barrier to entry and high-value sensitive data make this an attractive vulnerability for malicious actors.

## Defensive takeaways
- Implement proper authorization checks at the object level - verify the authenticated user has legitimate access to the requested resource before returning data
- Use session-based identity verification rather than accepting arbitrary user identifiers in API paths without authorization
- Apply principle of least privilege - only return data fields that are truly necessary for the legitimate use case
- Consider restricting profile endpoint access to only return the authenticated user's own data, or require explicit public profile settings
- Implement rate limiting on user enumeration endpoints to prevent large-scale data harvesting
- Audit all API endpoints that return user data to ensure consistent authorization controls
- Use automated security testing tools to identify IDOR vulnerabilities across the API surface

## Variant hunting
Check `/api/v1/users/{id}/orders` or similar endpoints for order data IDOR
Test other user-related endpoints like `/api/v1/users/{id}/activity`, `/api/v1/users/{id}/stats`, `/api/v1/users/{id}/projects`
Verify if `/api/v1/users/current` properly restricts data when accessed by different authenticated users
Check if numeric user IDs are predictable and if sequential ID enumeration is possible
Test variation in parameter formats: `/api/v1/users/username`, `/api/v1/users/email@domain.com`, `/api/v1/users/uuid`
Look for similar IDOR patterns in related endpoints: `/api/v1/profile`, `/api/v1/accounts`, `/api/v1/members`

## MITRE ATT&CK
- T1190
- T1526
- T1557
- T1087
- T1589

## Notes
The vulnerability report demonstrates a common authentication/authorization bypass pattern where endpoint-level access controls are missing. The attacker successfully obtained sensitive PII including full name, location (city/country/timezone), email confirmation status, social media usernames (GitHub, LinkedIn, Twitter), website, and photo URL. The report lacks specific impact on 'order information' as mentioned in the title - the PoC focuses on user profile enumeration. Response includes strong CSP and security headers but lacks effective backend authorization controls. This is a classic IDOR requiring minimal exploitation effort with significant privacy impact.

## Full report
<details><summary>Expand</summary>

Hi team,
I found one bug on your domain. It's IDOR bug.

##Summary:
Insecure Direct Object Reference ( IDOR ) is the method of controlling which users can perform a certain type of action or view set of data. Insecure Direct Object Reference ( IDOR ) is a vulnerability that allows an attacker to circumvent those controls and perform more actions than they are allowed to, or view content they typically don’t have access to. Such vulnerability, when exploited, could lead to massive loss of data.



##Steps To Reproduce:

1. Go to `https://wakatime.com/api/v1/users/current?`
2. Intercept your request. The request should look like this:
```
GET /api/v1/users/current? HTTP/2
Host: wakatime.com
Cookie: █████
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=1
Te: trailers
```
3. Send request in repeater tab ( i will show that request in my PoC video)
4. Now cut the `current?` at the end of `/api/v1/users/current?` and enter the user ID or username of the  victim 
`exmaple: GET /api/v1/users/@hasn0xxxx`
5. You will get victims some information like this 
```
HTTP/2 200 OK
Server: nginx
Date: Wed, 29 May 2024 08:26:00 GMT
Content-Type: application/json
Content-Length: 1337
Vary: Cookie
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Xss-Protection: 1; mode=block
Feature-Policy: accelerometer 'none';autoplay 'self';camera 'none';document-domain 'none';fullscreen 'self';geolocation 'none';gyroscope 'none';magnetometer 'none';microphone 'none';midi 'none';payment 'self';picture-in-picture 'none';sync-xhr 'self';usb 'none';
Referrer-Policy: strict-origin-when-cross-origin
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self'; frame-ancestors 'self'; script-src 'self' 'unsafe-eval' https://js.stripe.com https://*.braintreegateway.com https://client.crisp.chat/ https://api.github.com https://www.google.com/ https://www.gstatic.com/ https://www.googletagmanager.com https://www.google-analytics.com https://heapanalytics.com https://*.heapanalytics.com; img-src 'self' data: https://cdn.loom.com/ https://checkout.paypal.com https://*.braintreegateway.com https://*.crisp.chat/ heapanalytics.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com/ https://fonts.gstatic.com/ https://client.crisp.chat/; font-src 'self' https://fonts.googleapis.com/ https://fonts.gstatic.com/ https://client.crisp.chat/; media-src 'self' https://*.amazonaws.com; frame-src 'self' https://www.google.com/ https://js.stripe.com/ https://hooks.stripe.com/ https://client.crisp.chat/ https://www.youtube.com/ https://www.loom.com/ player.vimeo.com checkout.paypal.com; object-src 'self'; connect-src 'self' api.github.com https://www.google.com/ www.google-analytics.com heapanalytics.com https://avatar-cdn.atlassian.com wss://*.crisp.chat/ https://*.crisp.chat/ https://api.stripe.com;

{
  "data": {
    "bio": "hiiiiiii",
    "city": {
      "ascii_name": "Dhaka",
      "ascii_state": "Dhaka Division",
      "country": "Bangladesh",
      "country_code": "BD",
      "id": "fc1d7f6d-0da8-43b3-b124-96d401e07c7e",
      "name": "Dhaka",
      "population": 10356500,
      "state": "Dhaka Division",
      "timezone": "Asia/Dhaka",
      "title": "Dhaka, Bangladesh"
    },
    "created_at": "2024-05-29T07:11:57Z",
    "display_name": "habibbhai",
    "full_name": "habibbhai",
    "github_username": "blablabla",
    "human_readable_website": "http://blablabla.com",
    "id": "d42f6787-f856-4c55-9ff3-cd8549f9efe0",
    "is_email_confirmed": false,
    "is_email_public": false,
    "is_hireable": false,
    "languages_used_public": false,
    "linkedin_username": "testlinkedin",
    "logged_time_public": false,
    "photo": "https://wakatime.com/photo/d42f6787-f856-4c55-9ff3-cd8549f9efe0",
    "photo_public": true,
    "profile_url": "https://wakatime.com/@hasn0xxxx",
    "profile_url_escaped": "https://wakatime.com/@hasn0xxxx",
    "public_email": null,
    "public_profile_time_range": null,
    "share_all_time_badge": false,
    "share_last_year_days": false,
    "twitter_username": "testetstets",
    "username": "hasn0xxxx",
    "website": "http://blablabla.com",
    "wonderfuldev_username": null
  }
}
```

** note : i used my account username*

## PoC : ████

## Impact

An IDOR (Insecure Direct Object Reference) vulnerability can have serious consequences if it allows attackers to view order information and personal data of users. Here's a breakdown of the potential impacts:

* **Unauthorized Data Exposure:**  This is the most concerning impact. Attackers can exploit IDOR to gain access to a wide range of sensitive information, including names, addresses, phone numbers, email addresses, order history, and even financial details like credit card numbers. This data can be used for identity theft, fraud, or even stalking.

* **Loss of Trust and Reputation:**  If a data breach occurs due to IDOR, it can severely damage the organization's reputation. Customers may lose trust in the company's ability to protect their data, leading to a loss of business and potential legal repercussions.

* **Financial Loss:**  Data breaches can be very expensive for organizations. They may face fines from regulatory bodies, lawsuits from affected users, and the cost of investigating and fixing the vulnerability.

Here are some additional points to consider:

* IDOR vulnerabilities can be exploited relatively easily, often by simply manipulating a URL or form parameter.

*  The impact of an IDOR attack can be amplified depending on the type of data exposed. Leaked order information can be used for targeted attacks, while financial data can lead to significant financial losses for victims.

*  IDOR vulnerabilities are not always limited to viewing data. In some cases, attackers might be able to manipulate or even delete data, causing further disruption and damage.
 
By understanding the potential impacts of IDOR, organizations can take steps to mitigate these risks by implementing proper authorization controls and validating user permissions before granting access to sensitive data.

</details>

---
*Analysed by Claude on 2026-05-11*
