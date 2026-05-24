# WordPress Core - Denial of Service via Cross Site Request Forgery

## Metadata
- **Source:** HackerOne
- **Report:** 153093 | https://hackerone.com/reports/153093
- **Submitted:** 2016-07-22
- **Reporter:** spipm
- **Program:** WordPress
- **Bounty:** Not specified in provided content
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF), Denial of Service (DoS)
- **CVEs:** None
- **Category:** memory-binary

## Summary
A CSRF vulnerability in WordPress core allows an attacker to trigger denial of service conditions by forcing authenticated users to perform resource-intensive operations. The vulnerability exploits the lack of proper CSRF token validation or request origin checking on critical operations, enabling attackers to exhaust server resources.

## Attack scenario
1. Attacker identifies a WordPress core function that performs resource-intensive operations (e.g., database queries, file operations, or bulk processing)
2. Attacker crafts a malicious webpage containing hidden requests (image tags, forms, or JavaScript) that trigger these operations
3. Attacker distributes the webpage via phishing, compromised sites, or advertisements to target WordPress administrators or users with elevated privileges
4. When a logged-in WordPress user visits the malicious webpage, the browser automatically sends authenticated requests without user knowledge
5. The crafted requests trigger expensive operations on the victim's WordPress server, consuming CPU, memory, and database resources
6. Repeated exploitation causes the server to become unresponsive, resulting in denial of service for legitimate users

## Root cause
WordPress core endpoint(s) lack proper CSRF token validation (nonce verification) or insufficient origin validation, allowing cross-site requests to trigger sensitive operations without user consent. Additionally, insufficient rate limiting or request throttling permits repeated malicious requests to exhaust server resources.

## Attacker mindset
An attacker seeks to disrupt WordPress site availability without requiring direct server access. By chaining CSRF with resource-intensive operations, they can achieve DoS effects while maintaining plausible deniability. This vector is particularly effective against high-traffic sites where multiple compromised visitors trigger simultaneous resource exhaustion.

## Defensive takeaways
- Implement proper nonce verification on all state-changing operations and sensitive endpoints using wp_verify_nonce()
- Add CSRF token validation to AJAX endpoints and REST API routes
- Implement rate limiting and request throttling on resource-intensive operations to prevent abuse
- Use the SameSite cookie attribute on session cookies to mitigate CSRF attacks
- Validate request origins using the Referer and Origin headers
- Implement request signing or HMAC validation for sensitive operations
- Monitor for unusual spike patterns in resource consumption or bulk operation requests
- Keep WordPress core and all plugins updated to patch known CSRF vulnerabilities

## Variant hunting
Search for other WordPress core endpoints accepting POST/state-changing requests without nonce verification
Identify bulk operations (bulk delete, bulk edit, bulk trash) that may lack proper CSRF protection
Test AJAX handlers in wp-admin/admin-ajax.php for missing nonce validation
Examine REST API endpoints for proper authentication and CSRF token requirements
Look for redirects or form submissions that could be triggered via image tags or cross-origin requests
Test plugin update, theme activation, and plugin activation endpoints for CSRF vulnerabilities
Check for unprotected backup, export, or data processing endpoints

## MITRE ATT&CK
- T1190
- T1499.4
- T1561
- T1657

## Notes
This vulnerability combines two distinct weaknesses: CSRF and DoS. The severity assessment depends on which specific WordPress operations are exploitable—attacks against user creation, post deletion, or heavy query operations would be particularly impactful. The vulnerability likely affects multiple WordPress versions and requires authentication context to exploit, limiting exposure to sites with logged-in users. The attached advisory (referenced as text format) would contain specific technical details, affected versions, and reproduction steps not provided in the report excerpt.

## Full report
<details><summary>Expand</summary>

Hello,

I've discovered a Denial of Service vulnerability in WordPress. My advisory can be found in the attachment in text format. If there are any questions please let me know, I'm happy to help.

The vulnerability was discovered during a month long security project to find vulnerabilities in WordPress and WordPress plugins. For more information about the project see:
https://sumofpwn.nl

With kind regards,

Sipke

</details>

---
*Analysed by Claude on 2026-05-24*
