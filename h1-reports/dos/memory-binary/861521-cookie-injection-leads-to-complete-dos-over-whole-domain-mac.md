# Cookie Injection Leading to Domain-Wide Denial of Service via Cookie Bomb

## Metadata
- **Source:** HackerOne
- **Report:** 861521 | https://hackerone.com/reports/861521
- **Submitted:** 2020-04-28
- **Reporter:** mayurudiniya
- **Program:** MacKeeper
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Cookie Bomb, HTTP Request Smuggling, Denial of Service, Cookie Injection, Client-Side Cookie Manipulation
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can inject excessively large cookies into the *.mackeeper.com domain through a crafted link, causing the HTTP request headers to exceed server limits and resulting in complete denial of service across all subdomains. The vulnerability exploits improper cookie validation and the browser's automatic URI encoding mechanism, where special characters are percent-encoded and expand to three times their original length.

## Attack scenario
1. Attacker crafts a malicious HTML link that sets large cookies with special characters (e.g., commas) when clicked
2. Victim clicks the link from attacker-controlled domain (e.g., unequaledfloor.htmlpasta.com)
3. JavaScript or HTTP redirect in the link executes document.cookie assignments for *.mackeeper.com domain
4. Browser automatically URI-encodes special characters in cookie values, expanding them to %XX format (3 bytes per character)
5. The crafted cookie size exceeds the server's maximum HTTP header size limit (typically 8KB)
6. All subsequent requests to accountstage.mackeeper.com and other subdomains are rejected by the server due to oversized headers, rendering the entire domain inaccessible

## Root cause
The application lacks proper validation of cookie size before acceptance. The cookie handling mechanism does not enforce limits on cookie dimensions, and there is no server-side verification that incoming cookies conform to HTTP header size constraints. Additionally, the use of URL encoding (escape function) causes predictable expansion of special characters, which attackers can leverage to create valid-looking but ultimately oversized cookies.

## Attacker mindset
An attacker seeks to maximize disruption with minimal effort by exploiting the mathematical relationship between unencoded and encoded cookie data. By using high-repetition special characters, the attacker can craft a URL of reasonable length that, when decoded and expanded in the browser, becomes a massive cookie capable of breaking the entire service. This is a cost-effective DoS attack requiring no special tools or persistence.

## Defensive takeaways
- Implement strict server-side cookie size validation before processing any HTTP request
- Enforce maximum cookie size limits (recommend <4KB per cookie, <8KB total) and reject oversized cookies immediately
- Set explicit HTTP header size limits in web server configuration (nginx, Apache) to reject requests with headers exceeding threshold
- Implement pre-flight cookie validation on the client side to prevent setting excessively large cookies
- Use SameSite=Strict and Secure flags to restrict cross-domain cookie injection from untrusted sources
- Monitor for unusual cookie sizes in logs and implement alerting for potential cookie bomb attacks
- Document acceptable cookie size constraints in secure development guidelines
- Consider implementing rate limiting or request throttling for requests with abnormally large headers

## Variant hunting
Search for similar vulnerabilities in other cookie-handling implementations: (1) Other *.mackeeper.com subdomains with different injection points; (2) Related MacKeeper products or services using shared domain cookies; (3) Other applications using escape() function for cookie encoding without size validation; (4) Services using wildcard domain cookies (.domain.com) that allow cross-subdomain injection; (5) Applications accepting cookies from external referrer domains without origin validation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1561 - Disk Wipe
- T1499 - Endpoint Denial of Service

## Notes
This vulnerability demonstrates a classic cookie bomb attack pattern. The URI encoding expansion (3x multiplier for special characters) is the key exploitation mechanism. The wildcard domain scope (*.mackeeper.com) amplifies impact across all subdomains. This attack requires user interaction (clicking a link) but no authentication. The PoC domain 'unequaledfloor.htmlpasta.com' appears to be a proof-of-concept hosted externally. Similar vulnerabilities have been found in other web applications; this pattern should be considered in security reviews of any service accepting user-controllable cookies.

## Full report
<details><summary>Expand</summary>

## Summary:
 The cookie bomb works by setting large cookies that are way too big making the server decline any request send with them for having a too long request header.

##PoC
1.  Open below link and click on link
https://unequaledfloor.htmlpasta.com/

2.  Now open https://accountstage.mackeeper.com/ or https://.mackeeper.com/ , these domains won't open anymore.

## Impact

The escape function is used, which means a value consisting of special symbols will become three times longer. For example ,,, will turn into %2C. That means an attacker can create a valid link of proper length accepted both by the browser and the server, which however will make the cookie too long.

</details>

---
*Analysed by Claude on 2026-05-24*
