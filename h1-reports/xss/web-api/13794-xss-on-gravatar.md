# XSS on gravatar

## Metadata
- **Source:** HackerOne
- **Report:** 13794 | https://hackerone.com/reports/13794
- **Submitted:** 2014-05-28
- **Reporter:** simon90
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello team of Wordpress!

I am Simone and I am here to report a XSS on gravatar!

I think that you don't believe me, but it's true, because I have found 171 XSS with different directory and parametrers!

Let's the details:

Vulnerability:XSS.

Severity:High.

Vulnerability description:

Cross site scripting (also referred to as XSS) is a vulnerability that allows an attacker to send 

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

Hello team of Wordpress!

I am Simone and I am here to report a XSS on gravatar!

I think that you don't believe me, but it's true, because I have found 171 XSS with different directory and parametrers!

Let's the details:

Vulnerability:XSS.

Severity:High.

Vulnerability description:

Cross site scripting (also referred to as XSS) is a vulnerability that allows an attacker to send malicious code (usually in the form of Javascript) to another user. Because a browser cannot know if the script should be trusted or not, it will execute the script in the user context allowing the attacker to access any cookies or session tokens retained by the browser.

Proof of concept of the XSS (Only two):

1)http://grabilla.com/04318-cb553271-51b2-4fba-81ea-9a611d1db71f.html

2)http://grabilla.com/04318-00311a7d-3dd3-4032-8c79-3c3656330216.html

How to reproduce it:

1)Create an HTML file with this code:

See the pastebin link for the HTML CODE: http://pastebin.com/fsAKWTe1



2)Open it on Mozilla, Like this..poc below:

http://grabilla.com/04318-271a0763-cad8-4482-ab02-3d8948f33b04.html

3)Now, the payload is something like: "onmouseover='prompt(916137)'bad="> right? Well, pass the mouse on "JSON" or "XML" or etc and you will see the alert! :)

Like this:

FINAL POC: http://grabilla.com/04318-ff2c5eea-0491-4841-977a-a4b7b1fafc9e.html

Well, my report finish here,

Thanks and best regards,

Simone

</details>

---
*Analysed by Claude on 2026-05-24*
