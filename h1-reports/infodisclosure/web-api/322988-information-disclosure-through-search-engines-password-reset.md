# Information Disclosure Through Search Engine Indexing of Password Reset Tokens

## Metadata
- **Source:** HackerOne
- **Report:** 322988 | https://hackerone.com/reports/322988
- **Submitted:** 2018-03-06
- **Reporter:** luciann
- **Program:** Breadcrumb
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Information Disclosure, Improper Access Control, Search Engine Indexing, Sensitive Data Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
Password reset tokens on hq.breadcrumb.com were being indexed by search engines like Google, allowing attackers to discover and use valid reset tokens to compromise user accounts. An attacker could search for site-specific content and obtain unused password reset tokens, enabling unauthorized account takeover without user interaction.

## Attack scenario
1. Attacker performs Google search using site-specific query (site:hq.breadcrumb.com) to enumerate publicly indexed pages
2. Search results return pages containing password reset tokens in URLs or cached content
3. Attacker identifies valid password reset tokens from search engine cache or indexed pages
4. Attacker accesses the password reset endpoint with the discovered token
5. Attacker successfully resets target user's password without authorization
6. Attacker gains full account access and can perform any action as the compromised user

## Root cause
The application failed to implement proper robots.txt directives and/or meta tags to prevent search engine indexing of sensitive authentication endpoints containing password reset tokens. Password reset controller was accessible to search engine crawlers without authentication checks.

## Attacker mindset
An attacker would recognize that password reset functionality is often overlooked in security configurations. By leveraging public search engines, they can passively discover valid tokens without active scanning, making this a low-effort, high-impact attack vector for account takeover at scale.

## Defensive takeaways
- Implement robots.txt to explicitly disallow crawling of password reset and sensitive authentication endpoints
- Add X-Robots-Tag HTTP headers to password reset pages to prevent indexing across all search engines
- Implement noindex meta tags on all sensitive authentication pages
- Ensure password reset tokens have short expiration windows (e.g., 15-30 minutes)
- Require CSRF tokens on password reset endpoints
- Log and monitor password reset token generation and usage
- Implement rate limiting on password reset endpoints
- Consider requiring email verification before allowing token-based reset
- Use one-time use tokens that invalidate after first use
- Regularly audit robots.txt, sitemap.xml, and search engine indexing via Google Search Console

## Variant hunting
Search for other password reset endpoints on subdomains or different paths (e.g., /auth/reset, /account/password-reset)
Check for similar indexing issues on other sensitive endpoints: email verification tokens, 2FA setup links, account confirmation pages
Search for cached versions of reset pages in archive.org or other web caches
Look for password reset tokens in search engine caches even after robots.txt is implemented
Test other search engines (Bing, Yahoo, Baidu) for indexed sensitive content
Investigate if password reset tokens appear in error messages, logs, or referer headers that might be indexed

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1589
- T1592
- T1538

## Notes
This is a configuration oversight rather than a code vulnerability, making it particularly common in real-world applications. The attack requires no technical sophistication—just knowledge that search engines index publicly accessible content. This demonstrates the importance of security-aware infrastructure configuration and the principle of defense in depth for authentication mechanisms. Password reset tokens should never be treated as secret if they appear in URLs.

## Full report
<details><summary>Expand</summary>

Search on google for: 
site:"hq.breadcrumb.com"

Or access this link:
https://www.google.com/search?q=site%3A%22hq.breadcrumb.com%22&oq=site%3A%22hq.breadcrumb.com%22&aqs=chrome..69i57j69i58.6216j0j7&sourceid=chrome&ie=UTF-8

Note that this vulnerability can be obtain on other search engines.

## Impact

An attacker can obtain an unused password reset token found using google.com in order to get access to an user account. 

In order to better ensure the security of the application do not allow google indexing of the token/password reset controller.

</details>

---
*Analysed by Claude on 2026-05-24*
