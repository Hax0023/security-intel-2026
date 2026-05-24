# Reflected XSS via File Upload

## Metadata
- **Source:** HackerOne
- **Report:** 1816181 | https://hackerone.com/reports/1816181
- **Submitted:** 2022-12-24
- **Reporter:** greymanx1
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Reflected XSS in " https://reddit.zendesk.com/hc/en-us/requests/new " via file upload

## Impact:

!!
attacker can send that email to victim and steal user account or cookies

Cross site scripting attacks can have devastating consequences. Code injected into a vulnerable application can exfiltrate data or install malware on the user’s machine. Attackers can masquerade as authorized use

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

## Summary:
Reflected XSS in " https://reddit.zendesk.com/hc/en-us/requests/new " via file upload

## Impact:

!!
attacker can send that email to victim and steal user account or cookies

Cross site scripting attacks can have devastating consequences. Code injected into a vulnerable application can exfiltrate data or install malware on the user’s machine. Attackers can masquerade as authorized users via session cookies, allowing them to perform any action allowed by the user account.

XSS can also impact a business’s reputation. An attacker can deface a corporate website by altering its content, thereby damaging the company’s image or spreading misinformation. A hacker can also change the instructions given to users who visit the target website, misdirecting their behavior.

* Perform any action within the application that the user can perform.
* View any information that the user is able to view.
* Modify any information that the user is able to modify.
* Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user.

Note ! 
svg work with all browsers
xml file work with all browsers except ( google chrome )


## Steps To Reproduce:

  1. go to " https://reddithelp.com/hc/en-us/requests/new  " and select any type of report
  2. type your email in email fileds and type any text in other fileds 
  3. in upload function upload  <svg>  or <xml> file I attached and send the request
 4. now go to your mail box go to reddit mail and select the file you uploaded 
 5. after downlaoded the file open it in browser it will fire !

## Supporting Material/References:

  * Upload this files to site

{F2089769}
{F2089770}

## Impact

Steal user cookie 
Account Takeover !
Perform any action within the application that the user can perform.
View any information that the user is able to view.
Modify any information that the user is able to modify.
Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user

</details>

---
*Analysed by Claude on 2026-05-24*
