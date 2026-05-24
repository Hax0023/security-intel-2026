# Application-level DoS via WordPress xmlrpc.php Pingback Amplification

## Metadata
- **Source:** HackerOne
- **Report:** 787179 | https://hackerone.com/reports/787179
- **Submitted:** 2020-02-01
- **Reporter:** mohammedadam24
- **Program:** HackerOne (private program)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Denial of Service, Amplification Attack, Reflective Attack, Insecure Default Configuration
- **CVEs:** None
- **Category:** memory-binary

## Summary
WordPress installations with xmlrpc.php enabled expose pingback.ping method which can be abused to amplify DoS attacks against third-party targets. An attacker can use the vulnerable server as a reflector, sending HTTP requests to arbitrary victim hosts, potentially coordinating multiple compromised WordPress sites for large-scale botnet attacks.

## Attack scenario
1. Attacker discovers WordPress site with xmlrpc.php enabled by sending system.listMethods request
2. Attacker crafts pingback.ping XML-RPC request specifying victim URL as second parameter
3. Vulnerable WordPress server processes the pingback request and makes HTTP connection to victim host
4. Victim receives request from vulnerable server (third-party origin), causing log pollution and potential resource exhaustion
5. Attacker automates attack across multiple compromised WordPress instances to amplify traffic to victim
6. Coordinated botnet of vulnerable servers performs distributed reflection attack, causing DoS to victim infrastructure

## Root cause
WordPress xmlrpc.php file is enabled by default and exposes the pingback.ping method without proper rate limiting, origin validation, or access controls. The server does not verify that the pingback source actually exists before making outbound connections, enabling reflective attacks.

## Attacker mindset
Opportunistic attacker seeks low-effort amplification vectors for coordinated DoS campaigns. Recognizes that many WordPress sites run outdated configurations with unnecessary services exposed. Views xmlrpc as ideal botnet node due to widespread deployment and unpatched default state.

## Defensive takeaways
- Disable xmlrpc.php entirely if pingback/trackback functionality is not required
- Implement strict access controls and IP whitelisting on xmlrpc.php if it must remain enabled
- Add rate limiting to pingback.ping method to prevent amplification abuse
- Validate that pingback source URLs actually exist before making outbound connections
- Monitor outbound HTTP connections from web application for suspicious patterns
- Implement Web Application Firewall rules to block xmlrpc requests from untrusted sources
- Regularly audit and remove unnecessary APIs and legacy endpoints
- Use security headers and request validation to prevent method enumeration via system.listMethods

## Variant hunting
Check for other XML-RPC methods that make external connections (weblog.ping, trackback methods)
Identify other WordPress/PHP applications that expose similar reflection/amplification endpoints
Search for custom XML-RPC implementations in other CMS platforms
Investigate whether other pingback implementations lack validation
Test for HTTP request smuggling via malformed XML-RPC pingback requests
Examine whether user-supplied data in pingback responses can be leveraged for stored XSS

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1498 - Network Denial of Service
- T1570 - Lateral Tool Transfer
- T1566 - Phishing
- T1583 - Acquire Infrastructure

## Notes
This represents a classic amplification/reflection attack pattern. The xmlrpc.php pingback vulnerability has been widely documented and exploited for years. The report demonstrates proper methodology for identifying and exploiting the vulnerability but lacks specific impact metrics (bandwidth amplification factor, request volume impact). Many WordPress hosting providers now block xmlrpc.php by default or disable it automatically. The vulnerability highlights importance of disabling unnecessary legacy features and the risk of exposed administrative interfaces.

## Full report
<details><summary>Expand</summary>

#Vulnerability description:

Wordpress that have xmlrpc.php enabled for pingbacks, trackbacks, etc. can be made as a part of a huge botnet causing a major DDOS. The website https://████/ has the xmlrpc.php file enabled and could thus be potentially used for such an attack against other victim hosts.

#Vulnerable links: https://█████/xmlrpc.php

In order to determine whether the xmlrpc.php file is enabled or not, using the Repeater tab in Burp, send the request below. 

POST /xmlrpc.php HTTP/1.1
Host: ███
Accept: */*
Accept-Language: en
Connection: close
Content-Length: 93

<methodCall>
<methodName>system.listMethods</methodName>
<params></params>
</methodCall>

## Impact

#Impact:
Notice that a successful response is received showing that the xmlrpc.php file is enabled.
Now, considering the domain https://██████/ the xmlrpc.php file discussed above could potentially be abused to cause a DDOS attack against a victim host. This is achieved by simply sending a request that looks like below.

POST /xmlrpc.php HTTP/1.1
Host: ██████
Accept: */*
Accept-Language: en
Connection: close
Content-Length: 235

<methodCall>
<methodName>pingback.ping</methodName>
<params>
<param>
<value><string>http://██████/</string></value>
</param>
<param>
<value><string>https://███████/</string></value>
</param>
</params>
</methodCall>

As soon as the above request is sent, the victim host (█████████) gets an entry in its log file with a request originating from the https://█████/ domain verifying the pingback.

#Remediation:

If the XMLRPC.php file is not being used, it should be disabled and removed completely to avoid any potential risks. Otherwise, it should at the very least be blocked from external access.

</details>

---
*Analysed by Claude on 2026-05-24*
