# Cross-Domain JavaScript Source File Inclusion (XSSI) on RubyGems.org

## Metadata
- **Source:** HackerOne
- **Report:** 307681 | https://hackerone.com/reports/307681
- **Submitted:** 2018-01-21
- **Reporter:** mrunal
- **Program:** RubyGems.org
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Cross-Site Script Inclusion, Third-Party Dependency Risk, Supply Chain Security
- **CVEs:** None
- **Category:** web-api

## Summary
RubyGems.org includes a third-party JavaScript file (secure.gaug.es/track.js) from an external domain without adequate controls, creating a supply chain vulnerability. If the external domain is compromised or hijacked, malicious code could execute in the context of RubyGems.org, potentially exposing user data and session tokens. The vulnerability exists despite CSP headers that explicitly whitelist the third-party domain.

## Attack scenario
1. Attacker identifies that RubyGems.org includes JavaScript from secure.gaug.es (a third-party analytics service)
2. Attacker compromises the third-party domain or performs DNS hijacking/BGP hijacking to redirect traffic
3. Malicious JavaScript is served instead of the legitimate tracking code
4. When users visit RubyGems.org, the malicious script executes in the RubyGems.org security context
5. Script exfiltrates session cookies, authentication tokens, or sensitive data visible in the DOM
6. Attacker gains unauthorized access to user accounts or performs actions as authenticated users

## Root cause
The application includes external JavaScript files from third-party domains without implementing adequate security controls. While CSP headers are present, they whitelist the third-party domain broadly. There is no integrity verification mechanism (such as Subresource Integrity/SRI), no monitoring for unexpected changes, and no fallback mechanism if the external service becomes unavailable or compromised.

## Attacker mindset
An attacker recognizes that third-party dependencies represent an attractive attack surface, as compromising a single external service can impact multiple applications. The attacker could target the less-secured third-party domain rather than the well-defended primary application, leveraging the trust relationship to inject malicious code into a high-value target.

## Defensive takeaways
- Implement Subresource Integrity (SRI) hashes for all external script includes to ensure files have not been tampered with
- Restrict CSP script-src to specific, versioned URLs rather than entire domains when possible
- Minimize external dependencies; host critical functionality locally or use vendor-bundled versions
- Monitor external script files for unexpected changes using integrity monitoring or checksum verification
- Implement Content Security Policy violations reporting to detect tampering attempts
- Conduct regular audits of all third-party dependencies and their security posture
- Consider using a Web Application Firewall to detect and block suspicious script behavior
- Establish incident response procedures for compromised third-party services

## Variant hunting
Search for other instances where external scripts are included without SRI verification, particularly analytics services (Google Analytics, Mixpanel, Segment), CDN-hosted libraries (jQuery, Bootstrap), payment processors (Stripe, PayPal), and advertising networks. Examine CSP policies that whitelist broad domains or use wildcards. Test whether removing or blocking external scripts causes application failure, indicating hard dependencies.

## MITRE ATT&CK
- T1190
- T1195
- T1195.001
- T1199
- T1583.001

## Notes
This vulnerability demonstrates a critical gap in supply chain security. While the CSP header shows security awareness, it creates a false sense of security by explicitly trusting a third-party domain. The reporter correctly identifies that the organization has no control over the external server's security. This is particularly significant for package repositories like RubyGems.org, where users trust the platform implicitly. The vulnerability predates widespread adoption of SRI (Subresource Integrity), making this a historically important security lesson. Modern exploitation would target the analytics provider's infrastructure or use techniques like dependency confusion attacks. The fix is straightforward but the security model shift (from network-based trust to cryptographic verification) represents an important evolution in web security practices.

## Full report
<details><summary>Expand</summary>

The page includes one or more script files from a third-party domain.

XSSI is a fancy way of saying: you are including in your program, someone elses code; You don't have any control over what is in that code, and you don't have any control over the security of the server on which it is hosted.
 
parameter : //secure.gaug.es/track.js
evidence: <script type="text/javascript" async defer id="gauges-tracker" data-site-id="4eab0ac8613f5d1583000005" src="//secure.gaug.es/track.js"></script>

solution : Ensure JavaScript source files are loaded from only trusted sources, and the sources can't be controlled by end users of the application.


    <script type="text/javascript" async defer id="gauges-tracker" data-site-id="4eab0ac8613f5d1583000005" src="//secure.gaug.es/track.js"></script>
  </body>


HTTP request :

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Content-Security-Policy: default-src 'self'; script-src 'self' https://secure.gaug.es; style-src 'self' https://fonts.googleapis.com; img-src 'self' https://secure.gaug.es https://gravatar.com https://secure.gravatar.com; font-src 'self' https://fonts.gstatic.com; connect-src https://s3-us-west-2.amazonaws.com/rubygems-dumps/; frame-src https://ghbtns.com
Cache-Control: max-age=0, private, must-revalidate
Set-Cookie: _rubygems_session=R2ovd2tLZG9lUGtmY1pQczgvSFBjdC9IdjE5QnVJQ0Ywby9xbmNUSlRQU3JaOVNoNnF5WE1KZW14eGFlTTdZbHJPZFp6Vk5Udlp3QTRMSElkTmJnWlFlRjMyVWJJa2k5NU1LTm9XTVozWVBYaHdWLzg1dW1UaDd6TitZR1FYZ041M0oyZk94T2tVMG1vbU54Rm02SThnPT0tLTdZK1pRK0QxTW1GcS9GWVlPZlFoVUE9PQ%3D%3D--102c1918815967faefb0604b28daa2d3900df474; path=/; secure; HttpOnly
X-Request-Id: 282c9423-26fd-4517-8bfc-1359900c553e
X-Runtime: 0.013107
Strict-Transport-Security: max-age=0
X-UA-Compatible: IE=Edge,chrome=1
X-Backend: F_Rails 54.186.104.15:443
Accept-Ranges: bytes
Date: Sun, 21 Jan 2018 17:00:41 GMT
Via: 1.1 varnish
Age: 0
Connection: keep-alive
X-Served-By: cache-sin18034-SIN
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1516554041.101894,VS0,VE220
Vary: Accept-Encoding,Fastly-SSL
ETag: "a2988a0215687cad2553179ed0d2d3ef"
Server: RubyGems.org

## Impact

Browsers prevent pages of one domain from reading pages in other domains. But they do not prevent pages of a domain from referencing resources in other domains. In particular, they allow images to be rendered from other domains and scripts to be executed from other domains. An included script doesn't have its own security context. It runs in the security context of the page that included it. For example, if www.evil.example.com includes a script hosted on www.google.com then that script runs in the evil context not in the google context. So any user data in that script will "leak

</details>

---
*Analysed by Claude on 2026-05-24*
