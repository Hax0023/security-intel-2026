# An Accidental XSS on uu.nl

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** uu.nl
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Cross-Site Scripting (XSS), Reflected XSS
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered on a subdomain of uu.nl through a UUID parameter that reflected unsanitized user input within HTML title tags. The attacker used tag balancing to inject a script payload that executed arbitrary JavaScript in the victim's browser context.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of uu.nl and identifies www.*.uu.nl as potential targets
2. Using waybackurls tool, attacker discovers a URL pattern with a UUID parameter: https://www.*.uu.nl/XXXXXX/?uuid=vulnerablepoint
3. Attacker submits a test payload to identify where input reflects in the response
4. Attacker discovers the UUID parameter reflects within the HTML title tag without proper sanitization
5. Attacker crafts a tag-balancing payload: test</title><script>alert(document.domain)</script>
6. Attacker sends the malicious URL to a victim, causing the JavaScript to execute in the victim's browser with access to session cookies and sensitive data

## Root cause
Insufficient input validation and output encoding of the UUID parameter. The application failed to sanitize or properly escape user-supplied input before reflecting it in HTML title tags, allowing attackers to break out of the tag context and inject arbitrary HTML/JavaScript.

## Attacker mindset
Methodical reconnaissance through subdomain enumeration and historical URL mining, followed by systematic testing of parameters to identify reflection points. The attacker demonstrates understanding of HTML context-specific encoding by using tag-balancing techniques to escape the title element.

## Defensive takeaways
- Implement robust input validation and whitelist acceptable values for UUID parameters
- Apply context-appropriate output encoding (HTML entity encoding for HTML context, JavaScript encoding for script context)
- Use Content Security Policy (CSP) headers to restrict script execution and mitigate XSS impact
- Employ templating engines with auto-escaping features to prevent accidental XSS
- Conduct security testing on all subdomains and less-obvious endpoints
- Implement WAF rules to detect and block common XSS patterns including tag balancing attempts

## Variant hunting
['Test other parameters in the same endpoint for similar XSS vulnerabilities', 'Check for DOM-based XSS variants in JavaScript that processes the UUID parameter', 'Attempt stored XSS if the UUID value is persisted in databases or user profiles', 'Test different HTML contexts (attributes, event handlers, data attributes) for encoding bypasses', 'Probe for blind XSS using external callback mechanisms', 'Check for second-order XSS where the parameter is reflected in admin panels or dashboards']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing

## Notes
The writeup lacks specific details about subdomain redaction and bounty amount, limiting reproducibility. The vulnerability appears to be a classic reflected XSS with straightforward exploitation. The methodological approach using wayback machine data for URL discovery is noteworthy for reconnaissance. This represents an accidental XSS rather than a sophisticated chain, suggesting possible oversight in security controls rather than a complex logic flaw.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
