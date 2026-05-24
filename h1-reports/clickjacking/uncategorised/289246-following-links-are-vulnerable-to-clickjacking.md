# Multiple Semrush URLs Vulnerable to Clickjacking via Missing X-Frame-Options Header

## Metadata
- **Source:** HackerOne
- **Report:** 289246 | https://hackerone.com/reports/289246
- **Submitted:** 2017-11-10
- **Reporter:** karma1
- **Program:** Semrush
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Clickjacking, Missing Security Headers, UI Redressing
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple endpoints on semrush.com lack X-Frame-Options security headers, allowing attackers to embed the pages in iframes for clickjacking attacks. An attacker can overlay transparent iframes over legitimate content to trick users into performing unintended actions. The vulnerability affects critical user-facing pages including the homepage, academy, pricing, and blog sections.

## Attack scenario
1. Attacker creates a malicious webpage containing an invisible iframe pointing to a sensitive Semrush page (e.g., /prices/ or /academy/)
2. Attacker overlays the iframe on top of legitimate-looking content with opacity set to 0 or positioned off-screen
3. User visits the attacker's malicious page believing they are accessing legitimate content
4. User clicks on what appears to be a benign element (button, link) on the attacker's page
5. The click actually registers on the hidden Semrush iframe, causing unintended actions such as account modifications, subscription changes, or information disclosure
6. Attacker achieves objectives like unauthorized account changes or credential harvesting through social engineering

## Root cause
Missing or improperly configured X-Frame-Options HTTP response header on multiple Semrush endpoints. The header should be set to 'DENY' or 'SAMEORIGIN' to prevent the pages from being embedded in iframes from different origins.

## Attacker mindset
The attacker is conducting reconnaissance to identify security weaknesses in the target application's clickjacking defenses. They recognize that missing X-Frame-Options headers represent a common implementation gap and demonstrate this vulnerability systematically across multiple endpoints to show widespread exposure.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN header on all HTTP responses, particularly for pages handling sensitive operations
- Additionally deploy Content-Security-Policy frame-ancestors directive as defense-in-depth measure
- Apply security headers consistently across all endpoints including static assets, API responses, and dynamic content
- Conduct security header audit across entire application to identify missing protections
- Implement automated checks in CI/CD pipeline to detect missing security headers before deployment
- Consider SameSite cookie attributes as complementary defense against session hijacking via clickjacking
- Document security header requirements in development guidelines and code review checklists

## Variant hunting
Check other subdomains of semrush.com for the same missing headers
Test other HTTP endpoints including API endpoints (/api/*, /v1/*, /v2/*)
Review administrative or account management pages which may not have proper frame protection
Check Content-Security-Policy implementation to see if frame-ancestors is properly configured
Test with different framing techniques (object tags, embed tags, SVG embeds) to bypass any partial protections
Identify pages handling sensitive operations (payment, account settings) that would be high-value targets

## MITRE ATT&CK
- T1204.001
- T1539
- T1566.002

## Notes
The report demonstrates basic understanding of clickjacking but could be improved with actual proof-of-concept demonstrating user interaction triggering an unintended action. The vulnerability is relatively straightforward to fix. The report format suggests this may be an early-stage HackerOne submission with template sections not fully completed. Impact would depend on what sensitive operations exist on these pages. The inclusion of multiple endpoints strengthens the report by showing widespread exposure rather than isolated issues.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to verify and then potentially issue a bounty, so be sure to take your time filling out the report!

**Summary:** [The below listed links, dont have X-FRAME-OPTIONS set to DENY or SAMEORIGIN and they are vulnerable to clickjacking]

**Description:** [The following url can be easily vulnerable to clickjacking]

**Browsers Verified In:**
  * [Firefox V56]
  

**Steps To Reproduce:** [add details for how we can reproduce the issue]
  1. [Run below code from browser and you will see listed links are vulnerable to clickjacking attack]
  2. [<!DOCTYPE html>
<html>

<frameset cols="25%,*,25%">
  <frame src="https://www.semrush.com/?l=us">
  <frame src="https://www.semrush.com/academy/">
  <frame src="https://www.semrush.com/ranking-factors/">
</frameset>

</html>]

**Following links are vulnerable to clickjacking**

+ https://www.semrush.com/semrush-opensearch.xml
+ https://www.semrush.com/academy/
+ https://www.semrush.com/ranking-factors/
+ https://www.semrush.com/manifest.json
+ https://www.semrush.com/?l=us
+ https://www.semrush.com/blog/
+ https://www.semrush.com/ 
+ https://www.semrush.com/prices/
+ https://www.semrush.com/.
+ https://www.semrush.com/.?l=us
  

**Supporting Material/References:**
  * Screenshot is attached with ticket


</details>

---
*Analysed by Claude on 2026-05-24*
