# Clickjacking vulnerability on irclogs.wordpress.org

## Metadata
- **Source:** HackerOne
- **Report:** 267075 | https://hackerone.com/reports/267075
- **Submitted:** 2017-09-08
- **Reporter:** sameull
- **Program:** WordPress.com / Automattic
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Clickjacking, Missing X-Frame-Options Header
- **CVEs:** None
- **Category:** uncategorised

## Summary
The subdomain irclogs.wordpress.org is vulnerable to clickjacking attacks due to missing X-Frame-Options HTTP header, allowing the page to be embedded in iframes on attacker-controlled sites. This enables UI redressing attacks where users can be tricked into performing unintended actions on the legitimate domain.

## Attack scenario
1. Attacker creates a malicious webpage with transparent iframe embedding irclogs.wordpress.org
2. Attacker overlays deceptive UI elements or buttons on top of the iframe
3. User visits attacker's malicious page, unaware of the hidden iframe beneath visible content
4. User interacts with what appears to be legitimate buttons/links but actually clicks on hidden elements within irclogs.wordpress.org
5. User unknowingly performs actions on the legitimate domain (e.g., account changes, data modifications)
6. Attacker achieves unauthorized actions while maintaining plausible deniability

## Root cause
The irclogs.wordpress.org server fails to implement the X-Frame-Options HTTP response header (or Content-Security-Policy frame-ancestors directive), which is the standard mechanism to prevent embedding in iframes and mitigate clickjacking attacks.

## Attacker mindset
Opportunistic vulnerability hunter identifying low-hanging fruit in WordPress infrastructure. Likely performed automated security scanning across subdomains and identified missing security headers, demonstrating awareness of OWASP Top 10 and common web security oversights.

## Defensive takeaways
- Implement X-Frame-Options: DENY or X-Frame-Options: SAMEORIGIN on all subdomains to prevent iframe embedding
- Configure Content-Security-Policy header with frame-ancestors directive as defense-in-depth
- Conduct comprehensive security header audit across all subdomains (not just primary domain)
- Automate security header validation in CI/CD pipeline and monitoring
- Ensure subdomain security policies match primary domain standards
- Implement centralized header management for consistent application across infrastructure

## Variant hunting
Check other WordPress.com subdomains (blogs.wordpress.org, forums.wordpress.org, etc.) for missing X-Frame-Options
Test for missing Content-Security-Policy headers across domain portfolio
Verify whether clickjacking protections vary between subdomains inconsistently
Check if legacy or static content subdomains are excluded from security header implementation
Test for weak X-Frame-Options values (ALLOW-FROM which is deprecated) vs complete absence

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1204.001 - User Execution: Malicious Link

## Notes
Report is minimal with no technical depth but demonstrates valid vulnerability. Researcher provided video POC (F219474) which would show actual clickjacking demonstration. Issue affects IRC logs subdomain which may have lower severity than user-facing areas but still requires remediation. Report quality suggests responsible disclosure practice by WordPress security researcher.

## Full report
<details><summary>Expand</summary>

Hello! @wordpress security team,
I'm Md Sameull Soykot ( @sameull ). Recently I have tested you all sub-domain and got a domain which is vulnerable named as clickjacking. I have attached my video Poc for details. Hope you will fix this issue as soon as possible.

Reference: https://blogs.msdn.microsoft.com/ieinternals/2010/03/30/combating-clickjacking-with-x-frame-options/

{F219474}

Thank you

</details>

---
*Analysed by Claude on 2026-05-24*
