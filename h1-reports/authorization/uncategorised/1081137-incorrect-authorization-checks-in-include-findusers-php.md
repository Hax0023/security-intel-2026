# Incorrect Authorization Checks in /include/findusers.php - Unauthenticated Access via Token Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1081137 | https://hackerone.com/reports/1081137
- **Submitted:** 2021-01-19
- **Reporter:** egix
- **Program:** ImpressCMS
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Broken Authentication, Broken Access Control, Authorization Bypass, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The findusers.php script contains a logic flaw in its authorization check that allows unauthenticated users to bypass authentication by providing a valid CSRF token. Tokens are generated in multiple locations including unauthenticated pages like misc.php, enabling attackers to access user enumeration functionality and disclose usernames and real names without proper authentication.

## Attack scenario
1. Attacker navigates to /misc.php?action=showpopups&type=friend without authentication
2. Attacker extracts a valid security token from the XOOPS_TOKEN_REQUEST HTML parameter in the page source
3. Attacker crafts a request to /include/findusers.php?token=[VALID_TOKEN] with the extracted token
4. Authorization check at line 20-23 validates the token and sets $denied = false, bypassing the admin-only restriction
5. Attacker gains access to the user search functionality despite not being authenticated or an admin
6. Attacker enumerates registered users and extracts usernames and real names for information gathering

## Root cause
The authorization logic uses OR conditions that are mutually exclusive in intent but not in implementation. The token validation check (lines 20-23) was intended only for CSRF protection within authenticated sessions, but accepts ANY valid token regardless of user authentication status. Since tokens are generated on unauthenticated pages, this creates a bypass. The admin check (line 24) is unreachable if a valid token is provided, breaking the intended admin-only access control.

## Attacker mindset
An attacker would recognize that security tokens are meant for session validation but notice they're generated even for unauthenticated users. By collecting a token from a public page and reusing it on a restricted endpoint, they exploit the assumption that token possession implies proper authorization. This is a classic case of confusing authentication with authorization—a valid token doesn't prove the user should access this function.

## Defensive takeaways
- Authorization checks should verify user authentication status FIRST before accepting tokens: check if user is logged in and is admin, THEN validate CSRF token as secondary protection
- Tokens should only be generated for authenticated users or in contexts where user identity is established
- Implement proper separation of concerns: CSRF tokens protect against request forgery but should NOT serve as primary authentication mechanism
- Use explicit whitelist approach: define who can access each function (admin roles) before validating tokens
- Code review authorization logic carefully—OR conditions in security checks are often problematic when they should be AND conditions
- Audit all token generation points to ensure they only occur in authenticated contexts or explicitly document and restrict their use

## Variant hunting
Search for other endpoints using similar pattern: token validation before role/permission checks
Look for other pages generating tokens in unauthenticated contexts (search codebase for getTokenHTML calls)
Check if validateToken() is used elsewhere as primary authorization mechanism rather than CSRF protection
Identify admin-only functions that accept token parameters and test with tokens from public pages
Review all includes of mainfile.php followed by token checks to find similar authorization bypasses
Test if tokens from one context can be reused in different contexts (token portability issue)

## MITRE ATT&CK
- T1190
- T1078
- T1557
- T1592

## Notes
This vulnerability demonstrates the critical difference between authentication and authorization. While CSRF tokens are valid security mechanisms, they authenticate the request's origin, not the user's permission level. The vulnerability allows information disclosure (user enumeration) which could support further attacks. The fix should implement a logical AND condition: if (is_object(icms::$user) && icms::$user->isAdmin() && validateToken()) rather than the current OR-like structure. ImpressCMS 1.4.2 confirmed vulnerable.

## Full report
<details><summary>Expand</summary>

## Summary:
The vulnerability is located in the `/include/findusers.php` script:

```
16.	include "../mainfile.php";
17.	xoops_header(false);
18.	
19.	$denied = true;
20.	if (!empty($_REQUEST['token'])) {
21.		if (icms::$security->validateToken($_REQUEST['token'], false)) {
22.			$denied = false;
23.		}
24.	} elseif (is_object(icms::$user) && icms::$user->isAdmin()) {
25.		$denied = false;
26.	}
27.	if ($denied) {
28.		icms_core_Message::error(_NOPERM);
29.		exit();
30.	}
```

As far as I can see, I believe this script should be accessible by admin users only (due to line 24). However, because of the if statements at lines 20-23, this script could be accessed by unauthenticated attackers if they will provide a valid security token. Such a token will be generated in several places within the application (just search for the string `icms::$security->getTokenHTML()`), and some of them do not require the user to be authenticated, like in `misc.php` at [line 181](https://github.com/ImpressCMS/impresscms/blob/48af29c6b8150fbf4220bb5cc4f3c57bcd818384/misc.php#L181).



## ImpressCMS branch :
The vulnerability has been tested and confirmed on ImpressCMS version 1.4.2 (the latest at the time of writing).

## Steps To Reproduce:
  1. Try to access the `/include/findusers.php` script without being logged into the application
  1. You will see an error message saying **"Sorry, you don't have permission to access this area."**
  1. Go to `/misc.php?action=showpopups&type=friend` and look at the HTML source code, search the string `XOOPS_TOKEN_REQUEST` and copy the value of the token
  1. Go to `/include/findusers.php?token=[TOKEN_VALUE]` and you will be able to access the script and e.g. search through the registered users

## Impact

This vulnerability might allow unauthenticated attackers to access an otherwise restricted functionality of the application, which in turn might allow an information disclosure about the CMS users (specifically, only the username and real name will be disclosed).

</details>

---
*Analysed by Claude on 2026-05-24*
