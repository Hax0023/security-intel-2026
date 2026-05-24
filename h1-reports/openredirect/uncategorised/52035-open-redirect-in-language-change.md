# Open Redirect in Language Change Feature

## Metadata
- **Source:** HackerOne
- **Report:** 52035 | https://hackerone.com/reports/52035
- **Submitted:** 2015-03-15
- **Reporter:** seifelsallamy
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The language change functionality on HackerOne fails to validate redirect URLs properly, allowing attackers to craft URLs that redirect users to arbitrary external domains. By manipulating the language parameter with a double-slash prefix, an attacker can bypass origin validation and redirect to malicious sites.

## Attack scenario
1. Attacker identifies that language-change links use URL parameters to determine redirect destination
2. Attacker discovers that double-slash prefix (//example.com) bypasses hostname validation checks
3. Attacker crafts a malicious URL: https://hackerone.com//attacker.com/malware
4. Attacker shares the link in phishing emails or social media targeting HackerOne users
5. User clicks the link trusting the hackerone.com domain in the URL bar
6. User is redirected to attacker.com where malware or credential harvesting can occur

## Root cause
The application constructs redirect URLs from user-supplied language parameters without proper validation. The double-slash prefix (protocol-relative URL) technique bypasses simple hostname validation that may check for 'http://' or 'https://' patterns but fails to account for '//' at the beginning of paths.

## Attacker mindset
An attacker would recognize that language/localization features commonly redirect users and often receive less security scrutiny than authentication endpoints. The double-slash technique is a known bypass for URL validation. The attacker aims to establish trust through the legitimate domain while actually redirecting to attacker-controlled infrastructure.

## Defensive takeaways
- Implement strict URL validation using URL parsing libraries rather than string manipulation or regex
- Use whitelist approach: only allow redirects to known safe paths or relative URLs within the same origin
- Avoid constructing URLs from user input; use predefined safe redirect destinations indexed by user selection
- Validate that parsed URL hostname matches expected domain before allowing redirect
- Test language/locale switchers with protocol-relative URLs (//) and other bypass techniques
- Implement Content Security Policy (CSP) with frame-ancestors and redirect restrictions
- Add user-visible warning or confirmation before redirecting to external domains

## Variant hunting
Search for other language/locale switching implementations in the application
Test theme/regional preference features for similar redirect vulnerabilities
Check for open redirects in referral parameters or 'return to' URL parameters
Examine API endpoints that accept redirect_uri or similar callback parameters
Test mobile app deep linking handlers that may accept similar locale-based parameters
Look for other use cases of user-controlled URL construction in navigation flows

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link (delivering malicious redirect)
- T1189 - Drive-by Compromise (potential malware delivery via redirect)
- T1192 - Spearphishing Link

## Notes
The vulnerability leverages a common implementation flaw where developers assume URL validation catches all bypass techniques. The double-slash prefix is particularly dangerous because browsers interpret it as a protocol-relative URL, making it suitable for both HTTP and HTTPS contexts. This is a classic example of inadequate input validation in redirect functionality. The report demonstrates the vulnerability clearly with reproducible steps but lacks evidence of actual exploitation or user impact assessment.

## Full report
<details><summary>Expand</summary>

Hi guys!
Urls:
https://hackerone.com//example.com/ru/faq
and
https://hackerone.com//example.com/faq
or 
https://hackerone.com//example.com/disclosure-guidelines
and
https://hackerone.com//example.com/ru/disclosure-guidelines
scroll down > at the right side 
change the language to English
you will go to http://example.com
Thank you.

</details>

---
*Analysed by Claude on 2026-05-24*
