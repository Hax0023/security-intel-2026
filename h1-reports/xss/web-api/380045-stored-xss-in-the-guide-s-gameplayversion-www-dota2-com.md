# Stored XSS in Dota2 Guide GameplayVersion Field

## Metadata
- **Source:** HackerOne
- **Report:** 380045 | https://hackerone.com/reports/380045
- **Submitted:** 2018-07-10
- **Reporter:** mvc
- **Program:** Valve (Dota 2)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Dota 2 guide system where malicious JavaScript can be injected into the GameplayVersion field and persisted to the backend. The vulnerability allows attackers to bypass client-side sanitization by intercepting and modifying HTTP requests, causing the payload to execute when the guide is viewed on www.dota2.com.

## Attack scenario
1. Attacker creates a Dota 2 guide with XSS payload in the title field
2. Attacker publishes the guide to Steam through the Dota 2 client
3. Attacker intercepts the PUT request using a proxy tool (Fiddler) during guide editing
4. Attacker transfers the XSS payload from the sanitized Title field to the GameplayVersion field, maintaining identical content length to bypass hash validation
5. Attacker re-publishes the modified guide, successfully persisting the payload to the backend
6. When victims visit the public guide URL on www.dota2.com, the stored XSS executes in their browser context, allowing session hijacking or cookie theft

## Root cause
The GameplayVersion field lacks proper server-side input validation and output encoding. The application relied on client-side sanitization and hash-based validation that could be circumvented through request interception. The field was not properly sanitized before storage or rendering, allowing arbitrary JavaScript execution.

## Attacker mindset
The attacker demonstrated sophisticated exploitation technique by identifying that while one field (Title) was sanitized, another field (GameplayVersion) was not. They cleverly maintained content length to bypass hash verification mechanisms, showing understanding of backend validation logic. This indicates intent to create a persistent attack vector affecting all users viewing the malicious guide.

## Defensive takeaways
- Implement server-side input validation and sanitization for all user-supplied data, not just client-side filtering
- Apply proper output encoding/escaping when rendering user content in HTML context
- Never rely solely on client-side validation or hash-based integrity checks that can be modified in transit
- Validate and sanitize all relevant fields, not just obvious ones like 'Title'
- Use Content Security Policy (CSP) headers to mitigate XSS impact
- Implement strict HTML sanitization libraries (e.g., DOMPurify) for any user-generated content display
- Consider allowlisting safe values for version fields rather than free-form text input

## Variant hunting
Examine all text input fields in guide creation/editing functionality for similar XSS vulnerabilities. Test other Valve game workshop systems for identical patterns. Check for other fields in guide metadata that may lack proper sanitization such as description, tags, or category fields. Investigate whether hash-based validation mechanisms are used elsewhere and can be bypassed similarly.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1059 - Command and Scripting Interpreter
- T1185 - Traffic Mirroring

## Notes
This report builds upon a previous finding (HackerOne #369043). The attack exploits the gap between client-side sanitization and server-side validation. The researcher's use of Fiddler to intercept and modify requests demonstrates a common attack vector against applications that rely on in-transit data integrity checks. The vulnerability affects all users who view the malicious guide, making it a high-impact issue despite requiring moderate technical skill to exploit.

## Full report
<details><summary>Expand</summary>

Hi, team!

The beginning of this issue looks like my previous report #369043, but this one will be much more interesting :) So let's go!

Steps to reproduce:

1) Open dota2 client and create new simple guide with XSS in the name.

{F318796}

2) Publish this guide on steam.

{F318797}

3) Now go to the Fiddler app and look at the request from dota2 client:

{F318798}

The XSS script placed in the title, the title displays a safe HTML on the site, so, for now nothing terrible happens.

4) Next I write some piece of code in the Fiddler app:

```
if (oSession.uriContains("/cloud/CB/")) {
    var strBody=oSession.GetRequestBodyAsString();       
    strBody=strBody.replace("mvc123<svg/onload=alert(document.domain)>","mvc123");
    strBody=strBody.replace("7.18","7.18<svg/onload=alert(document.domain)>");
    oSession.utilSetRequestBody(strBody);       
}
```

So I transfer the XSS script from "Title" to "GameplayVersion". I decided to go this way, since in this case the content length of build's file does not change and it successfully passes the hash sum comparison.

5) Now we return to the dota2 client, click "Edit" and change anything in the our build and publish it again. And we see that the PUT request was successful and the XSS data in it is arranged the way we wanted:

{F318801}

6) Next i follow to the Dota2 Workshop Manager.

{F318802}

And here we see our public file ID. This connection with the public guide files I was found in the preparation of the previous report, but I did not know how to apply it (before today).

7) Put this FileID into a link below and we get the public infected page:

http://www.dota2.com/workshop/builds/view?fileid=949580646106367888

And the result in the latest versions of Firefox and Chrome:

{F318805}

{F318803}

{F318804}

Sincerely, @mvc

## Impact

As on any cross-site-scripting vulnerability. The top line would be that the attacker might steals cookies to abuse users session.

</details>

---
*Analysed by Claude on 2026-05-12*
