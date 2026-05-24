# Reflected XSS on Zomato API

## Metadata
- **Source:** HackerOne
- **Report:** 125762 | https://hackerone.com/reports/125762
- **Submitted:** 2016-03-24
- **Reporter:** murat
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
First of all [here] (https://hackerone.com/reports/115402) is another report looks like this report. 

Zomato using APIs for developers to create their restaurant search etc. 

You are using res_search_widget which is can be seen right [here] (https://www.zomato.com/widgets/res_search_widget.php). 

In the report which is 115402 number that i mentioned start of the report, reporter say something l

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

First of all [here] (https://hackerone.com/reports/115402) is another report looks like this report. 

Zomato using APIs for developers to create their restaurant search etc. 

You are using res_search_widget which is can be seen right [here] (https://www.zomato.com/widgets/res_search_widget.php). 

In the report which is 115402 number that i mentioned start of the report, reporter say something like this: 

I use a piece of javascript code that creates an alert box with the document.domain, which shows the SOP is bypassed: "}');alert(document.domain);console.log('.  But you dont need to add something to your API or widget code. You should only use '"> characters to bypass security and have xss alert.

So, here is xss:

Just go to your widget from [here](https://www.zomato.com/widgets/res_search_widget.php).

And just write this payload:

`'-->">'>'"<script>prompt(document.domain)</script>;" f0r=TRUE`

Here is your alert.



</details>

---
*Analysed by Claude on 2026-05-24*
