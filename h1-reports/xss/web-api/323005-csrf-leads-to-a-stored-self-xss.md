# CSRF-enabled Stored XSS via Favorites Folder Name Injection

## Metadata
- **Source:** HackerOne
- **Report:** 323005 | https://hackerone.com/reports/323005
- **Submitted:** 2018-03-06
- **Reporter:** hogarth45
- **Program:** Imgur
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Request Forgery (CSRF), Stored Cross-Site Scripting (XSS), Improper Input Validation, Missing CSRF Tokens
- **CVEs:** None
- **Category:** web-api

## Summary
A CSRF vulnerability combined with a stored XSS flaw allows attackers to create malicious favorites folders with XSS payloads in folder names. When a victim saves an image to the compromised folder, the XSS payload executes in their browser, potentially leading to account hijacking.

## Attack scenario
1. Attacker crafts an HTML page containing a CSRF form that POSTs to /3/folders API endpoint with XSS payload in folder name
2. Attacker distributes malicious link via Reddit/Imgur communities or other channels
3. Victim visits attacker-controlled page while logged into Imgur
4. CSRF form auto-submits, creating a folder with XSS payload name in victim's account
5. Victim later adds an image to the compromised folder via UI interaction
6. Stored XSS payload executes in victim's browser context, enabling session hijacking or credential theft

## Root cause
The application lacks CSRF token validation on the folder creation endpoint and fails to properly sanitize/escape folder names when rendering them in the DOM, allowing HTML/JavaScript injection

## Attacker mindset
Attacker recognized that while self-XSS and CSRF are individually out of scope, their combination creates a genuine security vulnerability. By automating the XSS injection via CSRF and distributing through high-traffic communities, they can achieve scale and bypass the need for user interaction to inject the payload.

## Defensive takeaways
- Implement CSRF token validation on all state-changing endpoints (POST, PUT, DELETE)
- Use double-submit cookie pattern or synchronizer token pattern for CSRF protection
- Properly escape all user-supplied data when rendering to HTML context
- Implement Content Security Policy (CSP) to mitigate XSS impact
- Validate and sanitize input on both client and server side
- Consider SameSite cookie attribute to prevent cross-site request interception
- Treat combinations of individually low-severity issues as potential high-severity chains

## Variant hunting
Other folder/collection creation endpoints that may lack CSRF tokens
Similar self-XSS issues in other user-controlled naming fields (albums, tags, descriptions)
CSRF vulnerabilities in other state-changing API endpoints
DOM-based XSS in folder management UI when rendering folder names
Stored XSS in user profile descriptions or settings
Other endpoints accepting JSON payloads without proper token validation

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001
- T1539

## Notes
Report acknowledges that individual vulnerabilities (self-XSS and CSRF) are out of scope per policy, but demonstrates that their combination creates a practical attack chain worthy of bounty consideration. The distributed nature via community platforms significantly increases real-world impact. Requires victim interaction (adding image to folder) after CSRF, reducing but not eliminating attack success rate.

## Full report
<details><summary>Expand</summary>

Followup from #311460

#Summary
Self xss and CSRF are both out of scope, but when paired it is possible to create an attack on a user.

#Description
A favorites folder with an xss payload for a name will launch when saving an image to said folder.

This can be verified by following these steps
* Visit your favorites
* Create New Folder
* Change name to
```
"'><img src=x onerror=prompt(1)>
```
* Save
* Visit a photo
* Click the little plus next to the heart on bottom left of image
* Add to the folder
* xss will launch

Since self xss is out of scope, we will need a method of delivering this attack to a user.
This can be done via a CSRF to create a favorites folder.

# POC

Using a form like so to create the CSRF:
```
<html>
<body onload='document.forms[0].submit()'>
  <form method='POST' enctype='application/json' action='https://api.imgur.com/3/folders'>
    <input name='name' value='New Test"><img src=x onerror=prompt(2)>'>
    <input name='is_private' value='false'>
  </form>
</body>
</html>
```

Or be logged into your imgur account and visit

http://blackdoorsec.net/sandbox/imgur2.html

This will create the folder with an xss name that can be used to attack an account.

## Impact

account hijacking
since a user would still need to add an image to the folder for the attack to work, the success rate will be lower than normal

#Scenerio
since reddit/imgur communities overlap malicious links containing the CSRF could be sent throughout the site. out of the few thousand hits the link would get, i imagine there would be several successful compromised imgur accounts.

</details>

---
*Analysed by Claude on 2026-05-12*
