# Open Redirect in WordPress Feed Statistics Plugin

## Metadata
- **Source:** HackerOne
- **Report:** 22142 | https://hackerone.com/reports/22142
- **Submitted:** 2014-08-02
- **Reporter:** mtk
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Insufficient Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Feed Statistics WordPress plugin contains an open redirect vulnerability in its feed-stats-url parameter that accepts base64-encoded URLs without proper validation. Attackers can craft malicious links to redirect users to arbitrary external websites, potentially used for phishing or malware distribution. The vulnerability affects all versions of the plugin across multiple WordPress installations.

## Attack scenario
1. Attacker identifies the Feed Statistics plugin installed on a WordPress site
2. Attacker base64-encodes a malicious URL (e.g., http://phishing-site.com)
3. Attacker crafts a legitimate-looking link with the feed-stats-url parameter: victim-site.com/?feed-stats-url=aHR0cDovL3BoaXNoaW5nLXNpdGUuY29t
4. Attacker distributes link via email, social media, or forum posts with social engineering pretext
5. User clicks the link trusting the victim domain in the URL
6. Plugin automatically decodes and redirects user to attacker-controlled phishing page

## Root cause
The plugin fails to validate or sanitize the feed-stats-url parameter before processing it. The code decodes base64 input and performs an immediate redirect without checking if the destination URL is internal to the site or trusted, allowing any external URL to be used.

## Attacker mindset
An attacker would leverage this for credential harvesting by creating convincing phishing pages. The trust users place in legitimate domain names makes this particularly effective for social engineering attacks. The base64 encoding obfuscation adds a layer of bypass against simple URL pattern detection.

## Defensive takeaways
- Implement strict URL validation: whitelist internal domains or verify URLs match expected patterns
- Use WordPress sanitization functions (sanitize_url, wp_safe_remote_get) for any user-supplied URLs
- Perform server-side redirect validation before executing any redirect operations
- Log and monitor redirect requests for anomalous patterns
- Implement CSP headers to limit redirect scope
- Update plugins immediately and establish a patch management process for security vulnerabilities
- Consider disabling redirects entirely if not critical functionality

## Variant hunting
Search for similar patterns in other WordPress plugins using query parameter names like 'redirect', 'return', 'url', 'goto', 'ref', 'redirect_to' that decode or process URLs without validation. Check for base64_decode() or similar decoding functions followed by wp_redirect() without intervening validation checks.

## MITRE ATT&CK
- T1598.003
- T1583.005
- T1657

## Notes
The researcher provided multiple active POCs on real websites including the plugin developer's own site, demonstrating widespread deployment. The base64 encoding appears intentional obfuscation suggesting the vulnerability may have been overlooked during initial design. The large number of affected sites (hesp-news.org, dropboxatwork.com, gamona.de, etc.) indicates significant real-world impact. No response timeline or patch status mentioned in the report.

## Full report
<details><summary>Expand</summary>

Hi,
    Feed Statistics Plugin is vulnerable to Open Redirect and effecting large amount of Websites. Which is the reason it should be patched swiftly. Detail description is given below:

Tested on:
Wordpress 3.9.1

Vulnerable Plugin:
Feed Statistics

Plugin Link:
http://wordpress.org/plugins/wordpress-feed-statistics/

Tested on:
Firefox 31.0 / Debian, Linux

P.O.C:

http://www.example.com/?feed-stats-url=any+website+in+Base64+Encoding+here
Like this:
http://www.example.com/?feed-stats-url=aHR0cDovL3d3dy5zb29ldmlsc2l0ZS5jb20v

Result Redirect to:
http://www.sooevilsite.com/

P.O.C P.O.C:

http://hesp-news.org/?feed-stats-url=aHR0cDovL3d3dy5zb29ldmlsc2l0ZS5jb20v

https://www.dropboxatwork.com/?feed-stats-url=aHR0cDovL3d3dy5zb29ldmlsc2l0ZS5jb20v

https://starwars.gamona.de/?feed-stats-url=aHR0cDovL3d3dy5zb29ldmlsc2l0ZS5jb20v

https://joyinthisjourney.com/?feed-stats-url=aHR0cDovL3d3dy5zb29ldmlsc2l0ZS5jb20v

http://www.apaixonadosporseries.com.br/?feed-stats-url=aHR0cDovL3d3dy5zb29ldmlsc2l0ZS5jb20v

https://graziasl.com/?feed-stats-url=aHR0cDovL3d3dy5zb29ldmlsc2l0ZS5jb20v


Developer site :)
http://www.chrisfinke.com/?feed-stats-url=aHR0cDovL3d3dy5zb29ldmlsc2l0ZS5jb20v

                Feel free to contact me anytime if there is more info required.

</details>

---
*Analysed by Claude on 2026-05-24*
