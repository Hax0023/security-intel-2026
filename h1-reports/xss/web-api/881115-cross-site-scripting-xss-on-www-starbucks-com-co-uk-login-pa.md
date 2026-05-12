# Cross-Site Scripting (XSS) on Starbucks Login Pages via URL Path Injection

## Metadata
- **Source:** HackerOne
- **Report:** 881115 | https://hackerone.com/reports/881115
- **Submitted:** 2020-05-23
- **Reporter:** cdl
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on Starbucks login pages (starbucks.com and starbucks.co.uk) where the application fails to properly escape user-controlled URL path segments when constructing HTML links. An attacker can inject malicious JavaScript via crafted URLs to execute arbitrary code in the victim's browser context, enabling credential theft on the authentication page.

## Attack scenario
1. Attacker crafts a malicious URL containing encoded XSS payload in the URL path segment (e.g., using double encoding and event handlers like onmouseover)
2. Attacker tricks victim into visiting the crafted URL via social engineering, phishing emails, or advertisement redirects
3. Victim navigates to the login page at the malicious URL
4. Application constructs HTML links using the unescaped URL path, breaking out of attribute context and injecting malicious event handlers
5. When victim hovers over interactive elements (e.g., 'Find the Store' button), the injected JavaScript executes in the victim's browser
6. Attacker's script extracts login credentials from form fields or redirects victim to credential harvesting page

## Root cause
The application builds HTML links using relative URL paths without proper HTML entity encoding or escaping. The path parameter is directly interpolated into HTML attributes and tag context, allowing attackers to break out of intended syntax and inject arbitrary JavaScript event handlers via URL-encoded payloads.

## Attacker mindset
An attacker would target this vulnerability to perform large-scale credential harvesting on a high-value target (Starbucks) by crafting phishing campaigns that direct users to the XSS payload URLs. The attack is particularly effective on login pages where users are primed to enter sensitive information. The relative ease of exploitation and high impact (password theft) makes this an attractive target.

## Defensive takeaways
- Always HTML-encode/escape user-controlled input when outputting to HTML context, regardless of whether it appears to be from a 'safe' source like URL paths
- Use context-aware output encoding: HTML entity encoding for HTML content, JavaScript encoding for JavaScript context, URL encoding for URL context
- Implement Content Security Policy (CSP) headers to mitigate XSS impact by restricting inline script execution and external script sources
- Use templating engines with auto-escaping enabled by default
- Apply whitelist validation for URL paths and reject unexpected characters
- Conduct security code reviews focused on output encoding in authentication-related pages
- Implement automated security testing (SAST/DAST) in CI/CD pipeline to detect XSS vulnerabilities early

## Variant hunting
Hunt for similar patterns in: (1) Other Starbucks regional domains with login functionality, (2) Other Starbucks pages that construct URLs from path parameters, (3) Similar authentication flows in other beverage/retail companies, (4) Admin or account management pages that might use unescaped URL parameters, (5) Redirect mechanisms that accept URL path parameters without validation, (6) Error pages or 404 handlers that reflect path information

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The vulnerability demonstrates the severity of improper output encoding on authentication pages. The use of double URL encoding in the payload (e.g., %252f for /) suggests the application may have attempted single-layer encoding that was bypassed. The fact that this affects multiple regional domains indicates a systemic issue in how the application was developed rather than an isolated misconfiguration. The researcher appropriately demonstrated both information disclosure (document.domain) and credential theft vectors, showing the full attack capability.

## Full report
<details><summary>Expand</summary>

Hi team,

**Summary:** 
There is a cross-site scripting vulnerability on the login page of  www.starbucks.com and various regions, due to improper escaping on the URL path.

**Description:**
The login page at https://www.starbucks.com/account/signin builds several links by the relative URL path. An attacker can actually control the relative path: 

{F839656}

Furthermore, the application does not escape certain characters –  allowing us to break out of the tags and inject a malicious event handler.

**Platform(s) Affected:** 
- https://www.starbucks.com/account/signin
- https://www.starbucks.co.uk/account/signin

## Steps To Reproduce:

  1. Open Chrome or Firefox
  2. Visit `https://www.starbucks.com/account/(A(%22%20%252fonmouseover=%22alert%25%32%38%64%6f%63%75%6d%65%6e%74.%64%6f%6d%61%69%6e%25%32%39%22))/signin` and in the upper right-hand corner, move your mouse over the "Find the Store" button.

The XSS will trigger and you'll get an `alert()` with the value of `document.domain`

{F839657}


## Exploitation: 
Since this is on the **login page**, it is absolutely trivial to steal user credentials.

Here's a simple proof-of-concept, this will just alert() your password back to you:

- `https://www.starbucks.com/account/(F(%22%20%252fonmouseover=%22%2561%256c%2565%2572%2574%2528%2564%256f%2563%2575%256d%2565%256e%2574%252e%2567%2565%2574%2545%256c%2565%256d%2565%256e%2574%2573%2542%2579%254e%2561%256d%2565%2528%2527%2541%2563%2563%256f%2575%256e%2574%252e%2550%2561%2573%2573%2557%256f%2572%2564%2527%2529%255b%2530%255d%252e%2576%2561%256c%2575%2565%2529%22))/signin`

{F839660}


## How can the system be exploited with this bug?
  An attacker can easily abuse this bug to steal user passwords, inject malicious javascript into the context of `www.starbucks.com`, etc.

## Suggested Mitigation
Implement HTML encoding / escaping on the path.

## Impact

This is a high impact vulnerability as this affects the login page.

Best,
@cdl

</details>

---
*Analysed by Claude on 2026-05-12*
