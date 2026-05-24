# Open Redirect Vulnerability on XNXX.com

## Metadata
- **Source:** HackerOne
- **Report:** 2957962 | https://hackerone.com/reports/2957962
- **Submitted:** 2025-01-25
- **Reporter:** p_anand1234
- **Program:** XNXX.com
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists on xnxx.com/todays-selection/ that allows attackers to manipulate href attributes to redirect users to arbitrary external websites. This could be exploited for phishing attacks, credential theft, or malware distribution by deceiving users into clicking malicious links.

## Attack scenario
1. Attacker crafts a malicious URL modifying the href parameter to point to a phishing site
2. Attacker shares the crafted URL via social engineering (email, messaging, etc.)
3. Victim clicks the link, trusting the xnxx.com domain
4. User is redirected to attacker-controlled phishing page (e.g., fake login portal)
5. Victim enters credentials believing they're on legitimate site
6. Attacker captures credentials or delivers malware to victim's system

## Root cause
The application fails to validate or whitelist redirect destinations, allowing arbitrary URLs in redirect parameters. Client-side href attribute manipulation is not properly controlled or server-side redirect validation is absent.

## Attacker mindset
Leverage the trusted domain reputation of xnxx.com to bypass user suspicion during phishing attacks. Use social engineering combined with the redirect to harvest credentials or distribute malware while maintaining plausible deniability through the legitimate-appearing domain.

## Defensive takeaways
- Implement server-side whitelist validation for all redirect destinations
- Only allow redirects to explicitly approved internal URLs or trusted partner domains
- Use relative URLs instead of absolute URLs where possible
- Validate and sanitize all user-supplied redirect parameters before processing
- Implement Content Security Policy (CSP) headers to restrict external redirects
- Log and monitor redirect attempts for suspicious patterns
- Educate users to verify URLs in browser address bar after clicks

## Variant hunting
Search for similar redirect parameters across the application (next, return, callback, redirect_uri, url, goto, continue, target). Test other endpoints accepting URL parameters. Check for parameter pollution or encoding bypass techniques (double encoding, Unicode, etc.). Test mobile and API endpoints which may have weaker validation.

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1192

## Notes
Report quality is low - the steps to reproduce appear to describe modifying client-side HTML rather than actual exploitation. Unclear if this is a true server-side redirect vulnerability or merely DOM manipulation. Lacks proof-of-concept demonstration and supporting evidence. No bounty amount provided, suggesting potential reject or low priority. Recommendation section is generic and standard.

## Full report
<details><summary>Expand</summary>

## Summary:
An open redirect vulnerability was discovered on the website https://www.xnxx.com/todays-selection/1. This issue allows attackers to modify URLs to redirect users to arbitrary external websites, including malicious or phishing sites. The vulnerability can be exploited by manipulating specific URL parameters, leading to potential phishing attacks, credential theft, or malware distribution.

## Steps To Reproduce:
1. Navigate to the following URL:https://www.xnxx.com/todays-selection/1
2. inspect the page
3. Go to this attribut:-"href="/todays-selection/2""
3. instead of the "href="/todays-selection/2"" put the "https://google.com"
4. Then browser are the redirect the page on the google.com 


## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * [attachment / reference]

## Impact

The open redirect vulnerability allows attackers to perform malicious redirections, leading to potential phishing attacks or malicious website access. By using this vulnerability, attackers could deceive users into clicking on harmful links that might steal credentials or compromise security.

## Recommendation:
The website should implement input validation for URLs provided in the redirection parameters, allowing only trusted domains or URLs. A whitelist of allowed domains should be enforced for redirection links to mitigate the risk of abuse.

</details>

---
*Analysed by Claude on 2026-05-24*
