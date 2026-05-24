# File upload XSS (Java applet) on http://slackatwork.com/

## Metadata
- **Source:** HackerOne
- **Report:** 97657 | https://hackerone.com/reports/97657
- **Submitted:** 2015-11-04
- **Reporter:** hassham
- **Program:** Unknown
- **Bounty:** $200
- **Severity:** unknown
- **Vuln:** Command Injection - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
The web application supports file uploads and I was able to upload a Java Applet (.class/.jar) file. If a web browser loads a Java applet from a trusted site, the browser provides no security warning. If an attacker can upload a CLASS/JAR file with an applet, the file is executed even if the web page, which embeds the applet is located on a different site. An attacker could use a file upload funct

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

The web application supports file uploads and I was able to upload a Java Applet (.class/.jar) file. If a web browser loads a Java applet from a trusted site, the browser provides no security warning. If an attacker can upload a CLASS/JAR file with an applet, the file is executed even if the web page, which embeds the applet is located on a different site. An attacker could use a file upload function to build an XSS attack using active content.

The impact of this vulnerability
Malicious users may inject JavaScript, VBScript, ActiveX, HTML or Flash into a vulnerable application to fool a user in order to gather data from them. An attacker can steal the session cookie and take over the account, impersonating the user. It is also possible to modify the content of the page presented to the user.


Here is the link of the file i was able to upload with class extension:-

Successfully uploaded file Applet3863.class with content type image/jpeg.

The file is available at: http://slackatwork.com/wp-content/uploads/job-manager-uploads/company_logo/2015/11/Applet3863.class. 


</details>

---
*Analysed by Claude on 2026-05-24*
