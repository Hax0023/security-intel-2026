# Stored XSS on Starbucks Singapore Career Landing Pages

## Metadata
- **Source:** HackerOne
- **Report:** 507957 | https://hackerone.com/reports/507957
- **Submitted:** 2019-03-11
- **Reporter:** 13ern
- **Program:** Starbucks
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Arbitrary HTML/JavaScript Injection, Malicious Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
Career landing pages on starbucks.com.sg were vulnerable to stored XSS attacks, allowing malicious actors to inject JavaScript and HTML that redirected users to external phishing sites. The injected payload used CSS positioning techniques to overlay an invisible clickable link redirecting visitors to a WordPress site impersonating legitimate Starbucks job offers.

## Attack scenario
1. Attacker identifies unprotected or weakly validated input fields on Starbucks career landing pages
2. Attacker injects malicious HTML/JavaScript payload containing an invisible overlay link
3. Payload is stored in the application's database or reflected on page load
4. Job seeker visits the compromised career landing page expecting legitimate employment information
5. Invisible overlay link (positioned fixed, full-screen with transparent styling) captures user clicks
6. User is redirected to attacker-controlled phishing site or malware distribution point

## Root cause
Insufficient input validation and output encoding on career landing page parameters. The application failed to sanitize user-supplied input before storing and rendering it, allowing arbitrary HTML/JavaScript injection. Likely vulnerable parameter: career-landing-* query parameter lacked proper Content Security Policy (CSP) and HTML escaping.

## Attacker mindset
Opportunistic malicious actor leveraging automated scanning to identify vulnerable endpoints for credential harvesting via job offer phishing. The use of invisible overlay technique demonstrates sophistication in concealing malicious intent while maximizing click-through rates.

## Defensive takeaways
- Implement strict input validation and whitelist acceptable characters for all user inputs
- Apply context-appropriate output encoding (HTML entity encoding, JavaScript escaping) when rendering user-controlled data
- Deploy Content Security Policy (CSP) headers to restrict inline script execution and external resource loading
- Use template engines with automatic escaping enabled by default
- Implement Web Application Firewall (WAF) rules to detect and block common XSS payloads
- Regularly scan for and remove orphaned or unused pages that may not receive security updates
- Employ security headers: X-Content-Type-Options: nosniff, X-Frame-Options: DENY, X-XSS-Protection
- Implement DOM-based XSS protections and avoid using innerHTML with user data
- Conduct regular security code reviews and penetration testing of career/recruiting pages

## Variant hunting
Hunt for similar vulnerabilities in: (1) Other starbucks regional domains with career pages, (2) Query parameters with numeric identifiers (career-landing-1 through -999), (3) Other input fields on career pages (search, filters, application forms), (4) Comments or review sections that may accept user input, (5) PDF or resume upload functionality

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002

## Notes
The use of fixed positioning with z-index manipulation and CSS opacity tricks to hide malicious links is a known technique for bypassing basic security awareness. The attacker appears to have compromised the page through an unspecified injection vector, potentially via a vulnerable plugin, weak access controls, or third-party content inclusion. The presence of multiple numbered pages (career-landing-5, implying -1 through -4 or higher) suggests systematic enumeration and compromise.

## Full report
<details><summary>Expand</summary>

**Summary:** 
While enumeration of the webpage for Starbucks I observed the following pages.

https://www.starbucks.com.sg/careers/career-center/career-landing-5?

The webpage have been highly spam by automated scanners or malicious attack.
By clicking on any of the pages it would redirect the user to a wordpress website

```
<a href="https://obatkebaskesemutan.wordpress.com/" rel="dofollow noopener" style="z-index:9999999999999999;oncontextmenu:return false;onkeydown:return false;onmousedown:return false;position:fixed;top:0px !important;left:0px;width:100%;height:100%;color:transparent !important;display:block;text-align:center;font-size:0px;background-color:transparent;background-position:center;background-repeat:no-repeat;background-size:cover;" target="_blank" title="Obat Herbal">Obat Kebas</a>

```
The owner of the following wordpress pages could manipulate user into redirecting to a Starbucks page for a job offer and an user by clicking on the webpage would redirect to a website of its choosing.

{F439338}
{F439340}

* List any recommendations for bug fix
Remove the pages from Starbucks webpage.

## Impact

The owner of the following wordpress pages could manipulate user into redirecting to a Starbucks page for a job offer and an user by clicking on the webpage would redirect to a website of its choosing.

</details>

---
*Analysed by Claude on 2026-05-12*
