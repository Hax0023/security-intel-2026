# Open Redirect via Third-Party Open Redirect Links on HackerOne

## Metadata
- **Source:** HackerOne
- **Report:** 296706 | https://hackerone.com/reports/296706
- **Submitted:** 2017-12-10
- **Reporter:** abidbaseer
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Open Redirect, Chained Open Redirect, Insufficient URL Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
HackerOne's open redirect detection mechanism fails to properly validate URLs containing nested redirects from third-party services like Facebook and Google. Attackers can embed links that appear to redirect to legitimate domains but actually chain through to malicious sites, bypassing security warnings.

## Attack scenario
1. Attacker crafts a report on HackerOne containing a Facebook or Google redirect link that chains to an attacker-controlled domain
2. The intermediate redirect service (facebook.com or google.com) is highlighted in the warning dialog, appearing trustworthy to users
3. Researcher clicks the 'proceed' button, trusting the highlighted legitimate domain
4. User is redirected through the third-party service's open redirect to the attacker's malicious domain
5. Attacker performs phishing, credential harvesting, or malware distribution
6. HackerOne's warning system failed to detect the chained nature of the redirect

## Root cause
HackerOne's open redirect detection logic only analyzes the immediate destination hostname rather than recursively following redirect chains. It extracts and displays only the first legitimate-looking domain in the chain, creating false confidence in users despite the final destination being malicious.

## Attacker mindset
Social engineering through authority exploitation - leveraging trusted intermediate domains to bypass security warnings. The attacker abuses third-party services' legitimate open redirects to obscure malicious intent and increase click-through rates in phishing campaigns.

## Defensive takeaways
- Implement recursive URL validation that follows redirect chains to identify the final destination
- Display warnings based on final destination, not intermediate hosts in redirect chains
- Block or sanitize known open redirect patterns from trusted services (URL shorteners, tracking redirects)
- Consider disallowing external redirects entirely or require explicit user consent with final URL visible
- Implement server-side redirect following to prevent client-side deception
- Use URL analysis tools that resolve redirect chains before trust assessment

## Variant hunting
Test other URL shortening services (bit.ly, tinyurl, etc.) for chained redirect bypass
Check for multiple levels of redirect chains (3+ hops) bypassing detection
Test with obfuscated parameters in tracking/redirect URLs
Attempt data exfiltration through redirect chain parameters
Test mixed protocols (http to https chains) for validation bypass
Check if other platforms susceptible to same attack (GitHub, GitLab, other report platforms)

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1204.001
- T1557.002

## Notes
This is a meta-vulnerability affecting security researchers - the very people reporting vulnerabilities are targeted via reports submitted to the platform. The attack is particularly effective because HackerOne's warning mechanism inadvertently builds trust in the intermediate redirect domain. The report demonstrates lack of understanding of how sophisticated open redirects work but identifies a real gap in validation logic.

## Full report
<details><summary>Expand</summary>

1. The open redirect feature in hackerone does not work properly
2. When users submit a report. They can also use links in the report. 
3. An attacker can deceive other users by using another website redirect link in hackerone.com
For example consider the links below
[https://l.facebook.com/l.php?u=https://evil.com/&h=ATMJdQSbOgLxx8kkZxvuz8D9mq0OTPfZ5OHToxZGQXr6M-ylbKvZxQ9p2xJv4TswF-pv2Nr75TIXzp1369GuPe3cmETf46pXKfIHlw]

when you click on the link the proceed button will appear and the facebook.com domain will be highlighted. When you click the proceed button you will be redirected to evil.com.

Similarly consider this link as an example
[https://www.google.com.pk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjx8qv0iYDYAhUIVhQKHe-pCGUQFggkMAA&url=https%3A%2F%2Fevilzone.org%2F&usg=AOvVaw36yGjkBQ68CeL5hPUPT7cp]

When you click the link google.com.pk will be highlighted and the proceed button will appear. By clicking the proceed button you will be redirected to the evilzone.org.
Just like the above examples other websites open redirects link can be used to deceive users. The open redirect feature of hackerone need attention to detect hosts specially when there are multiple hosts in the link. Thanks

## Impact

This vulnerability could redirect users to the attackers websites for phishing attacks.

</details>

---
*Analysed by Claude on 2026-05-24*
