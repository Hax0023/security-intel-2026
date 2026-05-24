# Subdomain Takeover to Authentication Bypass via Unclaimed HubSpot Instance

## Metadata
- **Source:** HackerOne
- **Report:** 335330 | https://hackerone.com/reports/335330
- **Submitted:** 2018-04-09
- **Reporter:** geekboy
- **Program:** Roblox
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Subdomain Takeover, Cookie Theft, CORS Misconfiguration, Credential Harvesting, Malware Distribution
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker could claim the expired/unclaimed HubSpot instance at devrel.roblox.com and exploit subdomain takeover to steal user authentication cookies scoped to *.roblox.com. The subdomain was also whitelisted for CORS requests to chat.roblox.com, enabling unauthorized access to private user conversations.

## Attack scenario
1. Attacker identifies that devrel.roblox.com CNAME points to an unclaimed/expired HubSpot instance
2. Attacker registers/claims the HubSpot instance and gains control over devrel.roblox.com
3. Attacker hosts malicious PHP code on devrel.roblox.com that captures .ROBLOSECURITY cookies automatically sent by browsers due to *.roblox.com scope
4. Attacker uses devrel.roblox.com origin to make CORS-allowed requests to chat.roblox.com/v2/get-messages with victims' credentials
5. Attacker optionally hosts fake Roblox login page on devrel.roblox.com to harvest credentials from phishing victims
6. Attacker distributes malicious files or sends emails spoofed from @devrel.roblox.com using GSuite

## Root cause
Roblox failed to manage DNS records for abandoned subdomains, leaving devrel.roblox.com pointing to an unclaimed external service. Additionally, overly permissive CORS policies whitelisted the subdomain for sensitive API endpoints, and cookie scope was set too broadly to *.roblox.com without subdomain validation.

## Attacker mindset
An opportunistic attacker could systematically scan Roblox subdomains for DNS misconfigurations pointing to unclaimed third-party services. Once takeover is achieved, the attacker recognizes the high-value nature of the target (authentication cookies, private chat access) and chains multiple attacks together for maximum impact, including account takeovers and data exfiltration.

## Defensive takeaways
- Implement regular DNS audits to identify and remove CNAME records pointing to external services that are no longer in use
- Maintain an inventory of all subdomains and their purposes; promptly decommission unused subdomains
- Scope authentication cookies with SameSite=Strict and avoid wildcard domain scoping; use explicit subdomain lists instead
- Implement strict CORS policies: whitelist only necessary origins and endpoints; avoid whitelisting user-controlled or delegated subdomains
- Monitor for subdomain takeover attempts using services that detect DNS misconfigurations
- Implement content security policies (CSP) to prevent inline script execution and cookie theft
- Use certificate transparency logs to detect unauthorized certificate issuance for company domains
- Require multi-factor authentication to prevent account takeover via stolen cookies alone

## Variant hunting
Search for other Roblox subdomains (api.*, platform.*, internal.*, staging.*, old.*, etc.) pointing to external services like Heroku, GitHub Pages, AWS S3, Firebase, or other PaaS platforms. Test CORS policies on remaining whitelisted subdomains. Review cookie scoping across all Roblox properties for overly permissive domain wildcards. Check for similar patterns in related gaming platforms and social networks.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1021 - Remote Services (via credential theft)
- T1555 - Credentials from Web Browsers (cookie theft)
- T1539 - Steal Web Session Cookie
- T1040 - Network Sniffing (CORS-enabled data exfiltration)
- T1598 - Phishing (fake login page)
- T1566 - Phishing (malware distribution)
- T1589 - Gather Victim Identity Information

## Notes
This report demonstrates a critical chain of vulnerabilities where subdomain takeover serves as the entry point for multiple downstream attacks. The CORS misconfiguration and broad cookie scoping amplified the impact significantly. The attacker could achieve account takeover, data exfiltration, and impersonation without needing to exploit application logic vulnerabilities. The report's proof-of-concept code, while conceptual, clearly illustrates the attack surface. Roblox's response should include not just removing the CNAME but conducting a comprehensive security review of all subdomain delegations and CORS policies.

## Full report
<details><summary>Expand</summary>

## Vulnerability Type: 
-----------
Subdomain Takeover

## Description: 
-----------
Due to unclaimed or expired Hubspot instance an attacker is able to claim and serve content from `devrel.roblox.com` and perform different kind of attacks which i shared in impact section.

## Affected Area: 
-----------
http://devrel.roblox.com

## Steps to Reproduce:
-----------
+ Visit: https://devrel.roblox.com/subdomain-takeover

{F283580}

## Mitigation:
-----------
+ Remove the CNAME entry for the `devrel.roblox.com`

## Impact

Let's talk about about in details, as attacker could possible takeover other users account. 

1. As `.ROBLOSECURITY` cookies is scoped to `*.roblox.com` means same cookies shared with all other subdomain, i'm not much familiar with hubspot with hosting following code on will steal all the users cookie who visit this subdomain.

{F283554}

###steal_cookie.php

```php
<html>
<body>
<?php
echo "Cookies received: <br>";

foreach ($_COOKIE as $key=>$val)
  {
    echo "Set-Cookie: $key=$val; Domain=.roblox.com; path=/<br>\n";
  }
?>
</body>
</html>
``` 

2. Also `devrel.roblox.com` can be used to read all the chats between other users as 
 `devrel.roblox.com` is also white listed to make CORS request at  `chat.roblox.com` 

{F283553}

Which can be done like this: 

````html

<h2>CORS To Read Chat</h2>
<div id="demo">
<button type="button" onclick="cors()">Chat Reader @ Roblox</button>
</div>
 
<script>
function cors() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML = document.write(this.responseText);
    }
  };
  xhttp.open("GET", "https://chat.roblox.com/v2/get-messages?conversationId=469104576&pageSize=3", true);
  xhttp.withCredentials = true;
  xhttp.send();
}
</script>
 ````

Apart form all above issue, attacker can do following things as well.
+ Creating fake login page for credentials harvesting.
+ Sharing malicious files using roblox.
+ Creating mail account using GSuite to send and recived emails on behalf of `*@devrel.roblox.com`

</details>

---
*Analysed by Claude on 2026-05-24*
