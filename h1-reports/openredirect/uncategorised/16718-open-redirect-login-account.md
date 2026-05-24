# Open Redirect in Slack Login Flow

## Metadata
- **Source:** HackerOne
- **Report:** 16718 | https://hackerone.com/reports/16718
- **Submitted:** 2014-06-17
- **Reporter:** jaysonzabate
- **Program:** Slack
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
Slack's login page accepts an unvalidated 'redir' parameter that redirects users to arbitrary URLs after authentication. This allows attackers to craft phishing links that appear legitimate (slack.com domain) but redirect to malicious sites after login, increasing success rates of credential harvesting attacks.

## Attack scenario
1. Attacker crafts a malicious URL: https://[victim-slack].slack.com/?redir=llink?url=https://attacker-phishing-site.com
2. Attacker sends this URL to target users via email or chat, claiming urgent account verification needed
3. User clicks the link and sees legitimate Slack login page, lowering suspicion
4. User enters credentials and logs in successfully
5. Application redirects user to attacker's phishing site (appearing to be part of normal flow)
6. Attacker captures additional sensitive data or installs malware

## Root cause
The 'redir' parameter in the Slack login endpoint is not properly validated or sanitized before being used in HTTP redirects. The application fails to implement whitelist-based redirect validation or URL scheme restrictions.

## Attacker mindset
Open redirects are low-severity individually but become critical in context of authentication flows. By chaining with a legitimate domain login, the attacker bypasses user trust signals and dramatically increases phishing effectiveness. This is particularly valuable for targeting Slack workspaces where users expect internal redirects.

## Defensive takeaways
- Implement strict whitelist-based redirect validation for all redirect parameters
- Use relative URLs exclusively when possible, avoiding absolute URL redirects
- Validate that redirect targets are on the same domain or pre-approved domains only
- Implement Content Security Policy (CSP) headers to restrict redirect destinations
- Add explicit user warnings before redirecting to external domains post-authentication
- Use security headers like X-Frame-Options and X-Content-Type-Options to prevent exploitation
- Implement logging and monitoring of redirect parameters for anomalous patterns

## Variant hunting
Test other redirect parameters: ?redirect=, ?return=, ?next=, ?url=, ?target=, ?goto=
Test double-encoding and URL encoding bypass attempts on redir parameter
Test data: and javascript: schemes in redirect parameters
Test protocol-relative URLs like //attacker.com
Test backslash variants like \\attacker.com on different browsers
Test redirects in password reset, account confirmation, and OAuth flows
Check custom scheme handlers (slack://) for redirect abuse

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1606.002

## Notes
Report lacks specific bounty amount and remediation timeline. The PoC shows the vulnerability chained with llink parameter, suggesting potential parameter pollution or confusion. The Slack domain legitimacy makes this particularly effective for phishing. This vulnerability type was more commonly awarded higher bounties in 2016 when reported, as the security community was raising awareness about redirect attacks in authentication contexts.

## Full report
<details><summary>Expand</summary>

An open redirect is an application that takes a parameter and redirects a user to the parameter value without any validation. This vulnerability is used in phishing attacks to get users to visit malicious sites without realizing it.

###Reproduction Instructions 

go to `www.[TEAM].slack.com/?redir=llink?url=https://twitter.com/` log in your account on this link then redirect to twitter,google and any webiste you want.


###Proof of concept:
```
https://asdasda.slack.com/?redir=llink?url=https://twitter.com/
```


Regards,
Jayson Zabate

</details>

---
*Analysed by Claude on 2026-05-24*
