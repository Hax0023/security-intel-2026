# CSS injection in avito.ru via IE11 

## Metadata
- **Source:** HackerOne
- **Report:** 276747 | https://hackerone.com/reports/276747
- **Submitted:** 2017-10-12
- **Reporter:** hussain_0x3c
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Team Security @avito

I discovered [CSS Injection](https://portswigger.net/knowledgebase/issues/details/00501300_cssinjectionreflected) on [avito.ru](https://avito.ru) in `form search` via IE11

####Description

`CSS injection` vulnerabilities arise when an application imports a style sheet from a **user-supplied URL**, or embeds user input in CSS blocks without adequate escaping. They are clos

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

Hi Team Security @avito

I discovered [CSS Injection](https://portswigger.net/knowledgebase/issues/details/00501300_cssinjectionreflected) on [avito.ru](https://avito.ru) in `form search` via IE11

####Description

`CSS injection` vulnerabilities arise when an application imports a style sheet from a **user-supplied URL**, or embeds user input in CSS blocks without adequate escaping. They are closely related to cross-site scripting (XSS) vulnerabilities but often trickier to exploit.

Being able to inject arbitrary CSS into the victim's browser may enable various attacks, including :

- Executing arbitrary JavaScript using IE's expression() function.
- Using CSS selectors to read parts of the HTML source, which may include sensitive data such as anti-CSRF tokens.
- Capturing any sensitive data within the URL query string by making a further style sheet import to a URL on the attacker's domain, and monitoring the incoming Referer header. 

**Affected URL**
~~~
https://www.avito.ru/rossiya/nedvizhimost?s='><b/style=position:fixed;top:0;left:0;font-size:200px>XSS<!--
~~~

####Proof of Concept 

{F228726}


####Remediation

Ensure that user input is adequately escaped before embedding it in CSS blocks, and consider using a whitelist to prevent loading of arbitrary style sheets.

####References

[Malicious CSS](http://mksben.l0.cm/2015/10/css-based-attack-abusing-unicode-range.html)

**Best Regards**
Hussain Adnan

</details>

---
*Analysed by Claude on 2026-05-24*
