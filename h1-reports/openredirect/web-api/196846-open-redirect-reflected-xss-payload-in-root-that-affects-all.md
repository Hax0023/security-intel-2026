# Open Redirect and Reflected XSS via Tag Stripping Bypass in Root Path and GET Parameters

## Metadata
- **Source:** HackerOne
- **Report:** 196846 | https://hackerone.com/reports/196846
- **Submitted:** 2017-01-09
- **Reporter:** inhibitor181
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected XSS, Open Redirect, Input Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A tag stripping filter on Starbucks and Teavana domains can be bypassed using the `<>` sequence followed by arbitrary JavaScript or URLs, allowing reflected XSS and open redirects via the root path or multiple GET parameters. The vulnerability affects store.starbucks.*, shop.starbucks.*, and teavana.com domains, with main starbucks.* domains appearing unaffected.

## Attack scenario
1. Attacker crafts a malicious URL containing `<>javascript:alert(document.cookie);` in the root path or GET parameter
2. Victim clicks the link or is redirected to the malicious URL
3. Starbucks/Teavana server receives the request and attempts to sanitize HTML tags
4. The sanitization logic strips `<>` but fails to properly validate the remaining payload structure
5. JavaScript payload executes in the victim's browser within the context of the Starbucks domain
6. Attacker steals session cookies, credentials, or performs actions on behalf of the user

## Root cause
Insufficient input validation and improper HTML sanitization logic. The application strips angle brackets but does not comprehensively validate or encode potentially dangerous content. The chained redirect mechanism combined with weak tag stripping creates an exploitable condition where `<>` acts as a bypass sequence.

## Attacker mindset
An attacker would recognize that simple tag stripping is insufficient for XSS prevention and systematically test bypass sequences. The discovery of `<>` as a valid bypass suggests fuzzing common delimiter combinations. The attacker would then map vulnerable injection points across multiple subdomains and parameters to maximize exploit surface.

## Defensive takeaways
- Implement proper HTML entity encoding for all user-supplied input before rendering in HTML context
- Use a robust, well-maintained HTML sanitization library (e.g., DOMPurify, OWASP Sanitizer) rather than custom tag stripping
- Apply Content Security Policy (CSP) headers with strict directives to mitigate XSS impact
- Validate and whitelist redirect URLs against a safe list of domains; reject any redirects to untrusted hosts
- Perform comprehensive input validation on all parameters, not just visible query parameters (include root paths)
- Use output encoding appropriate to the context (HTML, JavaScript, URL, CSS)
- Implement security testing (SAST/DAST) in CI/CD pipeline to catch bypass techniques

## Variant hunting
Test other tag delimiter combinations: `</>`, `<!>`, `<;>`, `<|>` to find additional bypasses
Check if other special sequences bypass the filter: `%3C%3E`, `\u003C\u003E`, double-encoded variants
Attempt event handler injection: `<>onload=alert(1)`, `<>onerror=alert(1)`
Test in different contexts: inline attributes, form actions, meta redirects, script src parameters
Check for similar bypass patterns in other Starbucks properties and partnered domains
Examine if the filter can be bypassed with case variations or encoding combinations
Test polyglot payloads that work across multiple injection contexts

## MITRE ATT&CK
- T1190
- T1566.002
- T1203
- T1059.007

## Notes
The report demonstrates a critical infrastructure-wide issue affecting multiple prominent Starbucks domains. The use of `<>` as a bypass sequence is elegant and suggests the developers were attempting basic tag stripping without understanding XSS fundamentals. The open redirect variant (`<>//domain.com`) shows the payload can be used for phishing attacks as well. The fact that the vulnerability exists 'in almost any GET parameter' and 'in the root URL' indicates a centralized vulnerability in a shared library or framework rather than isolated instances.

## Full report
<details><summary>Expand</summary>

Hello, during some open redirects testing, I have noticed a very strange redirect that occured when I had modified a parameter using something like `>cofee`. I have digged up further and then I have noticed that one can make a redirect by modifying GET parameters with this structure : `<>//google.com`

There seems to be a stripping of tags and after that some chained redirect, that will eventually trigger an XSS vulnerability if the payload is like : `<>javascript:alert(document.cookie);`.

__So, based on this I have noticed that all your websites except the starbucks.* are vulnerable to an XSS payload that is written directly in the root URL or almost ANY other get parameter__, thus making almost all the websites exploitable with multiple injection points (starbucks.* seems not affected)

POC EXAMPLES
-------
```
https://shop.starbucks.de/<>javascript:alert(document.cookie);
https://teavana.com/<>javascript:alert(document.cookie);
https://store.starbucks.com/<>javascript:alert(document.cookie);
https://shop.starbucks.de/coffee/coffee,de_DE,sc.html?prefn1=decaffeinated&prefv1=<>javascript:alert('xss parameter');
https://shop.starbucks.de/coffee/coffee,de_DE,sc.html?prefn1=<>javascript:alert('xss parameter');
```

Bonus - open redirect example :
```
https://shop.starbucks.de/coffee/coffee,de_DE,sc.html?prefn1=decaffeinated&prefv1=<>//google.com
https://teavana.com/<>//google.com
```

</details>

---
*Analysed by Claude on 2026-05-24*
