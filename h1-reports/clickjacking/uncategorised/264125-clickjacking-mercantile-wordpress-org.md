# Clickjacking on mercantile.wordpress.org - Multiple Endpoints Missing X-Frame-Options

## Metadata
- **Source:** HackerOne
- **Report:** 264125 | https://hackerone.com/reports/264125
- **Submitted:** 2017-08-28
- **Reporter:** villagelad
- **Program:** WordPress
- **Bounty:** Not specified - reporter queried whether it qualifies for bounty
- **Severity:** Medium
- **Vuln:** Clickjacking, UI Redressing, Missing Security Headers
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple endpoints on mercantile.wordpress.org lack X-Frame-Options HTTP headers, making them vulnerable to clickjacking attacks. This is a regression or incomplete fix of a previously reported vulnerability (Report #264124 by giantfire) that was claimed fixed on Aug 25 but remained unresolved on multiple URLs.

## Attack scenario
1. Attacker creates a malicious website with an invisible iframe pointing to mercantile.wordpress.org product pages
2. Attacker overlays transparent buttons on top of the iframe positioned to align with legitimate actions (e.g., 'Buy Now', 'Add to Cart')
3. Victim visits attacker's website believing they are viewing legitimate content or clickbait
4. Victim clicks what they believe is a benign button on the attacker's page
5. The click actually targets the invisible iframe, causing unintended action on mercantile.wordpress.org within victim's authenticated session
6. Attacker redirects victim to phishing page or completes unauthorized transactions using victim's credentials

## Root cause
X-Frame-Options header was not consistently applied across all endpoints on mercantile.wordpress.org. The fix implemented (SAMEORIGIN) may have been applied only to certain pages or not deployed to all affected URLs, suggesting incomplete remediation of the earlier report.

## Attacker mindset
Opportunistic attacker seeking to abuse e-commerce functionality through social engineering. The attacker discovered a regression/incomplete patch and leveraged it to maximize impact across multiple product pages. Young researcher (age 17) appears motivated by responsible disclosure rather than malice.

## Defensive takeaways
- Implement X-Frame-Options: DENY or SAMEORIGIN at the web server/framework level to ensure consistent application across all endpoints
- Use Content Security Policy (CSP) frame-ancestors directive as a modern replacement/supplement to X-Frame-Options
- Conduct regression testing and full-site scanning after security patches to verify fixes are deployed to all affected URLs
- Implement automated security header validation in CI/CD pipeline to detect missing headers before deployment
- For e-commerce sites, consider additional protections like frame-busting JavaScript and SameSite cookie attributes
- Maintain a comprehensive inventory of all endpoints and ensure security controls are applied uniformly

## Variant hunting
Scan all WordPress multisite installations for missing X-Frame-Options headers across subdomains
Check admin panels and checkout flows specifically, as these are high-value clickjacking targets
Test CORS policies in combination with frame options for bypasses
Look for inconsistency between different content types (HTML, JSON endpoints, API responses)
Examine dynamically-generated pages that may bypass centralized header configuration
Check for X-Frame-Options bypasses via alternative framing methods (embed, object, iframe with srcdoc)

## MITRE ATT&CK
- T1185 - Man in the Browser (UI redressing aspect)
- T1566.002 - Phishing: Spearphishing Link (combined with clickjacking)
- T1204.001 - User Execution: Malicious Link (social engineering via clicks)

## Notes
This report demonstrates a critical gap in patch verification processes. The original vulnerability (reported Aug 9, allegedly fixed Aug 25) was not fully remediated, indicating either incomplete deployment or that the fix was reverted/bypassed. The reporter's identification of multiple affected URLs suggests a systemic issue rather than isolated oversight. The 17-year-old researcher followed responsible disclosure practices and provided comprehensive documentation. The reference to MSDN documentation on X-Frame-Options is outdated; OWASP and MDN should be primary references. Modern approach would emphasize CSP frame-ancestors over X-Frame-Options alone.

## Full report
<details><summary>Expand</summary>

A Clickjaking Issue had been previously reported by  "giantfire" on Aug 9th (19 days ago) and the issue was fixed by "iandunn" on Aug 25th (3 days ago) and the same disclosed on Aug 28th. Here the affected URL is- https://mercantile.wordpress.org/

"iandunn closed the report and changed the status to Resolved.
Aug 25th (3 days ago)

The site is sending X-Frame-Options: SAMEORIGIN for front end requests now. Thanks for the report. I'll request disclosure and chat with the team to see if this qualifies for a bounty."


But the issue is still live. So here's my report. I found some others endpoints as well which can be Clickjacked easily.

Hello Team,
I am Mohammed Israil,17 found some security issue which are not very critical but can affect the system/service in future. So without delaying. I am reporting this issue hope you'll understand and implement some fix as soon as possible.

Vulnerability Type: Clickjacking (user-interface or UI redressing and IFRAME overlay) 

Affected URLs:
https://mercantile.wordpress.org/
https://mercantile.wordpress.org/#
https://mercantile.wordpress.org/product-category/accessories/
https://mercantile.wordpress.org/faq/
https://mercantile.wordpress.org/product-category/apparel/?subcat=women
https://mercantile.wordpress.org/product-category/apparel/?subcat=youth
https://mercantile.wordpress.org/product-category/apparel/?subcat=unisex


Description: Clickjacking, also known as a "UI redress attack", is when an attacker uses multiple transparent or opaque layers to trick a user into clicking on a button or link on another page when they were intending to click on the the top level page. Thus, the attacker is "hijacking" clicks meant for their page and routing them to another page, most likely owned by another application, domain, or both. 

Reason: X-Frame-Options header is not included in the HTTP response to protect against 'ClickJacking' attacks.

Evidence: I attached a screenshot as well, Please check that.

Solution: There are two main ways to prevent clickjacking:

    Sending the proper X-Frame-Options HTTP response headers that instruct the browser to not allow framing from other domains
    Employing defensive code in the UI to ensure that the current frame is the most top level window

Most modern Web browsers support the X-Frame-Options HTTP header. Ensure it's set on all web pages returned by your site (if you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. ALLOW-FROM allows specific websites to frame the web page in supported web browsers).

Reference: http://blogs.msdn.com/b/ieinternals/archive/2010/03/30/combating-clickjacking-with-x-frame-options.aspx



Thank You




</details>

---
*Analysed by Claude on 2026-05-24*
