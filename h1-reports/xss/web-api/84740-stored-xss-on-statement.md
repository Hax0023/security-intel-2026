# Stored XSS On Statement

## Metadata
- **Source:** HackerOne
- **Report:** 84740 | https://hackerone.com/reports/84740
- **Submitted:** 2015-08-26
- **Reporter:** ibram
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,
I've Found a Stored Cross-Site Scripting (XSS) In [Gratipay.com](https://gratipay.com/) .. This XSS is in The Statement, It Happens Because You're Not Sanitizing This From Markdown Malicious Codes.

##Steps To Reproduce :
1. Login To Your Account At [Gratipay.com](https://gratipay.com/)
2. Go To Your Profile Page .. And Click **Edit Statement**
3. Enter Any Of These 2 Payload : 
 * `

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

Hello,
I've Found a Stored Cross-Site Scripting (XSS) In [Gratipay.com](https://gratipay.com/) .. This XSS is in The Statement, It Happens Because You're Not Sanitizing This From Markdown Malicious Codes.

##Steps To Reproduce :
1. Login To Your Account At [Gratipay.com](https://gratipay.com/)
2. Go To Your Profile Page .. And Click **Edit Statement**
3. Enter Any Of These 2 Payload : 
 * `[notmalicious](javascript:window.onerror=alert;throw%20document.cookie)`
 * `<javascript:alert(document.cookie)>`
4. Click **Save**

Now You'll See 2 Links *(See Links.png)* .. Click On Any Of These 2 Links And The XSS Payload Will Be Triggered :)

Also This is Dangerous Because The Profile's Statement is Public .. 
So Anyone Visit The Attaker's Profile And Click On This Malicious Link, XSS Will Be Triggered On His Browser. 

Take a Look At My Profile On Gratipay : https://gratipay.com/~geekpero/.

Please Let Me Know If You Need Any Information.

**References About Markdown XSS:**
* http://stackoverflow.com/questions/1690601/markdown-and-xss
* https://michelf.ca/blog/2010/markdown-and-xss/

Best Regards,
Ebram Marzouk

</details>

---
*Analysed by Claude on 2026-05-24*
