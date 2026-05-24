# Open Redirection Filter Bypass via Whitelist Logic Flaw

## Metadata
- **Source:** HackerOne
- **Report:** 44157 | https://hackerone.com/reports/44157
- **Submitted:** 2015-01-17
- **Reporter:** securityidiots
- **Program:** Vimeo
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Open Redirection, Insufficient Input Validation, Whitelist Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
Vimeo's open redirection filter could be bypassed by crafting URLs that technically met the filter criteria (containing 'vimeocdn.com/' and image extension) while still redirecting to attacker-controlled domains. The filter used substring matching instead of proper URL parsing, allowing an attacker to inject the whitelist string within a malicious URL.

## Attack scenario
1. Attacker crafts a malicious URL: https://vimeo.com/tools/edit?image=http://securityidiots.com?vimeocdn.com/.png
2. The URL passes the first filter check by containing the substring 'vimeocdn.com/'
3. The URL passes the second filter check by ending with image extension '.png'
4. Application processes the image parameter and performs a redirect
5. User is redirected to http://securityidiots.com instead of legitimate vimeocdn.com domain
6. Attacker can use this for phishing, malware distribution, or credential harvesting

## Root cause
The security filter used simple substring matching ('vimeocdn.com/' must be present) and extension validation rather than proper URL parsing and validation. The filter checked if whitelist components existed anywhere in the URL string instead of validating the URL scheme and host origin.

## Attacker mindset
An attacker recognized that blacklist/whitelist filters are often bypassed through creative string manipulation. By including the required whitelist string as a query parameter within a malicious URL, they satisfied the filter logic while maintaining control over the actual redirect destination.

## Defensive takeaways
- Use proper URL parsing libraries (e.g., urlparse) instead of string matching for redirect validation
- Validate the URL scheme (http/https) and host/domain explicitly, not just presence of substrings
- Implement a whitelist of complete base URLs rather than checking for substrings
- For image serving, use server-side URL construction: prepend the trusted domain and only accept relative paths or IDs from user input
- Test bypass techniques: query parameters, fragments, encoding, protocol handlers, and alternative domain formats
- Perform security code review specifically for URL handling logic
- Log and monitor redirect attempts to detect unusual patterns

## Variant hunting
Test if filter can be bypassed with URL encoding (%3F instead of ?)
Try double encoding or mixed case variations
Attempt protocol-relative URLs (//attacker.com)
Use data: or javascript: protocols if redirect validation is insufficient
Test with fragment identifiers (#vimeocdn.com/) before malicious URL
Try percent-encoding the whitelist string itself
Test with subdomain manipulation if full domain checking is missing
Attempt with trailing dots or null bytes if older PHP versions are used

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1204.001

## Notes
This is a classic example of security through obscurity failing when input validation logic is flawed. The developers attempted to solve open redirection but chose the wrong implementation approach. The report includes a clear remediation path: hardcoding the trusted base URL and only accepting image identifiers/paths as user input, which is the recommended secure pattern for this use case.

## Full report
<details><summary>Expand</summary>

Hi,

The application is vulnerable to Open Redirection using a basic filter bypass which it was using for security against open redirection.

Here is the vulnerable link:
https://vimeo.com/tools/edit?image=http://securityidiots.com?vimeocdn.com/.png

Weakness in filter against Open Redirect.: Actually the application is using the below given filters against open redirection.
1. URL must contain "vimeocdn.com/"
2. It should end with an image extention for example jpg, png etc

The problem with the above filter can be seen in my payload, as i included both of the requirements and still redirected the user to my url.

Solution : Below changes can be made to the security.
If "https://f.vimeocdn.com/" is the URL for images then hardcode it and take the rest of input from GET so that in any case we will have "https://f.vimeocdn.com/" before the URL and user wont be able to do a open redirect to any other domain.

</details>

---
*Analysed by Claude on 2026-05-24*
