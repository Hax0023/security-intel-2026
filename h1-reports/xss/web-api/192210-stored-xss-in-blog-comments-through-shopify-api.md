# Stored XSS in Shopify Blog Comments via Undocumented API Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 192210 | https://hackerone.com/reports/192210
- **Submitted:** 2016-12-18
- **Reporter:** prakharprasad
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), API Input Validation Bypass, Mass Assignment/Parameter Pollution
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Shopify's blog comment system where the API accepts an undocumented 'body_html' parameter that bypasses HTML sanitization applied to the standard 'body' parameter. An authenticated application with comment permissions can inject arbitrary JavaScript that executes in the browser of blog visitors and Shopify admin users viewing comments.

## Attack scenario
1. Attacker creates or compromises a Shopify application with comment modification permissions
2. Attacker identifies a comment ID from an existing blog post (visible in HTML as comment-XXXX)
3. Attacker sends a PUT/POST request to /admin/comments/{id}.json with malicious JavaScript in the undocumented 'body_html' field
4. The API accepts and stores the HTML payload without sanitization, unlike the documented 'body' field
5. When legitimate users or administrators view the blog post or admin comment section, the injected JavaScript executes in their browser context
6. Attacker can steal session tokens, perform actions as victims, or deface content

## Root cause
The API endpoint implements inconsistent input validation across parameters. The documented 'body' parameter is sanitized server-side, but the undocumented 'body_html' parameter is accepted and stored as-is without sanitization. This suggests incomplete parameter whitelisting or failure to sanitize all potential input vectors in the comment update logic.

## Attacker mindset
An attacker with legitimate app credentials recognizes that APIs often accept undocumented parameters for backwards compatibility or development purposes. By fuzzing parameter names or reverse-engineering, they discover that 'body_html' bypasses protections that obviously exist for 'body'. The attack is subtle because it exploits a discrepancy between documented and actual API behavior.

## Defensive takeaways
- Implement consistent input sanitization across all parameters regardless of documentation status, not just documented fields
- Use a whitelist approach for API parameters; reject or ignore undocumented fields rather than silently accepting them
- Sanitize HTML content at storage time and display time (defense in depth)
- Audit all API endpoints for parameter handling inconsistencies, especially those related to user-generated content
- Implement Content Security Policy (CSP) headers to mitigate XSS impact even if sanitization fails
- Apply the same validation rules to API and web form submissions
- Regular security testing of APIs with fuzzing tools to discover unintended parameter acceptance

## Variant hunting
Search for other undocumented HTML-related parameters in comment or content API endpoints (_html, html_body, raw_html, unsafe_html)
Test other content types in Shopify (product descriptions, customer notes, articles) for similar parameter pollution
Check if other fields in comment endpoint have sanitization bypass variants
Test mass assignment vulnerabilities in other Shopify API resources that accept rich content
Look for similar patterns in webhook payloads or bulk API operations where validation might be less strict

## MITRE ATT&CK
- T1190
- T1566
- T1204

## Notes
This vulnerability demonstrates the danger of accepting undocumented parameters in APIs. The reporter helpfully noted that the payload executes in both the storefront and admin panel, indicating widespread impact. The attack requires authenticated API access, limiting exposure but making it dangerous for compromised or malicious apps. The two-request requirement suggests potential caching or session-related behavior. This is a classic example of parameter pollution in APIs where developers defend against known attack vectors but fail to sanitize all possible input channels.

## Full report
<details><summary>Expand</summary>

Hi there!

As far I understand the Shopify Shop have blogs which allow users to comment on blog posts, however the comments with HTML content automatically gets sanitised and then posted to avoid XSS issue. However using the API for comment modification, any application with comment permission can modify a comment and include arbitrary HTML leading to XSS. 

**Steps to Reproduce** 

1.  Open the Shopify Shop's blog and post a comment on a blogpost through a browser. 
2. Note the *comment id*, this can be easily grabbed by checking the HTML after the comment is posted: 
Eg. `<div id="comment-2929551246" class="comment border-bottom clearfix">`
3. Now setup an application with comment permission on the Shop 
4. Send the following JSON to the API endpoint /admin/comments/<comment-id>.json
`  {
  "comment": {
    "id": <comment-id>,
    "body": "blahblah",
    "body_html": "blah<img src=x onerror=alert(0);>"
  }
  }`
5. Send request twice.
6. Visit the blog post, JS in the comment should execute.

I believe this is a valid bug as the comment should get stripped of HTML, which is not the case in case of the above request, however it does gets stripped when posted via web or modified through the comment API documentation at https://help.shopify.com/api/reference/comment#update. To insert arbitrary HTML I've purposely added `body_html` in the request, which is not mentioned in the API reference, the allows me to add HTML, in the comment. The HTML even executes in the Shop's Admin Panel when viewing comments for a particular blog. 

PoC (see comment section for JS execution): https://derp-10.myshopify.com/blogs/news/43260355-first-post

Video: https://www.dropbox.com/s/7ie1tiex1eo4kk9/Comment%20XSS.mov?dl=0

Thanks,
Prakhar Prasad


</details>

---
*Analysed by Claude on 2026-05-12*
