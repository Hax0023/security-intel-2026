# Subdomain Takeover in GitLab Pages via Unverified Custom Domains

## Metadata
- **Source:** HackerOne
- **Report:** 2523654 | https://hackerone.com/reports/2523654
- **Submitted:** 2024-05-28
- **Reporter:** fdeleite
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Domain Verification Bypass, Insufficient Access Controls
- **CVEs:** None
- **Category:** infra-cloud

## Summary
GitLab Pages allows attackers to take over dangling custom domains by adding unverified domains that serve attacker-controlled content for up to 7 days before being disabled. An attacker can register an expired domain with a CNAME pointing to GitLab Pages infrastructure and add it as a custom domain in any GitLab project to serve malicious content on the legitimate domain.

## Attack scenario
1. Attacker identifies an expired or unclaimed domain that previously pointed to a GitLab Pages project (e.g., docs-dev.gitlab.com with CNAME to gitlab-com.gitlab.io)
2. Attacker creates or compromises a GitLab project and navigates to Deploy → Pages settings
3. Attacker adds the target dangling domain as a custom domain without domain verification and saves the configuration
4. GitLab Pages begins serving the attacker's project content on the legitimate domain due to lack of domain ownership verification
5. Attacker's content remains accessible for up to 7 days with valid SSL/TLS certificates, enabling phishing, cookie theft, or CSP/CORS bypass attacks
6. After 7 days, GitLab automatically disables unverified domains, but sufficient damage may have occurred

## Root cause
GitLab Pages does not require domain ownership verification before serving content on custom domains. The system trusts that users own domains they add, allowing a 7-day grace period before automatic disabling. An attacker can exploit this by adding any domain they control (including expired/dangling domains) and serving arbitrary content without proof of ownership.

## Attacker mindset
An opportunistic attacker would monitor for expired domains previously used as GitLab Pages custom domains (identifiable via DNS CNAME records), then quickly claim them and add them to their own GitLab projects to serve phishing pages, steal credentials, or conduct brand impersonation attacks before the 7-day window closes.

## Defensive takeaways
- Implement mandatory domain ownership verification (e.g., DNS TXT record, HTTP file validation) before allowing custom domains on Pages
- Reduce or eliminate the grace period before domain verification - enforce verification immediately or within 24 hours maximum
- Implement continuous domain ownership validation to detect and revoke domains that lose verification
- Monitor for suspicious patterns: multiple domains added by low-reputation accounts, bulk domain additions, or domains with known malicious history
- Send notifications to domain registrants when their domain is configured on GitLab Pages to detect unauthorized usage
- Implement rate limiting on custom domain additions per project/user
- Add a HSTS preload requirement and certificate pinning for verified custom domains

## Variant hunting
Similar vulnerabilities likely exist in other static hosting platforms offering custom domains (Vercel, Netlify, GitHub Pages, AWS CloudFront). Check for: (1) lack of domain verification before serving content, (2) long grace periods for unverified domains, (3) no continuous re-verification, (4) insufficient abuse monitoring on domain additions. Also test whether subdomains of gitlab.io can be claimed similarly.

## MITRE ATT&CK
- T1190
- T1098
- T1583.001
- T1583.006
- T1589.001

## Notes
The report demonstrates the vulnerability using docs-dev.gitlab.com but notes this is a staging/test domain. The actual impact extends to any expired custom domain previously configured on GitLab Pages. The 7-day window is critical - it provides a time window for attacks before automatic remediation. The vulnerability is particularly dangerous because GitLab Pages is widely used for documentation and marketing sites, making phishing highly credible.

## Full report
<details><summary>Expand</summary>

### Summary

It's possible for an attacker to take over a dangling custom domain pointing to GitLabPages using `instanceX.gitlab.io'

The problems arises when adding a custom domain to Gitlab Pages, without the domain being verified it still servers content (allowing 7 days before disabling it)

### Steps to reproduce

I did some tests with gitlab.com domains, `docs-dev.gitlab.com` worked correctly. 
The domain has the following fingerprints:

Dig  
```
docs-dev.gitlab.com.    300     IN      CNAME   gitlab-com.gitlab.io.
gitlab-com.gitlab.io.   300     IN      A       35.185.44.232
```
And going to the URL shows:

```
HTTP/1.1 302 Found
content-type: text/html; charset=utf-8
location: https://projects.staging.gitlab.io/auth?domain=http://docs-dev.gitlab.com&state=giZFQTsOOFXvR_0po68zrg==
permissions-policy: interest-cohort=()
set-cookie: gitlab-pages=..._; Path=/auth; Expires=Tue, 28 May 2024 21:07:33 GMT; Max-Age=600; HttpOnly
vary: Origin
date: Tue, 28 May 2024 20:57:33 GMT
gitlab-lb: haproxy-pages-01-lb-gstg
gitlab-sv: pages-us-east1-c

HTTP/2 401 
content-type: text/html; charset=utf-8
permissions-policy: interest-cohort=()
vary: Origin
x-content-type-options: nosniff
content-length: 2872
date: Tue, 28 May 2024 20:57:34 GMT

```

1. Create a GitLab pages using this project (https://gitlab.com/g15391522/pn1)
2. Go to  **Deploy** ->  ** Pages ** 
3. Disable `Force HTTPS (requires valid certificates)` 
4. Add the target custom domain and click in Save

Go to http://docs-dev.gitlab.com/

Now the content of the site will be :

{F3307313}

## Impact

They could perform several attacks like:

   -  Cookie Stealing
   - Phishing campaigns.
   - Bypass Content-Security Policies and CORS.

</details>

---
*Analysed by Claude on 2026-05-24*
