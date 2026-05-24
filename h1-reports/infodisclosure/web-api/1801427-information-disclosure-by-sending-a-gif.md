# Information disclosure by sending a GIF

## Metadata
- **Source:** HackerOne
- **Report:** 1801427 | https://hackerone.com/reports/1801427
- **Submitted:** 2022-12-12
- **Reporter:** qualw1n
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Client-Side Enforcement of Server-Side Security
- **CVEs:** None
- **Category:** web-api

## Summary
# Summary
- The attacker can view the Operating System, Version Of  The Operating System, Browser, IP Address, Device ID, Phone Model, Time Zone and other critical information about any LinkedIn user they have identified as a victim.

# Steps to Reproduce

1- Create a standard linkedin user account to use in the attack.
2- Select a GIF from the GIF Keyboard and capture the request with Burp Suite 

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

# Summary
- The attacker can view the Operating System, Version Of  The Operating System, Browser, IP Address, Device ID, Phone Model, Time Zone and other critical information about any LinkedIn user they have identified as a victim.

# Steps to Reproduce

1- Create a standard linkedin user account to use in the attack.
2- Select a GIF from the GIF Keyboard and capture the request with Burp Suite while sending it to your victim.
3- Forward all requests until you get to the voyager/api/voyagerMessagingDashMessengerMessages?action=createMessage endpoint. In this request, type the Burp Suite Collaborator url in message.renderContentUnions.externalMedia.media.url in the JSON Data containing (parameters) section.
4- When the victim opens the message box, the attacker will get critical information about the victim.

** Steps Photo **

{F2073194}
{F2073195}
{F2073196}
{F2073197}
{F2073200}
{F2073201}
{F2073202}

## Notes ##

- This vulnerability affects not only smartphones but all platforms where you can use the link (Smart Phones, iPads, Web Browser, Smart TV etc.)
- When the victim uses an apple phone, much more and critical data can be obtained than the android and web version.

{F2073291}
--------
{F2073293}

## PoC Video
{F2073296}
{F2073297}

## References
- Same Attack Scenarios

https://ph-hitachi.medium.com/facebook-bug-poc-external-service-interaction-dns-http-ab55bfdb98f6

## Impact

Black Hat Hackers can get critical information about all LinkedIn users. The information obtained is very important for the privacy of the users and includes information such as IP address, OS versions.

</details>

---
*Analysed by Claude on 2026-05-24*
