# Open Redirect via Hash Fragment Manipulation in NordVPN Support

## Metadata
- **Source:** HackerOne
- **Report:** 753399 | https://hackerone.com/reports/753399
- **Submitted:** 2019-12-06
- **Reporter:** nickelheck
- **Program:** NordVPN (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, Improper Input Validation, URL Parsing Logic Error
- **CVEs:** None
- **Category:** uncategorised

## Summary
The NordVPN support website contains an open redirect vulnerability in its hash-based routing logic. The vulnerable code extracts and redirects to user-supplied content after '#/path' without validating the target URL, allowing attackers to redirect users to arbitrary domains.

## Attack scenario
1. Attacker crafts a malicious URL containing #/path///example-malicious-domain.com
2. Attacker distributes URL via phishing email, social media, or ads targeting NordVPN users
3. Victim clicks the link believing they are accessing legitimate NordVPN support
4. JavaScript code detects '#/path' in URL and extracts everything after it
5. Browser redirects victim to attacker-controlled domain (e.g., phishing site mimicking login page)
6. Attacker harvests credentials or distributes malware

## Root cause
The code uses string slicing to extract redirect targets without URL validation. The slice operation `document.URL.slice(window.location.href.indexOf('#/path') + 6)` blindly extracts everything after '#/path' and assigns it to window.location.href without sanitization or domain whitelist validation.

## Attacker mindset
Social engineering through trusted domain spoofing. Attacker leverages the legitimate NordVPN domain to bypass user suspicion, making phishing attacks more effective since the initial URL appears trustworthy.

## Defensive takeaways
- Implement URL whitelist validation before any redirect operation
- Use URL parsing APIs (URL constructor) instead of string manipulation for URL handling
- Never trust user-supplied input in URL fragments for redirects
- Validate that redirect targets are same-origin or explicitly whitelisted domains
- Use Content Security Policy (CSP) with 'frame-ancestors' and 'form-action' directives
- Implement server-side redirect validation rather than client-side only
- Add security review for all hash-based routing logic
- Log and monitor redirect attempts for anomalous patterns

## Variant hunting
Search for similar hash-based routing patterns using '#/' followed by string manipulation without validation
Check for window.location.href assignments after indexOf/slice operations
Look for redirect logic in single-page applications (SPAs) with custom routing
Test other hash fragments like #redirect=, #url=, #return_to= with path traversal sequences
Check for similar vulnerabilities in other NordVPN subdomains or properties

## MITRE ATT&CK
- T1598 - Phishing (via open redirect)
- T1566 - Phishing (email delivery of malicious link)
- T1598.003 - Spearphishing Link
- T1547 - Abuse Elevation Control Mechanism (credential harvesting post-redirect)

## Notes
This is a classic client-side open redirect that demonstrates why complex URL routing logic should never be implemented with string manipulation. The use of triple slashes ('///') in the proof-of-concept exploits URL parsing ambiguity. The vulnerability is particularly dangerous because it originates from a security-focused vendor, making users more likely to trust the domain.

## Full report
<details><summary>Expand</summary>

The following URL is vulnerable to an open redirect (it will redirect to google.com):
https://support.nordvpn.com/#/path///google.com
vulnerable code:
```
<script>
			if (window.location.href.indexOf('#/path') !== -1) {
				console.log("document.URL", document.URL)
				window.location.href = document.URL.slice(window.location.href.indexOf('#/path') + 6);
			}
		</script>
```

## Impact

Users could get redirected to malicious domain.

</details>

---
*Analysed by Claude on 2026-05-24*
