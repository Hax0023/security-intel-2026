# Stored XSS in blog comments through Shopify API

## Metadata
- **Source:** HackerOne
- **Report:** 192210 | https://hackerone.com/reports/192210
- **Submitted:** 2016-12-18
- **Reporter:** prakharprasad
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there!

As far I understand the Shopify Shop have blogs which allow users to comment on blog posts, however the comments with HTML content automatically gets sanitised and then posted to avoid XSS issue. However using the API for comment modification, any application with comment permission can modify a comment and include arbitrary HTML leading to XSS. 

**Steps to Reproduce** 

1.  Open the S

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

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
*Analysed by Claude on 2026-05-24*
