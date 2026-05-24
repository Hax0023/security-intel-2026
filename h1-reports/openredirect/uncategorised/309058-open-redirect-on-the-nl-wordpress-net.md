# Open Redirect on nl.wordpress.net via Path Traversal

## Metadata
- **Source:** HackerOne
- **Report:** 309058 | https://hackerone.com/reports/309058
- **Submitted:** 2018-01-25
- **Reporter:** sp1d3rs
- **Program:** WordPress.com
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, URL Redirection to Untrusted Site
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists on nl.wordpress.net where user-supplied path input is reflected directly into HTTP 301 redirect Location headers without proper validation. By crafting a URL with `/@domain.com`, the redirect response sends users to `http://nl.wordpress.org@domain.com`, which browsers interpret as credentials (before @) in a URL, redirecting to the attacker-controlled domain while appearing to originate from a trusted WordPress subdomain.

## Attack scenario
1. Attacker crafts malicious link: `http://nl.wordpress.net/@attacker.com` and embeds it in phishing email or social media
2. Victim clicks the link trusting the wordpress.net domain name in the URL
3. Server responds with 301 redirect to `http://nl.wordpress.org@attacker.com`
4. Browser parses the URL and interprets everything before @ as credentials, treating attacker.com as the actual host
5. Victim is redirected to attacker.com but perceives legitimacy due to wordpress domain appearing in redirect chain
6. Attacker's phishing page harvests credentials or malware is served

## Root cause
The application constructs redirect URLs by concatenating the hostname with user-supplied path input without validating or sanitizing the path parameter. When a path contains `@domain.com`, the resulting URL `http://nl.wordpress.org@google.com` is malformed and exploitable due to URL credential syntax (user:pass@host) parsing in browsers.

## Attacker mindset
Leverage trusted domain reputation for credential theft. The @ symbol in URLs is a known browser parsing quirk that allows attackers to disguise redirect destinations. By using a legitimate WordPress subdomain, the attack bypasses initial trust checks. The attacker can create convincing phishing pages that appear to come from WordPress while actually being hosted elsewhere.

## Defensive takeaways
- Validate and sanitize all user input that influences redirect destinations; use allowlists for permitted redirect targets
- Implement strict URL parsing and validation before constructing Location headers
- Ensure redirect responses always use proper relative paths or fully-validated absolute URLs
- Add trailing slashes consistently to prevent path confusion and URL parsing ambiguities
- Use security headers like Content-Security-Policy to restrict redirect destinations
- Implement redirect destination verification and logging for security monitoring
- Test for open redirect vulnerabilities using @ symbol, //, ../, and other URL bypass techniques

## Variant hunting
Test other WordPress subdomains (de.wordpress.net, en.wordpress.net, etc.) for identical vulnerability
Check for similar patterns with other path-based redirects: `/@/`, `//domain.com`, `/%40domain.com` (URL encoded @)
Investigate if backslash handling differs: `\@domain.com` on Windows servers
Test double encoding: `/%2540domain.com`
Check redirect behavior with credentials syntax: `/user:pass@domain.com`
Test with internationalized domain names and unicode @ variants

## MITRE ATT&CK
- T1589.001 - Gather Victim Identity Information (phishing credential harvest)
- T1598.003 - Phishing - Spearphishing Link (malicious redirect in phishing email)
- T1566.002 - Phishing - Phishing - Spearphishing Link

## Notes
This is a classic open redirect leveraging browser URL parsing quirks. The @ symbol is interpreted as a credential separator (RFC 3986), causing `host@attacker.com` to redirect to attacker.com with host as a fake username. The bug report correctly identifies the fix (adding trailing slash), but the real issue is insufficient input validation on user-controlled redirect paths. WordPress responded to this report, indicating it was patched. Similar vulnerabilities have affected other major platforms.

## Full report
<details><summary>Expand</summary>

##Description
Hello. I discovered an Open redirect vulnerability on the `nl.wordpress.org`.

##Root cause
The 301 Redirect contains full hostname, followed with `@` without trailing slash, when using:
```
GET /@google.com HTTP/1.1
Host: nl.wordpress.net
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1

```
```
HTTP/1.1 301 Moved Permanently
Date: Thu, 25 Jan 2018 17:26:07 GMT
Server: Apache
Location: http://nl.wordpress.org@google.com
Content-Length: 242
Keep-Alive: timeout=2, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=iso-8859-1

```

##POC (Google Chrome)
http://nl.wordpress.net/@google.com

##Suggested fix
Appending the trailing slash after location hostname should fix the issue.
e.g.
```
Location: http://nl.wordpress.org@google.com
```
=>
```
Location: http://nl.wordpress.org/@google.com
```

## Impact

The attacker can redirect the victim to the malicious site using legit *.wordpress.net subdomain name, which can be the copy of the real site, asking for the user credentials.

</details>

---
*Analysed by Claude on 2026-05-24*
